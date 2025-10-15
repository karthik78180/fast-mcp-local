# PostgreSQL Verticle Template

## Description
A verticle for PostgreSQL database operations using Vert.x PostgreSQL client with reactive connection pooling.

## Gradle Dependencies
```gradle
dependencies {
    implementation 'io.vertx:vertx-core:4.5.0'
    implementation 'io.vertx:vertx-pg-client:4.5.0'
}
```

## Verticle Code
```java
package com.example.verticles;

import io.vertx.core.AbstractVerticle;
import io.vertx.core.Promise;
import io.vertx.core.json.JsonObject;
import io.vertx.pgclient.PgConnectOptions;
import io.vertx.pgclient.PgPool;
import io.vertx.sqlclient.PoolOptions;
import io.vertx.sqlclient.Row;
import io.vertx.sqlclient.RowSet;

public class PostgresVerticle extends AbstractVerticle {

    private PgPool client;

    @Override
    public void start(Promise<Void> startPromise) {
        JsonObject postgresConfig = config().getJsonObject("postgres", new JsonObject());

        PgConnectOptions connectOptions = new PgConnectOptions()
            .setPort(postgresConfig.getInteger("port", 5432))
            .setHost(postgresConfig.getString("host", "localhost"))
            .setDatabase(postgresConfig.getString("database", "mydb"))
            .setUser(postgresConfig.getString("user", "user"))
            .setPassword(postgresConfig.getString("password", "password"));

        PoolOptions poolOptions = new PoolOptions()
            .setMaxSize(postgresConfig.getInteger("poolSize", 5));

        client = PgPool.pool(vertx, connectOptions, poolOptions);

        // Test connection
        client.query("SELECT 1").execute(ar -> {
            if (ar.succeeded()) {
                System.out.println("PostgreSQL connection established");
                startPromise.complete();
            } else {
                System.err.println("Failed to connect to PostgreSQL: " + ar.cause().getMessage());
                startPromise.fail(ar.cause());
            }
        });
    }

    @Override
    public void stop(Promise<Void> stopPromise) {
        if (client != null) {
            client.close();
        }
        stopPromise.complete();
    }

    // Example query method
    public void executeQuery(String sql, io.vertx.core.Handler<io.vertx.core.AsyncResult<RowSet<Row>>> handler) {
        client.query(sql).execute(handler);
    }
}
```

## Configuration Example
```json
{
  "postgres": {
    "host": "localhost",
    "port": 5432,
    "database": "mydb",
    "user": "dbuser",
    "password": "dbpass",
    "poolSize": 10
  }
}
```

## Deployment Example
```java
JsonObject config = new JsonObject()
    .put("postgres", new JsonObject()
        .put("host", "localhost")
        .put("port", 5432)
        .put("database", "users")
        .put("user", "appuser")
        .put("password", "apppass")
        .put("poolSize", 10));

DeploymentOptions options = new DeploymentOptions()
    .setConfig(config)
    .setInstances(1);

vertx.deployVerticle(new PostgresVerticle(), options, res -> {
    if (res.succeeded()) {
        System.out.println("PostgreSQL Verticle deployed: " + res.result());
    } else {
        System.err.println("Deployment failed: " + res.cause().getMessage());
    }
});
```

## Use Cases
- CRUD operations on PostgreSQL database
- Connection pooling for high-performance applications
- Reactive database queries with non-blocking I/O
- Microservices with PostgreSQL backend
