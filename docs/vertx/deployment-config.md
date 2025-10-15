# Vert.x Deployment Configurations

## Overview
This guide covers common deployment configurations and patterns for Vert.x verticles.

## Standard Deployment Options

### Single Instance
Deploy a single instance of a verticle with custom configuration.

```java
JsonObject config = new JsonObject()
    .put("key", "value");

DeploymentOptions options = new DeploymentOptions()
    .setConfig(config)
    .setInstances(1);

vertx.deployVerticle(new MyVerticle(), options, res -> {
    if (res.succeeded()) {
        String deploymentID = res.result();
        System.out.println("Deployment ID: " + deploymentID);
    } else {
        System.err.println("Deployment failed");
    }
});
```

### Multiple Instances
Deploy multiple instances of a verticle for better throughput.

```java
DeploymentOptions options = new DeploymentOptions()
    .setConfig(config)
    .setInstances(4); // 4 instances

vertx.deployVerticle(new MyVerticle(), options);
```

### Worker Pool Deployment
For blocking operations, deploy as a worker verticle.

```java
DeploymentOptions options = new DeploymentOptions()
    .setConfig(config)
    .setWorker(true)
    .setWorkerPoolSize(10)
    .setWorkerPoolName("my-worker-pool");

vertx.deployVerticle(new MyVerticle(), options);
```

### High Availability (HA)
Enable HA for automatic failover in clustered mode.

```java
DeploymentOptions options = new DeploymentOptions()
    .setConfig(config)
    .setHa(true);

vertx.deployVerticle(new MyVerticle(), options);
```

## Configuration Sources

### JSON File
Load configuration from a JSON file.

```java
vertx.fileSystem().readFile("config.json", res -> {
    if (res.succeeded()) {
        JsonObject config = res.result().toJsonObject();
        DeploymentOptions options = new DeploymentOptions().setConfig(config);
        vertx.deployVerticle(new MyVerticle(), options);
    } else {
        System.err.println("Failed to read config file: " + res.cause());
    }
});
```

### Environment Variables
Read configuration from environment variables.

```java
JsonObject config = new JsonObject()
    .put("database.host", System.getenv("DB_HOST"))
    .put("database.port", Integer.parseInt(System.getenv("DB_PORT")))
    .put("database.name", System.getenv("DB_NAME"));

DeploymentOptions options = new DeploymentOptions().setConfig(config);
```

### System Properties
Use Java system properties for configuration.

```java
JsonObject config = new JsonObject()
    .put("http.port", Integer.parseInt(System.getProperty("http.port", "8080")))
    .put("http.host", System.getProperty("http.host", "0.0.0.0"));

DeploymentOptions options = new DeploymentOptions().setConfig(config);
```

### ConfigRetriever (Vert.x Config)
Use Vert.x Config module for advanced configuration management.

```gradle
dependencies {
    implementation 'io.vertx:vertx-config:4.5.0'
}
```

```java
import io.vertx.config.ConfigRetriever;
import io.vertx.config.ConfigRetrieverOptions;
import io.vertx.config.ConfigStoreOptions;

ConfigStoreOptions fileStore = new ConfigStoreOptions()
    .setType("file")
    .setConfig(new JsonObject().put("path", "config.json"));

ConfigStoreOptions envStore = new ConfigStoreOptions()
    .setType("env");

ConfigRetrieverOptions options = new ConfigRetrieverOptions()
    .addStore(fileStore)
    .addStore(envStore);

ConfigRetriever retriever = ConfigRetriever.create(vertx, options);

retriever.getConfig(ar -> {
    if (ar.succeeded()) {
        JsonObject config = ar.result();
        DeploymentOptions deployOptions = new DeploymentOptions().setConfig(config);
        vertx.deployVerticle(new MyVerticle(), deployOptions);
    }
});
```

## Undeployment

### Undeploy Specific Verticle
```java
vertx.undeploy(deploymentID, res -> {
    if (res.succeeded()) {
        System.out.println("Undeployed successfully");
    } else {
        System.err.println("Undeploy failed");
    }
});
```

### Undeploy All
```java
Set<String> deploymentIDs = vertx.deploymentIDs();
for (String id : deploymentIDs) {
    vertx.undeploy(id);
}
```

## Gradle Build Configuration

### build.gradle
```gradle
plugins {
    id 'java'
    id 'application'
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'io.vertx:vertx-core:4.5.0'
    implementation 'io.vertx:vertx-web:4.5.0'
    implementation 'io.vertx:vertx-pg-client:4.5.0'

    testImplementation 'io.vertx:vertx-junit5:4.5.0'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.9.0'
}

application {
    mainClass = 'com.example.MainVerticle'
}

test {
    useJUnitPlatform()
}
```

### Run with Gradle
```bash
./gradlew run
```

## Best Practices

1. **Configuration Management**: Use environment variables for sensitive data (passwords, API keys)
2. **Instance Count**: Match instance count to CPU cores for event loop verticles
3. **Worker Verticles**: Use worker verticles for blocking operations (file I/O, JDBC)
4. **HA Mode**: Enable HA in production for automatic failover
5. **Resource Cleanup**: Always close resources in `stop()` method
6. **Logging**: Use SLF4J for consistent logging across verticles
