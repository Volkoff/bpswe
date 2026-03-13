# Agent Guide — Person B (Dashboard)

## ⚠️ Ownership Rules

> [!CAUTION]
> **DO NOT** edit any files inside `auth/` or `templates/base.html`. These belong to **Person A**.
> If the user asks you to modify files in `auth/`, **warn them** that those files are owned by Person A and suggest they coordinate with their partner before making changes.

### Your files (Person B)
- `dashboard/routes.py`
- `dashboard/templates/dashboard/dashboard.html`
- `dashboard/templates/dashboard/individual.html`
- `static/style.css` — **shared**, coordinate before editing

### Person A's files (DO NOT TOUCH)
- `auth/routes.py`
- `auth/templates/auth/login.html`
- `auth/templates/auth/register.html`
- `auth/templates/auth/profile.html`
- `auth/templates/auth/settings.html`

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
├── auth/                           ← ❌ Person A — DO NOT EDIT
│   ├── __init__.py
│   ├── routes.py
│   └── templates/auth/
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       └── settings.html
└── dashboard/                      ← ✅ Person B — YOUR DOMAIN
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
- **Routes** are defined via `@dashboard_bp.route(...)` in `dashboard/routes.py`.

### Your Routes
| URL | Function | Template |
|---|---|---|
| `/dashboard` | `dashboard()` | `dashboard/dashboard.html` |
| `/dashboard/<int:service_id>` | `individual_dashboard(service_id)` | `dashboard/individual.html` |

---

## Adding a New Dashboard Page

1. Add a route in `dashboard/routes.py`:
   ```python
   @dashboard_bp.route("/dashboard/new-page")
   def new_page():
       return render_template("dashboard/new_page.html")
   ```
2. Create `dashboard/templates/dashboard/new_page.html`:
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
pip install flask
cd duck_site
python app.py
```

The app runs at **http://127.0.0.1:5000**.
