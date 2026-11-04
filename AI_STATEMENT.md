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
## Query log

### Query 1: Initial scaffold
- **Prompt (original Spanish, with both project PDFs attached):** "tengo que
  hacer este proyecto, tengo ya creado el jupyter notebook con el codigo, la
  carpeta src con sus respectivos archivos, lo del environment.yml, la carpeta
  con los tests, pero no me termina de funcionar el codigo, asi que dime que
  tengo que meter en cada archivo y en el codigo para que funcione y me de los
  resultados que quiero, el nia de cada uno de los 4 integrantes:
  NIA_LAST_TWO_DIGITS = [79, 95, 84, 54]"
- **AI output:** environment.yml, pytest.ini, src/ modules (microstates.py,
  combinatorics.py, thermodynamics.py), tests/, main.py and notebook cells.
  It computed N = 175 and noted that N is odd.
- **Team modifications:** removed a stray line in main.py
  (`sample_sicrostates ... if False else ...`) and adapted file paths.

### Query 2: Reliability check
- **Prompt:** "con este codigo me aseguras que va a salir bien?"
- **AI output:** stated the code had not been executed, and listed risks
  (Python >= 3.10 for int.bit_count, test tolerances, paths, the 5-minute
  wall being extrapolated rather than measured).
- **Team action:** ran everything ourselves in the statphys_lab1 environment.

### Query 3: ModuleNotFoundError
- **Prompt:** pasted traceback "ModuleNotFoundError: No module named 'src'"
  from pytest.
- **AI output:** check that pytest.ini exists in the project root, or use
  conftest.py or `python -m pytest`.

### Query 4: pytest.ini file type
- **Prompt:** "pytest.ini sale en dir y esta en la raiz, que tipo de documento
  tiene que ser, de texto, de codigo.."
- **AI output:** plain text file, how to check its name and content, and how
  to confirm pytest reads it (configfile: pytest.ini).
- **Resolution:** import path fixed; test modules were collected correctly.

### Query 5: ImportError cannot import name 'count_heads'
- **Prompt:** pasted traceback from tests/test_microstates.py.
- **Cause:** our src/microstates.py was incomplete (functions missing).
- **Resolution:** replaced it with the full version; all tests pass.

### Query 6: Remaining work
- **Prompt:** "vale ya funciona lo de los tests, ahora el resto del lab?"
- **AI output:** steps to run main.py, a benchmark script, notebook check,
  AI statement template, LaTeX report contents and Git workflow.

### Query 7: AttributeError 'compute_N'
- **Prompt:** pasted traceback from main.py.
- **Cause:** src/thermodynamics.py was incomplete. pytest did not detect it
  because no test imports that module.
- **Resolution:** restored the full file.

### Query 8: AttributeError 'probability_range'
- **Prompt:** pasted traceback and partial output from main.py.
- **Cause:** src/combinatorics.py was incomplete or outdated when main.py ran.
- **Resolution:** restored the full file; main.py ran end to end and wrote
  all figures to report/figures/.

### Query 9: Are we missing anything?
- **Prompt:** "tenemos todo lo que nos pide?" (with the full main.py output)
- **AI output:** checklist of pending items: measure the real 5-minute wall,
  interval convention for odd N, LaTeX report, AI statement, Git workflow,
  notebook run, oral defense preparation.

### Query 10: AI statement and team summary
- **Prompt:** "dime que tengo que meter en el file de AI_statement y hazme un
  resumen en ingles de lo que tenemos hecho y lo que falta"
- **AI output:** first draft of this file and an English progress summary.

## Human verification
- N computed by hand: harmonic mean of [79, 95, 84, 54] = 74.616, so M = 75
  and N = 175.
- Log-gamma results validated against exact integers (math.comb) for
  N in {1, 7, 20, 50, 100, 175} in tests/test_combinatorics.py.
- Enumeration validated against binomial coefficients
  ([1, 7, 21, 35, 35, 21, 7, 1] for N = 7) in tests/test_microstates.py.
- Distributions checked for normalization (sum = 1) and symmetry.
- main.py output reviewed by the team: P(k=87) = 0.0601,
  P(77 <= k <= 97) = 0.887, Delta S/k_B (k=112 -> 87) = -6.909.

## Problems found in AI output and how we solved them
1. **Incomplete files:** several src/ files were missing functions, and the
   errors only appeared at runtime (queries 5, 7, 8). pytest did not cover
   thermodynamics.py. We now run pytest and main.py after every change.
2. **Memory:** storing all 2^N microstates in a list needs O(2^N) memory
   (about 604 MB at N = 24). We use a generator (yield); peak RAM stays
   around 0.7 kB (measured with tracemalloc).
3. **Overflow:** factorials overflow for N >= 100, so we use log-space with
   scipy.special.gammaln. For N ~ 1e23 even gammaln loses precision through
   cancellation, so we use the Stirling form instead.
4. **N is odd (175):** N/2 = 87.5 is not an integer. The code uses k = 87
   (Omega(175, 87) = Omega(175, 88)). The interval [N/2 - 10, N/2 + 10] is
   implemented as k = 77..97. TODO: confirm or change this convention and
   explain why.
5. **5-minute wall:** the AI code first only extrapolated N_max (about 30).
   We measured it directly with benchmark_wall.py. TODO: N_max = <value>.

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
- **Prompt (Spanish):** "luego las explicaciones".
- **Output:** the interpretation paragraphs for the likelihood ratio, the
  Second Law, the large-N limit, and the conclusions.
- **Verification:** the figures quoted in the text (8.7σ for k = 30, 3.4σ
  for k = 65, Ω(87)/Ω(65) ≈ 3.4·10², P(65 ≤ k ≤ 85) = 0.381) were
  recomputed; one value (originally "two standard deviations, 2.4·10²")
  was wrong and was corrected before committing.


### 5. Merging `feature/full-lab1` and completing Part 2 (PR #4)
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

### 6. Final clean-up
- **Who:** Elena Valenzuela
- **Prompt (Spanish):** "haz la version nueva con los cambios correctos".
- **Output:** `main.py` now generates `thermodynamic_limit.pdf` (used in the
  report), figures regenerated, notebook moved to `notebooks/` and rewritten
  to use the current `src/` functions, `.gitignore`, this file.

---


