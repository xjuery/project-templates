# Object Manager — Angular Frontend

A data-management SPA that **dynamically generates create forms and list views** from JSON configuration files. Adding a new object type requires no code changes — just a JSON file.

Built with **Angular 21** (standalone components) and **PrimeNG 21** (Aura theme).

---

## Table of contents

1. [Getting started](#getting-started)
2. [Architecture overview](#architecture-overview)
3. [Project structure](#project-structure)
4. [How the dynamic form works](#how-the-dynamic-form-works)
5. [Object-type configuration files](#object-type-configuration-files)
6. [Adding a new object type](#adding-a-new-object-type)
7. [Mock backend (json-server)](#mock-backend-json-server)
8. [Development commands](#development-commands)

---

## Getting started

> The Makefile at the repository root is the recommended way to run the project.
> See the root `README` or run `make help` from there.

To run the frontend on its own:

```bash
# Install dependencies
npm install

# Start the dev server (http://localhost:4200)
npm start
```

The app proxies every `/api/*` request to `http://localhost:3001` (the json-server mock).
You must also start the mock server for data operations to work:

```bash
cd ../mockserver && npm start
```

---

## Architecture overview

```
Browser
  └── Angular SPA (port 4200)
        ├── reads object-type configs from  /assets/object-types/*.json
        └── proxies /api/* to  http://localhost:3001  (json-server mock)
```

The application is **schema-driven**: the shape of every form and list is determined at runtime by a JSON configuration file loaded from the `public/assets/object-types/` directory.  No TypeScript changes are required to support a new entity type.

Key design choices:

| Choice | Rationale |
|---|---|
| **Angular 21 standalone components** | No NgModules — each component declares its own imports |
| **Angular Signals** | Reactive state without RxJS boilerplate (`signal`, `computed`) |
| **Reactive Forms** | Validators are built programmatically from the JSON config |
| **PrimeNG 21 (Aura theme)** | Rich component library; configured once in `app.config.ts` |
| **`providePrimeNG` in `app.config.ts`** | Single provider, no per-module setup |
| **HTTP proxy (`proxy.conf.json`)** | Keeps the frontend free of hard-coded backend URLs |

---

## Project structure

```
src/
├── main.ts                         Entry point
├── styles.scss                     Global styles + PrimeIcons import
│
├── app/
│   ├── app.ts                      Root component (sidebar navigation)
│   ├── app.html / app.scss         Layout shell
│   ├── app.config.ts               Application providers (router, HTTP, PrimeNG)
│   ├── app.routes.ts               Route definitions
│   │
│   ├── core/
│   │   ├── models/
│   │   │   └── field-config.model.ts   TypeScript interfaces for JSON config
│   │   └── services/
│   │       ├── object-config.service.ts  Loads & caches *.json from assets
│   │       └── object-data.service.ts    GET / POST / DELETE against the API
│   │
│   ├── shared/
│   │   └── components/
│   │       └── dynamic-form/
│   │           ├── dynamic-form.ts       Builds FormGroup from config at runtime
│   │           ├── dynamic-form.html     Renders the right PrimeNG input per type
│   │           └── dynamic-form.scss
│   │
│   └── pages/
│       ├── create-object/
│       │   ├── create-object.ts          Loads config, submits form data to API
│       │   ├── create-object.html
│       │   └── create-object.scss
│       └── list-objects/
│           ├── list-objects.ts           Loads config + data, builds dynamic table
│           ├── list-objects.html
│           └── list-objects.scss
│
└── (no src/assets — see below)

public/
└── assets/
    └── object-types/               ← JSON config files live here
        ├── person.json
        └── product.json
```

> **Why `public/` and not `src/assets/`?**
> Angular 21's `@angular/build:application` builder serves static files from the `public/` directory (mapped to the root URL `/`).
> Files placed in `public/assets/object-types/` are available at `/assets/object-types/`.

---

## How the dynamic form works

### 1. Config loading — `ObjectConfigService`

When a route like `/objects/person/create` is activated, `CreateObject` calls:

```ts
this.configService.getConfig('person')
// → GET /assets/object-types/person.json
```

The service caches results in a `Map` so each config is fetched only once per session.

### 2. Form construction — `DynamicForm`

`DynamicForm` receives the `ObjectTypeConfig` as an `input()` signal and builds a `FormGroup` in `buildForm()`:

```ts
for (const field of config.fields) {
  const validators = [];
  if (field.required)   validators.push(Validators.required);
  if (field.minLength)  validators.push(Validators.minLength(field.minLength));
  if (field.type === 'email') validators.push(Validators.email);
  // … etc.
  controls[field.name] = new FormControl(field.default ?? null, validators);
}
this.form = new FormGroup(controls);
```

### 3. Template rendering

The template loops over `config.fields` and uses `@if` blocks to render the correct PrimeNG component based on `field.type`:

| `type` value | PrimeNG component |
|---|---|
| `text` | `<input pInputText>` |
| `email` | `<input pInputText type="email">` |
| `number` | `<p-inputnumber>` |
| `date` | `<p-datepicker>` |
| `boolean` | `<p-checkbox [binary]="true">` |
| `select` | `<p-select>` |
| `textarea` | `<textarea pTextarea>` |

### 4. Validation feedback

Errors are shown below each field once the control is `touched`, using PrimeNG `<p-message>` for styled inline messages.

### 5. Submission

On a valid submit, `CreateObject` calls `ObjectDataService.create(config.apiEndpoint, formValue)`, which issues a `POST` to the configured endpoint (e.g. `/api/persons`). On success a toast notification is shown and the user is redirected to the list page.

---

## Object-type configuration files

Each entity type is described by a single JSON file stored in:

```
public/assets/object-types/<objectType>.json
```

### Top-level schema

```jsonc
{
  "objectType": "person",        // Matches the URL segment and the file name
  "displayName": "Person",       // Human-readable label used in the UI
  "apiEndpoint": "/api/persons", // Endpoint used for GET (list) and POST (create)
  "fields": [ /* see below */ ]
}
```

### Field schema

```jsonc
{
  "name":        "email",          // FormControl name and API payload key (required)
  "label":       "Email Address",  // Label shown in the form and table column (required)
  "type":        "email",          // Input type — see table above (required)

  // Validation (all optional)
  "required":    true,
  "minLength":   2,
  "maxLength":   255,
  "min":         0,                // Numeric minimum
  "max":         999,              // Numeric maximum
  "pattern":     "^[A-Z0-9-]+$",  // Regex pattern

  // Select options (required when type = "select")
  "options": [
    { "label": "Admin", "value": "admin" },
    { "label": "User",  "value": "user"  }
  ],

  // Defaults and hints (all optional)
  "default":     true,             // Initial value in the form
  "placeholder": "you@example.com",
  "hint":        "Used for login"  // Small grey text below the field
}
```

### Supported field types

| `type` | Rendered as | Applicable validations |
|---|---|---|
| `text` | Text input | `required`, `minLength`, `maxLength`, `pattern` |
| `email` | Text input (email keyboard) | `required`, built-in email format check |
| `number` | Numeric spinner | `required`, `min`, `max` |
| `date` | Date picker | `required` |
| `boolean` | Checkbox | — |
| `select` | Dropdown | `required` — also needs `options` array |
| `textarea` | Multi-line text | `required`, `minLength`, `maxLength` |

> `textarea` fields are hidden in the list table to keep columns readable.

---

## Adding a new object type

Follow these three steps — **no TypeScript changes are needed**.

### Step 1 — Create the config file

Create `public/assets/object-types/<yourtype>.json`:

```json
{
  "objectType": "invoice",
  "displayName": "Invoice",
  "apiEndpoint": "/api/invoices",
  "fields": [
    { "name": "number",   "label": "Invoice #", "type": "text",   "required": true },
    { "name": "amount",   "label": "Amount",    "type": "number", "required": true, "min": 0 },
    { "name": "dueDate",  "label": "Due Date",  "type": "date",   "required": true },
    { "name": "paid",     "label": "Paid",      "type": "boolean","default": false }
  ]
}
```

### Step 2 — Register it in the navigation

Open [`src/app/app.ts`](src/app/app.ts) and add an entry to `OBJECT_TYPES`:

```ts
export const OBJECT_TYPES = [
  { id: 'person',  label: 'Person',  icon: 'pi-user' },
  { id: 'product', label: 'Product', icon: 'pi-box'  },
  { id: 'invoice', label: 'Invoice', icon: 'pi-file' }, // ← add this
];
```

Available PrimeIcons can be browsed at [primeng.org/icons](https://primeng.org/icons).

### Step 3 — Add the collection to the mock database

Open [`../mockserver/db.json`](../mockserver/db.json) and add an empty array for the new type:

```json
{
  "persons":  [ ],
  "products": [ ],
  "invoices": [ ]
}
```

The new **Create Invoice** and **List Invoices** pages are now available at:

- `http://localhost:4200/objects/invoice/create`
- `http://localhost:4200/objects/invoice/list`

---

## Mock backend (json-server)

The mock server lives in `../mockserver/` and is powered by [json-server](https://github.com/typicode/json-server) v0.17.

- Data is persisted in `../mockserver/db.json` across restarts.
- All standard REST endpoints are generated automatically:

| Method | URL | Action |
|---|---|---|
| `GET` | `/persons` | List all persons |
| `POST` | `/persons` | Create a person |
| `DELETE` | `/persons/:id` | Delete a person |

The Angular proxy (`proxy.conf.json`) rewrites `/api/persons` → `http://localhost:3001/persons`, so the frontend never needs to know the mock server's port.

---

## Development commands

These are exposed via the Makefile at the repository root (`make help`).

| Command | Description |
|---|---|
| `npm start` | Start Angular dev server on port 4200 |
| `npm run build` | Production build into `dist/` |
| `npm run lint` | Run ESLint |
| `make dev` | Start frontend **and** mock server in parallel |
| `make reset-data` | Wipe `mockserver/db.json` back to empty arrays |
| `make clean-all` | Remove `node_modules` and `dist` everywhere |
