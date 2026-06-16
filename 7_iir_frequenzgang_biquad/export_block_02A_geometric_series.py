from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "02_frequenzgang_iir" / "02A_geometric_series"

DPI = 200
FIGSIZE = (13.8, 5.2)
TITLE_SIZE = 18
SUPTITLE_SIZE = 22
LABEL_SIZE = 19
TICK_SIZE = 14

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
OUTPUT_BLUE = "#2b7bbb"
REFERENCE_GREY = "0.72"
LIMIT_RED = "#c44e52"

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


def plot_partial_stems(
    ax,
    indices: np.ndarray,
    values: np.ndarray,
    *,
    color: str,
    marker_size: float = 7.0,
    alpha: float = 1.0,
    line_width: float = 2.2,
    zorder: int = 3,
) -> None:
    if indices.size == 0:
        return
    ax.vlines(indices, 0.0, values, color=color, lw=line_width, alpha=alpha, zorder=zorder)
    ax.scatter(
        indices,
        values,
        s=marker_size**2,
        color=color,
        edgecolor="white",
        linewidth=0.9,
        zorder=zorder + 1,
        alpha=alpha,
    )


def style_terms_axis(ax, n_max: int) -> None:
    ax.set_xlim(-0.5, n_max + 0.5)
    ax.set_ylim(-0.04, 1.08)
    ax.set_xticks(np.arange(0, n_max + 1, 1))
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_xlabel("Term index n", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Term $q^n$", fontsize=LABEL_SIZE)
    ax.set_title(r"Terms of the series", fontsize=TITLE_SIZE, pad=12)
    ax.grid(alpha=0.22)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_sum_axis(ax, n_max: int, limit: float, *, show_limit: bool) -> None:
    ax.set_xlim(-0.5, n_max + 0.5)
    ax.set_ylim(-0.08, limit * 1.12)
    ax.set_xticks(np.arange(0, n_max + 1, 1))
    if show_limit:
        ax.set_yticks([0.0, 1.0, 2.0, 3.0, limit])
        ax.set_yticklabels(["0", "1", "2", "3", f"{limit:.2f}"])
    else:
        ax.set_yticks([0.0, 1.0, 2.0, 3.0])
        ax.set_yticklabels(["0", "1", "2", "3"])
    ax.set_xlabel("Last added term N", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Partial sum $S_N$", fontsize=LABEL_SIZE)
    ax.set_title(r"Partial sum approaches the limit", fontsize=TITLE_SIZE, pad=12)
    ax.grid(alpha=0.22)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    if show_limit:
        ax.axhline(limit, color=LIMIT_RED, lw=2.2, ls="--", zorder=1)
        ax.text(
            n_max - 0.1,
            limit + 0.08,
            rf"$S_\infty={limit:.2f}$",
            ha="right",
            va="bottom",
            fontsize=16,
            color=LIMIT_RED,
        )
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def add_frame_caption(fig, q: float, frame_index: int, partial_sum: float) -> None:
    fig.suptitle(
        rf"Geometric series for $q={q:.1f}$",
        fontsize=SUPTITLE_SIZE,
        y=0.97,
    )


def export_frame(q: float, n_max: int, frame_index: int, filename: str) -> None:
    n = np.arange(n_max + 1)
    terms = q**n
    partial_sums = np.cumsum(terms)
    limit = 1.0 / (1.0 - q)

    active = n <= frame_index
    previous = n < frame_index
    current = n == frame_index

    fig, (ax_terms, ax_sum) = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.17, top=0.78, wspace=0.30)
    add_frame_caption(fig, q, frame_index, partial_sums[frame_index])

    plot_partial_stems(
        ax_terms,
        n[previous],
        terms[previous],
        color=SYSTEM_GREEN,
        marker_size=7.2,
        alpha=0.65,
        line_width=2.2,
        zorder=3,
    )
    plot_partial_stems(
        ax_terms,
        n[current],
        terms[current],
        color=SYSTEM_GREEN,
        marker_size=10.5,
        line_width=3.0,
        zorder=5,
    )
    ax_terms.axvline(frame_index, color="0.35", lw=1.5, ls="--", zorder=2)
    style_terms_axis(ax_terms, n_max)

    if np.any(active):
        ax_sum.plot(n[active], partial_sums[active], color=OUTPUT_BLUE, lw=2.8, zorder=3)
        ax_sum.scatter(n[previous], partial_sums[previous], s=60, color=OUTPUT_BLUE, edgecolor="white", linewidth=0.9, zorder=4)
        ax_sum.scatter(
            n[current],
            partial_sums[current],
            s=120,
            color=OUTPUT_BLUE,
            edgecolor="white",
            linewidth=1.0,
            zorder=5,
        )
        ax_sum.text(
            0.97,
            0.08,
            rf"$S_{frame_index}={partial_sums[frame_index]:.3f}$",
            transform=ax_sum.transAxes,
            ha="right",
            va="bottom",
            fontsize=17,
            color=OUTPUT_BLUE,
        )
    ax_sum.axvline(frame_index, color="0.35", lw=1.5, ls="--", zorder=2)
    style_sum_axis(ax_sum, n_max, limit, show_limit=False)

    save_figure(fig, filename)


def export_limit_frame(q: float, n_max: int, filename: str) -> None:
    n = np.arange(n_max + 1)
    terms = q**n
    partial_sums = np.cumsum(terms)
    limit = 1.0 / (1.0 - q)

    fig, (ax_terms, ax_sum) = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.17, top=0.78, wspace=0.30)
    fig.suptitle(
        rf"Limit of the geometric series for $q={q:.1f}$",
        fontsize=SUPTITLE_SIZE,
        y=0.97,
    )

    plot_partial_stems(
        ax_terms,
        n,
        terms,
        color=SYSTEM_GREEN,
        marker_size=7.8,
        alpha=0.85,
        line_width=2.4,
        zorder=3,
    )
    style_terms_axis(ax_terms, n_max)

    ax_sum.plot(n, partial_sums, color=OUTPUT_BLUE, lw=2.8, zorder=3)
    ax_sum.scatter(n, partial_sums, s=68, color=OUTPUT_BLUE, edgecolor="white", linewidth=0.9, zorder=4)
    style_sum_axis(ax_sum, n_max, limit, show_limit=True)
    ax_sum.text(
        0.97,
        0.08,
        rf"$\sum_{{n=0}}^\infty q^n=\frac{{1}}{{1-q}}={limit:.3f}$",
        transform=ax_sum.transAxes,
        ha="right",
        va="bottom",
        fontsize=16,
        color=SIGNAL_BLACK,
    )

    save_figure(fig, filename)


def main() -> None:
    q = 0.7
    n_max = 14
    clear_output_dir()
    for frame_index in range(n_max + 1):
        export_frame(q, n_max, frame_index, f"{frame_index + 1:02d}_geometric_series_n_{frame_index:02d}.png")
    export_limit_frame(q, n_max, f"{n_max + 2:02d}_geometric_series_limit.png")
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
