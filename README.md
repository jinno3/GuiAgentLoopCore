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

### Streaming Support
Unified handling of both sync and async streaming responses through StreamWrapper


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

## System Invariants

This project enforces hard invariants to guarantee system correctness:

- **INV-STATE-001**: Interpreter state transitions are monotonic (STATE_INIT → STATE_RUNNING → STATE_STOP)
- **INV-SESSION-001**: Sessions are uniquely identified by UUID
- **INV-MSG-001**: Message types are restricted to defined enum values
- **INV-MESSAGE-001**: Message history is limited to MAX_MESSAGE_LENGTH=100
- **INV-AUTO-001**: AutoChat only triggers when state is STATE_STOP

See [AGENTS.md](AGENTS.md) or [SYSTEM_CONSTITUTION.md](SYSTEM_CONSTITUTION.md) for complete invariant documentation.

## AUTO Decisions

This project uses AUTO decisions (provisional specifications) to resolve ambiguities. Key AUTO decisions include:

- **AUTO:Agent.role:classification** - Agents are classified by role
- **AUTO:Agent.type:implementation_property** - AgentType is an implementation property (independent of AgentName role)
- **AUTO:State.lifecycle:monotonic** - State transitions are monotonic (INIT → RUNNING → STOP)
- **AUTO:State.transition:auto_on_input** - User input (textbox.submit) automatically transitions to RUNNING
- **AUTO:Message.limit:100** - MAX_MESSAGE_LENGTH=100 is a hard limit
- **AUTO:AutoChat.trigger:stop_only** - AutoChat only fires at STATE_STOP
- **AUTO:Backend.primary:gradio** - Gradio is the primary backend (provisional)
- **AUTO:Memory.window:k10** - Memory window size is k=10 (provisional)
- **AUTO:Session.jwt:algorithm_hs256** - JWT uses HS256 algorithm (provisional)

> **Note**: AUTO decisions are provisional specifications. See `.concept/ambiguities.yml` for details and evidence.

## Documentation

- [AGENTS.md](AGENTS.md) - AI Agent Guidelines
- [CLAUDE.md](CLAUDE.md) - Claude-specific Instructions
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture Overview
- [GLOSSARY.md](GLOSSARY.md) - Terminology

## License

See LICENSE file.
