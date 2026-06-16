from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "04_pm_fm_delayline_modulation"
    / "04c_fm_phase_derivation"
)

FIG_DPI = 200
FIGSIZE = (12.0, 9.2)

SAMPLE_RATE_HZ = 60.0
N_SAMPLES = 120
DISPLAY_OVERSAMPLE = 8
MODULATOR_CYCLES = 1.0
CARRIER_CYCLES = 8.0
F_C_HZ = CARRIER_CYCLES * SAMPLE_RATE_HZ / N_SAMPLES
F_M_HZ = MODULATOR_CYCLES * SAMPLE_RATE_HZ / N_SAMPLES
DELTA_F_HZ = 2.0

MODULATION_VIOLET = "#7b4ab8"
MODULATION_VIOLET_LIGHT = "#a77bd5"
FM_PHASE_COLOR = MODULATION_VIOLET
REFERENCE_COLOR = "0.65"
OMEGA_STEM_COLOR = "0.74"
PHI_PREVIEW_COLOR = "0.70"
BASELINE_COLOR = "0.78"
GRID_ALPHA = 0.25

TITLE_SIZE = 22
LABEL_SIZE = 18
TICK_SIZE = 15
LEGEND_SIZE = 13

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def sample_axis() -> np.ndarray:
    return np.arange(N_SAMPLES, dtype=float)


def display_axis() -> np.ndarray:
    point_count = (N_SAMPLES - 1) * DISPLAY_OVERSAMPLE + 1
    return np.linspace(0.0, N_SAMPLES - 1, point_count)


def modulator(kind: str, n: np.ndarray) -> np.ndarray:
    phase = 2.0 * np.pi * F_M_HZ * n / SAMPLE_RATE_HZ
    if kind == "sine":
        return np.sin(phase)
    if kind == "triangle":
        return (2.0 / np.pi) * np.arcsin(np.sin(phase))
    if kind == "rectangle":
        return np.where(np.sin(phase) >= 0.0, 1.0, -1.0)
    raise ValueError(f"Unsupported modulator kind: {kind}")


def modulator_text(kind: str) -> tuple[str, str, str]:
    if kind == "sine":
        return "Modulator signal", r"$m[n]$", r"m[n]"
    if kind == "triangle":
        return "Triangle modulator signal", r"$m_\mathrm{tri}[n]$", r"m_\mathrm{tri}[n]"
    if kind == "rectangle":
        return "Rectangle modulator signal", r"$m_\mathrm{rect}[n]$", r"m_\mathrm{rect}[n]"
    raise ValueError(f"Unsupported modulator kind: {kind}")


def fm_phase_from_frequency(f_i_hz: np.ndarray) -> np.ndarray:
    omega_i = 2.0 * np.pi * f_i_hz / SAMPLE_RATE_HZ
    phi = np.zeros_like(omega_i)
    phi[1:] = np.cumsum(omega_i[:-1])
    return phi


def phase_formatter(value: float, _position: int) -> str:
    ratio = value / np.pi
    if abs(ratio) < 1e-9:
        return "0"
    if abs(ratio - round(ratio)) < 1e-9:
        integer = int(round(ratio))
        if integer == 1:
            return r"$\pi$"
        return rf"${integer}\pi$"
    return rf"${ratio:.1f}\pi$"


def style_axis(ax: plt.Axes) -> None:
    ax.grid(alpha=GRID_ALPHA)
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(0, N_SAMPLES - 1)
    ax.set_xticks([0, 30, 60, 90, 119])
    ax.tick_params(labelsize=TICK_SIZE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_series(visible_steps: int, output_name: str, *, modulator_kind: str = "sine") -> Path:
    n = sample_axis()
    n_dense = display_axis()

    modulator_title, modulator_label, modulator_formula_symbol = modulator_text(modulator_kind)

    m = modulator(modulator_kind, n)
    m_dense = modulator(modulator_kind, n_dense)

    f_i = F_C_HZ + DELTA_F_HZ * m
    f_i_dense = F_C_HZ + DELTA_F_HZ * m_dense

    omega_c = 2.0 * np.pi * F_C_HZ / SAMPLE_RATE_HZ
    omega_i = 2.0 * np.pi * f_i / SAMPLE_RATE_HZ
    omega_i_dense = 2.0 * np.pi * f_i_dense / SAMPLE_RATE_HZ
    phi_fm = fm_phase_from_frequency(f_i)

    fig, axes = plt.subplots(3, 1, figsize=FIGSIZE, sharex=True)
    axes = np.atleast_1d(axes).tolist()
    fig.subplots_adjust(left=0.11, right=0.90, bottom=0.09, top=0.90, hspace=0.42)
    fig.suptitle("FM phase derivation", fontsize=24, y=0.975)

    ax_m, ax_f, ax_phase = axes

    # 1. Modulator signal.
    ax_m.plot(n_dense, m_dense, color=MODULATION_VIOLET_LIGHT, lw=2.5, label=modulator_label)
    ax_m.plot(n[::4], m[::4], linestyle="", marker="o", ms=4.2, color=MODULATION_VIOLET_LIGHT)
    ax_m.set_ylim(-1.15, 1.15)
    ax_m.set_yticks([-1, 0, 1])
    ax_m.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax_m.set_title(modulator_title, fontsize=TITLE_SIZE, pad=8)
    style_axis(ax_m)
    ax_m.legend(loc="upper right", fontsize=LEGEND_SIZE, framealpha=0.95)

    # 2. Instantaneous frequency.
    ax_f.set_ylim(F_C_HZ - 1.35 * DELTA_F_HZ, F_C_HZ + 1.35 * DELTA_F_HZ)
    ax_f.set_yticks([F_C_HZ - DELTA_F_HZ, F_C_HZ, F_C_HZ + DELTA_F_HZ])
    ax_f.set_ylabel(r"$f_i[n]$ in Hz", fontsize=LABEL_SIZE)
    ax_f.set_title("Instantaneous frequency", fontsize=TITLE_SIZE, pad=8)
    style_axis(ax_f)
    if visible_steps >= 2:
        ax_f.plot(
            n_dense,
            f_i_dense,
            color=MODULATION_VIOLET_LIGHT,
            lw=2.5,
            ls="--",
            label=rf"$f_i[n]=f_c+\Delta f\,{modulator_formula_symbol}$",
        )
        ax_f.plot(n[::4], f_i[::4], linestyle="", marker="o", ms=4.2, color=MODULATION_VIOLET_LIGHT)
        ax_f.axhline(F_C_HZ, color=REFERENCE_COLOR, lw=1.8, ls="--", label=r"$f_c$")
        ax_f.legend(loc="upper right", fontsize=LEGEND_SIZE, framealpha=0.95)

    # 3. Discrete angular frequency and accumulated phase.
    if visible_steps <= 4:
        ax_phase.set_ylim(0.0, 0.72)
        ax_phase.set_yticks([0.0, omega_c, 0.7])
        ax_phase.set_yticklabels(["0", r"$\Omega_c$", "0.7"])
        ax_phase.set_ylabel(r"$\Omega_i[n]$ in rad/sample", fontsize=LABEL_SIZE)
        ax_phase.set_title("Discrete angular frequency", fontsize=TITLE_SIZE, pad=8)
        style_axis(ax_phase)
        if visible_steps >= 3:
            if visible_steps == 3:
                ax_phase.plot(
                    n_dense,
                    omega_i_dense,
                    color=MODULATION_VIOLET_LIGHT,
                    lw=2.5,
                    ls="--",
                    label=r"$\Omega_i[n]=2\pi f_i[n]/f_s$",
                )
                ax_phase.plot(n[::4], omega_i[::4], linestyle="", marker="o", ms=4.2, color=MODULATION_VIOLET_LIGHT)
            else:
                ax_phase.vlines(
                    n[::4],
                    0.0,
                    omega_i[::4],
                    color=OMEGA_STEM_COLOR,
                    lw=1.4,
                    alpha=0.72,
                    label=r"$\Omega_i[n]$",
                )
                ax_phase.plot(n[::4], omega_i[::4], linestyle="", marker="o", ms=3.2, color=OMEGA_STEM_COLOR, alpha=0.85)
            ax_phase.axhline(omega_c, color=REFERENCE_COLOR, lw=1.8, ls="--", label=r"$\Omega_c$")
            ax_phase.legend(loc="upper right", fontsize=LEGEND_SIZE, framealpha=0.95)
    else:
        ax_phi = ax_phase.twinx()

        ax_phase.vlines(
            n[::4],
            0.0,
            omega_i[::4],
            color=OMEGA_STEM_COLOR,
            lw=1.4,
            alpha=0.72,
            label=r"$\Omega_i[n]$",
        )
        ax_phase.plot(n[::4], omega_i[::4], linestyle="", marker="o", ms=3.2, color=OMEGA_STEM_COLOR, alpha=0.85)
        ax_phase.set_ylim(0.0, 0.72)
        ax_phase.set_yticks([0.0, omega_c, 0.7])
        ax_phase.set_yticklabels(["0", r"$\Omega_c$", "0.7"])
        ax_phase.set_ylabel(r"$\Omega_i[n]$ in rad/sample", fontsize=LABEL_SIZE)
        ax_phase.set_title("Accumulating discrete angular frequency", fontsize=TITLE_SIZE, pad=8)
        style_axis(ax_phase)

        ax_phi.plot(
            n,
            phi_fm,
            color=FM_PHASE_COLOR,
            lw=2.8,
            alpha=1.0,
            label=r"$\varphi_\mathrm{FM}[n]=\varphi_0+\sum_{k=0}^{n-1}\Omega_i[k]$",
        )
        ax_phi.plot(n[::4], phi_fm[::4], linestyle="", marker="o", ms=4.0, color=FM_PHASE_COLOR)
        ax_phi.set_ylim(0.0, 17.0 * np.pi)
        ax_phi.set_yticks([0, 4 * np.pi, 8 * np.pi, 12 * np.pi, 16 * np.pi])
        ax_phi.yaxis.set_major_formatter(FuncFormatter(phase_formatter))
        ax_phi.set_ylabel(r"$\varphi_\mathrm{FM}[n]$ in rad", fontsize=LABEL_SIZE, color=FM_PHASE_COLOR)
        ax_phi.tick_params(labelsize=TICK_SIZE, colors=FM_PHASE_COLOR)
        ax_phi.spines["top"].set_visible(False)
        ax_phi.spines["left"].set_visible(False)
        ax_phi.spines["right"].set_color("0.35")
        ax_phi.patch.set_alpha(0.0)
        ax_phase.legend(loc="upper left", fontsize=LEGEND_SIZE, framealpha=0.95)
        ax_phi.legend(loc="lower right", fontsize=LEGEND_SIZE, framealpha=0.95)

    ax_m.tick_params(labelbottom=False)
    ax_f.tick_params(labelbottom=False)
    ax_phase.set_xlabel("Sample index n", fontsize=LABEL_SIZE)

    path = OUTPUT_DIR / output_name
    fig.savefig(path, dpi=FIG_DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*.png"):
        old_file.unlink()

    saved_paths = [
        plot_series(1, "01_fm_derivation_modulator_m_n.png"),
        plot_series(2, "02_fm_derivation_instantaneous_frequency.png"),
        plot_series(3, "03_fm_derivation_discrete_angular_frequency_omega_i.png"),
        plot_series(4, "04_fm_derivation_omega_i_before_sum.png"),
        plot_series(5, "05_fm_derivation_accumulated_phase_phi_fm.png"),
        plot_series(5, "06_fm_derivation_triangle_accumulated_phase_phi_fm.png", modulator_kind="triangle"),
        plot_series(5, "07_fm_derivation_rectangle_accumulated_phase_phi_fm.png", modulator_kind="rectangle"),
    ]

    for path in saved_paths:
        print(path)


if __name__ == "__main__":
    main()
