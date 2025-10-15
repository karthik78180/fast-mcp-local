# Vert.x Anti-Patterns

## Overview

This document lists common anti-patterns and mistakes in Vert.x applications that should be avoided. These patterns can lead to performance issues, bugs, security vulnerabilities, and maintenance headaches.

## 🔴 Critical Anti-Patterns

### ❌ Blocking the Event Loop

**The Problem:** Using blocking operations in the event loop causes performance degradation and can crash your application.

**Examples:**
```java
// ❌ NEVER DO THIS
public void handle(HttpServerRequest request) {
    Thread.sleep(1000);  // Blocks event loop!
    request.response().end();
}

// ❌ ALSO BAD
public void start() {
    InputStream is = new FileInputStream("file.txt");  // Blocking I/O!
}
```

**Why It's Bad:**
- Blocks all other operations
- Causes thread starvation
- Triggers "Event Loop Blocked" warnings
- Degrades overall performance

**Solution:**
```java
// ✅ Use timers
vertx.setTimer(1000, id -> {
    request.response().end();
});

// ✅ Use executeBlocking for truly blocking code
vertx.executeBlocking(promise -> {
    InputStream is = new FileInputStream("file.txt");
    // Do blocking work
    promise.complete();
}, res -> {
    // Back on event loop
});
```

### ❌ Hardcoded Credentials

**The Problem:** Storing passwords, API keys, or secrets in source code is a critical security vulnerability.

**Examples:**
```java
// ❌ CRITICAL SECURITY ISSUE
String dbPassword = "mySecretPassword123";
String apiKey = "sk_live_abc123xyz456";
String jwtSecret = "my-super-secret-key";
```

**Why It's Bad:**
- Credentials visible in version control
- Easy to leak in logs or stack traces
- Cannot rotate without code changes
- Violates security best practices

**Solution:**
```java
// ✅ Use configuration
String dbPassword = config().getString("database.password");

// ✅ Use environment variables
String apiKey = System.getenv("API_KEY");

// ✅ Use secret management
String jwtSecret = secretManager.getSecret("jwt.secret");
```

### ❌ SQL String Concatenation

**The Problem:** Building SQL queries with string concatenation opens SQL injection vulnerabilities.

**Examples:**
```java
// ❌ SQL INJECTION VULNERABILITY
String userId = request.getParam("id");
String query = "SELECT * FROM users WHERE id = " + userId;
client.query(query).execute(...);

// ❌ ALSO VULNERABLE
String name = request.getParam("name");
String sql = "SELECT * FROM users WHERE name = '" + name + "'";
```

**Why It's Bad:**
- Allows SQL injection attacks
- Attackers can execute arbitrary SQL
- Can lead to data theft or corruption
- Critical security vulnerability

**Solution:**
```java
// ✅ Use parameterized queries
client.preparedQuery("SELECT * FROM users WHERE id = $1")
    .execute(Tuple.of(userId), ar -> {
        // Safe from SQL injection
    });

// ✅ With multiple parameters
client.preparedQuery("SELECT * FROM users WHERE name = $1 AND age > $2")
    .execute(Tuple.of(name, age), ar -> {
        // Completely safe
    });
```

## 🟠 High-Priority Anti-Patterns

### ❌ Missing Error Handling

**The Problem:** Not checking AsyncResult leads to crashes and undefined behavior.

**Examples:**
```java
// ❌ Assumes success
client.query("SELECT * FROM users").execute(ar -> {
    RowSet<Row> rows = ar.result();  // Throws if query failed!
    processRows(rows);
});

// ❌ No error handling
httpServer.listen(8080, ar -> {
    System.out.println("Server started");  // But what if it failed?
});
```

**Why It's Bad:**
- Application crashes unexpectedly
- Silent failures
- No error visibility
- Hard to debug

**Solution:**
```java
// ✅ Always check succeeded/failed
client.query("SELECT * FROM users").execute(ar -> {
    if (ar.succeeded()) {
        RowSet<Row> rows = ar.result();
        processRows(rows);
    } else {
        logger.error("Query failed", ar.cause());
        handleError(ar.cause());
    }
});

// ✅ Handle server start failures
httpServer.listen(8080, ar -> {
    if (ar.succeeded()) {
        logger.info("Server started on port 8080");
    } else {
        logger.error("Server failed to start", ar.cause());
        vertx.close();
    }
});
```

### ❌ No Connection Pooling

**The Problem:** Creating new database connections for each query wastes resources.

**Examples:**
```java
// ❌ New connection every time
public void queryUser(String id, Handler<AsyncResult<User>> handler) {
    PgConnection.connect(vertx, connectOptions, ar -> {
        if (ar.succeeded()) {
            PgConnection connection = ar.result();
            connection.query("SELECT * FROM users WHERE id = " + id).execute(...);
            connection.close();  // Wasteful!
        }
    });
}
```

**Why It's Bad:**
- Poor performance
- Resource exhaustion
- Slow connection establishment
- Doesn't scale

**Solution:**
```java
// ✅ Use connection pool
PgPool pool = PgPool.pool(vertx, connectOptions, poolOptions);

public void queryUser(String id, Handler<AsyncResult<User>> handler) {
    pool.preparedQuery("SELECT * FROM users WHERE id = $1")
        .execute(Tuple.of(id), ar -> {
            // Pool handles connection management
        });
}
```

### ❌ Using printStackTrace()

**The Problem:** printStackTrace() is not suitable for production applications.

**Examples:**
```java
// ❌ Not production-ready
try {
    processData();
} catch (Exception e) {
    e.printStackTrace();  // Goes to stderr, not logged properly
}
```

**Why It's Bad:**
- Output goes to stderr, not log files
- Can't be filtered or searched
- Missing context and metadata
- Not suitable for production monitoring

**Solution:**
```java
// ✅ Use proper logging
private static final Logger logger = LoggerFactory.getLogger(MyVerticle.class);

try {
    processData();
} catch (Exception e) {
    logger.error("Failed to process data", e);
}
```

## 🟡 Medium-Priority Anti-Patterns

### ❌ Hardcoded URLs and Endpoints

**The Problem:** Hardcoding URLs makes code inflexible and environment-specific.

**Examples:**
```java
// ❌ Hardcoded URLs
String apiUrl = "https://api.production.example.com";
String dbHost = "db.company.internal";
int port = 8080;
```

**Why It's Bad:**
- Can't change environments without code changes
- Different configs for dev/test/prod
- Hard to test
- Not cloud-friendly

**Solution:**
```java
// ✅ Externalize all endpoints
String apiUrl = config().getString("api.url");
String dbHost = config().getString("database.host");
int port = config().getInteger("server.port", 8080);
```

### ❌ Manual Route Parsing

**The Problem:** Not using Router for HTTP server leads to messy code.

**Examples:**
```java
// ❌ Manual route handling
httpServer.requestHandler(request -> {
    String path = request.path();
    HttpMethod method = request.method();

    if (path.equals("/api/users") && method == HttpMethod.GET) {
        handleGetUsers(request);
    } else if (path.equals("/api/users") && method == HttpMethod.POST) {
        handleCreateUser(request);
    } else if (path.startsWith("/api/users/")) {
        String id = path.substring(11);
        handleGetUser(request, id);
    } else {
        request.response().setStatusCode(404).end();
    }
});
```

**Why It's Bad:**
- Error-prone
- Hard to maintain
- No middleware support
- No path parameters
- Messy conditional logic

**Solution:**
```java
// ✅ Use Router
Router router = Router.router(vertx);
router.get("/api/users").handler(this::handleGetUsers);
router.post("/api/users").handler(this::handleCreateUser);
router.get("/api/users/:id").handler(this::handleGetUser);

httpServer.requestHandler(router).listen(8080);
```

### ❌ Ignoring Promise/Future Completion

**The Problem:** Not completing promises in verticle lifecycle methods.

**Examples:**
```java
// ❌ Never completes
@Override
public void start(Promise<Void> startPromise) {
    httpServer.listen(8080);
    // startPromise never completed!
}

// ❌ Forgot to handle failure
@Override
public void start(Promise<Void> startPromise) {
    httpServer.listen(8080, ar -> {
        startPromise.complete();  // Always completes, even on failure!
    });
}
```

**Why It's Bad:**
- Verticle deployment hangs
- No failure propagation
- Can't detect startup issues
- Breaks deployment orchestration

**Solution:**
```java
// ✅ Properly complete promise
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

## Checklist: Avoid These

- [ ] ❌ No `Thread.sleep()` or blocking calls in event loop
- [ ] ❌ No hardcoded passwords, API keys, or secrets
- [ ] ❌ No SQL string concatenation
- [ ] ❌ No missing error handling in async callbacks
- [ ] ❌ No creating connections without pooling
- [ ] ❌ No `printStackTrace()` in production code
- [ ] ❌ No hardcoded URLs or endpoints
- [ ] ❌ No manual route parsing (use Router)
- [ ] ❌ No ignoring Promise completion
- [ ] ❌ No synchronous file I/O

## How to Fix

1. **Run code scoring:** `mcp score-codebase /path/to/verticle --pattern vertx-best-practices`
2. **Review violations:** Focus on critical issues first
3. **Refactor:** Apply recommended fixes
4. **Re-score:** Verify improvements
5. **Document:** Update code comments and docs

## References

- Best Practices Guide: `docs/patterns/vertx/best-practices.md`
- Vert.x Core Documentation: https://vertx.io/docs/vertx-core/java/
- Security Best Practices: https://vertx.io/docs/vertx-core/java/#_security_notes
