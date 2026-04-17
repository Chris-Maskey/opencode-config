# OpenCode Configuration

Personal OpenCode setup with custom agents, skills, and AI provider configuration.

## Overview

This is the configuration directory for OpenCode, an AI-powered coding assistant. It includes:

- **MCP Servers**: Context7, Stitch, shadcn, Exa
- **Plugins**: notifier, md-table-formatter, superpowers
- **Custom Agents**: 10 specialized agents for various tasks
- **Skills**: 60+ skills covering React, TypeScript, product management, psychology, and more

## Directory Structure

```
.
├── agents/              # Custom agent definitions
│   ├── code-reviewer.md
│   ├── code-simplifier.md
│   ├── deep-thinker.md
│   ├── effort-estimator.md
│   ├── prompt-simplifier.md
│   ├── refactoring.md
│   ├── requirements-analyzer.md
│   ├── skill-creator.md
│   ├── talk.md
│   └── web-researcher.md
├── skills/              # Specialized skills
│   ├── agent-browser/
│   ├── brainstorming/
│   ├── frontend-design/
│   ├── react-use-state/
│   ├── typescript-*
│   ├── vercel-*
│   └── ... (60+ more)
├── opencode.json        # Main configuration
└── package.json         # Dependencies
```

## Configuration

See `opencode.json` for:

- MCP server endpoints
- AI model configurations
- Plugin settings

## Usage

Start OpenCode with this configuration to access all custom agents and skills.

