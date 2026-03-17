---
name: "research_assistant"
description: "Search for info and automatically save key findings to OneContext long-term memory."
parameters:
  topic:
    type: "string"
    description: "The topic to research"
  depth:
    type: "string"
    description: "Level of detail: 'basic' or 'deep'"
    enum: ["basic", "deep"]
---

# Research Assistant Skill

This skill bridges AgentSkills and OneContext. It researches a topic and persists the knowledge for future use.
