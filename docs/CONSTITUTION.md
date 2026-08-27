# Phase I: Constitution

## Core Principles

### 1. Spec-Driven Development
- All code must derive from approved specifications
- No manual coding outside of Claude Code generation
- Specifications are the source of truth

### 2. Domain-Driven Design
- Business logic lives in domain models
- Infrastructure concerns are isolated
- Clear bounded contexts

### 3. Evolution Over Perfection
- Build for the next phase, not just the current one
- Interfaces over implementations
- Extensibility through abstraction

### 4. Type Safety & Validation
- All inputs validated at boundaries
- Type hints on all functions
- Explicit error handling

### 5. Testability First
- Pure functions where possible
- Dependency injection for repositories
- Clear success/failure paths

## Constraints

### Technology
- ✅ Python 3.11+
- ✅ Standard library only (no external dependencies for Phase I)
- ✅ In-memory storage (dict-based)
- ❌ No databases
- ❌ No web frameworks
- ❌ No AI/LLM integration (reserved for Phase III)

### Architecture
- ✅ Must use Repository Pattern
- ✅ Must separate domain from infrastructure
- ✅ Must use dataclasses or Pydantic-style models
- ❌ No tight coupling to console I/O
- ❌ No global state outside repository

### Data
- ✅ UUIDs for task identification
- ✅ ISO 8601 timestamps
- ✅ Enum-based priorities and statuses
- ❌ No data persistence between runs (Phase I only)

## Non-Goals (For Phase I)

- ❌ User authentication (Phase II+)
- ❌ Multi-user support (Phase II+)
- ❌ Data persistence (Phase II)
- ❌ Web interface (Phase II)
- ❌ Natural language processing (Phase III)
- ❌ Containerization (Phase IV)
- ❌ Event streaming (Phase V)

## Security & Quality Rules

### 1. Input Validation
- All user inputs must be sanitized
- Enum validation for priorities/statuses
- Length limits on text fields

### 2. Error Handling
- No silent failures
- User-friendly error messages
- Graceful degradation

### 3. Code Quality
- Type hints on all public functions
- Docstrings on all classes and public methods
- Maximum function length: 50 lines
- Maximum file length: 300 lines

### 4. Scalability Readiness
- Repository interface designed for async (Phase II)
- Domain models ready for ORM mapping (Phase II)
- Service layer ready for API exposure (Phase II)
