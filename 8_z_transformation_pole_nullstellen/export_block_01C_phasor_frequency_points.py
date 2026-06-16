from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "01_delay_phase_zeitbereich" / "01C_phasor_kreisfrequenz"

DPI = 200
FIGSIZE = (11.2, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 23
TICK_SIZE = 17
SHOW_TITLES = False
SHOW_AXIS_LABELS = True

SIGNAL_BLACK = "0.10"
LIGHT_GREY = "0.84"

OMEGA_CASES = (
    ("dc", 0.0),
    ("half_nyquist", 0.5 * np.pi),
    ("nyquist", np.pi),
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


def draw_phasor(ax, omega: float) -> None:
    value = np.exp(1j * omega)
    ax.annotate(
        "",
        xy=(value.real, value.imag),
        xytext=(0.0, 0.0),
        arrowprops=dict(arrowstyle="-|>", color=SIGNAL_BLACK, lw=3.2, mutation_scale=17),
        zorder=4,
    )
    ax.scatter(
        [value.real],
        [value.imag],
        s=100,
        color=SIGNAL_BLACK,
        edgecolor="white",
        linewidth=1.0,
        zorder=5,
    )


def draw_phase_arc(ax, omega: float) -> None:
    radius = 1.13
    if np.isclose(omega, 0.0):
        ax.scatter([radius], [0.0], s=38, color=SIGNAL_BLACK, zorder=6)
        return

    num_points = max(80, int(90 * abs(omega) / np.pi))
    theta = np.linspace(0.0, omega, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color=SIGNAL_BLACK, lw=2.5, alpha=0.95, zorder=2)
    arrow = FancyArrowPatch(
        (x[-2], y[-2]),
        (x[-1], y[-1]),
        arrowstyle="-|>",
        mutation_scale=15,
        color=SIGNAL_BLACK,
        lw=2.5,
        zorder=3,
    )
    ax.add_patch(arrow)


def export_frame(figure_number: int, key: str, omega: float) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.99, bottom=0.17, top=0.98)
    setup_complex_axis(ax, key.replace("_", " "))
    draw_phase_arc(ax, omega)
    draw_phasor(ax, omega)
    save_figure(fig, f"{figure_number:02d}_{key}_phasor.png")


def main() -> None:
    clear_output_dir()
    for figure_number, (key, omega) in enumerate(OMEGA_CASES, start=1):
        export_frame(figure_number, key, omega)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
