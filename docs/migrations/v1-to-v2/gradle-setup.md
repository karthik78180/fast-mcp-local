# Gradle Setup for V1 to V2 Migration

## Quick Reference

This document provides a quick reference for setting up OpenRewrite in your Gradle project.

## Basic Setup

### build.gradle (Groovy)

```gradle
plugins {
    id 'java'
    id 'org.openrewrite.rewrite' version '6.1.0'
}

dependencies {
    // Add migration recipe
    rewrite 'com.example:migration-recipes:1.0.0'
}

// Optional: Configure OpenRewrite
rewrite {
    activeRecipe('com.example.V1ToV2Migration')
}
```

### build.gradle.kts (Kotlin DSL)

```kotlin
plugins {
    java
    id("org.openrewrite.rewrite") version "6.1.0"
}

dependencies {
    // Add migration recipe
    rewrite("com.example:migration-recipes:1.0.0")
}

// Optional: Configure OpenRewrite
rewrite {
    activeRecipe("com.example.V1ToV2Migration")
}
```

## Commands

### Discover Available Recipes

```bash
./gradlew rewriteDiscover
```

### Dry Run (Preview Changes)

```bash
./gradlew rewriteDryRun -Drewrite.activeRecipes=com.example.V1ToV2Migration
```

### Apply Migration

```bash
./gradlew rewriteRun -Drewrite.activeRecipes=com.example.V1ToV2Migration
```

### Check Dependencies

```bash
./gradlew dependencies --configuration rewrite
```

## Advanced Configuration

### Exclude Specific Files

```gradle
rewrite {
    activeRecipe('com.example.V1ToV2Migration')
    exclusions = ['**/generated/**', '**/build/**']
}
```

### Multiple Recipes

```gradle
rewrite {
    activeRecipes = [
        'com.example.V1ToV2Migration',
        'org.openrewrite.java.format.AutoFormat'
    ]
}
```

### Custom Configuration

```gradle
rewrite {
    activeRecipe('com.example.V1ToV2Migration')

    // Set JVM args
    jvmArgs = ['-Xmx2g']

    // Enable metrics
    metricsUri = 'https://your-metrics-endpoint.com'
}
```

## Troubleshooting

### Issue: Plugin Version Conflict

If you see plugin version conflicts:

```gradle
buildscript {
    repositories {
        gradlePluginPortal()
    }
    dependencies {
        classpath 'org.openrewrite:plugin:6.1.0'
    }
}
```

### Issue: Recipe Not Found

Ensure the dependency is in the `rewrite` configuration:

```gradle
dependencies {
    rewrite('com.example:migration-recipes:1.0.0') {
        // Force latest version
        force = true
    }
}
```

### Issue: Out of Memory

Increase Gradle memory:

**gradle.properties:**
```properties
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=512m
```

**Or in build.gradle:**
```gradle
rewrite {
    jvmArgs = ['-Xmx4g']
}
```

## Repository Configuration

If your migration recipes are in a private repository:

```gradle
repositories {
    mavenCentral()

    // Private repository
    maven {
        url 'https://your-private-repo.com/maven'
        credentials {
            username = project.findProperty('repoUser') ?: System.getenv('REPO_USER')
            password = project.findProperty('repoPassword') ?: System.getenv('REPO_PASSWORD')
        }
    }
}
```

## References

- OpenRewrite Gradle Plugin: https://docs.openrewrite.org/reference/gradle-plugin-configuration
- Recipe Development: https://docs.openrewrite.org/authoring-recipes
- Migration Recipes Repository: [Your recipe repository URL]
