# Platform AsyncHandler Verticle

## Description

The `AsyncHandler` interface is provided by the platform for handling asynchronous, non-blocking operations. Teams implement this interface to build verticles that handle async HTTP requests, database queries, message processing, etc.

**Platform handles**: Deployment, routing, configuration loading, lifecycle management

**Teams implement**: Business logic in `handle()` method using platform-provided interfaces

## AsyncHandler Interface

```java
package com.example.api;

import io.vertx.core.Vertx;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;

/**
 * Interface for asynchronous, non-blocking request handlers
 */
public interface AsyncHandler {
    /**
     * Called when verticle is deployed
     * Initialize resources (DB connections, HTTP clients, etc.)
     */
    void start(Vertx vertx, JsonObject config);

    /**
     * Handle incoming async request
     * Implement business logic here
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

## Example 1: Async PostgreSQL Handler

This example shows an async handler that queries PostgreSQL database.

### Verticle Code

```java
package com.example.verticles;

import com.example.api.AsyncHandler;
import io.vertx.core.Vertx;
import io.vertx.core.json.JsonArray;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;
import io.vertx.pgclient.PgConnectOptions;
import io.vertx.pgclient.PgPool;
import io.vertx.sqlclient.PoolOptions;
import io.vertx.sqlclient.Row;
import io.vertx.sqlclient.RowSet;
import io.vertx.sqlclient.Tuple;

public class UserQueryVerticle implements AsyncHandler {

    private PgPool pgPool;
    private JsonObject config;

    @Override
    public void start(Vertx vertx, JsonObject config) {
        this.config = config;

        // Get database config from config.json
        JsonObject dbConfig = config().getData().getJsonObject("database");

        // Initialize PostgreSQL connection pool
        PgConnectOptions connectOptions = new PgConnectOptions()
            .setHost(dbConfig.getString("host", "localhost"))
            .setPort(dbConfig.getInteger("port", 5432))
            .setDatabase(dbConfig.getString("database"))
            .setUser(dbConfig.getString("user"))
            .setPassword(dbConfig.getString("password"));

        PoolOptions poolOptions = new PoolOptions()
            .setMaxSize(dbConfig.getInteger("maxPoolSize", 10));

        pgPool = PgPool.pool(vertx, connectOptions, poolOptions);

        System.out.println("UserQueryVerticle started with database: " + dbConfig.getString("database"));
    }

    @Override
    public void handle(RoutingContext context) {
        // Parse request
        JsonObject requestBody = context.body().asJsonObject();
        String userId = requestBody.getString("userId");

        // Execute async query
        pgPool.preparedQuery("SELECT * FROM users WHERE id = $1")
            .execute(Tuple.of(userId))
            .onSuccess(rows -> {
                JsonArray results = new JsonArray();
                for (Row row : rows) {
                    JsonObject user = new JsonObject()
                        .put("id", row.getString("id"))
                        .put("name", row.getString("name"))
                        .put("email", row.getString("email"));
                    results.add(user);
                }

                // Send response
                context.response()
                    .putHeader("Content-Type", "application/json")
                    .end(new JsonObject()
                        .put("success", true)
                        .put("users", results)
                        .encodePrettily());
            })
            .onFailure(err -> {
                // Handle error
                context.response()
                    .setStatusCode(500)
                    .putHeader("Content-Type", "application/json")
                    .end(new JsonObject()
                        .put("success", false)
                        .put("error", err.getMessage())
                        .encodePrettily());
            });
    }

    @Override
    public void stop() {
        // Cleanup resources
        if (pgPool != null) {
            pgPool.close();
            System.out.println("PostgreSQL connection pool closed");
        }
    }

    @Override
    public JsonObject getData() {
        return config;
    }
}
```

### Configuration Structure

**Location**: `config/CRUDUsersVerticle.v1/`

**lambda.json** (metadata):
```json
{
  "artifactId": "user-query-service",
  "verticleClass": "com.example.verticles.UserQueryVerticle",
  "version": "v1",
  "endpoint": "/api/users/query",
  "handlerType": "AsyncHandler"
}
```

**config.json** (endpoint-specific config):
```json
{
  "database": {
    "host": "postgres.example.com",
    "port": 5432,
    "database": "userdb",
    "user": "app_user",
    "password": "${DB_PASSWORD}",
    "maxPoolSize": 20
  },
  "timeout": 5000,
  "retryAttempts": 3
}
```

## Example 2: Async HTTP Client Handler

This example shows an async handler that calls external REST APIs.

### Verticle Code

```java
package com.example.verticles;

import com.example.api.AsyncHandler;
import io.vertx.core.Vertx;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;
import io.vertx.ext.web.client.WebClient;
import io.vertx.ext.web.client.WebClientOptions;

public class ExternalApiVerticle implements AsyncHandler {

    private WebClient webClient;
    private JsonObject config;

    @Override
    public void start(Vertx vertx, JsonObject config) {
        this.config = config;

        // Get API config from config.json
        JsonObject apiConfig = config().getData().getJsonObject("externalApi");

        // Initialize HTTP client
        WebClientOptions options = new WebClientOptions()
            .setDefaultHost(apiConfig.getString("host"))
            .setDefaultPort(apiConfig.getInteger("port", 443))
            .setSsl(apiConfig.getBoolean("ssl", true))
            .setConnectTimeout(apiConfig.getInteger("connectTimeout", 5000))
            .setMaxPoolSize(apiConfig.getInteger("maxPoolSize", 50));

        webClient = WebClient.create(vertx, options);

        System.out.println("ExternalApiVerticle started with API host: " + apiConfig.getString("host"));
    }

    @Override
    public void handle(RoutingContext context) {
        // Parse request
        JsonObject requestBody = context.body().asJsonObject();
        String resourceId = requestBody.getString("resourceId");

        // Get config
        JsonObject apiConfig = config().getData().getJsonObject("externalApi");
        String apiPath = apiConfig.getString("path");
        String apiKey = apiConfig.getString("apiKey");

        // Make async HTTP call
        webClient
            .get(apiPath + "/" + resourceId)
            .putHeader("Authorization", "Bearer " + apiKey)
            .putHeader("Accept", "application/json")
            .send()
            .onSuccess(response -> {
                // Process response
                JsonObject data = response.bodyAsJsonObject();

                // Send response
                context.response()
                    .putHeader("Content-Type", "application/json")
                    .end(new JsonObject()
                        .put("success", true)
                        .put("statusCode", response.statusCode())
                        .put("data", data)
                        .encodePrettily());
            })
            .onFailure(err -> {
                // Handle error
                context.response()
                    .setStatusCode(500)
                    .putHeader("Content-Type", "application/json")
                    .end(new JsonObject()
                        .put("success", false)
                        .put("error", err.getMessage())
                        .encodePrettily());
            });
    }

    @Override
    public void stop() {
        // Cleanup resources
        if (webClient != null) {
            webClient.close();
            System.out.println("WebClient closed");
        }
    }

    @Override
    public JsonObject getData() {
        return config;
    }
}
```

### Configuration Structure

**Location**: `config/ExternalApiVerticle.v1/`

**lambda.json** (metadata):
```json
{
  "artifactId": "external-api-service",
  "verticleClass": "com.example.verticles.ExternalApiVerticle",
  "version": "v1",
  "endpoint": "/api/external/fetch",
  "handlerType": "AsyncHandler"
}
```

**config.json** (endpoint-specific config):
```json
{
  "externalApi": {
    "host": "api.external-service.com",
    "port": 443,
    "ssl": true,
    "path": "/v1/resources",
    "apiKey": "${EXTERNAL_API_KEY}",
    "connectTimeout": 5000,
    "requestTimeout": 10000,
    "maxPoolSize": 50
  },
  "retryConfig": {
    "maxAttempts": 3,
    "backoffMs": 1000
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

    // For PostgreSQL example
    implementation 'io.vertx:vertx-pg-client:4.5.0'

    // For HTTP client example
    implementation 'io.vertx:vertx-web-client:4.5.0'

    // JSON support
    implementation 'io.vertx:vertx-json-schema:4.5.0'
}
```

## Key Patterns

### 1. Configuration Access
```java
// In start() method
JsonObject dbConfig = config().getData().getJsonObject("database");

// In handle() method
JsonObject apiConfig = config().getData().getJsonObject("externalApi");
```

### 2. Async Response Pattern
```java
// Success
context.response()
    .putHeader("Content-Type", "application/json")
    .end(jsonResponse.encodePrettily());

// Error
context.response()
    .setStatusCode(500)
    .putHeader("Content-Type", "application/json")
    .end(errorJson.encodePrettily());
```

### 3. Resource Initialization (start)
- Initialize connection pools
- Create HTTP clients
- Load configuration
- Set up any shared resources

### 4. Resource Cleanup (stop)
- Close connection pools
- Close HTTP clients
- Release any allocated resources

## Best Practices

1. **Never block the event loop** - Use async operations only
2. **Always handle errors** - Implement `.onFailure()` handlers
3. **Use connection pooling** - Initialize pools in `start()`, reuse in `handle()`
4. **Close resources in stop()** - Clean up to prevent resource leaks
5. **Use config().getData()** - Don't hardcode values, use configuration
6. **Validate input** - Check request body before processing
7. **Return proper status codes** - 200 for success, 4xx for client errors, 5xx for server errors

## Common Use Cases

- Database queries (PostgreSQL, MySQL, MongoDB)
- REST API calls to external services
- Message queue operations (Kafka, RabbitMQ)
- Cache operations (Redis, Memcached)
- Email/SMS notifications
- Any non-blocking I/O operations

## Notes

- **Deployment is handled by platform** - No need to write deployment code
- **Routing is handled by platform** - Endpoint configured in `lambda.json`
- **Configuration is managed by platform** - Placed in `config/{VerticleName}.v{version}/` directory
