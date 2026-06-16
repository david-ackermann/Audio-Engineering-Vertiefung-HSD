from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "03_rekursives_iir_mehrere_taps" / "03B_impulse_response_build"

DPI = 200
FIGSIZE = (10.5, 4.2)
TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"

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


@dataclass(frozen=True)
class Contribution:
    source_index: int | None
    value: float
    label: str
    color: str


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


def contributions_for_sample(h: np.ndarray, n: int) -> list[Contribution]:
    if n == 0:
        return [
            Contribution(
                source_index=None,
                value=B0,
                label=r"$b_0\delta[0]$",
                color=SOURCE_COLORS[0],
            )
        ]

    contributions: list[Contribution] = []
    for r, a_r in enumerate(A_COEFFICIENTS, start=1):
        source_index = n - r
        if source_index < 0:
            continue
        contributions.append(
            Contribution(
                source_index=source_index,
                value=-a_r * h[source_index],
                label=rf"$-a_{r}h[{source_index}]$",
                color=SOURCE_COLORS[source_index],
            )
        )
    return contributions


def offsets(count: int) -> np.ndarray:
    if count == 1:
        return np.array([-0.16])
    if count == 2:
        return np.array([-0.22, 0.22])
    if count == 3:
        return np.array([-0.30, -0.12, 0.18])
    if count == 4:
        return np.array([-0.34, -0.16, 0.16, 0.34])
    return np.linspace(-0.34, 0.34, count)


def plot_stem(
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


def add_text_with_stroke(ax, x: float, y: float, text: str, *, color: str, fontsize: int, ha: str = "center", va: str = "center") -> None:
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


def setup_axis(ax, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.55, MAX_SAMPLE + 0.65)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xticks(np.arange(0, MAX_SAMPLE + 1))
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Amplitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    add_coefficient_label(ax)


def equation_for_sample(h: np.ndarray, n: int) -> str:
    if n == 0:
        return rf"$h[0]=b_0={h[n]:.2f}$"
    terms = "".join(rf"-a_{r}h[{n-r}]" for r in range(1, min(len(A_COEFFICIENTS), n) + 1))
    return rf"$h[{n}]={terms}={h[n]:.2f}$"


def export_sample_frame(h: np.ndarray, n: int, figure_number: int) -> None:
    contributions = contributions_for_sample(h, n)
    sample_color = SOURCE_COLORS[n]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    setup_axis(ax, equation_for_sample(h, n))

    for previous in range(n):
        plot_stem(
            ax,
            float(previous),
            h[previous],
            color=SOURCE_COLORS[previous],
            marker_size=6.0,
            line_width=2.0,
            alpha=0.58,
            zorder=2,
        )
        previous_label_y = h[previous] + (0.075 if h[previous] >= 0.0 else -0.075)
        previous_label_va = "bottom" if h[previous] >= 0.0 else "top"
        add_text_with_stroke(
            ax,
            previous,
            previous_label_y,
            rf"$h[{previous}]$",
            color=SOURCE_COLORS[previous],
            fontsize=13,
            va=previous_label_va,
        )

    for contribution, x_offset in zip(contributions, offsets(len(contributions))):
        x_position = n + x_offset
        plot_stem(
            ax,
            x_position,
            contribution.value,
            color=contribution.color,
            marker_size=7.0,
            line_width=2.5,
            alpha=0.90,
            zorder=3,
        )
        if n == 0:
            add_text_with_stroke(
                ax,
                x_position,
                contribution.value + 0.065,
                contribution.label,
                color=contribution.color,
                fontsize=13,
                va="bottom",
            )

    plot_stem(
        ax,
        float(n),
        h[n],
        color=sample_color,
        marker_size=10.5,
        line_width=3.8,
        alpha=1.0,
        zorder=5,
    )
    current_label_y = h[n] + (0.10 if h[n] >= 0.0 else -0.10)
    current_label_va = "bottom" if h[n] >= 0.0 else "top"
    add_text_with_stroke(
        ax,
        n + 0.12,
        current_label_y,
        rf"$h[{n}]$",
        color=sample_color,
        fontsize=16,
        ha="left",
        va=current_label_va,
    )
    ax.axvline(n, color="0.35", lw=1.6, ls="--", zorder=3)

    filename_stem = "direct_b0" if n == 0 else f"sample_h{n}"
    save_figure(fig, f"{figure_number:02d}_{filename_stem}.png")


def export_result_frame(h: np.ndarray, figure_number: int) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    setup_axis(ax, rf"Result: impulse response samples, $M={A_COEFFICIENTS.size}$")

    for n, value in enumerate(h):
        plot_stem(
            ax,
            float(n),
            value,
            color=SYSTEM_GREEN,
            marker_size=9.5,
            line_width=3.2,
            alpha=1.0,
            zorder=4,
        )

    save_figure(fig, f"{figure_number:02d}_resulting_impulse_response.png")


def main() -> None:
    clear_output_dir()
    h = impulse_response_samples()
    for figure_number, n in enumerate(range(MAX_SAMPLE + 1), start=1):
        export_sample_frame(h, n, figure_number)
    export_result_frame(h, MAX_SAMPLE + 2)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
