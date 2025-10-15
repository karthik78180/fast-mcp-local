# V1 to V2 Migration - Step-by-Step Instructions

## Overview

This guide provides detailed step-by-step instructions for migrating from V1 to V2.

**Important:** Execute these steps in your target project repository (not this repo).

---

## Step 1: Add OpenRewrite Plugin and Dependency

### Action

Add the OpenRewrite Gradle plugin and migration recipe dependency to your `build.gradle`:

```gradle
plugins {
    id 'java'
    id 'org.openrewrite.rewrite' version '6.1.0'  // Add this
}

dependencies {
    // Your existing dependencies...

    // Add OpenRewrite migration recipe
    rewrite 'com.example:migration-recipes:1.0.0'
}
```

### Verification

Run the following command to verify the plugin is installed:

```bash
./gradlew rewriteDiscover
```

**Expected output:** List of available recipes including `com.example.V1ToV2Migration`

### Troubleshooting

**Problem:** Plugin not found
- **Solution:** Check Gradle version (must be 7.0+)
- **Solution:** Try `./gradlew --refresh-dependencies`

**Problem:** Recipe not listed in `rewriteDiscover`
- **Solution:** Verify dependency coordinates (group:artifact:version)
- **Solution:** Check artifact repository accessibility
- **Solution:** Run `./gradlew dependencies --configuration rewrite` to debug

---

## Step 2: Run Prerequisites Check

### Action

Verify your environment meets all requirements:

```bash
# Check Java version (must be 11+)
java -version

# Check Gradle version (must be 7.0+)
./gradlew --version

# Check git status (should be clean)
git status
```

### Expected Results

- **Java:** Version 11 or higher
- **Gradle:** Version 7.0 or higher
- **Git:** No uncommitted changes (recommended)

### Recommendations

If you have uncommitted changes:
```bash
# Create a backup branch
git checkout -b pre-migration-backup

# Or commit your current work
git add .
git commit -m "Pre-migration checkpoint"
git checkout -b v2-migration
```

---

## Step 3: Run Dry Run (Preview Changes)

### Action

Run OpenRewrite in dry-run mode to preview changes without modifying files:

```bash
./gradlew rewriteDryRun -Drewrite.activeRecipes=com.example.V1ToV2Migration
```

### Expected Output

You should see:
- List of files that will be modified
- Summary of transformations
- No actual file changes (dry run only)

### What to Look For

Review the output to understand:
- Which files will be changed
- What types of transformations will occur
- Estimated scope of migration

### Troubleshooting

**Problem:** No recipes run
- **Solution:** Check recipe name spelling: `com.example.V1ToV2Migration`
- **Solution:** Verify recipe is in `rewriteDiscover` output

**Problem:** Unexpected files in output
- **Solution:** Review recipe scope - may be correct
- **Solution:** Check if you're in the right directory

---

## Step 4: Apply Migration

### Action

Apply the migration transformations to your codebase:

```bash
./gradlew rewriteRun -Drewrite.activeRecipes=com.example.V1ToV2Migration
```

### Expected Output

- Progress indicators for each file
- Summary of changes applied
- Modified files written to disk

### Verification

Check what changed:

```bash
# See all modified files
git status

# Review changes
git diff

# See statistics
git diff --stat
```

### What Changed

The migration typically updates:
- Method signatures
- Import statements
- Configuration files
- Deprecated API usage
- Package references

### Troubleshooting

**Problem:** Migration fails midway
- **Solution:** Check error message for specific file/issue
- **Solution:** May need to fix syntax errors first
- **Solution:** Revert with `git checkout .` and retry after fixes

**Problem:** Some files not updated
- **Solution:** May be expected - some changes require manual updates
- **Solution:** Check migration guide for known manual steps

---

## Step 5: Verify and Test

### Action

Verify the migration succeeded and all tests pass:

```bash
# Clean build
./gradlew clean

# Compile code
./gradlew build

# Run tests
./gradlew test

# Or all in one
./gradlew clean build test
```

### Expected Results

- ✅ Compilation succeeds
- ✅ All tests pass
- ✅ No new warnings (or expected warnings)

### Review Changes

Manually review critical changes:

```bash
# Review all changes
git diff

# Review specific file types
git diff -- '*.java'
git diff -- '*.gradle'
git diff -- '*.properties'
```

### Manual Fixes (If Needed)

Some edge cases may need manual updates:

1. **Custom configurations** - Review config files
2. **Complex generics** - May need type parameter adjustments
3. **Reflection code** - Update class/method names if changed
4. **Documentation** - Update README, javadocs

### Commit Migration

Once verified:

```bash
git add .
git commit -m "Migrate from V1 to V2 using OpenRewrite

Applied automated migration recipe: com.example.V1ToV2Migration

Changes:
- Updated API signatures to V2
- Migrated configuration format
- Removed deprecated method usage
- Reorganized package structure

All tests passing.
"
```

### Troubleshooting

**Problem:** Build fails
- **Solution:** Check error messages for specific issues
- **Solution:** May need manual fixes for complex code patterns
- **Solution:** Review migration guide for known issues

**Problem:** Tests fail
- **Solution:** Review test failures - may be test code needs updates
- **Solution:** Check if test assertions need updating for V2 behavior
- **Solution:** Update test dependencies if needed

**Problem:** Runtime errors
- **Solution:** Check configuration files are properly migrated
- **Solution:** Verify all dependencies are V2-compatible
- **Solution:** Look for reflection/dynamic code that may need updates

---

## Post-Migration Checklist

After completing all steps:

- [ ] All files compiled successfully
- [ ] All tests passing
- [ ] No unexpected warnings
- [ ] Manual review of critical changes completed
- [ ] Documentation updated
- [ ] Changes committed to git
- [ ] CI/CD pipeline passing (if applicable)

## Rollback (If Needed)

If you need to rollback:

```bash
# If on migration branch
git checkout main  # or your previous branch

# If committed to main
git revert HEAD

# Nuclear option (destroys all changes)
git reset --hard HEAD~1  # Use with caution!
```

## Next Steps

- Deploy to test environment
- Perform integration testing
- Update team documentation
- Plan production deployment

## Support

For issues or questions:
- Review OpenRewrite documentation: https://docs.openrewrite.org
- Check recipe repository for known issues
- Contact migration recipe maintainers
