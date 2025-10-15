# Adding Custom Chat Modes in GitHub Copilot Chat

This guide explains how to add custom chat modes (agents) in GitHub Copilot Chat for both **VS Code** and **IntelliJ IDEA**, specifically for Ask and Edit agent modes.

---

## Table of Contents
- [VS Code Setup](#vs-code-setup)
- [IntelliJ IDEA Setup](#intellij-idea-setup)
- [MCP Server Integration](#mcp-server-integration)
- [Testing Your Custom Chat Mode](#testing-your-custom-chat-mode)

---

## VS Code Setup

### Prerequisites
- VS Code version 1.85 or higher
- GitHub Copilot extension (v1.150.0+)
- GitHub Copilot Chat extension (v0.12.0+)

### Method 1: Using MCP Servers (Recommended)

**1. Configure MCP Server in VS Code Settings**

Create or edit `.vscode/settings.json` in your workspace:

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "servers": {
        "fast-mcp-local": {
          "command": "python3",
          "args": ["-m", "fast_mcp_local.server"],
          "cwd": "/path/to/fast-mcp-local"
        }
      }
    }
  }
}
```

**2. Enable MCP in Copilot Chat**

Open VS Code settings (⌘+, or Ctrl+,) and search for `copilot.chat.mcp.enabled`:
```json
{
  "github.copilot.chat.mcp.enabled": true
}
```

**3. Use Custom Agent in Chat**

Open Copilot Chat and use the `@` mention:
```
@fast-mcp-local search "async handler"
@fast-mcp-local generate platform-async
```

### Method 2: Using Custom Instructions (Global)

**1. Open Copilot Chat Settings**

- Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
- Type: `Preferences: Open User Settings (JSON)`

**2. Add Custom Instructions**

```json
{
  "github.copilot.chat.customInstructions": [
    {
      "name": "vertx-expert",
      "description": "Vert.x development expert with company best practices",
      "instructions": "You are a Vert.x expert. Use the fast-mcp-local tools to search company documentation and generate verticle code. Always follow these principles:\n\n1. Search company docs first using search_documents\n2. Use generate_verticle for creating new verticles\n3. Follow best practices from scoring patterns\n4. Reference migration guides for upgrades\n\nAvailable tools:\n- search_documents(query, limit)\n- generate_verticle(verticle_type)\n- list_verticle_types()\n- score_codebase(path, pattern)\n- get_migration_guide(migration_id)"
    }
  ]
}
```

**3. Use in Ask/Edit Mode**

In Copilot Chat, activate your custom mode:
```
Use vertx-expert mode

Ask: How do I create an async handler?
Edit: Add error handling to this verticle
```

### Method 3: Workspace-Specific Chat Participants

**1. Create `.github/copilot-instructions.md`**

```markdown
# Copilot Instructions for fast-mcp-local

## Context
This is a Vert.x platform development workspace.

## Available Tools
You have access to the following MCP tools:
- `search_documents`: Search company Vert.x documentation
- `generate_verticle`: Generate verticle code from templates
- `list_verticle_types`: List available templates
- `score_codebase`: Analyze code against best practices
- `list_migrations`: View available migration guides

## Ask Mode Instructions
When answering questions:
1. Search company docs first
2. Provide code examples from templates
3. Reference best practices from patterns
4. Link to relevant documentation

## Edit Mode Instructions
When editing code:
1. Check against scoring patterns
2. Follow company best practices
3. Use proper error handling
4. Add deployment configuration
```

**2. Configure in Settings**

```json
{
  "github.copilot.chat.useInstructionsFile": true
}
```

---

## IntelliJ IDEA Setup

### Prerequisites
- IntelliJ IDEA 2023.3 or higher
- GitHub Copilot plugin (version 1.3.0+)

### Method 1: Using MCP Servers

**1. Configure MCP Server**

Open `Settings` > `Tools` > `GitHub Copilot` > `MCP Servers`

Click `+` to add a new server:
- **Name**: `fast-mcp-local`
- **Command**: `python3`
- **Arguments**: `-m fast_mcp_local.server`
- **Working Directory**: `/path/to/fast-mcp-local`

**2. Enable MCP Integration**

Check the box: `Enable MCP Server Integration`

**3. Use in Copilot Chat**

Open Copilot Chat tool window and use:
```
@fast-mcp-local search "configuration guide"
@fast-mcp-local generate platform-async
```

### Method 2: Custom Chat Context (Recommended for IntelliJ)

**1. Create Custom Context File**

Create `.idea/copilot-context.json`:

```json
{
  "context": {
    "name": "Vert.x Development",
    "description": "Custom context for Vert.x platform development",
    "tools": [
      {
        "name": "search_documents",
        "description": "Search company Vert.x documentation",
        "example": "@search async handler"
      },
      {
        "name": "generate_verticle",
        "description": "Generate verticle code from template",
        "example": "@generate platform-async"
      }
    ],
    "instructions": {
      "ask": "When answering questions:\n1. Search company docs first\n2. Provide concrete code examples\n3. Reference best practices",
      "edit": "When editing code:\n1. Follow company patterns\n2. Add proper error handling\n3. Include deployment config"
    }
  }
}
```

**2. Add to Settings**

Open `Settings` > `Tools` > `GitHub Copilot` > `Chat`:
- Check: `Use workspace context files`
- Select: `.idea/copilot-context.json`

### Method 3: Chat Participants (IntelliJ 2024.1+)

**1. Open Settings**

Go to `Settings` > `Tools` > `GitHub Copilot` > `Chat Participants`

**2. Add Custom Participant**

Click `+` and configure:
- **ID**: `vertx-expert`
- **Name**: `Vert.x Expert`
- **Description**: `Expert in Vert.x development with company context`
- **System Prompt**:
  ```
  You are a Vert.x development expert with access to company documentation and templates.

  Available MCP Tools:
  - search_documents(query, limit): Search company Vert.x docs
  - generate_verticle(type): Generate code from templates
  - score_codebase(path, pattern): Analyze against best practices

  In ASK mode:
  - Search docs before answering
  - Provide code examples from templates
  - Reference company patterns

  In EDIT mode:
  - Follow company best practices
  - Add proper error handling
  - Include deployment configuration
  - Check against scoring patterns
  ```

**3. Use in Chat**

```
@vertx-expert how do I create an async handler?
@vertx-expert /edit add error handling to this verticle
```

---

## MCP Server Integration

### Connecting Fast MCP Local Server

**Option 1: Local Python Server**

```bash
# Start the server
cd /path/to/fast-mcp-local
source .venv/bin/activate
python3 -m fast_mcp_local.server
```

**Option 2: Using MCP CLI**

```bash
# Install MCP CLI
npm install -g @modelcontextprotocol/cli

# Start server via MCP
mcp start fast-mcp-local --command "python3 -m fast_mcp_local.server"
```

**Option 3: VS Code Launch Configuration**

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "MCP Server: fast-mcp-local",
      "type": "python",
      "request": "launch",
      "module": "fast_mcp_local.server",
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```

### Verifying MCP Connection

**VS Code:**
1. Open Command Palette (`Cmd+Shift+P`)
2. Run: `GitHub Copilot: Show MCP Servers`
3. Verify `fast-mcp-local` is listed and connected

**IntelliJ:**
1. Open Settings > Tools > GitHub Copilot > MCP Servers
2. Check status indicator next to `fast-mcp-local`

---

## Testing Your Custom Chat Mode

### Test Cases for Ask Mode

**1. Documentation Search**
```
Ask: Search for async handler best practices
Expected: Uses search_documents tool, returns relevant docs
```

**2. Code Generation**
```
Ask: How do I create a PostgreSQL verticle?
Expected: Uses generate_verticle("postgres"), returns code
```

**3. Migration Guidance**
```
Ask: How do I migrate from v1 to v2?
Expected: Uses get_migration_guide("v1-to-v2"), returns steps
```

### Test Cases for Edit Mode

**1. Add Error Handling**
```
File: MyVerticle.java
Edit: Add proper error handling to this verticle
Expected: Uses score_codebase to check patterns, adds try-catch blocks
```

**2. Add Deployment Config**
```
File: MyVerticle.java
Edit: Add deployment configuration
Expected: Generates DeploymentOptions code
```

**3. Refactor to Best Practices**
```
File: MyVerticle.java
Edit: Refactor to follow company best practices
Expected: Uses score_codebase, applies recommendations
```

### Verification Commands

**VS Code:**
```bash
# Check MCP server status
code --list-extensions | grep copilot

# View Copilot logs
Developer: Open Extension Logs > GitHub Copilot
```

**IntelliJ:**
```bash
# View plugin logs
Help > Show Log in Finder (Mac) or Help > Show Log in Explorer (Windows)
```

---

## Troubleshooting

### VS Code Issues

**Issue: MCP server not detected**
```json
// Add debug logging in settings.json
{
  "github.copilot.advanced": {
    "debug": {
      "logLevel": "debug",
      "logNetworkTraffic": true
    }
  }
}
```

**Issue: Custom instructions not working**
- Restart VS Code after adding custom instructions
- Check `Cmd+Shift+P` > `GitHub Copilot: Check Status`

### IntelliJ Issues

**Issue: MCP server connection failed**
- Verify Python path is correct
- Check working directory exists
- Test server manually: `python3 -m fast_mcp_local.server`

**Issue: Chat participant not showing**
- Update GitHub Copilot plugin to latest version
- Restart IntelliJ after adding participant

---

## Example Workflows

### Workflow 1: New Developer Onboarding (VS Code)

```
1. Open Copilot Chat
2. @fast-mcp-local search "platform overview"
3. @fast-mcp-local search "getting started"
4. @fast-mcp-local list_verticle_types
5. @fast-mcp-local generate platform-async
6. Copy generated code to new file
7. @fast-mcp-local score MyVerticle.java --pattern vertx-best-practices
```

### Workflow 2: Code Review (IntelliJ)

```
1. Open file in editor
2. Open Copilot Chat
3. @vertx-expert analyze this verticle
4. @vertx-expert /edit add missing error handling
5. @vertx-expert /edit add deployment configuration
6. @vertx-expert check against best practices
```

### Workflow 3: Migration (Both IDEs)

```
1. @fast-mcp-local list_migrations
2. @fast-mcp-local get_migration_guide v1-to-v2
3. @fast-mcp-local get_migration_step v1-to-v2 1
4. Follow steps manually or use /edit mode
5. @fast-mcp-local score ./verticles/ --pattern vertx-best-practices
```

---

## Advanced Configuration

### Custom Prompts for Specific Tasks

**VS Code `.github/copilot-prompts/vertx-review.md`:**
```markdown
# Vert.x Code Review Prompt

## Task
Review the current file for Vert.x best practices.

## Steps
1. Use score_codebase to analyze the file
2. Check for common anti-patterns:
   - Blocking operations in event loop
   - Missing error handlers
   - Hardcoded credentials
3. Provide specific recommendations
4. Reference company documentation
```

**IntelliJ `.idea/copilot-prompts/add-async.md`:**
```markdown
# Add Async Handler Template

## Task
Convert synchronous code to async using company AsyncHandler pattern.

## Steps
1. Search for "async handler" documentation
2. Generate platform-async template
3. Apply pattern to current code
4. Add proper Promise handling
5. Add error handlers
```

---

## Best Practices

### For Ask Mode
1. **Always search company docs first** before providing generic answers
2. **Use concrete examples** from templates and generated code
3. **Reference scoring patterns** when discussing best practices
4. **Link to migration guides** when discussing upgrades

### For Edit Mode
1. **Run scoring checks** before and after edits
2. **Follow company patterns** from templates
3. **Add comprehensive error handling** (try-catch, promise.fail())
4. **Include deployment configuration** when creating verticles
5. **Verify changes** against scoring patterns

### General Guidelines
1. Keep custom instructions concise (under 500 words)
2. Use MCP tools explicitly in prompts
3. Test custom modes with simple queries first
4. Document your custom modes in team wiki
5. Update instructions as company patterns evolve

---

## Resources

### Official Documentation
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [FastMCP Guide](https://github.com/jlowin/fastmcp)

### Fast MCP Local Docs
- [README_HACKATHON.md](./README_HACKATHON.md) - Quick start guide
- [FEATURES.md](./FEATURES.md) - Complete feature list
- [DEPENDENCIES.md](./DEPENDENCIES.md) - File dependencies
- [ARCHITECTURE.md](./design/ARCHITECTURE.md) - System architecture

---

**Last Updated**: 2025-10-15
**Status**: Production Ready ✅
**Tested On**: VS Code 1.85+, IntelliJ IDEA 2023.3+
