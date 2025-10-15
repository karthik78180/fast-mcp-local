# Platform MultipartHandler Verticle

## Description

The `MultipartHandler` interface is provided by the platform for handling **file uploads and multipart form data**. Use this for file upload endpoints, image processing, document storage, or any operation that needs to process multipart/form-data requests.

**Platform handles**: Deployment, routing, configuration, multipart parsing

**Teams implement**: Business logic in `handle()` method using platform-provided interfaces

⚠️ **Important**: MultipartHandler runs on worker threads to handle potentially large file uploads without blocking the event loop.

## MultipartHandler Interface

```java
package com.example.api;

import io.vertx.core.Vertx;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;

/**
 * Interface for handling file uploads and multipart form data
 * Executes on worker thread pool - file I/O is safe
 */
public interface MultipartHandler {
    /**
     * Called when verticle is deployed
     * Initialize resources (file storage clients, validators, etc.)
     */
    void start(Vertx vertx, JsonObject config);

    /**
     * Handle incoming multipart request
     * Runs on worker thread - blocking file I/O is safe here
     */
    void handle(RoutingContext context);

    /**
     * Called when verticle is undeployed
     * Cleanup resources
     */
    void stop();

    /**
     * Get configuration for this endpoint
     * @return JsonObject with endpoint-specific config
     */
    JsonObject getData();
}
```

## Example 1: File Upload Handler

This example shows a multipart handler that uploads files to local storage with validation.

### Verticle Code

```java
package com.example.verticles;

import com.example.api.MultipartHandler;
import io.vertx.core.Vertx;
import io.vertx.core.json.JsonArray;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;
import io.vertx.ext.web.FileUpload;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Set;
import java.util.UUID;

public class FileUploadVerticle implements MultipartHandler {

    private JsonObject config;
    private String uploadDirectory;
    private long maxFileSize;
    private Set<String> allowedMimeTypes;

    @Override
    public void start(Vertx vertx, JsonObject config) {
        this.config = config;

        // Get upload config from config.json
        JsonObject uploadConfig = config().getData().getJsonObject("upload");

        this.uploadDirectory = uploadConfig.getString("directory");
        this.maxFileSize = uploadConfig.getLong("maxFileSizeBytes", 10485760L); // 10MB default

        // Parse allowed MIME types
        JsonArray mimeTypes = uploadConfig.getJsonArray("allowedMimeTypes");
        this.allowedMimeTypes = new HashSet<>();
        for (int i = 0; i < mimeTypes.size(); i++) {
            allowedMimeTypes.add(mimeTypes.getString(i));
        }

        // Create upload directory if it doesn't exist
        try {
            Files.createDirectories(Paths.get(uploadDirectory));
            System.out.println("FileUploadVerticle started with directory: " + uploadDirectory);
        } catch (IOException e) {
            System.err.println("Failed to create upload directory: " + e.getMessage());
        }
    }

    @Override
    public void handle(RoutingContext context) {
        try {
            // Get uploaded files
            Set<FileUpload> uploads = context.fileUploads();

            if (uploads.isEmpty()) {
                context.response()
                    .setStatusCode(400)
                    .putHeader("Content-Type", "application/json")
                    .end(new JsonObject()
                        .put("success", false)
                        .put("error", "No files uploaded")
                        .encodePrettily());
                return;
            }

            JsonArray uploadedFiles = new JsonArray();

            for (FileUpload upload : uploads) {
                // Validate file size
                if (upload.size() > maxFileSize) {
                    context.response()
                        .setStatusCode(413)
                        .putHeader("Content-Type", "application/json")
                        .end(new JsonObject()
                            .put("success", false)
                            .put("error", "File too large: " + upload.fileName())
                            .put("maxSizeBytes", maxFileSize)
                            .encodePrettily());
                    return;
                }

                // Validate MIME type
                String contentType = upload.contentType();
                if (!allowedMimeTypes.contains(contentType)) {
                    context.response()
                        .setStatusCode(415)
                        .putHeader("Content-Type", "application/json")
                        .end(new JsonObject()
                            .put("success", false)
                            .put("error", "File type not allowed: " + contentType)
                            .put("allowedTypes", new JsonArray(allowedMimeTypes.stream().toList()))
                            .encodePrettily());
                    return;
                }

                // Generate unique filename
                String fileExtension = getFileExtension(upload.fileName());
                String uniqueFileName = UUID.randomUUID().toString() + fileExtension;
                Path targetPath = Paths.get(uploadDirectory, uniqueFileName);

                // Move uploaded file to target directory (blocking - safe in MultipartHandler)
                Files.move(
                    Paths.get(upload.uploadedFileName()),
                    targetPath,
                    StandardCopyOption.REPLACE_EXISTING
                );

                // Record uploaded file info
                JsonObject fileInfo = new JsonObject()
                    .put("originalName", upload.fileName())
                    .put("storedName", uniqueFileName)
                    .put("contentType", upload.contentType())
                    .put("size", upload.size())
                    .put("path", targetPath.toString());

                uploadedFiles.add(fileInfo);
            }

            // Send success response
            context.response()
                .putHeader("Content-Type", "application/json")
                .end(new JsonObject()
                    .put("success", true)
                    .put("filesUploaded", uploadedFiles.size())
                    .put("files", uploadedFiles)
                    .encodePrettily());

        } catch (IOException e) {
            // Handle file I/O error
            context.response()
                .setStatusCode(500)
                .putHeader("Content-Type", "application/json")
                .end(new JsonObject()
                    .put("success", false)
                    .put("error", "File upload failed: " + e.getMessage())
                    .encodePrettily());
        }
    }

    @Override
    public void stop() {
        System.out.println("FileUploadVerticle stopped");
    }

    @Override
    public JsonObject getData() {
        return config;
    }

    private String getFileExtension(String fileName) {
        int lastDot = fileName.lastIndexOf('.');
        return lastDot > 0 ? fileName.substring(lastDot) : "";
    }
}
```

### Configuration Structure

**Location**: `config/FileUploadVerticle.v1/`

**lambda.json** (metadata):
```json
{
  "artifactId": "file-upload-service",
  "verticleClass": "com.example.verticles.FileUploadVerticle",
  "version": "v1",
  "endpoint": "/api/files/upload",
  "handlerType": "MultipartHandler"
}
```

**config.json** (endpoint-specific config):
```json
{
  "upload": {
    "directory": "/var/uploads",
    "maxFileSizeBytes": 10485760,
    "allowedMimeTypes": [
      "image/jpeg",
      "image/png",
      "image/gif",
      "application/pdf",
      "text/plain"
    ],
    "generateUniqueNames": true
  },
  "validation": {
    "requireAuthentication": true,
    "maxFilesPerRequest": 5
  }
}
```

## Example 2: Image Upload with S3 Storage

This example shows a multipart handler that uploads images to AWS S3.

### Verticle Code

```java
package com.example.verticles;

import com.example.api.MultipartHandler;
import io.vertx.core.Vertx;
import io.vertx.core.json.JsonArray;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;
import io.vertx.ext.web.FileUpload;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.File;
import java.nio.file.Paths;
import java.util.Set;
import java.util.UUID;

public class ImageUploadS3Verticle implements MultipartHandler {

    private JsonObject config;
    private S3Client s3Client;
    private String bucketName;
    private String s3Region;
    private long maxImageSize;

    @Override
    public void start(Vertx vertx, JsonObject config) {
        this.config = config;

        // Get S3 config from config.json
        JsonObject s3Config = config().getData().getJsonObject("s3");
        JsonObject uploadConfig = config().getData().getJsonObject("upload");

        this.bucketName = s3Config.getString("bucketName");
        this.s3Region = s3Config.getString("region", "us-east-1");
        this.maxImageSize = uploadConfig.getLong("maxImageSizeBytes", 5242880L); // 5MB default

        // Initialize S3 client
        AwsBasicCredentials credentials = AwsBasicCredentials.create(
            s3Config.getString("accessKeyId"),
            s3Config.getString("secretAccessKey")
        );

        this.s3Client = S3Client.builder()
            .region(Region.of(s3Region))
            .credentialsProvider(StaticCredentialsProvider.create(credentials))
            .build();

        System.out.println("ImageUploadS3Verticle started with bucket: " + bucketName);
    }

    @Override
    public void handle(RoutingContext context) {
        try {
            // Get uploaded files
            Set<FileUpload> uploads = context.fileUploads();

            if (uploads.isEmpty()) {
                context.response()
                    .setStatusCode(400)
                    .putHeader("Content-Type", "application/json")
                    .end(new JsonObject()
                        .put("success", false)
                        .put("error", "No images uploaded")
                        .encodePrettily());
                return;
            }

            JsonArray uploadedImages = new JsonArray();

            for (FileUpload upload : uploads) {
                // Validate image type
                String contentType = upload.contentType();
                if (!contentType.startsWith("image/")) {
                    context.response()
                        .setStatusCode(415)
                        .putHeader("Content-Type", "application/json")
                        .end(new JsonObject()
                            .put("success", false)
                            .put("error", "Only image files are allowed")
                            .encodePrettily());
                    return;
                }

                // Validate image size
                if (upload.size() > maxImageSize) {
                    context.response()
                        .setStatusCode(413)
                        .putHeader("Content-Type", "application/json")
                        .end(new JsonObject()
                            .put("success", false)
                            .put("error", "Image too large: " + upload.fileName())
                            .put("maxSizeBytes", maxImageSize)
                            .encodePrettily());
                    return;
                }

                // Generate S3 key (path in bucket)
                String fileExtension = getFileExtension(upload.fileName());
                String s3Key = "images/" + UUID.randomUUID().toString() + fileExtension;

                // Upload to S3 (blocking - safe in MultipartHandler)
                File uploadedFile = new File(upload.uploadedFileName());

                PutObjectRequest putRequest = PutObjectRequest.builder()
                    .bucket(bucketName)
                    .key(s3Key)
                    .contentType(contentType)
                    .build();

                s3Client.putObject(putRequest, Paths.get(uploadedFile.getAbsolutePath()));

                // Generate public URL
                String publicUrl = String.format(
                    "https://%s.s3.%s.amazonaws.com/%s",
                    bucketName, s3Region, s3Key
                );

                // Record uploaded image info
                JsonObject imageInfo = new JsonObject()
                    .put("originalName", upload.fileName())
                    .put("s3Key", s3Key)
                    .put("url", publicUrl)
                    .put("contentType", contentType)
                    .put("size", upload.size());

                uploadedImages.add(imageInfo);

                // Delete temporary file
                uploadedFile.delete();
            }

            // Send success response
            context.response()
                .putHeader("Content-Type", "application/json")
                .end(new JsonObject()
                    .put("success", true)
                    .put("imagesUploaded", uploadedImages.size())
                    .put("images", uploadedImages)
                    .encodePrettily());

        } catch (Exception e) {
            // Handle S3 upload error
            context.response()
                .setStatusCode(500)
                .putHeader("Content-Type", "application/json")
                .end(new JsonObject()
                    .put("success", false)
                    .put("error", "Image upload failed: " + e.getMessage())
                    .encodePrettily());
        }
    }

    @Override
    public void stop() {
        // Cleanup S3 client
        if (s3Client != null) {
            s3Client.close();
            System.out.println("S3 client closed");
        }
    }

    @Override
    public JsonObject getData() {
        return config;
    }

    private String getFileExtension(String fileName) {
        int lastDot = fileName.lastIndexOf('.');
        return lastDot > 0 ? fileName.substring(lastDot) : "";
    }
}
```

### Configuration Structure

**Location**: `config/ImageUploadS3Verticle.v1/`

**lambda.json** (metadata):
```json
{
  "artifactId": "image-upload-s3-service",
  "verticleClass": "com.example.verticles.ImageUploadS3Verticle",
  "version": "v1",
  "endpoint": "/api/images/upload",
  "handlerType": "MultipartHandler"
}
```

**config.json** (endpoint-specific config):
```json
{
  "s3": {
    "bucketName": "my-app-images",
    "region": "us-east-1",
    "accessKeyId": "${AWS_ACCESS_KEY_ID}",
    "secretAccessKey": "${AWS_SECRET_ACCESS_KEY}"
  },
  "upload": {
    "maxImageSizeBytes": 5242880,
    "allowedImageTypes": ["image/jpeg", "image/png", "image/gif"],
    "generateThumbnails": true
  },
  "storage": {
    "pathPrefix": "images/",
    "publicRead": true
  }
}
```

## Gradle Dependencies

Add these dependencies to your `build.gradle`:

```gradle
dependencies {
    // Platform API (provided by your organization)
    implementation 'com.example:platform-api:1.0.0'

    // Vert.x Core
    implementation 'io.vertx:vertx-core:4.5.0'
    implementation 'io.vertx:vertx-web:4.5.0'

    // For S3 example
    implementation platform('software.amazon.awssdk:bom:2.20.0')
    implementation 'software.amazon.awssdk:s3'
    implementation 'software.amazon.awssdk:auth'

    // For image processing (optional)
    implementation 'org.imgscalr:imgscalr-lib:4.2'
}
```

## Key Patterns

### 1. Configuration Access
```java
// In start() method
JsonObject uploadConfig = config().getData().getJsonObject("upload");

// In handle() method
JsonObject s3Config = config().getData().getJsonObject("s3");
```

### 2. File Upload Handling
```java
// Get uploaded files
Set<FileUpload> uploads = context.fileUploads();

for (FileUpload upload : uploads) {
    String fileName = upload.fileName();
    String contentType = upload.contentType();
    long size = upload.size();
    String uploadedPath = upload.uploadedFileName(); // Temp file path
}
```

### 3. File Validation
```java
// Size validation
if (upload.size() > maxFileSize) {
    context.response().setStatusCode(413).end(errorJson);
    return;
}

// MIME type validation
if (!allowedMimeTypes.contains(upload.contentType())) {
    context.response().setStatusCode(415).end(errorJson);
    return;
}
```

### 4. File Storage (Blocking is OK)
```java
// Local filesystem - blocking is safe in MultipartHandler
Files.move(
    Paths.get(upload.uploadedFileName()),
    targetPath,
    StandardCopyOption.REPLACE_EXISTING
);

// S3 upload - blocking is safe in MultipartHandler
s3Client.putObject(putRequest, Paths.get(file.getAbsolutePath()));
```

### 5. Resource Cleanup
```java
@Override
public void stop() {
    if (s3Client != null) {
        s3Client.close();
    }
}
```

## Best Practices

1. **Validate file size** - Check before processing to prevent memory issues
2. **Validate MIME types** - Only allow expected file types
3. **Generate unique filenames** - Use UUIDs to prevent collisions
4. **Use config().getData()** - Don't hardcode paths or credentials
5. **Clean up temp files** - Delete uploaded files after processing
6. **Set proper status codes** - 413 for too large, 415 for unsupported type
7. **Handle errors gracefully** - File I/O can fail, always catch exceptions
8. **Close external clients** - Clean up S3/cloud storage clients in stop()

## Common Use Cases

- Image uploads with validation
- Document uploads (PDF, Word, etc.)
- CSV/Excel file imports
- Profile picture uploads
- Bulk file uploads
- File uploads to cloud storage (S3, Azure Blob, GCS)
- File virus scanning before storage
- Image resizing and thumbnail generation

## MultipartHandler vs AsyncHandler vs SyncHandler

| Aspect | MultipartHandler | AsyncHandler | SyncHandler |
|--------|------------------|--------------|-------------|
| **Thread Pool** | Worker threads | Event loop | Worker threads |
| **Blocking** | ✅ Safe to block | ❌ Never block | ✅ Safe to block |
| **Use Case** | File uploads | HTTP, Async DB | SOAP, JDBC |
| **File I/O** | ✅ Safe | ❌ Must use async | ✅ Safe |
| **Concurrency** | Limited by worker pool | High concurrency | Limited by worker pool |

## Notes

- **Deployment is handled by platform** - No need to write deployment code
- **Routing is handled by platform** - Endpoint configured in `lambda.json`
- **Worker threads are managed by platform** - Platform configures worker pool size
- **Blocking file I/O is safe** - MultipartHandler runs on dedicated worker threads
- **Multipart parsing is handled by platform** - Files are already parsed in `context.fileUploads()`
