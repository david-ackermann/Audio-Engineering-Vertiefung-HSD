from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "01_delay_phase_zeitbereich" / "01B_phasenfaktor_multiplikation"

DPI = 200
FIGSIZE = (11.2, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 23
TICK_SIZE = 17
SHOW_TITLES = False
SHOW_AXIS_LABELS = True
SHOW_ANNOTATIONS = False
SHOW_LEGEND = False

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
OUTPUT_BLUE = "#2b7bbb"
REFERENCE_GREY = "0.74"
LIGHT_GREY = "0.84"
FACTOR_ORANGE = "#d98c2f"

SAMPLE_INDEX = 1
DELAY_VALUES = (1, 2)

OMEGA_CASES = (
    ("dc", "DC", 0.0, r"$\Omega=0$"),
    ("half_nyquist", "Half Nyquist", 0.5 * np.pi, r"$\Omega=\pi/2$"),
    ("nyquist", "Nyquist", np.pi, r"$\Omega=\pi$"),
)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.rglob("*.png"):
        image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def phasor(angle: float) -> complex:
    return np.exp(1j * angle)


def pi_label_inner(value: float) -> str:
    ratio = value / np.pi
    if np.isclose(ratio, 0.0):
        return r"0"
    if np.isclose(ratio, -0.5):
        return r"-\pi/2"
    if np.isclose(ratio, -1.0):
        return r"-\pi"
    if np.isclose(ratio, -2.0):
        return r"-2\pi"
    if np.isclose(ratio, 0.5):
        return r"\pi/2"
    if np.isclose(ratio, 1.0):
        return r"\pi"
    return rf"{ratio:.2f}\pi"


def pi_label(value: float) -> str:
    return rf"${pi_label_inner(value)}$"


def setup_complex_axis(ax, title: str) -> None:
    if SHOW_TITLES:
        ax.set_title(title, fontsize=TITLE_SIZE, pad=12)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.35, 1.55)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_yticks([-1.0, 0.0, 1.0])
    if SHOW_AXIS_LABELS:
        ax.set_xlabel(r"Real part", fontsize=LABEL_SIZE)
        ax.set_ylabel(r"Imaginary part", fontsize=LABEL_SIZE)
    else:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    theta = np.linspace(0.0, 2.0 * np.pi, 720)
    ax.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.2, zorder=1)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.1, zorder=1)
    ax.axvline(0.0, color=SIGNAL_BLACK, lw=1.1, zorder=1)
    ax.grid(alpha=0.23)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE, length=3.5 if SHOW_AXIS_LABELS else 0)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def draw_arrow(ax, value: complex, *, color: str, label: str, alpha: float = 1.0, zorder: int = 4) -> None:
    ax.annotate(
        "",
        xy=(value.real, value.imag),
        xytext=(0.0, 0.0),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=3.2, mutation_scale=17, alpha=alpha),
        zorder=zorder,
    )
    ax.scatter(
        [value.real],
        [value.imag],
        s=100,
        color=color,
        edgecolor="white",
        linewidth=1.0,
        alpha=alpha,
        zorder=zorder + 1,
        label=label,
    )


def draw_rotation_arc(ax, start_angle: float, delta_angle: float) -> None:
    if np.isclose(delta_angle, 0.0):
        return

    radius = 1.13
    num_points = max(80, int(90 * abs(delta_angle) / np.pi))
    theta = np.linspace(start_angle, start_angle + delta_angle, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color=FACTOR_ORANGE, lw=2.5, alpha=0.95, zorder=2)

    arrow = FancyArrowPatch(
        (x[-2], y[-2]),
        (x[-1], y[-1]),
        arrowstyle="-|>",
        mutation_scale=15,
        color=FACTOR_ORANGE,
        lw=2.5,
        zorder=3,
    )
    ax.add_patch(arrow)

    label_angle = start_angle + 0.5 * delta_angle
    if SHOW_ANNOTATIONS:
        ax.text(
            1.23 * np.cos(label_angle),
            1.23 * np.sin(label_angle),
            pi_label(delta_angle),
            color=FACTOR_ORANGE,
            fontsize=18,
            ha="center",
            va="center",
        )


def add_factor_box(ax, *, delay: int, omega_label: str, factor_angle: float) -> None:
    text = "\n".join(
        (
            rf"$F_D(\Omega)=e^{{-jD\Omega}}$",
            rf"$D={delay}$, {omega_label}",
            rf"$|F_D|=1$",
            rf"$\arg(F_D)={pi_label_inner(factor_angle)}$",
        )
    )
    ax.text(
        1.48,
        -1.10,
        text,
        fontsize=15,
        ha="right",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="0.82", alpha=0.95),
        zorder=10,
    )


def add_legend(ax) -> None:
    legend = ax.legend(loc="upper right", fontsize=15, frameon=True, framealpha=0.92)
    legend.set_zorder(100)


def export_frame(
    figure_number: int,
    *,
    delay: int,
    key: str,
    title: str,
    omega: float,
    omega_label: str,
    step: int,
) -> None:
    factor_angle = -delay * omega
    input_angle = SAMPLE_INDEX * omega
    input_value = phasor(input_angle)
    factor_value = phasor(factor_angle)
    output_value = input_value * factor_value

    step_titles = {
        1: rf"$D={delay}$, {title}: input phasor",
        2: rf"$D={delay}$, {title}: phase factor",
        3: rf"$D={delay}$, {title}: $y[n]=e^{{-jD\Omega}}x[n]$",
    }

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.99, bottom=0.17, top=0.98)
    setup_complex_axis(ax, step_titles[step])

    draw_arrow(ax, input_value, color=SIGNAL_BLACK, label=r"$x[n]$", alpha=1.0 if step < 3 else 0.60, zorder=4)

    if step >= 2:
        draw_arrow(ax, factor_value, color=FACTOR_ORANGE, label=r"$e^{-jD\Omega}$", alpha=1.0, zorder=5)
        if SHOW_ANNOTATIONS:
            add_factor_box(ax, delay=delay, omega_label=omega_label, factor_angle=factor_angle)

    if step >= 3:
        draw_rotation_arc(ax, input_angle, factor_angle)
        draw_arrow(ax, output_value, color=OUTPUT_BLUE, label=r"$y[n]$", alpha=1.0, zorder=6)

    if SHOW_LEGEND:
        add_legend(ax)
    save_figure(fig, f"{figure_number:02d}_delay_d{delay}_{key}_step_{step:02d}.png")


def main() -> None:
    clear_output_dir()
    figure_number = 1
    for delay in DELAY_VALUES:
        for key, title, omega, omega_label in OMEGA_CASES:
            for step in (1, 2, 3):
                export_frame(
                    figure_number,
                    delay=delay,
                    key=key,
                    title=title,
                    omega=omega,
                    omega_label=omega_label,
                    step=step,
                )
                figure_number += 1
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
