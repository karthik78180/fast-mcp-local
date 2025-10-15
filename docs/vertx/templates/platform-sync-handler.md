# Platform SyncHandler Verticle

## Description

The `SyncHandler` interface is provided by the platform for handling **synchronous, blocking operations**. Use this for SOAP services, legacy databases with JDBC, file I/O, or any operation that blocks the thread.

**Platform handles**: Deployment, routing, configuration, worker thread pool management

**Teams implement**: Business logic in `handle()` method using platform-provided interfaces

⚠️ **Important**: SyncHandler runs on worker threads, not event loop threads, so blocking is safe.

## SyncHandler Interface

```java
package com.example.api;

import io.vertx.core.Vertx;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;

/**
 * Interface for synchronous, blocking request handlers
 * Executes on worker thread pool - blocking operations are safe
 */
public interface SyncHandler {
    /**
     * Called when verticle is deployed
     * Initialize resources (JDBC connections, SOAP clients, etc.)
     */
    void start(Vertx vertx, JsonObject config);

    /**
     * Handle incoming sync/blocking request
     * Runs on worker thread - blocking is safe here
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

## Example 1: SOAP Service Handler

This example shows a sync handler that calls a SOAP web service.

### Verticle Code

```java
package com.example.verticles;

import com.example.api.SyncHandler;
import io.vertx.core.Vertx;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;

import javax.xml.soap.*;
import java.net.URL;

public class SoapServiceVerticle implements SyncHandler {

    private JsonObject config;
    private String soapEndpoint;
    private String soapAction;

    @Override
    public void start(Vertx vertx, JsonObject config) {
        this.config = config;

        // Get SOAP config from config.json
        JsonObject soapConfig = config().getData().getJsonObject("soap");

        this.soapEndpoint = soapConfig.getString("endpoint");
        this.soapAction = soapConfig.getString("soapAction");

        System.out.println("SoapServiceVerticle started with endpoint: " + soapEndpoint);
    }

    @Override
    public void handle(RoutingContext context) {
        try {
            // Parse request
            JsonObject requestBody = context.body().asJsonObject();
            String customerId = requestBody.getString("customerId");

            // Get SOAP config
            JsonObject soapConfig = config().getData().getJsonObject("soap");
            String namespace = soapConfig.getString("namespace");

            // Create SOAP message (blocking operation - safe in SyncHandler)
            MessageFactory messageFactory = MessageFactory.newInstance();
            SOAPMessage soapMessage = messageFactory.createMessage();
            SOAPPart soapPart = soapMessage.getSOAPPart();

            // Build SOAP envelope
            SOAPEnvelope envelope = soapPart.getEnvelope();
            SOAPBody soapBody = envelope.getBody();

            // Add SOAP body content
            SOAPElement operation = soapBody.addChildElement("GetCustomer", "ns", namespace);
            SOAPElement customerIdElement = operation.addChildElement("CustomerId", "ns");
            customerIdElement.addTextNode(customerId);

            // Set SOAP action header
            MimeHeaders headers = soapMessage.getMimeHeaders();
            headers.addHeader("SOAPAction", soapAction);

            soapMessage.saveChanges();

            // Call SOAP service (blocking - safe here)
            SOAPConnectionFactory soapConnectionFactory = SOAPConnectionFactory.newInstance();
            SOAPConnection soapConnection = soapConnectionFactory.createConnection();

            URL endpoint = new URL(soapEndpoint);
            SOAPMessage response = soapConnection.call(soapMessage, endpoint);

            // Parse SOAP response
            SOAPBody responseBody = response.getSOAPBody();
            String responseText = responseBody.getTextContent();

            soapConnection.close();

            // Send JSON response
            context.response()
                .putHeader("Content-Type", "application/json")
                .end(new JsonObject()
                    .put("success", true)
                    .put("data", responseText)
                    .encodePrettily());

        } catch (Exception e) {
            // Handle error
            context.response()
                .setStatusCode(500)
                .putHeader("Content-Type", "application/json")
                .end(new JsonObject()
                    .put("success", false)
                    .put("error", e.getMessage())
                    .encodePrettily());
        }
    }

    @Override
    public void stop() {
        System.out.println("SoapServiceVerticle stopped");
    }

    @Override
    public JsonObject getData() {
        return config;
    }
}
```

### Configuration Structure

**Location**: `config/SoapServiceVerticle.v1/`

**lambda.json** (metadata):
```json
{
  "artifactId": "soap-customer-service",
  "verticleClass": "com.example.verticles.SoapServiceVerticle",
  "version": "v1",
  "endpoint": "/api/soap/customer",
  "handlerType": "SyncHandler"
}
```

**config.json** (endpoint-specific config):
```json
{
  "soap": {
    "endpoint": "https://legacy.example.com/CustomerService",
    "soapAction": "http://example.com/GetCustomer",
    "namespace": "http://example.com/customer",
    "timeout": 30000,
    "username": "${SOAP_USERNAME}",
    "password": "${SOAP_PASSWORD}"
  },
  "retry": {
    "maxAttempts": 3,
    "delayMs": 2000
  }
}
```

## Example 2: JDBC Database Handler

This example shows a sync handler using traditional JDBC (blocking operations).

### Verticle Code

```java
package com.example.verticles;

import com.example.api.SyncHandler;
import io.vertx.core.Vertx;
import io.vertx.core.json.JsonArray;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.RoutingContext;

import java.sql.*;

public class JdbcQueryVerticle implements SyncHandler {

    private JsonObject config;
    private String jdbcUrl;
    private String username;
    private String password;

    @Override
    public void start(Vertx vertx, JsonObject config) {
        this.config = config;

        // Get JDBC config from config.json
        JsonObject dbConfig = config().getData().getJsonObject("database");

        this.jdbcUrl = dbConfig.getString("jdbcUrl");
        this.username = dbConfig.getString("username");
        this.password = dbConfig.getString("password");

        // Load JDBC driver
        try {
            Class.forName(dbConfig.getString("driverClass", "com.mysql.cj.jdbc.Driver"));
            System.out.println("JdbcQueryVerticle started with URL: " + jdbcUrl);
        } catch (ClassNotFoundException e) {
            System.err.println("JDBC driver not found: " + e.getMessage());
        }
    }

    @Override
    public void handle(RoutingContext context) {
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;

        try {
            // Parse request
            JsonObject requestBody = context.body().asJsonObject();
            String departmentId = requestBody.getString("departmentId");

            // Get database connection (blocking - safe in SyncHandler)
            conn = DriverManager.getConnection(jdbcUrl, username, password);

            // Execute query (blocking)
            String sql = "SELECT emp_id, emp_name, email FROM employees WHERE dept_id = ?";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, departmentId);

            rs = stmt.executeQuery();

            // Process results
            JsonArray employees = new JsonArray();
            while (rs.next()) {  // Blocking iteration
                JsonObject employee = new JsonObject()
                    .put("empId", rs.getString("emp_id"))
                    .put("name", rs.getString("emp_name"))
                    .put("email", rs.getString("email"));
                employees.add(employee);
            }

            // Send response
            context.response()
                .putHeader("Content-Type", "application/json")
                .end(new JsonObject()
                    .put("success", true)
                    .put("count", employees.size())
                    .put("employees", employees)
                    .encodePrettily());

        } catch (SQLException e) {
            // Handle database error
            context.response()
                .setStatusCode(500)
                .putHeader("Content-Type", "application/json")
                .end(new JsonObject()
                    .put("success", false)
                    .put("error", e.getMessage())
                    .put("sqlState", e.getSQLState())
                    .encodePrettily());
        } finally {
            // Cleanup resources (important for blocking operations)
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
            } catch (SQLException e) {
                System.err.println("Error closing resources: " + e.getMessage());
            }
        }
    }

    @Override
    public void stop() {
        System.out.println("JdbcQueryVerticle stopped");
    }

    @Override
    public JsonObject getData() {
        return config;
    }
}
```

### Configuration Structure

**Location**: `config/JdbcQueryVerticle.v1/`

**lambda.json** (metadata):
```json
{
  "artifactId": "jdbc-employee-service",
  "verticleClass": "com.example.verticles.JdbcQueryVerticle",
  "version": "v1",
  "endpoint": "/api/employees/query",
  "handlerType": "SyncHandler"
}
```

**config.json** (endpoint-specific config):
```json
{
  "database": {
    "jdbcUrl": "jdbc:mysql://legacy-db.example.com:3306/hrdb",
    "username": "${JDBC_USERNAME}",
    "password": "${JDBC_PASSWORD}",
    "driverClass": "com.mysql.cj.jdbc.Driver",
    "queryTimeout": 30000
  },
  "connectionPool": {
    "maxConnections": 20,
    "minConnections": 5,
    "idleTimeout": 600000
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

    // For SOAP example
    implementation 'javax.xml.soap:javax.xml.soap-api:1.4.0'
    implementation 'com.sun.xml.messaging.saaj:saaj-impl:1.5.3'

    // For JDBC example
    implementation 'mysql:mysql-connector-java:8.0.33'
    // or
    implementation 'org.postgresql:postgresql:42.6.0'
}
```

## Key Patterns

### 1. Configuration Access
```java
// In start() method
JsonObject soapConfig = config().getData().getJsonObject("soap");

// In handle() method
JsonObject dbConfig = config().getData().getJsonObject("database");
```

### 2. Blocking Operations (Safe in SyncHandler)
```java
// JDBC operations - blocking is OK
Connection conn = DriverManager.getConnection(url, user, pass);
ResultSet rs = stmt.executeQuery();

// SOAP calls - blocking is OK
SOAPMessage response = soapConnection.call(message, endpoint);

// File I/O - blocking is OK
FileInputStream fis = new FileInputStream(filePath);
```

### 3. Resource Cleanup
```java
// Always use try-finally for resource cleanup
finally {
    if (rs != null) rs.close();
    if (stmt != null) stmt.close();
    if (conn != null) conn.close();
}
```

### 4. Error Handling
```java
try {
    // Blocking operations
} catch (SQLException | SOAPException e) {
    context.response()
        .setStatusCode(500)
        .end(errorJson);
}
```

## Best Practices

1. **Use SyncHandler for blocking operations** - SOAP, JDBC, File I/O, Thread.sleep()
2. **Always cleanup resources** - Use try-finally blocks
3. **Handle exceptions properly** - Catch specific exceptions
4. **Close connections** - Don't leak database connections or file handles
5. **Use config().getData()** - Don't hardcode connection strings
6. **Set timeouts** - Configure reasonable timeouts for blocking operations
7. **Return proper status codes** - Match HTTP semantics

## Common Use Cases

- SOAP web service calls
- Legacy JDBC database queries
- File system operations (read/write files)
- Blocking HTTP clients
- Thread.sleep() or blocking computations
- Integration with legacy systems
- Synchronous message queue operations

## SyncHandler vs AsyncHandler

| Aspect | SyncHandler | AsyncHandler |
|--------|-------------|--------------|
| **Thread Pool** | Worker threads | Event loop |
| **Blocking** | ✅ Safe to block | ❌ Never block |
| **Use Case** | SOAP, JDBC, File I/O | HTTP, Async DB, Message queues |
| **Concurrency** | Limited by worker pool | High concurrency |
| **Performance** | Lower throughput | Higher throughput |

## Notes

- **Deployment is handled by platform** - No need to write deployment code
- **Routing is handled by platform** - Endpoint configured in `lambda.json`
- **Worker threads are managed by platform** - Platform configures worker pool size
- **Blocking is safe** - SyncHandler runs on dedicated worker threads
