"""Ejecuta todo el Lab 1: tablas, benchmarks y figuras (PDF vectorial)."""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src import combinatorics as comb
from src import microstates as ms
from src import thermodynamics as th

NIA_LAST_TWO_DIGITS = [79, 95, 84, 54]
FIG_DIR = Path("report/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Evita UnicodeEncodeError al imprimir Ω, σ, μ en terminales de Windows (cp1252)
sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # ---------- Parámetro N ----------
    hm, M, N = th.compute_N(NIA_LAST_TWO_DIGITS, rounding="round")  # o "floor"
    k_mid = N // 2
    print(f"Media armónica = {hm:.4f}  ->  M = {M},  N = {N},  k_mid = {k_mid}")

    # ---------- 3.1 Enumeración N = 7 ----------
    print("\n== N = 7 ==")
    counts7 = ms.enumerate_counts(7)
    samples = ms.sample_microstates(7)
    for k in range(7, -1, -1):
        print(f"k={k}  tails={7-k}  {samples[k]}  Ω={counts7[k]}")
    print("Total:", counts7.sum())

    # ---------- 3.2 Muro 2^N ----------
    print("\n== Benchmark enumeración ==")
    last = None
    for n in (16, 18, 20, 22, 24):
        r = ms.benchmark_enumeration(n)
        last = r
        print(f"N={n}: 2^N={r['states']:.3e}  t={r['time_mean']:.3f}±{r['time_std']:.3f} s  "
              f"pico RAM (generador)={r['peak_bytes']/1e3:.1f} kB  "
              f"RAM si fuese lista≈{r['list_bytes_estimate']/1e6:.0f} MB")
    n_max = ms.estimate_N_max(last["N"], last["time_mean"], 300.0)
    print(f"N_max estimado en 5 min ≈ {n_max:.1f}")
    print(f"float(Ω(N, N/2)) desborda para N > {comb.float_overflow_N()}")

    # ---------- 3.3 Distribuciones ----------
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for n in (20, 50, 80, 100):
        k, P = comb.distribution(n)
        ax[0].plot(k, P, "o-", ms=3, label=f"N={n}")
        ax[1].plot(k / n, P * np.sqrt(n), label=f"N={n}")
    ax[0].set(xlabel="k (caras)", ylabel=r"$P_k=\Omega/2^N$")
    ax[1].set(xlabel="k/N", ylabel=r"$\sqrt{N}\,P_k$")
    for a in ax:
        a.legend()
        a.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "distributions.pdf")
    plt.close(fig)

    # ---------- 3.4 Límite termodinámico ----------
    print("\n== Fluctuaciones relativas σ/μ = 1/√N ==")
    for n in (20, 100, N, 10**6, 10**12, 1e23):
        print(f"N={n:.3e}: σ/μ = {th.relative_fluctuation(n):.3e}")
    N_big = 1e23
    print(f"ln Ω(N,N/2) para N=1e23 ≈ {th.ln_omega_max_stirling(N_big):.6e}"
          f"  (S/k_B ≈ N ln2 = {N_big*th.LN2:.6e})")
    print(f"ln P(desviación 1e-6 en k/N) ≈ {th.ln_prob_deviation(N_big, 2e-6):.3e}")

    ns = np.logspace(1, 23, 200)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.loglog(ns, 1 / np.sqrt(ns))
    ax.set(xlabel="N", ylabel=r"$\sigma/\mu=1/\sqrt{N}$")
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "relative_fluctuation.pdf")
    plt.close(fig)

    # ---------- 4.2 Tabla 3 ----------
    print(f"\n== Tabla 3 (N = {N}) ==")
    P30 = float(comb.probability(N, 30))
    Pmid = float(comb.probability(N, k_mid))
    Pint = comb.probability_range(N, k_mid - 10, k_mid + 10)
    k1, k2 = k_mid + 25, k_mid
    dS = comb.delta_S_over_kB(N, k1, k2)
    print(f"P(k=30)                      = {P30:.4e}")
    print(f"P(k={k_mid}) (más probable)     = {Pmid:.4e}   (ΔS/kB = 0)")
    print(f"P(k∈[{k_mid-10},{k_mid+10}])         = {Pint:.6f}")
    print(f"ΔS/kB (k={k1} -> k={k2})     = {dS:.4f}   (Ω ratio = {np.exp(dS):.4e})")

    # ---------- 4.2 Resto de la Parte 2 ----------
    Pd = comb.probability_range(N, k_mid - 20, k_mid + 20)
    print(f"P(cruces∈[{k_mid-20},{k_mid+20}])      = {Pd:.6f}   (simetría caras/cruces)")
    S_max = float(comb.log_omega(N, k_mid))
    print(f"S_max/kB = {S_max:.4f}   S_max = {th.K_B * S_max:.4e} J/K")
    for label, (a, b) in {"e": (k_mid + 25, k_mid), "f": (k_mid + 10, k_mid),
                          "g": (k_mid, 20)}.items():
        x = comb.delta_S_over_kB(N, a, b)
        print(f"({label}) ΔS(k={a}, k={b}): ΔS/kB = {x:.4f}   ΔS = {th.K_B * x:.4e} J/K")
    err = comb.log_omega_error_bound(N, k_mid)
    print(f"Incertidumbre: |δ lnΩ| ≲ {err:.1e}  ->  δS ≈ {th.K_B * err:.1e} J/K")

    t = th.waiting_time_seconds(N, 8)
    years = t / th.SECONDS_PER_YEAR
    print(f"(h) Espera para k=8: {t:.3e} s = {years:.3e} años "
          f"= {years / th.AGE_OF_UNIVERSE_YEARS:.3e} edades del universo")
    ratio = comb.likelihood_ratio(N, k_mid, M - 10, M + 10)
    print(f"(i) P(k={k_mid}) / P({M-10} ≤ k ≤ {M+10}) = {ratio:.4f}")

    # Figura con la distribución de N y marcas
    k, P = comb.distribution(N)
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.bar(k, P, width=1.0, color="C0", alpha=0.6)
    ax.axvspan(k_mid - 10, k_mid + 10, color="C1", alpha=0.25, label=r"$N/2\pm10$")
    ax.axvline(30, color="C3", ls="--", label="k=30")
    ax.set(xlabel="k", ylabel=r"$P_k$", title=f"N={N}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "distribution_N.pdf")
    plt.close(fig)

    print("\nFiguras guardadas en", FIG_DIR)


if __name__ == "__main__":
    main()