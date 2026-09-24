# Wizard Architecture

## Overview

Wizard is designed as a modular personal AI agent.

The architecture separates reasoning, memory, tools, interfaces, device integrations, and security so that each component can evolve independently.

The primary design goals are:

- Modularity
- Extensibility
- Security
- Testability
- Provider independence
- Clear separation of responsibilities

Wizard should be able to gain new capabilities without requiring major changes to the existing core.

---

## High-Level Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         │ Text / Voice / Other │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     INTERFACES       │
                         │ CLI / Voice / Web    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │       ORCHESTRATOR           │
                    │                              │
                    │ Understand → Plan → Execute  │
                    └───────┬─────────┬────────────┘
                            │         │
                            ▼         ▼
                     ┌──────────┐ ┌──────────────┐
                     │  BRAIN   │ │   CONTEXT    │
                     │          │ │   MANAGER    │
                     │ Reasoning│ │              │
                     │ Planning │ │ User context │
                     └────┬─────┘ │ Conversation  │
                          │       └──────┬───────┘
                          └───────┬──────┘
                                  ▼
                         ┌──────────────────┐
                         │  TOOL REGISTRY   │
                         │                  │
                         │ Tool discovery   │
                         │ Validation       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    SECURITY      │
                         │   & PERMISSIONS  │
                         └────────┬─────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 ▼                ▼                ▼
          ┌────────────┐   ┌────────────┐   ┌────────────┐
          │  Computer  │   │   Phone    │   │    Web     │
          │   Tools    │   │   Tools    │   │   Tools    │
          └────────────┘   └────────────┘   └────────────┘

                         ┌──────────────────┐
                         │      MEMORY      │
                         │                  │
                         │ Short-term       │
                         │ Long-term        │
                         │ User preferences │
                         └────────┬─────────┘
                                  │
                                  ▼
                           Context Manager
```

---

## Core Components

### 1. Orchestrator

The orchestrator is the central coordinator of Wizard.

Its responsibilities include:

- Receiving requests from interfaces
- Maintaining the execution flow
- Providing relevant context to the brain
- Coordinating planning and tool execution
- Handling tool results
- Producing the final response

The orchestrator should coordinate components rather than contain their internal implementation.

---

### 2. Brain

The brain is responsible for reasoning and planning.

Responsibilities include:

- Understanding user requests
- Interpreting context
- Generating plans
- Selecting appropriate tools
- Processing tool results
- Producing responses

The brain should not directly control operating-system resources or external devices.

Instead, it requests controlled tools through the tool system.

This separation allows the underlying AI model to be replaced without redesigning the rest of Wizard.

---

### 3. Context Manager

The context manager provides relevant information to the orchestrator and brain.

Potential context includes:

- Current conversation
- Recent actions
- Current task
- User preferences
- Relevant memory
- Tool results

Context should be managed separately from the underlying model so that different AI providers can use the same Wizard context system.

---

### 4. Memory

Memory stores information that may remain useful beyond the current interaction.

Wizard will eventually support different types of memory.

#### Short-Term Memory

Contains information relevant to the current conversation or task.

Examples:

- Recent messages
- Current task state
- Recent tool results

#### Long-Term Memory

Contains information that remains useful across sessions.

Examples:

- User preferences
- Important facts explicitly saved by the user
- Long-running project information

Memory should be accessed through a controlled interface rather than directly by individual components.

---

### 5. Tool Registry

The tool registry manages the capabilities available to Wizard.

Responsibilities include:

- Registering tools
- Discovering available tools
- Describing tool capabilities
- Validating tool inputs
- Routing tool requests
- Providing a consistent interface for tool execution

Example tools may eventually include:

```text
search_web()
read_file()
create_file()
open_application()
get_calendar_events()
send_message()
get_weather()
get_wearable_data()
```

The exact tool implementations are outside the responsibility of the brain.

---

### 6. Security and Permissions

Security is a core architectural component.

Wizard should never receive unrestricted access to the user's systems when a controlled tool interface can be used instead.

The security layer is responsible for:

- Validating requested actions
- Checking permissions
- Restricting sensitive operations
- Preventing unauthorized tool execution
- Providing an auditable boundary between Wizard and external systems

Different tools may require different permission levels.

For example:

```text
Read information
       ↓
Modify information
       ↓
Perform external action
       ↓
Perform sensitive or destructive action
```

The exact permission model will be implemented in a future phase.

---

### 7. Interfaces

Interfaces provide different ways for users to communicate with Wizard.

Potential interfaces include:

- Command-line interface
- Voice interface
- Web interface
- Desktop interface
- Mobile interface

Interfaces should remain separate from the core reasoning system.

For example:

```text
CLI ─────┐
Voice ───┼──→ Wizard Orchestrator
Web ─────┤
Mobile ──┘
```

This allows new interfaces to be added without rewriting the core agent.

---

### 8. Device Adapters

Device adapters provide a boundary between Wizard tools and external devices or platforms.

Potential integrations include:

- Computer
- Smartphone
- Wearables
- Smart-home devices
- External APIs

A device adapter should hide platform-specific implementation details from the rest of Wizard.

For example:

```text
Wizard Tool
     │
     ▼
Device Adapter
     │
     ▼
Platform-specific API
```

This makes it possible to support different platforms without changing the higher-level architecture.

---

## Request Execution Flow

A typical Wizard interaction should follow this general flow:

```text
User request
     │
     ▼
Interface
     │
     ▼
Orchestrator
     │
     ├──────► Context Manager
     │
     ▼
    Brain
     │
     ▼
   Plan
     │
     ▼
Tool Registry
     │
     ▼
Security / Permission Check
     │
     ▼
Tool Execution
     │
     ▼
Tool Result
     │
     ▼
Brain / Orchestrator
     │
     ▼
Interface
     │
     ▼
User
```

Not every request will require a tool.

For example, a simple conversational request may follow:

```text
User → Interface → Orchestrator → Brain → Interface → User
```

A request requiring an external action will pass through the tool and security layers.

---

## Separation of Responsibilities

Wizard follows a separation-of-concerns model.

| Component | Primary Responsibility |
|---|---|
| Interface | User interaction |
| Orchestrator | Coordinate execution |
| Brain | Reasoning and planning |
| Context Manager | Current task context |
| Memory | Persistent information |
| Tool Registry | Tool discovery and execution routing |
| Security | Permissions and safety boundaries |
| Tools | Perform specific actions |
| Device Adapters | Platform-specific integrations |

Components should avoid taking responsibility for unrelated layers.

For example, the brain should not contain code for controlling a smartphone.

---

## Provider Independence

Wizard should not be tightly coupled to a single AI model provider.

The architecture should allow the underlying model to be replaced through an abstraction layer.

Conceptually:

```text
                  Wizard Brain
                      │
                LLM Interface
                 /    |    \
                /     |     \
           Provider  Local  Other
            Model    Model  Provider
```

This allows Wizard to evolve independently from the underlying AI provider.

---

## Extensibility

New capabilities should generally be added as tools or adapters rather than by modifying the core orchestrator.

For example, adding calendar functionality should look conceptually like:

```text
Calendar API
     │
     ▼
Calendar Adapter
     │
     ▼
Calendar Tool
     │
     ▼
Tool Registry
     │
     ▼
Wizard
```

The same principle can be applied to:

- Email
- Calendar
- Web search
- Computer control
- Phone integration
- Wearable data
- Smart-home devices

---

## Security Boundary

The most important architectural boundary is between **reasoning** and **execution**.

```text
┌─────────────────────────────┐
│       AI / Reasoning        │
│                             │
│ Understand + Plan           │
└──────────────┬──────────────┘
               │
               │ Tool request
               ▼
┌─────────────────────────────┐
│      Security Boundary      │
│                             │
│ Validate + Authorize        │
└──────────────┬──────────────┘
               │
               │ Authorized action
               ▼
┌─────────────────────────────┐
│        External System      │
│                             │
│ OS / Phone / Web / Device   │
└─────────────────────────────┘
```

This boundary is intended to reduce the risk of unintended or unauthorized actions.

---

## Testing Strategy

Each architectural layer should be testable independently.

Examples:

- Configuration → configuration tests
- Logging → logger tests
- Brain → reasoning/planning tests
- Tools → tool-specific tests
- Security → permission tests
- Memory → storage/retrieval tests
- Orchestrator → integration tests

The project should prefer unit tests for isolated components and integration tests for interactions between components.

---

## Future Project Structure

The architecture is expected to evolve toward the following structure:

```text
src/
└── wizard/
    ├── main.py
    ├── config.py
    ├── logger.py
    │
    ├── core/
    │   ├── orchestrator.py
    │   ├── context.py
    │   └── types.py
    │
    ├── brain/
    │   ├── llm.py
    │   ├── planner.py
    │   └── prompts.py
    │
    ├── memory/
    │   ├── manager.py
    │   ├── short_term.py
    │   └── long_term.py
    │
    ├── tools/
    │   ├── registry.py
    │   ├── base.py
    │   └── ...
    │
    ├── security/
    │   ├── permissions.py
    │   └── policy.py
    │
    ├── interfaces/
    │   ├── cli.py
    │   └── ...
    │
    └── devices/
        ├── computer/
        ├── phone/
        └── wearable/
```

This structure represents the **planned architecture**, not the current implementation.

Components will be introduced incrementally as their corresponding roadmap phases are implemented.

---

## Architectural Principles

Wizard will follow these principles:

1. **Separation of concerns**  
   Each component should have a clearly defined responsibility.

2. **Least privilege**  
   Wizard should receive only the permissions required for an action.

3. **Tool-based execution**  
   External actions should be performed through controlled tools.

4. **Provider independence**  
   The core system should not depend on one AI model provider.

5. **Modularity**  
   Components should be replaceable without requiring large-scale rewrites.

6. **Testability**  
   Components should be independently testable wherever practical.

7. **User control**  
   The user should remain in control of sensitive actions and permissions.

8. **Incremental development**  
   Future capabilities should be introduced and validated one subsystem at a time.
  