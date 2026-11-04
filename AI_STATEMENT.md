# AI Statement — Statistical Physics Lab 1, Group E

This file logs every use of AI tools in the project, as required by the
course guidelines (Phase 3): the prompt, what the AI generated, how the team
verified it, and what the team changed.

**Tools used:** Claude (Anthropic) — Claude Code desktop app and chat.

**Verification policy:** every AI-generated function is covered by `pytest`
unit tests that compare log-space results with exact integer combinatorics
(`math.comb`). Numerical results quoted in the report were cross-checked
between `main.py` and an independent calculation with Python's exact
integers.

---

## Log

### 1. Understanding the assignment
- **Who:** Elena Valenzuela
- **Prompt (Spanish):** "dime todas las instrucciones que tengo que seguir"
  (with the course guidelines, the report template and last year's report).
- **Output:** a phase-by-phase summary of the guidelines and a list of
  errors in last year's report that we should not repeat.
- **Team action:** used as a checklist; no code generated.

### 2. First version of `main.py` (PR #3)
- **Who:** Elena Valenzuela
- **Prompt:** request to write a script that runs every part of the lab.
  *(TODO: paste the exact prompt.)*
- **Output:** a `main.py` that ran every part of the lab.
- **Problem found:** it imported functions (`group_microstates`,
  `system_size`, ...) that do not exist in the final `src/` written by the
  team, and its NIA list was copied from last year's report.
- **Resolution:** the team decided to keep the `main.py` from branch
  `feature/full-lab1` (written by the team). The AI version stays in the git
  history (commit `22c52dd`) but is not used.

### 3. LaTeX report skeleton (`report/main.tex`, PR #5)
- **Who:** Elena Valenzuela
- **Prompt (Spanish):** "puedes hacerlo?" — answering an offer to prepare a
  `main.tex` with every section, table and figure of the template.
- **Output:** the full report structure, tables, equations and the
  numerical results for N = 175.
- **Verification:** every number was computed with exact integers
  (`math.comb`) and later reproduced by `main.py` (see item 6).
- **Team changes:** authors, NIAs and GitHub users; removed the header
  instructions; reviewed the text.

### 4. Explanations of questions (i), (j), (k) and conclusions
- **Who:** Elena Valenzuela
- **Prompt (Spanish):** "luego las explicaciones y eso por q no me las das".
- **Output:** the interpretation paragraphs for the likelihood ratio, the
  Second Law, the large-N limit, and the conclusions.
- **Verification:** the figures quoted in the text (8.7σ for k = 30, 3.4σ
  for k = 65, Ω(87)/Ω(65) ≈ 3.4·10², P(65 ≤ k ≤ 85) = 0.381) were
  recomputed; one value (originally "two standard deviations, 2.4·10²")
  was wrong and was corrected before committing.

### 5. Benchmark measurement
- **Who:** Elena Valenzuela
- **Prompt (Spanish):** "bueno y esto?" (the empty benchmark table).
- **Output:** the AI ran `benchmark_enumeration` on Elena's laptop and
  filled Table 2.
- **Note:** the first run used Python 3.12 outside the Conda environment;
  it was repeated with Python 3.11 to match `environment.yml`. Repeated runs
  gave N_max between 29.4 and 30.4, reported as N_max = 30 ± 1.

### 6. Merging `feature/full-lab1` and completing Part 2 (PR #4)
- **Who:** Elena Valenzuela
- **Prompt (Spanish):** "Vale haz la opcion 1 pero que no se pierda nada".
- **Output:** merge of `main` into `feature/full-lab1` keeping the team's
  `main.py`; new functions `likelihood_ratio`, `log_omega_error_bound`,
  `float_overflow_N`, `waiting_time_seconds`; the missing Part 2
  calculations in `main.py`; new tests.
- **Problems found and resolved:**
  - `tests/test_combinatorics.py` called functions that no longer existed
    in `src/combinatorics.py`, so the tests could not pass. The tests were
    rewritten for the current API, keeping the same checks.
  - `main.py` crashed with `UnicodeEncodeError` when printing Ω, σ, μ on a
    Windows console (cp1252). Fixed with
    `sys.stdout.reconfigure(encoding="utf-8")`.
- **Verification:** 18 tests pass; the output of `main.py` matches every
  number in the report.

### 7. Final clean-up
- **Who:** Elena Valenzuela
- **Prompt (Spanish):** "haz la version nueva con los cambios correctos".
- **Output:** `main.py` now generates `thermodynamic_limit.pdf` (used in the
  report), figures regenerated, notebook moved to `notebooks/` and rewritten
  to use the current `src/` functions, `.gitignore`, this file.

---

## Other team members

*(TODO: each member adds here any AI use of their own — prompt, output,
verification and changes — or writes "No AI tools used".)*

- **Claudia Valiente:**
- **Justin Ryan Kotrba:**
- **Vassily Martin Schnell:**
