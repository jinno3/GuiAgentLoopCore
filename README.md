# GuiAgentLoopCore

GuiAgentLoopCore provides the core logic for bridging GUI frameworks and LLM agents, managing conversation flow, agent interactions, and state control.


## Core Value

Reliable, type-safe, and extensible foundation for GUI-LLM integration with predictable state management and clear component boundaries.


## Target Users

This project is designed for:

- **Application Developers**: Building LLM-powered applications with GUI interfaces
- **AI Agent Developers**: Creating specialized agents for specific tasks
- **Framework Developers**: Building new GUI backend implementations
- **AI Agents**: Claude, Gemini, Codex, and other AI models working with this codebase

> **Note**: This repository uses normalized terminology for consistency. Key terms include `Interpreter` (core conversation management), `Agent` (specialized AI entities), `Session` (unique conversation contexts), `Message` (structured communication), and `State` (interpreter execution states). See [GLOSSARY.md](GLOSSARY.md) for complete terminology.

## Core Functions

### Centralized Conversation Management
Interpreter component centralizes conversation flow, state management, and agent coordination

### State Machine with Monotonic Transitions
Enforce monotonic state transitions (INIT → RUNNING → STOP) through hard invariants

### Multi-Agent Coordination
Role-based agent system (AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, etc.) with clear boundaries

### Structured Message Processing
Handle structured communication between users, systems, and agents

### Backend Abstraction
Enable multiple GUI framework implementations (Gradio, extensible to others)


## Installation

\`\`\`bash
pip install gui-agent-loop-core
\`\`\`

## Quick Start

\`\`\`python
from gui_agent_loop_core import InterpreterManager

# Initialize the interpreter
interpreter = InterpreterManager()

# Start a session
session_id = interpreter.create_session()

# Run the interpreter with state management
interpreter.change_state_running()
# ... your code here
\`\`\`

## Documentation

- [AGENTS.md](AGENTS.md) - AI Agent Guidelines
- [CLAUDE.md](CLAUDE.md) - Claude-specific Instructions
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture Overview
- [GLOSSARY.md](GLOSSARY.md) - Terminology

## License

See LICENSE file.
