# Architecture Decisions

This document records important technical decisions made during Wizard's development and the reasoning behind them.

---

## ADR-001 — Use Python for the initial implementation

**Status:** Accepted

### Decision

Wizard's initial implementation will use Python.

### Reasoning

Python provides a strong ecosystem for:

- AI/LLM integration
- API development
- automation
- speech processing
- data processing
- rapid prototyping

The architecture will remain modular so that other languages can be introduced later if a specific component requires them.

---

## ADR-002 — Use a tool-based architecture

**Status:** Accepted

### Decision

The AI model will interact with the outside world through controlled tools rather than unrestricted system access.

### Reasoning

This provides:

- Better security
- Explicit permissions
- Easier testing
- Easier debugging
- Replaceable integrations
- Better control over destructive actions

---

## ADR-003 — Separate the AI brain from interfaces

**Status:** Accepted

### Decision

The core Wizard agent will be independent from its user interfaces.

### Reasoning

Wizard may eventually support CLI, desktop, voice, and mobile interfaces.

Keeping these separate allows the same core agent to be reused across different interfaces.

---

## ADR-004 — Keep external device integrations modular

**Status:** Accepted

### Decision

Phone, computer, and wearable integrations will use separate adapters/modules.

### Reasoning

Device APIs and manufacturers may change.

A modular adapter architecture allows individual integrations to be replaced without redesigning Wizard's core.

---

## ADR-005 — Security is a core component

**Status:** Accepted

### Decision

Security and permission management will be designed as part of the architecture rather than added later.

### Reasoning

Wizard may eventually have access to highly sensitive personal information and powerful device capabilities.

Actions should therefore be controlled, auditable, and user-authorized where appropriate.