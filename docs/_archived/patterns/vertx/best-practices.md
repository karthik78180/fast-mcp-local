# Vert.x Best Practices

## Overview

This document outlines best practices for building Vert.x verticles and applications. Following these practices will improve code quality, maintainability, performance, and security.

## Deployment & Lifecycle

### ✅ Use DeploymentOptions

Always use `DeploymentOptions` when deploying verticles to control configuration, instances, and resources.

**Good:**
```java
DeploymentOptions options = new DeploymentOptions()
    .setConfig(config)
    .setInstances(4)
    .setWorker(false);

vertx.deployVerticle(new MyVerticle(), options);
```

**Bad:**
```java
vertx.deployVerticle(new MyVerticle());  // No configuration control
```

### ✅ Use Promise for Async Start

Override `start(Promise<Void>)` instead of `start()` for proper async initialization.

**Good:**
```java
@Override
public void start(Promise<Void> startPromise) {
    httpServer.listen(8080, ar -> {
        if (ar.succeeded()) {
            startPromise.complete();
        } else {
            startPromise.fail(ar.cause());
        }
    });
}
```

**Bad:**
```java
@Override
public void start() {
    httpServer.listen(8080);  // No way to signal completion
}
```

## Error Handling

### ✅ Always Check AsyncResult

Every async operation should check `succeeded()` and handle `failed()` cases.

**Good:**
```java
client.query("SELECT * FROM users").execute(ar -> {
    if (ar.succeeded()) {
        RowSet<Row> rows = ar.result();
        // Process rows
    } else {
        logger.error("Query failed", ar.cause());
        // Handle error
    }
});
```

**Bad:**
```java
client.query("SELECT * FROM users").execute(ar -> {
    RowSet<Row> rows = ar.result();  // May throw if failed!
});
```

### ✅ Use Proper Logging

Use a logger instead of `printStackTrace()`.

**Good:**
```java
try {
    // code
} catch (Exception e) {
    logger.error("Operation failed", e);
}
```

**Bad:**
```java
try {
    // code
} catch (Exception e) {
    e.printStackTrace();  // Not production-ready
}
```

### ❌ Never Block the Event Loop

**Critical:** Never use `Thread.sleep()` or other blocking operations in the event loop.

**Bad:**
```java
public void handle(HttpServerRequest request) {
    Thread.sleep(1000);  // BLOCKS EVENT LOOP!
    request.response().end("Done");
}
```

**Good:**
```java
public void handle(HttpServerRequest request) {
    vertx.setTimer(1000, id -> {
        request.response().end("Done");
    });
}
```

For truly blocking operations:
```java
vertx.executeBlocking(promise -> {
    // Blocking code here
    Thread.sleep(1000);
    promise.complete();
}, res -> {
    // Back on event loop
});
```

## Configuration

### ✅ Externalize Configuration

Use the `config()` method to access externalized configuration.

**Good:**
```java
JsonObject dbConfig = config().getJsonObject("database");
String host = dbConfig.getString("host", "localhost");
int port = dbConfig.getInteger("port", 5432);
```

**Bad:**
```java
String host = "localhost";  // Hardcoded!
int port = 5432;
```

### ❌ Never Hardcode Credentials

**Critical:** Credentials, API keys, and secrets must NEVER be in source code.

**Bad:**
```java
String password = "mySecretPassword123";  // CRITICAL SECURITY ISSUE!
String apiKey = "sk_live_abc123xyz";
```

**Good:**
```java
String password = config().getString("database.password");
String apiKey = System.getenv("API_KEY");
```

### ✅ Externalize URLs and Endpoints

**Bad:**
```java
String apiUrl = "https://api.example.com";  // Hardcoded
```

**Good:**
```java
String apiUrl = config().getString("api.url");
```

## Database

### ✅ Use Connection Pooling

Always use connection pools for database access.

**Good:**
```java
PgConnectOptions connectOptions = new PgConnectOptions()
    .setHost(host)
    .setPort(port)
    .setDatabase(database);

PoolOptions poolOptions = new PoolOptions()
    .setMaxSize(10);

PgPool pool = PgPool.pool(vertx, connectOptions, poolOptions);
```

**Bad:**
```java
// Creating new connection for each query (inefficient!)
PgConnection.connect(vertx, connectOptions, ar -> {
    // Use connection
});
```

### ✅ Use Parameterized Queries

**Critical:** Prevent SQL injection with parameterized queries.

**Good:**
```java
client.preparedQuery("SELECT * FROM users WHERE id = $1")
    .execute(Tuple.of(userId), ar -> {
        // Process result
    });
```

**Bad:**
```java
String query = "SELECT * FROM users WHERE id = " + userId;  // SQL INJECTION!
client.query(query).execute(ar -> {
    // Process result
});
```

### ❌ Never Concatenate SQL

**Critical:** String concatenation in SQL queries is dangerous.

**Bad:**
```java
String query = "SELECT * FROM users WHERE name = '" + name + "'";  // DANGER!
```

**Good:**
```java
client.preparedQuery("SELECT * FROM users WHERE name = $1")
    .execute(Tuple.of(name), ar -> {
        // Safe from SQL injection
    });
```

## HTTP

### ✅ Use Vert.x Web Router

For HTTP servers, use Router for better route management.

**Good:**
```java
Router router = Router.router(vertx);
router.get("/api/users").handler(this::getUsers);
router.post("/api/users").handler(this::createUser);

httpServer.requestHandler(router).listen(8080);
```

**Bad:**
```java
httpServer.requestHandler(request -> {
    if (request.path().equals("/api/users")) {
        // Manual routing is error-prone
    }
}).listen(8080);
```

### ✅ Add Global Error Handler

Always add error handlers to catch exceptions.

**Good:**
```java
router.errorHandler(500, ctx -> {
    logger.error("Internal error", ctx.failure());
    ctx.response()
        .setStatusCode(500)
        .end("Internal Server Error");
});
```

## Summary Checklist

- [ ] Use `DeploymentOptions` for verticle deployment
- [ ] Override `start(Promise<Void>)` for async init
- [ ] Check `ar.succeeded()` / `ar.failed()` in all async callbacks
- [ ] Never use `Thread.sleep()` in event loop
- [ ] Use `config()` for all configuration
- [ ] No hardcoded credentials or secrets
- [ ] Use connection pools for databases
- [ ] Use parameterized queries (prevent SQL injection)
- [ ] Use Router for HTTP servers
- [ ] Add global error handlers
- [ ] Use proper logging (not `printStackTrace()`)

## References

- [Vert.x Documentation](https://vertx.io/docs/)
- [Vert.x Best Practices](https://vertx.io/docs/vertx-core/java/#_best_practices)
- Verticle Templates: `docs/vertx/templates/`
- Deployment Config: `docs/vertx/deployment-config.md`
