---
name: agent_chat
description: "Communicate with other AI agents in a shared group chat. Use this to sync tasks, report progress, and coordinate on large projects."
parameters:
  action:
    type: string
    description: "Action to perform: 'send' or 'read'."
  content:
    type: string
    description: "Message content (only for 'send')."
    default: ""
  agent_name:
    type: string
    description: "Your human-readable identity (e.g. 'Windsurf-FE', 'Kiro-API')."
    default: "AI-Agent"
---

# Agent Group Chat Tool

This tool acts as a communication hub for multiple AI agents working on the same project.

### When to use:
- **Progress Reports**: Tell others when you finish a sub-task.
- **Coordination**: Ask if anyone is working on a specific file.
- **Conflict Resolution**: Warn others about breaking changes you are about to make.
