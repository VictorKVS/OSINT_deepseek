# FATHER Programmer Training Gym

## Purpose

Create a standards-aware programmer model by specializing an existing coder model, not by training a foundation model from scratch.

The model weights should learn professional behavior: decompose tasks, extract constraints, choose algorithms and designs, test code, repair defects, respect secure-coding rules, and produce concise source-aware decision summaries.

Version-sensitive truth remains outside the weights in traceable retrieval: Russian regulation, GOST/ISO/IEEE/NIST/IETF/OWASP material, language specifications, framework documentation, and project conventions.

## MIN conveyor

```text
Task source
  -> normalized task
  -> MIN/MEDIUM/MAX + NECESSARY/DESIRABLE/INTERESTING_LATER
  -> source bindings
  -> candidate solution
  -> tests/checks
  -> score
  -> critic review
  -> Golden Case
  -> training example
  -> model candidate
  -> holdout/regression
  -> human promotion
```

## Current seed

The first seed contains 12 deterministic MIN Python tasks:

- 8 TRAIN tasks;
- 4 HOLDOUT tasks;
- all classified `MIN + NECESSARY`;
- domains include Python fundamentals, algorithms, data structures, robustness, validation, secure coding, and reliability.

The repository HOLDOUT split is excluded from training export but is **not secret** because the repository is public. Before a real model is promoted, a separate private/external holdout corpus is required.

## Why Golden Cases are separate

Raw tasks are not training examples. A task becomes a Golden Case only after:

1. mandatory correctness checks pass;
2. requirements are satisfied;
3. critical security defects are absent;
4. the concise decision summary is traceable to source references or explicit GAPs;
5. critic review is complete.

This prevents unverified reference answers from silently becoming model behavior.

## No private chain-of-thought target

Training artifacts store concise plans, assumptions, decision summaries, tests, evidence references, and final implementations. Long hidden reasoning traces are not required and are not a training target.

## Execution safety

The MIN foundation only builds and validates task artifacts. Unattended execution of model-generated code requires a sandbox gate. Local execution is reserved for trusted reference fixtures until that sandbox is implemented.

## One-click build

```powershell
cd "G:\1\OSINT_deepseek"
git pull --ff-only
.\RUN_PROGRAMMER_TRAINING_GYM.cmd
```

Outputs:

- `reports/programmer_training_gym/TASK_MANIFEST.json`
- `reports/programmer_training_gym/TRAIN_PROMPTS.jsonl`
- `reports/programmer_training_gym/HOLDOUT_MANIFEST.json`
- `reports/programmer_training_gym/GOLDEN_CASE_QUEUE.json`
- `reports/programmer_training_gym/LATEST_PROGRAMMER_TRAINING_GYM_BUILD.json`

At this stage `golden_cases_total` and `training_examples_total` must remain zero until reference solutions and review evidence exist.

## Next gates

### MIN

- generate/reference-solve the 8 TRAIN tasks;
- implement deterministic tests;
- score reference solutions;
- critic review;
- create first Golden Cases;
- export first SFT-ready records;
- establish a private holdout set.

### MEDIUM

Add pytest, SQL, HTTP/API, refactoring, debugging, secure coding, dependency handling, and sandboxed model-code execution. Generate preference pairs from measured competing solutions.

### MAX

Add architecture, DevSecOps, concurrency, performance, project-scale work, benchmark-driven rewards, and a regression league comparing model versions.

## Metrics

Only measured values are reported. The gym tracks task counts, train/holdout split, Golden Cases, training examples, pass rate, security failure rate, rework rate, and regressions. Speedup and ETA stay null until comparable telemetry exists.
