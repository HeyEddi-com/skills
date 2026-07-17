
# Examples: PR submission review

## Fetch context (live)

```bash
python scripts/fetch_pr_context.py --pr 42 --project-root . --write-cache
```

## Fixture mode (eval / no gh)

```bash
python scripts/fetch_pr_context.py --pr 42 --fixture fixtures/sample-pr-diff.json --project-root .
python scripts/check_doc_drift.py --pr 42 --fixture fixtures/sample-pr-diff.json --project-root .
python scripts/audit_pr_changes.py --pr 42 --fixture fixtures/sample-pr-diff.json --project-root .
```

## Write report

```bash
python scripts/write_pr_review.py --pr 42 --fixture fixtures/sample-pr-diff.json --force --project-root .
```

## Verify before merge

```bash
python scripts/verify_pr_review.py --pr 42 --check --project-root .
```
