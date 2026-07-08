# Examples — TaskFlow dashboard review

```bash
python scripts/init_product_docs.py --project-root .
python scripts/load_product_context.py --project-root .
python scripts/audit_product.py --project-root . --check
python scripts/write_feature_spec.py --project-root . --json '{
  "route": "/dashboard",
  "title": "Team roster",
  "problem": "Jordan sees team status fast.",
  "user_stories": ["As Jordan, I want a roster table so that I spot blockers before standup."],
  "acceptance_criteria": ["GET /api/users populates table", "No placeholder copy in DashboardView"]
}' --force
python scripts/check_features.py --project-root .
python scripts/write_review_plan.py --project-root . --title "TaskFlow build review" --force
# Delegate ux-flow-auditor, heyeddi-design critique, visual-auditor, engineering-excellence
# Fill review plan synthesis + recommendations
python scripts/verify_product.py --project-root . --check
```
