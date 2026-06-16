from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "03_rekursives_iir_mehrere_taps" / "03C_ir_superposition"

DPI = 200
FIGSIZE = (10.5, 4.2)
TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
TERM_GREY = "0.72"

SOURCE_COLORS = (
    "#c45b4d",  # h[0]
    "#d98c2f",  # h[1]
    "#2b7bbb",  # h[2]
    "#7c6aa6",  # h[3]
    "#4b9a88",  # h[4]
    "#b35aa4",  # h[5]
    "#6f8f2a",  # h[6]
    "#4f6fb3",  # h[7]
)

B0 = 1.0
A_COEFFICIENTS = np.array([0.55, -0.12, 0.04, -0.01])
MAX_SAMPLE = 7

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
    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def impulse_response_samples() -> np.ndarray:
    h = np.zeros(MAX_SAMPLE + 1)
    for n in range(MAX_SAMPLE + 1):
        direct = B0 if n == 0 else 0.0
        feedback = 0.0
        for r, a_r in enumerate(A_COEFFICIENTS, start=1):
            if n - r >= 0:
                feedback -= a_r * h[n - r]
        h[n] = direct + feedback
    return h


def term_values(h: np.ndarray, delay: int) -> np.ndarray:
    values = np.zeros_like(h)
    if delay == 0:
        values[0] = B0
        return values

    a_r = A_COEFFICIENTS[delay - 1]
    values[delay:] = -a_r * h[: h.size - delay]
    return values


def sample_color(index: int) -> str:
    return SOURCE_COLORS[index % len(SOURCE_COLORS)]


def term_color(delay: int, sample_index: int) -> str:
    if delay == 0:
        return SOURCE_COLORS[0]
    source_index = sample_index - delay
    if source_index < 0:
        return TERM_GREY
    return sample_color(source_index)


def setup_axis(ax, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.55, MAX_SAMPLE + 0.65)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xticks(np.arange(0, MAX_SAMPLE + 1))
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    add_coefficient_label(ax)


def add_text_with_stroke(
    ax,
    x: float,
    y: float,
    text: str,
    *,
    color: str,
    fontsize: int,
    ha: str = "center",
    va: str = "center",
) -> None:
    label = ax.text(x, y, text, color=color, fontsize=fontsize, ha=ha, va=va)
    label.set_path_effects([path_effects.withStroke(linewidth=4, foreground="white")])


def add_coefficient_label(ax) -> None:
    coefficient_text = (
        rf"$M={A_COEFFICIENTS.size}$" + "\n"
        + rf"$b_0={B0:.1f}$" + "\n"
        + rf"$a_1={A_COEFFICIENTS[0]:+.2f}$" + "\n"
        + rf"$a_2={A_COEFFICIENTS[1]:+.2f}$" + "\n"
        + rf"$a_3={A_COEFFICIENTS[2]:+.2f}$" + "\n"
        + rf"$a_4={A_COEFFICIENTS[3]:+.2f}$"
    )
    label = ax.text(
        0.985,
        0.955,
        coefficient_text,
        transform=ax.transAxes,
        fontsize=12,
        color=SIGNAL_BLACK,
        ha="right",
        va="top",
        zorder=10,
    )
    label.set_path_effects([path_effects.withStroke(linewidth=3.0, foreground="white")])


def plot_single_stem(
    ax,
    x: float,
    y: float,
    *,
    color: str,
    marker_size: float,
    line_width: float,
    alpha: float = 1.0,
    zorder: int = 3,
) -> None:
    ax.vlines(x, 0.0, y, color=color, lw=line_width, alpha=alpha, zorder=zorder)
    ax.scatter(
        [x],
        [y],
        s=marker_size**2,
        color=color,
        edgecolor="white",
        linewidth=0.9,
        alpha=alpha,
        zorder=zorder + 1,
    )


def plot_colored_term(
    ax,
    values: np.ndarray,
    *,
    delay: int,
    x_offset: float = 0.0,
    alpha: float = 1.0,
    marker_size: float = 7.5,
    line_width: float = 2.6,
    zorder: int = 3,
) -> None:
    for n, value in enumerate(values):
        if np.isclose(value, 0.0):
            continue
        plot_single_stem(
            ax,
            n + x_offset,
            value,
            color=term_color(delay, n),
            marker_size=marker_size,
            line_width=line_width,
            alpha=alpha,
            zorder=zorder,
        )


def plot_impulse_response_reference(ax, h: np.ndarray) -> None:
    for n, value in enumerate(h):
        plot_single_stem(
            ax,
            float(n),
            value,
            color=sample_color(n),
            marker_size=7.0,
            line_width=2.1,
            alpha=0.42,
            zorder=2,
        )


def term_title(delay: int) -> str:
    if delay == 0:
        return r"Direct term: $b_0\delta[n]$"
    return rf"Weighted delayed IR: $-a_{delay}h[n-{delay}]$"


def export_term_frame(h: np.ndarray, delay: int, figure_number: int) -> None:
    term_count = A_COEFFICIENTS.size + 1
    offsets = np.linspace(-0.30, 0.30, term_count)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)

    for previous_delay in range(delay + 1):
        values = term_values(h, previous_delay)
        is_current = previous_delay == delay
        plot_colored_term(
            ax,
            values,
            delay=previous_delay,
            x_offset=float(offsets[previous_delay]),
            alpha=1.0 if is_current else 0.72,
            marker_size=8.3 if is_current else 6.2,
            line_width=3.0 if is_current else 1.9,
            zorder=5 if is_current else 3,
        )

    setup_axis(ax, term_title(delay))
    save_figure(fig, f"{figure_number:02d}_term_r{delay}.png")


def export_overlay_frame(h: np.ndarray, figure_number: int) -> None:
    term_count = A_COEFFICIENTS.size + 1
    offsets = np.linspace(-0.30, 0.30, term_count)
    terms = [term_values(h, delay) for delay in range(term_count)]
    reconstructed = np.sum(np.stack(terms), axis=0)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)

    for delay, (values, x_offset) in enumerate(zip(terms, offsets)):
        plot_colored_term(
            ax,
            values,
            delay=delay,
            x_offset=float(x_offset),
            alpha=0.72,
            marker_size=5.8,
            line_width=1.7,
            zorder=3,
        )

    for n, value in enumerate(reconstructed):
        plot_single_stem(
            ax,
            float(n),
            value,
            color=SYSTEM_GREEN,
            marker_size=10.0,
            line_width=3.4,
            alpha=1.0,
            zorder=6,
        )

    setup_axis(ax, "Superposition of weighted delayed impulse responses")
    save_figure(fig, f"{figure_number:02d}_superposition_result.png")


def main() -> None:
    clear_output_dir()
    h = impulse_response_samples()
    for figure_number, delay in enumerate(range(A_COEFFICIENTS.size + 1), start=1):
        export_term_frame(h, delay, figure_number)
    export_overlay_frame(h, A_COEFFICIENTS.size + 2)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
