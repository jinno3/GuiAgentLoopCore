# Architecture

> **GuiAgentLoopCore Architecture Documentation**
> **Version**: 1.0

---

## System Overview

GuiAgentLoopCore is organized into distinct layers with clear responsibilities:

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│                  (User's Application)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Backend Layer                            │
│  (Gradio UI, Future: Streamlit, React, etc.)               │
│  - Event handling                                          │
│  - UI rendering                                            │
│  - I/O conversion                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Core Layer (★Main Focus★)                 │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Interpreter                                    │     │
│  │  - State management (INIT → RUNNING → STOP)     │     │
│  │  - Session management                          │     │
│  │  - Agent coordination                         │     │
│  │  - Message routing                            │     │
│  └──────────────────────────────────────────────────┘     │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐         │
│  │  Agent   │  │ Message  │  │      State       │         │
│  │ Manager  │  │ Handler  │  │    Machine       │         │
│  └──────────┘  └──────────┘  └──────────────────┘         │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Agent Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ AGENT_       │  │ LLM_         │  │ SUPERVISOR   │     │
│  │ EXECUTOR     │  │ PLANNER      │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  - Role-based execution                                     │
│  - Tool calling                                             │
│  - Structured chat                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                 Utility Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Stream      │  │  Converter   │  │   Memory     │     │
│  │  Wrapper     │  │              │  │   Buffer     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### Core Components

#### Interpreter (Central Orchestrator)
**Location**: `gui_agent_loop_core/core/interpreter_manager.py`

**Responsibilities**:
- State management (STATE_INIT, STATE_RUNNING, STATE_STOP)
- Session lifecycle management
- Agent coordination and task distribution
- Message routing between users, agents, and system
- AutoChat trigger management

**Key Methods**:
- `change_state_running()`: Transition to RUNNING state
- `create_session()`: Initialize new session with unique UUID
- `process_message()`: Route message to appropriate handler
- `auto_chat()`: Trigger continuation when in STATE_STOP

**Invariants**:
- INV-STATE-001: State transitions are monotonic
- INV-AUTO-001: AutoChat only triggers in STATE_STOP
- INV-SESSION-001: Sessions have unique UUIDs

#### Agent Manager
**Location**: `gui_agent_loop_core/schema/agent/`

**Responsibilities**:
- Agent role management (AgentName enum)
- Agent type handling (TOOL_CALLING, STRUCTURED_CHAT)
- Agent lifecycle (creation, execution, termination)

**Agent Roles**:
- `AGENT_EXECUTOR`: Executes tool calls
- `LLM_PLANNER`: Plans task decomposition
- `SUPERVISOR`: Coordinates multiple agents
- `THOUGHT`: Handles reasoning tasks
- `CREW`: Manages agent teams
- `OTHER`: Catch-all for undefined roles

**Invariants**:
- INV-AGENT-001: Agents have defined roles

#### Message Handler
**Location**: `gui_agent_loop_core/schema/message/`

**Responsibilities**:
- Message type validation
- Message structure enforcement
- Message transformation and flattening

**Message Types** (MessageTypeEnum):
- `MESSAGE`: Standard text message
- `CODE`: Code execution result
- `CONFIRMATION`: User confirmation request
- `CONSOLE`: Console output
- `IMAGE`: Image content
- `FUNCTION`: Function call/response

**Invariants**:
- INV-MSG-001: Only enumerated message types allowed

### Utility Components

#### StreamWrapper
**Location**: `gui_agent_loop_core/util/gui_agent_stream_wrapper.py`

**Responsibilities**:
- Unified sync/async streaming interface
- Response aggregation
- Stream lifecycle management

**Invariants**:
- INV-STREAM-001: Supports both sync and async

#### Converter
**Location**: `gui_agent_loop_core/converter/request_converter.py`

**Responsibilities**:
- Request format conversion
- Dictionary flattening (recursive)
- Code content extraction (format/language fields)

#### Memory Buffer
**Location**: `gui_agent_loop_core/memory/` (planned)

**Responsibilities**:
- Conversation history management
- Sliding window (k=10, AUTO decision)
- Message retrieval and filtering

**Invariants**:
- INV-MEM-001: Maximum 100 messages (soft limit)

---

## Data Flow

### Message Flow
```
User Input (Backend)
    │
    ├─► I/O Conversion
    │   └─► RequestConverter (flatten, extract code)
    │
    ├─► Interpreter (state: RUNNING)
    │   │
    │   ├─► Agent Selection (based on role)
    │   │
    │   ├─► Agent Execution
    │   │   └─► LLM API Call
    │   │
    │   └─► Response Collection
    │       └─► StreamWrapper (sync/async)
    │
    └─► Response Formatting
        └─► Backend → User
```

### State Transition Flow
```
INIT
  │ user sends message
  ├─► RUNNING
  │     │
  │     ├─► Agent executes
  │     ├─► Response sent
  │     │
  │     └─► STOP
  │           │
  │           ├─► AutoChat? (if enabled)
  │           │     └─► RUNNING (loop)
  │           │
  │           └─► Wait for user input
  │                 └─► RUNNING
```

---

## Component Boundaries

### Interpreter Boundaries
**Includes**:
- State management
- Session management
- Message routing

**Excludes**:
- UI rendering (Backend's responsibility)
- LLM execution (Agent's responsibility)

### Agent Boundaries
**Includes**:
- Role definition
- Task execution
- LLM interaction

**Excludes**:
- Session management (Interpreter's responsibility)
- UI rendering (Backend's responsibility)

### Backend Boundaries
**Includes**:
- UI component rendering
- Event handling
- I/O format conversion

**Excludes**:
- Conversation logic (Interpreter's responsibility)
- Agent management (Interpreter's responsibility)

---

## Extension Points

### Adding a New Backend
1. Implement the server interface
2. Handle UI-specific event conversion
3. Call Interpreter methods for logic
4. Format responses for UI

**Example**: See `gui_agent_loop_core/backend/server_impl_gradio.py`

### Adding a New Agent Role
1. Add to `AgentName` enum in `schema/core/schema.py`
2. Implement agent-specific logic
3. Update `.concept/ontology.yml` with new term if needed
4. Add tests for the new agent

### Adding a New Message Type
1. Add to `MessageTypeEnum` in `schema/message/schema.py`
2. Update message handlers
3. Add tests for the new type
4. Document in `.concept/invariants.yml`

---

## Technology Decisions

### Python
**Rationale**: 
- Excellent LLM library support
- Type hints for safety
- Async/await for streaming

### Enums for Types
**Rationale**:
- Compile-time type checking
- IDE autocomplete support
- Prevents invalid values

### UUID for Sessions
**Rationale**:
- Global uniqueness
- No centralized coordination needed
- Security (unpredictable)

### Monotonic State Machine
**Rationale**:
- Predictable behavior
- Easy to reason about
- Testable

---

**Related Documents**:
- [SYSTEM_CONSTITUTION.md](SYSTEM_CONSTITUTION.md) - Constitutional constraints
- [PURPOSE.md](PURPOSE.md) - Project purpose and objectives
- `.concept/mappings.yml` - Concept-to-code mappings
