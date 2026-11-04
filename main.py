"""Statistical Physics - Lab 1: Microstates of a system of coins.

Runs every part of the practice and writes:
  * report/figures/*.pdf   vector figures for the LaTeX report
  * report/results.tex     LaTeX macros with every number quoted in the report
  * report/benchmark.tex   rows of the enumeration benchmark table

Usage:
  python main.py                 # full run, enumeration wall at 300 s (5 min)
  python main.py --wall 20       # quick run (smaller time limit)
  python main.py --skip-benchmark
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src import combinatorics as comb
from src import microstates as micro
from src import thermodynamics as thermo

# Last two digits of each team member's NIA -> edit with your own team's values
NIA_LAST_TWO_DIGITS = [84, 54, 79, 95]

ROOT = Path(__file__).parent
FIG_DIR = ROOT / "report" / "figures"
TEX_RESULTS = ROOT / "report" / "results.tex"
TEX_BENCH = ROOT / "report" / "benchmark.tex"

# Figure style (sequential blue ramp for ordered N, neutral chrome)
SEQ_BLUES = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
plt.rcParams.update({
    "figure.dpi": 150, "font.size": 10, "axes.edgecolor": AXIS, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 2, "legend.frameon": False, "savefig.bbox": "tight",
})


def sci_tex(x: float, digits: int = 3) -> str:
    """Format a float as LaTeX scientific notation, e.g. 5.20\\times10^{-11}."""
    if x == 0:
        return "0"
    exp = int(math.floor(math.log10(abs(x))))
    mant = x / 10**exp
    if -2 <= exp <= 3:
        return f"{x:.{max(digits - 1 - exp, 0)}f}"
    return f"{mant:.{digits - 1}f}\\times10^{{{exp}}}"


# --------------------------------------------------------------------------- #
# Part 1: computational analysis of microstates
# --------------------------------------------------------------------------- #
def part_n7() -> None:
    groups = micro.group_microstates(7)
    print("\n=== N = 7: microstates grouped by number of heads ===")
    for k, states in groups.items():
        print(f"{k} heads, {7 - k} tails: Omega = {len(states):3d}  {states}")


def part_benchmark(wall: float) -> list[micro.BenchmarkResult]:
    print(f"\n=== Enumeration benchmark (generator, limit {wall:.0f} s) ===")
    results = micro.find_wall(time_limit=wall, n_start=10)
    for r in results:
        print(f"N={r.n:2d}  2^N={r.n_states:>12,d}  t={r.seconds:9.3f} s  peak RAM={r.peak_mib:8.3f} MiB")
    # Naive list-based version, only up to N=22 to keep RAM reasonable
    naive = [micro.benchmark_enumeration(n, store=True) for n in range(10, 23, 2)]
    print("--- naive (all states stored in a list) ---")
    for r in naive:
        print(f"N={r.n:2d}  t={r.seconds:8.3f} s  peak RAM={r.peak_mib:9.2f} MiB")

    rows = []
    naive_by_n = {r.n: r for r in naive}
    for r in results:
        nv = naive_by_n.get(r.n)
        nv_mem = f"{nv.peak_mib:.1f}" if nv else "--"
        rows.append(f"{r.n} & " + f"{r.n_states:,}".replace(",", "{,}") + f" & {r.seconds:.3f} & {r.peak_mib:.3f} & {nv_mem} \\\\")
    TEX_BENCH.write_text("\n".join(rows) + "\n", encoding="utf-8")

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    ns = [r.n for r in results]
    a1.semilogy(ns, [r.seconds for r in results], "o-", color=BLUE, ms=5)
    if len(ns) > 2:  # fitted 2^N slope through the last point
        t_last = results[-1].seconds
        a1.semilogy(ns, [t_last * 2.0 ** (n - ns[-1]) for n in ns], "--", color=MUTED, lw=1)
        a1.text(ns[0], t_last * 2.0 ** (ns[0] - ns[-1]) * 2.5, r"$\propto 2^N$", color=INK2)
    a1.set(xlabel="Number of coins $N$", ylabel="Wall-clock time (s)", title="Run time")
    a2.semilogy(ns, [r.peak_mib for r in results], "o-", color=BLUE, ms=5, label="generator")
    a2.semilogy([r.n for r in naive], [r.peak_mib for r in naive], "s-", color=ORANGE, ms=5, label="list of states")
    a2.set(xlabel="Number of coins $N$", ylabel="Peak memory (MiB)", title="Memory")
    a2.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "benchmark.pdf")
    plt.close(fig)
    return results


def part_distributions() -> None:
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    for n, c in zip([20, 50, 80, 100], SEQ_BLUES):
        k, p = comb.distribution(n)
        a1.plot(k, p, "o-", color=c, ms=3, lw=1.5, label=f"$N={n}$")
        a2.plot(k / n, p * n, "-", color=c, lw=1.5, label=f"$N={n}$")
    a1.set(xlabel="Number of heads $k$", ylabel=r"$P_k=\Omega(N,k)/2^N$", title="Macrostate probability")
    a2.set(xlabel="Fraction of heads $k/N$", ylabel=r"$N\,P_k$", title=r"Rescaled: peak narrows as $1/\sqrt{N}$")
    a1.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "distributions.pdf")
    plt.close(fig)


def part_overflow() -> dict[str, str]:
    """Largest N for which Omega(N, N/2) still fits in a float64."""
    n = 2
    while True:
        try:
            float(math.comb(n + 2, (n + 2) // 2))
        except OverflowError:
            break
        n += 2
    print(f"\nfloat(Omega(N, N/2)) overflows for N > {n}")
    return {"NOverflow": str(n)}


def part_thermo_limit() -> None:
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    for n, c in zip([1e2, 1e3, 1e4, 1e5], SEQ_BLUES):
        x = np.linspace(0.3, 0.7, 40001)
        p = comb.probability(n, x * n) * n  # continuous extension via lnGamma
        a1.plot(x, p / p.max(), color=c, lw=1.5, label=f"$N=10^{{{int(math.log10(n))}}}$")
    a1.set(xlabel="Fraction of heads $k/N$", ylabel="$P / P_{max}$", title="Distribution vs $N$")
    a1.legend()
    ns = np.logspace(1, 23, 50)
    a2.loglog(ns, [comb.relative_width(n) for n in ns], color=BLUE)
    a2.set(xlabel="Number of coins $N$", ylabel=r"$\sigma/\mu = 1/\sqrt{N}$", title="Relative fluctuation")
    a2.annotate(r"$N=10^{23}$: $3\times10^{-12}$", xy=(1e23, 1 / math.sqrt(1e23)),
                xytext=(1e7, 1e-11), color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED))
    fig.tight_layout()
    fig.savefig(FIG_DIR / "thermodynamic_limit.pdf")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Part 2: probabilities, entropy and thermodynamics for N = 100 + M
# --------------------------------------------------------------------------- #
def part_thermodynamics() -> dict[str, str]:
    m_exact, m, n = thermo.system_size(NIA_LAST_TWO_DIGITS)
    h = n // 2  # N/2 rounded down (N odd -> k=66 and k=67 are equally probable)
    print(f"\n=== N = 100 + M: harmonic mean = {m_exact:.6f} -> M = {m}, N = {n} ===")

    res = {
        "Mexact": f"{m_exact:.4f}", "M": str(m), "N": str(n), "Nhalf": str(h),
        "Pa": comb.probability(n, 30),
        "Pb": comb.probability(n, h),
        "Pc": comb.cumulative_probability(n, h - 10, h + 10),
        "Pd": comb.cumulative_probability(n, h - 20, h + 20),
        "Smax": thermo.entropy(n, h),
        "dSe": thermo.entropy_change(n, h + 25, h),
        "dSf": thermo.entropy_change(n, h + 10, h),
        "dSg": thermo.entropy_change(n, h, 20),
        "tSec": thermo.waiting_time_seconds(n, 8),
        "ratio": thermo.likelihood_ratio(n, h, m - 10, m + 10),
        "ratioHalf": thermo.likelihood_ratio(n, h, h - 10, h + 10),
    }
    res["tYears"] = res["tSec"] / thermo.SECONDS_PER_YEAR
    res["tAges"] = res["tYears"] / thermo.AGE_OF_UNIVERSE_YEARS
    err = comb.ln_omega_abs_error(n, h)
    res["lnOmegaErr"] = err
    res["dSErr"] = thermo.K_B * err
    res["SmaxOverkB"] = comb.ln_omega(n, h)

    for key in ["Pa", "Pb", "Pc", "Pd", "Smax", "dSe", "dSf", "dSg", "tSec", "tYears", "ratio", "dSErr"]:
        print(f"{key:>8s} = {res[key]:.6e}")

    # Figure: entropy and probability in two stacked panels (one y-axis each)
    k = np.arange(n + 1)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6, 5), sharex=True)
    a1.plot(k, thermo.entropy(n, k), color=BLUE)
    a1.set(ylabel="Entropy $S$ (J/K)", title=f"Entropy and probability, $N={n}$")
    a2.plot(k, comb.probability(n, k), color=BLUE)
    a2.axvspan(h - 10, h + 10, color=BLUE, alpha=0.12, lw=0)
    a2.text(h + 12, comb.probability(n, h) * 0.8, r"$N/2\pm10$", color=INK2)
    a2.set(xlabel="Number of heads $k$", ylabel="$P_k$")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "entropy_probability.pdf")
    plt.close(fig)

    out = {}
    for key, v in res.items():
        out[key] = v if isinstance(v, str) else sci_tex(v, 5 if key.startswith("P") else 4)
    return out


def write_results(macros: dict[str, str]) -> None:
    lines = ["% Auto-generated by main.py -- do not edit by hand"]
    for key, val in macros.items():
        name = "res" + "".join(ch for ch in key if ch.isalpha())
        lines.append(f"\\newcommand{{\\{name}}}{{{val}}}")
    TEX_RESULTS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--wall", type=float, default=300.0, help="time limit (s) for full enumeration")
    parser.add_argument("--skip-benchmark", action="store_true")
    args = parser.parse_args()
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    part_n7()
    macros: dict[str, str] = {}
    if not args.skip_benchmark:
        bench = part_benchmark(args.wall)
        macros["NWall"] = str(bench[-1].n)
        macros["TWall"] = f"{bench[-1].seconds:.1f}"
        macros["WallLimit"] = f"{args.wall:.0f}"
    else:
        macros.update({"NWall": "?", "TWall": "?", "WallLimit": f"{args.wall:.0f}"})
    part_distributions()
    macros.update(part_overflow())
    part_thermo_limit()
    macros.update(part_thermodynamics())
    write_results(macros)
    print(f"\nFigures written to {FIG_DIR}\nLaTeX macros written to {TEX_RESULTS}")


if __name__ == "__main__":
    main()
