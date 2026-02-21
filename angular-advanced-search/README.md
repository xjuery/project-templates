# Angular Advanced Search App

An Angular 20 application with PrimeNG components that provides Kibana-like advanced search capabilities with complex filter building.

## Features

- **Text search**: Full-text search across all fields
- **Filter builder**: Create multiple filters with field/operator/value
  - String: contains, does not contain, equals, starts with, ends with, is empty, is not empty
  - Number: equals, not equals, greater than (or equal), less than (or equal), between
  - Date: before, after, on date, on or before, on or after, between
  - Boolean: is true/false
- **AND/OR combinator**: Combine filters with AND or OR logic
- **Results table**: Sortable, paginated results display
- **CSV export**: Export all matching results to CSV
- **Mock backend**: Express server with 30 sample records

## Quick Start

```bash
# Install dependencies
npm install

# Run mock server + Angular app together
npm run dev

# Or separately:
npm run mock-server   # Mock API on http://localhost:3000
npm start             # Angular app on http://localhost:4200
```

## Project Structure

```
src/app/
├── models/
│   └── search.models.ts         # Interfaces and operator definitions
├── services/
│   └── search.service.ts        # HTTP service for API calls
├── components/
│   └── filter-builder/          # Reusable filter builder component
├── pages/
│   ├── search/                  # Search page with text + filters
│   └── results/                 # Results table with sort/paginate/export
mock-server/
└── server.js                    # Express mock API (port 3000)
```

## Mock API

- `GET /api/fields` — Returns field definitions (name, type)
- `POST /api/search` — Search with filters, returns paginated results

### Sample Data Fields

| Field | Type | Description |
|-------|------|-------------|
| id | number | Unique identifier |
| name | string | Full name |
| email | string | Email address |
| age | number | Age in years |
| salary | number | Annual salary |
| score | number | Performance score |
| status | string | active / inactive / pending |
| department | string | Team/department |
| description | string | Bio/description |
| isActive | boolean | Active status |
| isVerified | boolean | Verification status |
| createdAt | date | Record creation date |
| updatedAt | date | Last update date |
| birthDate | date | Date of birth |
