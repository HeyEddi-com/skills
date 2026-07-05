@backend-type-bridger and @composable-patterns must wire the frontend to the API:

- Types from openapi.json in src/types/api.ts
- useApi + useUsers composables following skill context docs
- Tests for composables where applicable
- Backend pytest passes

Read all changed files. Flag any fetch URL mistakes, missing error handling, or command warnings.
