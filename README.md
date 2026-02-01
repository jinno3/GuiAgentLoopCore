# GuiAgentLoopCore

![Top Image](docs/images/top_image.png)

## Architecture Diagram

```mermaid
graph LR
    User((<i class="fas fa-user"></i>))---UI
    UI --- OpenGuiConnector
    OpenGuiConnector --- TaskAgent
    TaskAgent --- Agent1
    TaskAgent --- Agent2
    Agent1 --- LLM
    Agent2 --- LLM

    subgraph Interaction_Layer
    User((<i class="fas fa-user"></i>))
    UI(UI)
    end

    subgraph Processing_Layer
    OpenGuiConnector(OpenGuiConnector<br>- Event handling<br>- I/O conversion<br>- Multimodal support)
    end

    subgraph Task_Management_Layer
    TaskAgent(TaskAgent<br>- Task decomposition<br>- Subtask prioritization<br>- Agent assignment)
    end

    subgraph Execution_Layer
    Agent1(Agent1<br>Specialized role)
    Agent2(Agent2<br>Specialized role)
    end

    subgraph Language_Model_Layer
    LLM(LLM<br>Base language model)
    end

    style Interaction_Layer fill:#f9f,stroke:#333,stroke-width:2px,color:#333
    style Processing_Layer fill:#cff,stroke:#333,stroke-width:2px,color:#333
    style Task_Management_Layer fill:#ffc,stroke:#333,stroke-width:2px,color:#333
    style Execution_Layer fill:#cfc,stroke:#333,stroke-width:2px,color:#333
    style Language_Model_Layer fill:#ccf,stroke:#333,stroke-width:2px,color:#333


```

### Interaction_Layer - Processing_Layer

```mermaid
graph LR
    subgraph Interaction_Layer
        GuiAgentLoopCore(gui_agent_loop_core.py)
        GradioUI(Gradio UI)
        OpenAPISpec(OpenAPI Specification)
        InterpreterManager(InterpreterManager)
        AppLogic(Application Logic)

        GuiAgentLoopCore --> |Launch| GradioUI
        GradioUI --> |User Input| InterpreterManager
        InterpreterManager --> |Parse and Validate| OpenAPISpec
        OpenAPISpec --> |Formatted Data| AppLogic
        AppLogic --> |Result| OpenAPISpec
        OpenAPISpec --> |Formatted Data| InterpreterManager
        InterpreterManager --> |Format Response| GradioUI
    end

    style Interaction_Layer fill:#f9f,stroke:#333,stroke-width:2px,color:#333
```

[![pypi](https://img.shields.io/pypi/v/GuiAgentLoopCore.svg)](https://pypi.org/project/GuiAgentLoopCore/)
[![python](https://img.shields.io/pypi/pyversions/GuiAgentLoopCore.svg)](https://pypi.org/project/GuiAgentLoopCore/)
[![Build Status](https://github.com/nobu007/GuiAgentLoopCore/actions/workflows/dev.yml/badge.svg)](https://github.com/nobu007/GuiAgentLoopCore/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/nobu007/GuiAgentLoopCore/branch/main/graphs/badge.svg)](https://codecov.io/github/nobu007/GuiAgentLoopCore)

## What is GuiAgentLoopCore?

GuiAgentLoopCore provides the core logic for bridging GUI frameworks and LLM agents, managing conversation flow, agent interactions, and state control.

### Core Components

This project is built around the following key concepts (see [GLOSSARY.md](GLOSSARY.md) for detailed definitions):

- **Interpreter**: Manages conversation flow and agent interactions as the central component
- **Agent**: Specialized AI entities with specific roles and implementation types
- **Session**: Unique conversation contexts with message history
- **Message**: Structured communication between users, systems, and agents
- **State**: Represents interpreter execution state (STATE_INIT → STATE_RUNNING → STATE_STOP)

### Key Features

- **State Management**: Monotonic state transitions ensure consistent interpreter behavior
- **Multi-Agent Support**: Role-based agents with specialized capabilities
- **Streaming Support**: Unified handling of both sync and async streaming responses
- **Type Safety**: Enumerated types for messages, states, and agents prevent runtime errors
- **AutoChat**: Automatic conversation continuation when in STATE_STOP

## Getting Started


### Prerequisites


### Installation


## Usage


* Documentation: <https://nobu007.github.io/GuiAgentLoopCore>
* GitHub: <https://github.com/nobu007/GuiAgentLoopCore>
* PyPI: <https://pypi.org/project/GuiAgentLoopCore/>
* Free software: MIT


## Features

- **Interpreter**: Central component managing chat sessions and state handling
- **Agent System**: Role-based agents (AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, THOUGHT, CREW)
- **Message Types**: Structured communication (MESSAGE, CODE, CONFIRMATION, CONSOLE, IMAGE, FUNCTION)
- **State Machine**: Reliable state transitions (INIT → RUNNING → STOP)
- **AutoChat**: Automatic continuation prompts when execution stops
- **StreamWrapper**: Unified sync/async streaming response handling
- **Converter**: Request conversion with dictionary flattening and code content extraction
- **Backend Support**: Gradio-based GUI implementation (with extensible framework support)

> **Note**: This project uses a formal concept dictionary. All documentation uses canonical terminology. See [AGENTS.md](AGENTS.md) for AI agent guidelines and [GLOSSARY.md](GLOSSARY.md) for term definitions.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
