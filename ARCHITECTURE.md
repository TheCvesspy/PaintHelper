# MiniPaint Tracker - Architecture Guide

**Version:** 1.0  
**Last Updated:** 2026-02-01  
**Framework:** Reflex (Python full-stack framework)

---

## Overview

MiniPaint Tracker is a Reflex-based web application for managing miniature painting projects, paint inventory, and painting guides. The architecture follows a modular, component-based design with clear separation of concerns.

## Technology Stack

- **Framework:** Reflex (reflex.dev)
- **Language:** Pure Python (no JavaScript/TypeScript)
- **Database:** Supabase (PostgreSQL)
- **Storage:** Google Drive API (for reference images)
- **State Management:** Reflex State classes
- **Deployment Target:** Google Cloud Run (Free Tier)

---

## Project Structure

```
minipaint/
├── minipaint.py              # Main app entry point
├── styles.py                 # Global theme and color definitions
├── models/                   # Data models (Pydantic & TypedDict)
│   ├── __init__.py
│   ├── batch.py             # Batch, PrintJob, PrintJobItem
│   ├── paint.py             # Paint-related TypeDicts
│   └── guide.py             # PaintingGuide, GuideDetail
├── state/                    # State management
│   ├── __init__.py
│   └── base.py              # BaseState (user authentication)
├── services/                 # External service integrations
│   ├── supabase.py          # Database client
│   └── drive_service.py     # Google Drive integration
├── components/               # Reusable UI components
│   ├── __init__.py
│   ├── common/              # Shared components
│   │   ├── __init__.py
│   │   └── sidebar.py       # Navigation sidebar
│   └── batch/               # Feature-specific components
│       ├── __init__.py
│       ├── create_batch_modal.py
│       └── add_job_modal.py
├── views/                    # Page view modules
│   ├── __init__.py
│   └── dashboard/           # Dashboard tab views
│       ├── __init__.py
│       ├── print_jobs_view.py
│       ├── paints_view.py
│       ├── guides_view.py
│       └── settings_view.py
└── pages/                    # Page components & state
    ├── __init__.py
    ├── index.py             # Landing/login page
    ├── register.py          # Registration page
    └── dashboard.py         # Main dashboard (state + helper functions)
```

---

## Architecture Principles

### 1. Modular Organization

**Purpose:** Each module has a single, clear responsibility

- **models/** - Data structures only, no business logic
- **components/** - Reusable UI elements, accept state_class parameter
- **views/** - Tab/page view functions, use local imports
- **pages/** - Page routes, state classes, and page-specific logic
- **services/** - External API/service integrations

### 2. Separation of Concerns

- **Data structures** (models) separated from **UI** (components/views)
- **Business logic** (state methods) kept in state classes
- **Service layer** abstracts external dependencies

### 3. Import Strategy

**Critical Pattern: Preventing Circular Imports**

```python
# ❌ BAD - Top-level imports cause circular dependency
from ...pages.dashboard import DashboardState

def my_view():
    return rx.vstack(...)

# ✅ GOOD - Local imports inside functions
def my_view():
    from ...pages.dashboard import DashboardState
    return rx.vstack(...)
```

**Reason:** `pages/dashboard.py` imports views, so views cannot import dashboard at module level.

---

## Component Patterns

### Standard Component Signature

Components accept a `state_class` parameter for flexibility:

```python
def my_component(state_class):
    """Reusable component description"""
    return rx.card(
        rx.text(state_class.some_property),
        on_click=state_class.some_handler
    )
```

**Usage:**
```python
from ..components import my_component

# In page code
my_component(DashboardState)
```

### Component Organization

- **common/** - Shared across features (sidebar, headers, etc.)
- **[feature]/** - Feature-specific (batch/, paint/, guide/)

### Component Naming

- Functions: `snake_case` (e.g., `create_batch_modal`)
- Files: `snake_case.py` (e.g., `create_batch_modal.py`)
- Always include docstring describing purpose

---

## View Patterns

### View Function Structure

Views represent entire tab/page sections and use local imports:

```python
def my_tab_view():
    """Tab view description"""
    # Import dependencies locally to prevent circular imports
    from ...pages.dashboard import DashboardState, helper_function
    from ...components import my_component
    
    return rx.vstack(
        # View implementation
        width="100%",
        spacing="4"
    )
```

### View Organization

- Group related views in subdirectories (`views/dashboard/`)
- One view = one tab or major page section
- Keep views focused on layout/composition, not business logic

---

## State Management

### State Class Pattern

```python
from ..state import BaseState

class DashboardState(BaseState):
    """Dashboard state management"""
    
    # State variables
    active_tab: str = "print_jobs"
    batches: list[Batch] = []
    
    # Computed properties
    @rx.var
    def filtered_batches(self) -> list[Batch]:
        return [b for b in self.batches if not b.is_archived]
    
    # Event handlers
    def set_active_tab(self, tab: str):
        self.active_tab = tab
    
    async def fetch_batches(self):
        # Async operations for data fetching
        pass
```

### State Organization (Current Approach)

- **Monolithic state class** in `pages/dashboard.py`
- **Future improvement:** Can split into substates as complexity grows

---

## Model Patterns

### Pydantic Models

Use for structured data with validation:

```python
from pydantic import BaseModel

class Batch(BaseModel):
    id: str
    name: str
    tag: str | None
    is_archived: bool
```

### TypedDicts

Use for simple data structures from API responses:

```python
from typing import TypedDict, Optional

class PaintDict(TypedDict):
    id: str
    name: str
    color_hex: str
```

### Model Organization

- Group by domain: `batch.py`, `paint.py`, `guide.py`
- Export all from `models/__init__.py`

---

## Service Integration Patterns

### Supabase Client

**Location:** `services/supabase.py`

```python
from supabase import create_client

supabase = create_client(url, key)

# Usage in state methods
async def fetch_data(self):
    response = supabase.table("batches").select("*").execute()
```

### Google Drive Integration

**Location:** `services/drive_service.py`

- OAuth flow for user authentication
- File upload/download helpers
- Used in painting guides for reference images

---

## Naming Conventions

### Files & Directories

- `snake_case` for all Python files
- `__init__.py` in every package directory
- Descriptive names: `create_batch_modal.py` not `modal.py`

### Functions

- Views: `[feature]_tab()` or `render_[feature]_view()`
- Components: `[component_name]()` (e.g., `sidebar()`)
- Helpers: `render_[item]()` (e.g., `render_batch()`)

### State Variables

- `snake_case` for all state variables
- Boolean: `is_[state]` or `has_[state]`
- Collections: plural nouns (`batches`, `paints`)

### Components/Elements

- Follow Reflex conventions: `rx.vstack()`, `rx.card()`, etc.

---

## Best Practices

### 1. Import Management

```python
# Standard library
import os
from typing import Any, Optional

# Third-party (Reflex)
import reflex as rx
from pydantic import BaseModel

# Local imports - grouped by type
from ..state import BaseState
from ..models import Batch, Paint
from ..components import sidebar
from ..services.supabase import supabase
```

### 2. Component Composition

- Keep components small and focused
- Use `rx.foreach()` for dynamic lists
- Use `rx.cond()` for conditional rendering
- Pass state_class, not individual properties

### 3. State Methods

- Keep methods focused on single responsibility
- Use `async def` for database operations
- Use `@rx.var` for computed properties (cached)
- Name handlers clearly: `handle_[action]`, `on_[event]`

### 4. Error Handling

```python
async def fetch_data(self):
    try:
        response = supabase.table("batches").select("*").execute()
        self.batches = [Batch(**item) for item in response.data]
    except Exception as e:
        print(f"Error fetching batches: {e}")
        self.batches = []
```

### 5. Styling

- Use theme colors from `styles.py`
- Consistent spacing: spacing="4" for major sections
- Consistent sizing: size="5" for headings
- Use color mode conditionals: `rx.color_mode_cond(light=..., dark=...)`

---

## Common Patterns

### Modal Dialog Pattern

```python
def my_modal(state_class):
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Modal Title"),
            rx.vstack(
                # Modal content
                spacing="4"
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancel", variant="soft")
                ),
                rx.button("Confirm", on_click=state_class.handle_confirm),
                justify="end",
                margin_top="16px"
            )
        ),
        open=state_class.modal_open,
        on_open_change=state_class.set_modal_open
    )
```

### List Rendering Pattern

```python
def render_item(item: ItemType):
    return rx.card(
        rx.text(item.name),
        # ... item content
    )

def item_list_view():
    from ...pages.dashboard import DashboardState
    return rx.vstack(
        rx.foreach(DashboardState.items, render_item),
        width="100%"
    )
```

### Tab View Pattern

```python
def dashboard_page():
    return rx.match(
        DashboardState.active_tab,
        ("tab1", tab1_view()),
        ("tab2", tab2_view()),
        tab1_view()  # Default
    )
```

---

## Extending the Application

### Adding a New Feature

1. **Create models** (if needed) in `models/[feature].py`
2. **Add state variables/methods** to relevant state class
3. **Create components** in `components/[feature]/`
4. **Create view** in `views/dashboard/[feature]_view.py`
5. **Update imports** in relevant `__init__.py` files
6. **Add to navigation** in `components/common/sidebar.py`
7. **Test** - run app and verify all paths work

### Adding a New Component

1. Create file in appropriate `components/` subdirectory
2. Write component function with `state_class` parameter
3. Add docstring describing purpose
4. Export from `components/[subdirectory]/__init__.py`
5. Export from `components/__init__.py`
6. Use in views/pages

### Adding a New View

1. Create file in `views/dashboard/[feature]_view.py`
2. Use local imports pattern (see View Patterns)
3. Export from `views/dashboard/__init__.py`
4. Export from `views/__init__.py`
5. Import and use in `pages/dashboard.py`

---

## Database Schema Notes

### Supabase Tables

- `batches` - Print batches
- `print_jobs` - Jobs within batches
- `print_job_items` - Individual items in jobs
- `batch_reprints` - Reprint tracking
- `painting_guides` - Custom painting guides
- `guide_details` - Guide sections/steps
- `guide_paints` - Paints used in guides
- `paints` - Catalog of all paints
- `owned_paints` - User's paint inventory
- `custom_paints` - User-created custom paints
- `wishlist_paints` - Shopping wishlist

### Key Relationships

- Batch → PrintJob (one-to-many)
- PrintJob → PrintJobItem (one-to-many)
- PaintingGuide → GuideDetail (one-to-many)
- GuideDetail → GuidePaint (one-to-many)

---

## Testing Approach

### Manual Verification

```bash
# Start app
.\run.bat

# Test each tab/feature
# Check console for errors

# Shutdown
.\shutdown.bat
```

### When to Test

- After adding new components
- After modifying state methods
- After changing database queries
- Before committing changes

---

## Deployment Notes

- **Target:** Google Cloud Run (Free Tier)
- **Constraints:** Must stay within free tier limits
- **Access Control:** Custom token system (bypasses Cloud Identity)
- **Environment:** Requires `.env` file with Supabase and Google Drive credentials

---

## Common Issues & Solutions

### Circular Import Errors

**Symptom:** `ImportError: cannot import name 'X' from partially initialized module`  
**Solution:** Use local imports inside view/component functions

### State Not Updating

**Symptom:** UI doesn't reflect state changes  
**Solution:** Ensure state methods are called correctly, use `self.` prefix

### Build Errors

**Symptom:** Reflex compilation fails  
**Solution:** Check for syntax errors, missing imports, ensure all `__init__.py` files exist

---

## Future Improvements

### Potential Refactorings

1. **State Splitting** - Break DashboardState into feature-specific substates
2. **Helper Modules** - Extract state methods into `helpers/` modules
3. **Component Library** - Extract more reusable components
4. **API Layer** - Abstract Supabase calls into dedicated API layer

### Code Quality

- Add type hints to all functions
- Implement automated testing
- Add logging/monitoring
- Improve error handling with user-friendly messages

---

## Agent Guidelines

When working on this codebase:

1. **Always follow the import patterns** - Use local imports in views
2. **Maintain the directory structure** - Put files in the right places
3. **Use consistent naming** - Follow established conventions
4. **Test after changes** - Run the app to verify functionality
5. **Document decisions** - Update this file if architecture changes
6. **Keep components reusable** - Accept state_class parameter
7. **Write clear docstrings** - Help future agents understand your code

---

**For questions or clarifications about this architecture, refer to:**
- Reflex documentation: https://reflex.dev/docs
- Project walkthrough: `.gemini/antigravity/brain/[conversation-id]/walkthrough.md`
- This document: `ARCHITECTURE.md`
