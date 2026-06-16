from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = (
    OUTPUT_ROOT
    / "05_feedforward_dirac_baustein"
    / "05A_shifted_dirac_fir_term"
)

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
LIGHT_GREY = "0.75"
DARK_GREY = "0.35"
BLUE = "#2b7bbb"

OMEGA = np.pi / 4.0
MAX_DELAY = 6
NUM_SAMPLES = 8

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


def complex_sample(sample_index: int) -> complex:
    return np.exp(-1j * OMEGA * sample_index)


def style_common_axis(ax) -> None:
    ax.grid(alpha=0.22)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def plot_dirac_axis(ax, delay: int) -> None:
    samples = np.arange(NUM_SAMPLES)
    values = np.zeros(NUM_SAMPLES)
    values[delay] = 1.0

    ax.scatter(samples, np.zeros_like(samples), s=58, color=LIGHT_GREY, zorder=2)
    ax.vlines(delay, 0.0, 1.0, color=SYSTEM_GREEN, lw=4.0, zorder=4)
    ax.scatter(
        [delay],
        [1.0],
        s=130,
        color=SYSTEM_GREEN,
        edgecolor="white",
        linewidth=1.2,
        zorder=5,
    )
    ax.axvline(delay, color=DARK_GREY, lw=1.6, ls="--", zorder=1)

    ax.set_title(rf"Shifted Dirac impulse, $k={delay}$", fontsize=TITLE_SIZE, pad=12)
    ax.set_xlim(-0.5, NUM_SAMPLES - 0.5)
    ax.set_ylim(-0.08, 1.18)
    ax.set_xticks(samples)
    ax.set_yticks([0.0, 1.0])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$\delta[n-k]$", fontsize=LABEL_SIZE)
    ax.text(
        delay,
        1.08,
        rf"$n=k={delay}$",
        color=SYSTEM_GREEN,
        fontsize=18,
        ha="center",
        va="bottom",
    )
    style_common_axis(ax)


def plot_unit_circle_axis(ax, delay: int, *, show_history: bool = True) -> None:
    angles = np.linspace(0.0, 2.0 * np.pi, 512)
    ax.plot(np.cos(angles), np.sin(angles), color=LIGHT_GREY, lw=1.6, zorder=1)
    ax.axhline(0.0, color=DARK_GREY, lw=1.0, zorder=1)
    ax.axvline(0.0, color=DARK_GREY, lw=1.0, zorder=1)

    sample_indices = np.arange(NUM_SAMPLES)
    all_samples = np.exp(-1j * OMEGA * sample_indices)
    ax.scatter(
        all_samples.real,
        all_samples.imag,
        s=58,
        color=LIGHT_GREY,
        edgecolor="white",
        linewidth=0.8,
        zorder=2,
    )

    if show_history and delay > 0:
        previous_indices = np.arange(delay)
        previous_samples = np.exp(-1j * OMEGA * previous_indices)
        ax.scatter(
            previous_samples.real,
            previous_samples.imag,
            s=74,
            color=DARK_GREY,
            edgecolor="white",
            linewidth=0.8,
            zorder=3,
        )

    selected = complex_sample(delay)
    ax.arrow(
        0.0,
        0.0,
        selected.real * 0.88,
        selected.imag * 0.88,
        color=SYSTEM_GREEN,
        width=0.012,
        head_width=0.075,
        length_includes_head=True,
        zorder=5,
    )
    ax.scatter(
        [selected.real],
        [selected.imag],
        s=145,
        color=SYSTEM_GREEN,
        edgecolor="white",
        linewidth=1.2,
        zorder=6,
    )

    label_x = selected.real * 1.14
    label_y = selected.imag * 1.14
    ax.text(
        label_x,
        label_y,
        rf"$e^{{-j{delay}\Omega}}$",
        color=SYSTEM_GREEN,
        fontsize=18,
        ha="center",
        va="center",
    )

    for n, value in enumerate(all_samples[: MAX_DELAY + 1]):
        if n == delay:
            continue
        ax.text(
            value.real * 1.08,
            value.imag * 1.08,
            rf"$n={n}$",
            color="0.45",
            fontsize=11,
            ha="center",
            va="center",
        )

    ax.set_title("Selected complex value", fontsize=TITLE_SIZE, pad=12)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.32, 1.32)
    ax.set_ylim(-1.32, 1.32)
    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel("Real part", fontsize=LABEL_SIZE)
    ax.set_ylabel("Imaginary part", fontsize=LABEL_SIZE)
    style_common_axis(ax)


def export_intro_frame() -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.96, bottom=0.18, top=0.82)

    sample_indices = np.arange(NUM_SAMPLES)
    samples = np.exp(-1j * OMEGA * sample_indices)
    angles = np.linspace(0.0, 2.0 * np.pi, 512)

    ax.plot(np.cos(angles), np.sin(angles), color=LIGHT_GREY, lw=1.8, zorder=1)
    ax.axhline(0.0, color=DARK_GREY, lw=1.0, zorder=1)
    ax.axvline(0.0, color=DARK_GREY, lw=1.0, zorder=1)
    ax.plot(samples.real, samples.imag, color=BLUE, lw=2.0, alpha=0.45, zorder=2)
    ax.scatter(
        samples.real,
        samples.imag,
        s=95,
        color=BLUE,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
    )
    for n, value in enumerate(samples):
        ax.text(
            value.real * 1.12,
            value.imag * 1.12,
            rf"$n={n}$",
            fontsize=14,
            color=SIGNAL_BLACK,
            ha="center",
            va="center",
        )

    ax.set_title(r"Complex test sequence $e^{-j\Omega n}$", fontsize=TITLE_SIZE, pad=14)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.32, 1.32)
    ax.set_ylim(-1.32, 1.32)
    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel("Real part", fontsize=LABEL_SIZE)
    ax.set_ylabel("Imaginary part", fontsize=LABEL_SIZE)
    style_common_axis(ax)
    save_figure(fig, "01_complex_test_sequence.png")


def export_delay_frame(delay: int, frame_number: int) -> None:
    fig, (ax_left, ax_right) = plt.subplots(
        1,
        2,
        figsize=FIGSIZE,
        gridspec_kw={"width_ratios": [1.25, 1.0]},
    )
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.78, wspace=0.28)
    fig.text(
        0.5,
        0.947,
        rf"$\sum_n \delta[n-k]e^{{-j\Omega n}}=e^{{-jk\Omega}}$",
        fontsize=15,
        ha="center",
        va="center",
    )

    plot_dirac_axis(ax_left, delay)
    plot_unit_circle_axis(ax_right, delay)

    save_figure(fig, f"{frame_number:02d}_k{delay}_dirac_selects_complex_sample.png")


def export_summary_frame(frame_number: int) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.96, bottom=0.18, top=0.72)
    fig.text(
        0.5,
        0.945,
        "Shifted Dirac copies create FIR phase factors",
        fontsize=22,
        ha="center",
        va="center",
    )
    fig.text(
        0.5,
        0.86,
        r"$\sum_n \delta[n-k]e^{-j\Omega n}=e^{-jk\Omega}$",
        fontsize=17,
        ha="center",
        va="center",
    )

    angles = np.linspace(0.0, 2.0 * np.pi, 512)
    ax.plot(np.cos(angles), np.sin(angles), color=LIGHT_GREY, lw=1.8, zorder=1)
    ax.axhline(0.0, color=DARK_GREY, lw=1.0, zorder=1)
    ax.axvline(0.0, color=DARK_GREY, lw=1.0, zorder=1)

    for delay in range(MAX_DELAY + 1):
        value = complex_sample(delay)
        ax.arrow(
            0.0,
            0.0,
            value.real * 0.86,
            value.imag * 0.86,
            color=SYSTEM_GREEN,
            alpha=0.55 if delay < MAX_DELAY else 1.0,
            width=0.008,
            head_width=0.06,
            length_includes_head=True,
            zorder=3,
        )
        ax.scatter(
            [value.real],
            [value.imag],
            s=95,
            color=SYSTEM_GREEN,
            edgecolor="white",
            linewidth=1.0,
            alpha=0.70 if delay < MAX_DELAY else 1.0,
            zorder=4,
        )
        ax.text(
            value.real * 1.13,
            value.imag * 1.13,
            rf"$k={delay}$",
            fontsize=13,
            color=SIGNAL_BLACK,
            ha="center",
            va="center",
        )

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.32, 1.32)
    ax.set_ylim(-1.32, 1.32)
    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel("Real part", fontsize=LABEL_SIZE)
    ax.set_ylabel("Imaginary part", fontsize=LABEL_SIZE)
    style_common_axis(ax)
    save_figure(fig, f"{frame_number:02d}_dirac_terms_summary.png")


def main() -> None:
    clear_output_dir()
    export_intro_frame()
    for frame_number, delay in enumerate(range(MAX_DELAY + 1), start=2):
        export_delay_frame(delay, frame_number)
    export_summary_frame(MAX_DELAY + 3)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
