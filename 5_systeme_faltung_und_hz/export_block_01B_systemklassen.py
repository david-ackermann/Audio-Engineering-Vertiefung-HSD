from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "01B_systemklassen"

DPI = 200
FIGSIZE_TALL = (12.0, 6.4)
FIGSIZE_DISTORTION = (12.0, 6.8)

TITLE_SIZE = 23
LABEL_SIZE = 17
SMALL_LABEL_SIZE = 14

SIGNAL_BLACK = "0.10"
COMPARE_ORANGE = "#d98c2f"
LFO_LIGHT_GREEN = "#8fd19e"
ACTIVE_RED = "crimson"
GRID_GREY = "0.75"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*"):
        if image_file.suffix.lower() in {".png", ".gif"}:
            image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def stem_sequence(ax, n: np.ndarray, values: np.ndarray, *, color: str) -> None:
    markerline, stemlines, baseline = ax.stem(n, values)
    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor("white")
    markerline.set_markeredgewidth(0.8)
    markerline.set_markersize(7)
    stemlines.set_color(color)
    stemlines.set_linewidth(2.4)
    baseline.set_color(SIGNAL_BLACK)
    baseline.set_linewidth(1.5)


def style_sequence_axis(ax, title: str) -> None:
    ax.set_xlim(-0.5, 31.5)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xticks([0, 8, 16, 24, 31])
    ax.set_yticks([-1, 0, 1])
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.set_title(title, fontsize=SMALL_LABEL_SIZE + 2, pad=8)
    ax.set_xlabel(r"$n$", fontsize=SMALL_LABEL_SIZE + 1)
    ax.tick_params(labelsize=SMALL_LABEL_SIZE - 1)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_lfo_gain_axis(ax, title: str) -> None:
    ax.set_xlim(-0.5, 15.5)
    ax.set_ylim(-0.05, 1.10)
    ax.set_xticks(np.arange(0, 16, 2))
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlabel("Sampleindex n", fontsize=LABEL_SIZE + 1)
    ax.set_ylabel("Gain", fontsize=LABEL_SIZE + 1)
    ax.tick_params(labelsize=SMALL_LABEL_SIZE + 3)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def export_ltv_lfo_gain_sequence() -> None:
    n = np.arange(16)
    g = 0.65 + 0.35 * np.sin(2.0 * np.pi * n / n.size)

    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.82)
    stem_sequence(ax, n, g, color=LFO_LIGHT_GREEN)
    style_lfo_gain_axis(ax, r"LFO-Gainfolge $g[n]$")

    save_figure(fig, "08_ltv_lfo_gainfolge.png")


def compact_discrete_trace(
    ax,
    n: np.ndarray,
    values: np.ndarray,
    *,
    color: str,
    label_text: str,
    baseline: float = 0.0,
) -> None:
    ax.vlines(n, baseline, values, color=color, lw=1.8, alpha=0.72)
    ax.plot(n, values, color=color, lw=2.3, alpha=0.95, label=label_text)
    ax.scatter(n, values, s=32, color=color, edgecolor="white", linewidth=0.75, zorder=3)


def sample_stem_trace(
    ax,
    n: np.ndarray,
    values: np.ndarray,
    *,
    color: str,
    label_text: str,
    baseline: float = 0.0,
) -> None:
    ax.vlines(n, baseline, values, color=color, lw=2.0, alpha=0.88, label=label_text)
    ax.scatter(n, values, s=34, color=color, edgecolor="white", linewidth=0.75, zorder=3)


def style_sidechain_axis(
    ax,
    ylabel: str,
    *,
    ylim: tuple[float, float],
    yticks: list[float],
    show_xlabel: bool = False,
) -> None:
    ax.set_xlim(-0.5, 63.5)
    ax.set_ylim(*ylim)
    ax.set_xticks(np.arange(0, 64, 8))
    ax.set_yticks(yticks)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    if show_xlabel:
        ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE + 1)
    else:
        ax.tick_params(labelbottom=False)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.1)
    ax.tick_params(labelsize=SMALL_LABEL_SIZE + 1)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def sidechain_signal(t: np.ndarray) -> np.ndarray:
    amplitude = (
        0.16
        + 0.78 * np.exp(-0.5 * ((t - 17) / 5.2) ** 2)
        + 0.58 * np.exp(-0.5 * ((t - 43) / 7.5) ** 2)
    )
    return amplitude * np.sin(2.0 * np.pi * 0.17 * t + 0.35)


def sidechain_compressor_sequences() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    n = np.arange(64)
    s = sidechain_signal(n)

    alpha = 0.88
    envelope = np.zeros_like(s)
    for index, value in enumerate(np.abs(s)):
        previous = envelope[index - 1] if index > 0 else 0.0
        envelope[index] = alpha * previous + (1.0 - alpha) * value

    threshold = 0.30
    ratio = 5.0
    gain = np.ones_like(envelope)
    active = envelope > threshold
    compressed_level = threshold + (envelope[active] - threshold) / ratio
    gain[active] = compressed_level / np.maximum(envelope[active], 1e-12)
    return n, s, envelope, gain, threshold


def export_ntv_sidechain_gain_sequence() -> None:
    n, s, envelope, gain, threshold = sidechain_compressor_sequences()
    t = np.linspace(0.0, 63.0, 1200)

    fig, axes = plt.subplots(3, 1, figsize=FIGSIZE_TALL, sharex=True)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.11, top=0.88, hspace=0.18)
    fig.suptitle(r"Sidechain compressor: $s[n] \rightarrow e_s[n] \rightarrow g_s[n]$", fontsize=TITLE_SIZE, fontweight="bold")

    axes[0].plot(t, sidechain_signal(t), color="0.68", lw=2.4, alpha=0.88)
    sample_stem_trace(axes[0], n, s, color=SIGNAL_BLACK, label_text=r"Sidechain signal $s[n]$")
    style_sidechain_axis(axes[0], r"$s[n]$", ylim=(-1.05, 1.05), yticks=[-1.0, 0.0, 1.0])
    axes[0].legend(loc="upper right", fontsize=SMALL_LABEL_SIZE, frameon=True, framealpha=0.95)

    compact_discrete_trace(axes[1], n, envelope, color=COMPARE_ORANGE, label_text=r"Envelope $e_s[n]$")
    axes[1].axhline(threshold, color=ACTIVE_RED, lw=1.8, ls="--", label="Threshold")
    style_sidechain_axis(axes[1], r"$e_s[n]$", ylim=(-0.04, 0.82), yticks=[0.0, threshold, 0.8])
    axes[1].legend(loc="upper right", fontsize=SMALL_LABEL_SIZE, frameon=True, framealpha=0.95)

    compact_discrete_trace(axes[2], n, gain, color=LFO_LIGHT_GREEN, label_text=r"time-varying gain $g_s[n]$")
    style_sidechain_axis(axes[2], r"$g_s[n]$", ylim=(0.45, 1.05), yticks=[0.5, 0.75, 1.0], show_xlabel=True)
    axes[2].legend(loc="lower right", fontsize=SMALL_LABEL_SIZE, frameon=True, framealpha=0.95)

    save_figure(fig, "09_ntv_sidechain_gainfolge.png")


def stem_lines(ax, positions: np.ndarray, heights: np.ndarray, *, color: str) -> None:
    ax.vlines(positions, 0.0, heights, color=color, lw=3.0)
    ax.scatter(positions, heights, s=42, color=color, edgecolor="white", linewidth=0.8, zorder=3)


def style_harmonic_axis(ax, title: str, labels: list[str]) -> None:
    ax.set_xlim(0.4, 7.6)
    ax.set_ylim(0.0, 1.08)
    ax.set_xticks(np.arange(1, 8))
    ax.set_xticklabels(labels)
    ax.set_yticks([])
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.4)
    ax.set_title(title, fontsize=SMALL_LABEL_SIZE + 1, pad=8)
    ax.tick_params(labelsize=SMALL_LABEL_SIZE - 1)
    for spine in ("left", "top", "right"):
        ax.spines[spine].set_visible(False)


def export_nls_clipped_sine_sequence() -> None:
    n = np.arange(32)
    sine = 0.95 * np.sin(2.0 * np.pi * 1.25 * n / n.size + 0.20)
    clip_level = 0.55
    clipped = np.clip(sine, -clip_level, clip_level)

    fig = plt.figure(figsize=FIGSIZE_DISTORTION)
    fig.patch.set_facecolor("white")

    input_ax = fig.add_axes([0.07, 0.58, 0.27, 0.28])
    output_ax = fig.add_axes([0.66, 0.58, 0.27, 0.28])
    input_spec_ax = fig.add_axes([0.11, 0.18, 0.19, 0.18])
    output_spec_ax = fig.add_axes([0.70, 0.18, 0.19, 0.18])
    overlay = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    overlay.set_xlim(0.0, 1.0)
    overlay.set_ylim(0.0, 1.0)
    overlay.patch.set_alpha(0.0)
    overlay.axis("off")

    stem_sequence(input_ax, n, sine, color=ACTIVE_RED)
    style_sequence_axis(input_ax, "Input: sine sequence")

    stem_sequence(output_ax, n, clipped, color=ACTIVE_RED)
    output_ax.axhline(clip_level, color=GRID_GREY, lw=1.1, ls="--")
    output_ax.axhline(-clip_level, color=GRID_GREY, lw=1.1, ls="--")
    style_sequence_axis(output_ax, "Output: clipped sequence")

    harmonic_labels = [r"$f_0$", "2", "3", "4", "5", "6", "7"]
    stem_lines(input_spec_ax, np.array([1]), np.array([1.0]), color=ACTIVE_RED)
    style_harmonic_axis(input_spec_ax, "idealized spectrum", harmonic_labels)

    stem_lines(output_spec_ax, np.array([1, 3, 5, 7]), np.array([1.0, 0.42, 0.24, 0.15]), color=ACTIVE_RED)
    style_harmonic_axis(output_spec_ax, "additional harmonics", harmonic_labels)

    block_x, block_y, block_w, block_h = 0.43, 0.62, 0.14, 0.095
    overlay.add_patch(Rectangle((block_x, block_y), block_w, block_h, facecolor="0.90", edgecolor=SIGNAL_BLACK, linewidth=1.8))
    curve_x = np.linspace(-1.0, 1.0, 120)
    curve_y = np.clip(1.45 * curve_x, -0.58, 0.58)
    curve_px = block_x + 0.18 * block_w + (curve_x + 1.0) / 2.0 * 0.64 * block_w
    curve_py = block_y + 0.18 * block_h + (curve_y + 0.75) / 1.50 * 0.64 * block_h
    overlay.plot([block_x + 0.18 * block_w, block_x + 0.82 * block_w], [block_y + 0.50 * block_h, block_y + 0.50 * block_h], color="0.55", lw=1.0)
    overlay.plot([block_x + 0.50 * block_w, block_x + 0.50 * block_w], [block_y + 0.18 * block_h, block_y + 0.82 * block_h], color="0.55", lw=1.0)
    overlay.plot(curve_px, curve_py, color=ACTIVE_RED, lw=2.0)
    overlay.annotate("", xy=(block_x, block_y + block_h / 2), xytext=(0.35, block_y + block_h / 2), arrowprops=dict(arrowstyle="->", lw=2.2, color=SIGNAL_BLACK))
    overlay.annotate("", xy=(0.65, block_y + block_h / 2), xytext=(block_x + block_w, block_y + block_h / 2), arrowprops=dict(arrowstyle="->", lw=2.2, color=SIGNAL_BLACK))

    save_figure(fig, "07_nls_sinus_clipping_folge.png")


def main() -> None:
    clear_output_dir()
    export_nls_clipped_sine_sequence()
    export_ltv_lfo_gain_sequence()
    export_ntv_sidechain_gain_sequence()


if __name__ == "__main__":
    main()
