# HTTP Server Verticle Template

## Description
A verticle for creating HTTP REST API servers using Vert.x Web router with middleware support.

## Gradle Dependencies
```gradle
dependencies {
    implementation 'io.vertx:vertx-core:4.5.0'
    implementation 'io.vertx:vertx-web:4.5.0'
}
```

## Verticle Code
```java
package com.example.verticles;

import io.vertx.core.AbstractVerticle;
import io.vertx.core.Promise;
import io.vertx.core.http.HttpServer;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.Router;
import io.vertx.ext.web.RoutingContext;
import io.vertx.ext.web.handler.BodyHandler;
import io.vertx.ext.web.handler.CorsHandler;

public class HttpVerticle extends AbstractVerticle {

    private HttpServer server;

    @Override
    public void start(Promise<Void> startPromise) {
        JsonObject httpConfig = config().getJsonObject("http", new JsonObject());
        int port = httpConfig.getInteger("port", 8080);
        String host = httpConfig.getString("host", "0.0.0.0");

        Router router = Router.router(vertx);

        // Middleware
        router.route().handler(BodyHandler.create());
        router.route().handler(CorsHandler.create());

        // Routes
        router.get("/api/health").handler(this::healthCheck);
        router.get("/api/items").handler(this::getItems);
        router.get("/api/items/:id").handler(this::getItem);
        router.post("/api/items").handler(this::createItem);
        router.put("/api/items/:id").handler(this::updateItem);
        router.delete("/api/items/:id").handler(this::deleteItem);

        // Create HTTP server
        server = vertx.createHttpServer()
            .requestHandler(router)
            .listen(port, host, http -> {
                if (http.succeeded()) {
                    System.out.println("HTTP server started on " + host + ":" + port);
                    startPromise.complete();
                } else {
                    System.err.println("Failed to start HTTP server: " + http.cause().getMessage());
                    startPromise.fail(http.cause());
                }
            });
    }

    @Override
    public void stop(Promise<Void> stopPromise) {
        if (server != null) {
            server.close(ar -> {
                if (ar.succeeded()) {
                    stopPromise.complete();
                } else {
                    stopPromise.fail(ar.cause());
                }
            });
        } else {
            stopPromise.complete();
        }
    }

    private void healthCheck(RoutingContext ctx) {
        ctx.response()
            .putHeader("content-type", "application/json")
            .end(new JsonObject().put("status", "UP").encode());
    }

    private void getItems(RoutingContext ctx) {
        // Example: Return list of items
        ctx.response()
            .putHeader("content-type", "application/json")
            .end(new JsonObject().put("items", new JsonObject()).encode());
    }

    private void getItem(RoutingContext ctx) {
        String id = ctx.pathParam("id");
        ctx.response()
            .putHeader("content-type", "application/json")
            .end(new JsonObject().put("id", id).encode());
    }

    private void createItem(RoutingContext ctx) {
        JsonObject body = ctx.body().asJsonObject();
        ctx.response()
            .setStatusCode(201)
            .putHeader("content-type", "application/json")
            .end(body.encode());
    }

    private void updateItem(RoutingContext ctx) {
        String id = ctx.pathParam("id");
        JsonObject body = ctx.body().asJsonObject();
        ctx.response()
            .putHeader("content-type", "application/json")
            .end(body.put("id", id).encode());
    }

    private void deleteItem(RoutingContext ctx) {
        String id = ctx.pathParam("id");
        ctx.response()
            .setStatusCode(204)
            .end();
    }
}
```

## Configuration Example
```json
{
  "http": {
    "host": "0.0.0.0",
    "port": 8080
  }
}
```

## Deployment Example
```java
JsonObject config = new JsonObject()
    .put("http", new JsonObject()
        .put("host", "0.0.0.0")
        .put("port", 8080));

DeploymentOptions options = new DeploymentOptions()
    .setConfig(config)
    .setInstances(1);

vertx.deployVerticle(new HttpVerticle(), options, res -> {
    if (res.succeeded()) {
        System.out.println("HTTP Verticle deployed: " + res.result());
    } else {
        System.err.println("Deployment failed: " + res.cause().getMessage());
    }
});
```

## Use Cases
- REST API servers
- Microservices HTTP endpoints
- Web application backends
- API gateways
- Health check endpoints
