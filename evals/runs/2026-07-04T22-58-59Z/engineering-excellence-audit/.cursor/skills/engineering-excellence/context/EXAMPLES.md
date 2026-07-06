
# Examples — Engineering excellence

## Init docs

```bash
python scripts/init_engineering_docs.py --project-root .
```

## Audit before merge

```bash
python scripts/audit_engineering.py --project-root . --check
```

## Record ADR

```bash
python scripts/append_decision.py \
  --project-root . \
  --title "Single composable per API domain" \
  --context "Three views duplicated fetch logic" \
  --decision "Add useTasks composable; views import only that" \
  --consequences "Remove direct fetch from DashboardView"
```
