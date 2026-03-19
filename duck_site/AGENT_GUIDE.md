# Agent Guide — Person B (Auth)

## ⚠️ Ownership Rules

> [!CAUTION]
> **DO NOT** edit any files inside `dashboard/` or `templates/base.html`. These belong to **Person A**.
> If the user asks you to modify files in `dashboard/`, **warn them** that those files are owned by Person A and suggest they coordinate with their partner before making changes.

### Your files (Person B)
- `auth/routes.py`
- `auth/templates/auth/login.html`
- `auth/templates/auth/register.html`
- `auth/templates/auth/profile.html`
- `auth/templates/auth/settings.html`

### Person A's files (DO NOT TOUCH)
- `dashboard/routes.py`
- `dashboard/templates/dashboard/dashboard.html`
- `dashboard/templates/dashboard/individual.html`

### Shared files (coordinate before editing)
- `app.py`
- `templates/base.html`
- `static/style.css`

---

## Project Structure

This is a Flask app using **Blueprints** to separate concerns:

```
duck_site/
├── app.py                          ← Main app (shared)
├── static/style.css                ← Shared CSS
├── templates/base.html             ← Shared base template
├── auth/                           ← ✅ Person B — YOUR DOMAIN
│   ├── __init__.py
│   ├── routes.py
│   └── templates/auth/
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       └── settings.html
└── dashboard/                      ← ❌ Person A — DO NOT EDIT
    ├── __init__.py
    ├── routes.py
    └── templates/dashboard/
        ├── dashboard.html
        └── individual.html
```

---

## How It Works

- **`app.py`** creates the Flask app and registers both blueprints (`auth_bp` and `dashboard_bp`).
- **Templates** extend `templates/base.html` using Jinja2 (`{% extends "base.html" %}`).
- **Routes** are defined via `@auth_bp.route(...)` in `auth/routes.py`.

### Your Routes
| URL | Function | Template |
|---|---|---|
| `/login` | `login()` | `auth/login.html` |
| `/register` | `register()` | `auth/register.html` |
| `/profile` | `profile()` | `auth/profile.html` |
| `/settings` | `settings()` | `auth/settings.html` |

---

## Adding a New Auth Page

1. Add a route in `auth/routes.py`:
   ```python
   @auth_bp.route("/new-page")
   def new_page():
       return render_template("auth/new_page.html")
   ```
2. Create `auth/templates/auth/new_page.html`:
   ```html
   {% extends "base.html" %}
   {% block title %}New Page{% endblock %}
   {% block content %}
   <h1>New Page</h1>
   {% endblock %}
   ```

---

## Running the App

```bash
docker compose up -d

```

The app runs at **http://127.0.0.1:5000**.
