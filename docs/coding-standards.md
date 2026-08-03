# Coding Standards

---

# Philosophy

Readable code is preferred over clever code.

Architecture is preferred over shortcuts.

Business logic belongs to Services.

Routes coordinate requests.

Templates render data.

---

# File Header

Every important Python module should start with:

- Module
- Purpose
- Responsibilities
- Consumers

---

# Function Organization

Functions must be grouped using section separators.

Example

=====================================================
CREATE LEAGUE
=====================================================

=====================================================
JOIN LEAGUE
=====================================================

---

# Naming

Functions

snake_case

Variables

snake_case

Classes

PascalCase

Constants

UPPER_CASE

---

# Comments

Comments should explain "why", not "what".

---

# Routes

Routes should remain thin.

They should:

- receive request
- call service
- return response

---

# Services

Services contain business rules.

They should never depend on HTML.

---

# Templates

Templates should never contain business logic.

---

# Definition of Done

Every User Story must include:

- implementation
- integration
- testing
- Git commit