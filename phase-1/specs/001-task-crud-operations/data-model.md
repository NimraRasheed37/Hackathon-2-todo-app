# Data Model: Task

This data model is based on the `spec.md`.

## Task Entity

| Field       | Type     | Description              | Validation Rules         |
|-------------|----------|--------------------------|--------------------------|
| id          | int      | Unique task identifier   | Auto-generated, unique   |
| title       | str      | Short title (required)   | Required, 1-200 characters |
| description | str      | Optional details         | None                     |
| completed   | bool     | Completion status        | Boolean, defaults to false |
| created_at  | datetime | Creation timestamp       | Auto-generated           |
| updated_at  | datetime | Last update timestamp    | Auto-generated on update |
