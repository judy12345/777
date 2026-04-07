# CausalAudit Prototype (MVP+)

This repository includes a runnable prototype for CausalAudit:

- `causalaudit/schema.py`: trace/event schema + JSON conversion
- `causalaudit/policy.py`: Policy IR + dict conversion
- `causalaudit/checker.py`: compliance checker + evidence chain + violation details
- `causalaudit/counterfactual.py`: cost-ranked counterfactual edits (delete/insert/replace)
- `scripts/generate_benchmark.py`: generate benchmark v0 (30 cases)
- `scripts/evaluate_benchmark.py`: evaluate checker + counterfactual metrics
- `paper/causalaudit_paper.md`: paper draft
- `scripts/build_paper_pdf.py`: build PDF from the draft without external dependencies

## Run demo

```bash
python examples/demo.py
```

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Generate and evaluate benchmark

```bash
python scripts/generate_benchmark.py
python scripts/evaluate_benchmark.py
```

## Build paper PDF

```bash
python scripts/build_paper_pdf.py
```
