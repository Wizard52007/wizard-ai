# Wizard Architecture

## Overview

Wizard will be designed as a modular personal AI agent.

The system will separate the AI reasoning layer from the tools and devices that Wizard can interact with.

The LLM should not directly control the user's operating system or personal devices.

Instead, Wizard will use controlled tools with explicit permissions.

## High-Level Architecture

User
  |
  v
Interface Layer
  |
  v
Agent / Orchestrator
  |
  +---- Brain
  |
  +---- Memory
  |
  +---- Tool Registry
  |
  +---- Security / Permissions
  |
  +---- Context Manager
  |
  v
Tools
  |
  +---- Computer
  +---- Web
  +---- Calendar
  +---- Email
  +---- Phone
  +---- Wearable
  |
  v
External Systems

## Core Components

### Brain

Responsible for:

- Understanding user requests
- Reasoning
- Planning
- Selecting tools
- Generating responses

### Agent / Orchestrator

Responsible for:

- Managing the interaction loop
- Providing context to the model
- Executing approved tools
- Returning tool results to the model
- Managing multi-step tasks

### Memory

Responsible for:

- Conversation history
- Persistent user preferences
- Relevant facts
- Task history
- Context retrieval

### Tools

Tools are controlled interfaces that allow Wizard to perform actions.

Examples:

- `search_web()`
- `read_file()`
- `open_application()`
- `read_calendar()`
- `draft_message()`
- `get_fitness_data()`

### Security

Security sits between Wizard's reasoning layer and actions.

Potential permission levels:

- Read-only
- Low-risk action
- Confirmation required
- Restricted

Wizard should never rely on unrestricted operating-system access when a controlled tool can perform the same operation.

### Interfaces

Wizard may eventually support:

- Command line
- Desktop application
- Voice
- Mobile application

The interface should remain separate from the core agent so that the same Wizard brain can operate through multiple interfaces.

## Device Architecture

External devices should generally communicate through dedicated adapters.

Example:

Wizard
  |
  v
Wearable Adapter
  |
  v
Wearable API / Health Platform
  |
  v
Fitness Band

This prevents the core Wizard system from becoming tightly coupled to a single device manufacturer.

## Design Principles

1. Modular
2. Secure by default
3. User-controlled
4. Testable
5. Observable
6. Replaceable components
7. Minimal required permissions
8. Device-agnostic where possible