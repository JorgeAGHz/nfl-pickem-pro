# Architecture

Version: 1.0

---

# Architecture Principles

The project follows a Domain First Architecture.

Business logic must never depend on the presentation layer.

Presentation layers consume Application Services.

---

# Layers

Presentation

- Flask Web
- REST API
- iOS
- Android

↓

Application Services

↓

Domain Services

↓

Persistence

↓

Database

---

# Project Structure

app/

models/

services/

providers/

routes/

templates/

---

# Principles

- Thin Controllers
- Services First
- Domain First
- Mobile Ready
- API Ready
- Separation of Concerns

---

# Frozen Architecture

The following modules should only change when there is functional value.

- models
- providers
- constants
- project structure