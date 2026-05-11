from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_hausaufgaben"
)

DPI = 200
FIGSIZE = (13.0, 4.8)

TITLE_SIZE = 22
LABEL_SIZE = 20
TICK_SIZE = 17

SIGNAL_BLUE = "#2b7bbb"
SIGNAL_LIGHT_BLUE = "#bddcf3"
WINDOW_GREEN = "#66b77a"
CLICK_RED = "#cc3d3d"
GRID_GREY = "0.78"
INACTIVE_GREY = "0.86"

TASK3_WINDOW_LENGTH = 512
TASK3_HOP_SIZE = 128
TASK3_N_WINDOWS = 4

TASK4_WINDOW_LENGTH = 16
TASK4_HOP_SIZE = 8
TASK4_N_WINDOWS = 5
TASK4_CLICK_INDEX = 20


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def hann_shape(local_index: np.ndarray, window_length: int) -> np.ndarray:
    return np.sin(np.pi * local_index / (window_length - 1)) ** 2


def draw_sample_grid(ax, xmin: int, xmax: int, step: int = 1) -> None:
    for n in range(xmin, xmax + 1, step):
        ax.axvline(n, color=INACTIVE_GREY, lw=0.7, alpha=0.55, zorder=0)


def style_task3_axis(ax, title: str) -> None:
    last_start = (TASK3_N_WINDOWS - 1) * TASK3_HOP_SIZE
    xmax = last_start + TASK3_WINDOW_LENGTH - 1
    starts = np.arange(TASK3_N_WINDOWS) * TASK3_HOP_SIZE
    stops = starts + TASK3_WINDOW_LENGTH - 1
    ax.axhline(0.0, color=GRID_GREY, lw=1.0, zorder=0)
    ax.set_xlim(-20, xmax + 20)
    ax.set_ylim(-0.12, 1.18)
    ax.set_xticks(np.unique(np.r_[starts, stops]))
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlabel(r"Sample index $n$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Window amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_task4_axis(ax, title: str) -> None:
    xmax = (TASK4_N_WINDOWS - 1) * TASK4_HOP_SIZE + TASK4_WINDOW_LENGTH - 1
    ax.axhline(0.0, color=GRID_GREY, lw=1.0, zorder=0)
    ax.set_xlim(-1, xmax + 1)
    ax.set_ylim(-0.18, 1.35)
    ax.set_xticks(np.arange(0, xmax + 1, 4))
    ax.set_yticks([0.0, 1.0])
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlabel(r"Sample index $n$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Window / click", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def export_task3_sketch() -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.20, top=0.84)

    last_start = (TASK3_N_WINDOWS - 1) * TASK3_HOP_SIZE
    xmax = last_start + TASK3_WINDOW_LENGTH - 1
    draw_sample_grid(ax, 0, xmax, step=TASK3_HOP_SIZE)
    draw_sample_grid(ax, TASK3_WINDOW_LENGTH - 1, xmax, step=TASK3_HOP_SIZE)

    local_dense = np.linspace(0, TASK3_WINDOW_LENGTH - 1, 900)

    for m in range(TASK3_N_WINDOWS):
        start = m * TASK3_HOP_SIZE
        color = SIGNAL_BLUE if m % 2 == 0 else WINDOW_GREEN
        dense_n = start + local_dense
        dense_w = hann_shape(local_dense, TASK3_WINDOW_LENGTH)

        ax.plot(dense_n, dense_w, color=color, lw=2.6, alpha=0.92, zorder=2)
        ax.plot([start, start], [-0.045, 0.0], color=color, lw=2.0, zorder=4)
        ax.plot([start + TASK3_WINDOW_LENGTH - 1, start + TASK3_WINDOW_LENGTH - 1], [-0.045, 0.0], color=color, lw=2.0, zorder=4)
        ax.text(start + 0.5 * (TASK3_WINDOW_LENGTH - 1), 1.04, chr(ord("A") + m), color=color, fontsize=LABEL_SIZE, ha="center")

    style_task3_axis(ax, "Aufgabe 3: STFT-Parameter aus einer Fenster-Skizze bestimmen")
    fig.savefig(OUTPUT_DIR / "03_aufgabe_stft_parameter_fenster_skizze.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def export_task3_solution_sketch() -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.20, top=0.84)

    last_start = (TASK3_N_WINDOWS - 1) * TASK3_HOP_SIZE
    xmax = last_start + TASK3_WINDOW_LENGTH - 1
    draw_sample_grid(ax, 0, xmax, step=TASK3_HOP_SIZE)
    draw_sample_grid(ax, TASK3_WINDOW_LENGTH - 1, xmax, step=TASK3_HOP_SIZE)

    local_dense = np.linspace(0, TASK3_WINDOW_LENGTH - 1, 900)

    for m in range(TASK3_N_WINDOWS):
        start = m * TASK3_HOP_SIZE
        color = SIGNAL_BLUE if m % 2 == 0 else WINDOW_GREEN
        dense_n = start + local_dense
        dense_w = hann_shape(local_dense, TASK3_WINDOW_LENGTH)

        ax.plot(dense_n, dense_w, color=color, lw=2.6, alpha=0.92, zorder=2)
        ax.text(start + 0.5 * (TASK3_WINDOW_LENGTH - 1), 1.04, chr(ord("A") + m), color=color, fontsize=LABEL_SIZE, ha="center")

    # The solution sketch is kept separate from the task figure.
    ax.annotate(
        "",
        xy=(0, 0.10),
        xytext=(TASK3_WINDOW_LENGTH - 1, 0.10),
        arrowprops=dict(arrowstyle="<->", lw=2.0, color=SIGNAL_BLUE),
        annotation_clip=False,
    )
    ax.text(
        (TASK3_WINDOW_LENGTH - 1) / 2,
        0.135,
        r"$N=512$",
        color=SIGNAL_BLUE,
        fontsize=LABEL_SIZE,
        ha="center",
        va="bottom",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5),
    )

    ax.annotate(
        "",
        xy=(0, 0.92),
        xytext=(TASK3_HOP_SIZE, 0.92),
        arrowprops=dict(arrowstyle="<->", lw=2.0, color=WINDOW_GREEN),
        annotation_clip=False,
    )
    ax.text(
        TASK3_HOP_SIZE / 2,
        0.955,
        r"$H=128$",
        color=WINDOW_GREEN,
        fontsize=LABEL_SIZE,
        ha="center",
        va="bottom",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5),
    )

    ax.annotate(
        "",
        xy=(TASK3_HOP_SIZE, 0.78),
        xytext=(TASK3_WINDOW_LENGTH - 1, 0.78),
        arrowprops=dict(arrowstyle="<->", lw=2.0, color=SIGNAL_LIGHT_BLUE),
        annotation_clip=False,
    )
    ax.text(
        (TASK3_HOP_SIZE + TASK3_WINDOW_LENGTH - 1) / 2,
        0.815,
        r"overlap: $N-H=384$",
        color=SIGNAL_BLUE,
        fontsize=LABEL_SIZE - 2,
        ha="center",
        va="bottom",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5),
    )

    style_task3_axis(ax, "Aufgabe 3: Musterloesung zur Fenster-Skizze")
    fig.savefig(OUTPUT_DIR / "03_loesung_stft_parameter_fenster_skizze.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def draw_rectangular_stft_windows(ax, *, annotate_solution: bool = False) -> None:
    colors = [SIGNAL_BLUE, WINDOW_GREEN, SIGNAL_BLUE, WINDOW_GREEN, SIGNAL_BLUE]
    for m in range(TASK4_N_WINDOWS):
        start = m * TASK4_HOP_SIZE
        stop = start + TASK4_WINDOW_LENGTH - 1
        color = colors[m]
        ax.fill_between([start, stop], 0.0, 1.0, color=color, alpha=0.16, step="post", zorder=1)
        ax.plot([start, start, stop, stop], [0, 1, 1, 0], color=color, lw=2.4, zorder=2)
        ax.scatter([start, stop], [0, 0], s=44, color=color, edgecolor="white", linewidth=0.7, zorder=3)
        ax.text((start + stop) / 2, 1.05, rf"$m={m}$", color=color, fontsize=LABEL_SIZE - 2, ha="center")

    ax.vlines(TASK4_CLICK_INDEX, 0.0, 1.22, color=CLICK_RED, lw=2.8, zorder=4)
    ax.scatter([TASK4_CLICK_INDEX], [1.22], s=70, color=CLICK_RED, edgecolor="white", linewidth=0.8, zorder=5)
    ax.text(TASK4_CLICK_INDEX, 1.27, r"$n_c=20$", color=CLICK_RED, fontsize=LABEL_SIZE - 2, ha="center")

    if annotate_solution:
        ax.annotate(
            r"local $n=12$",
            xy=(TASK4_CLICK_INDEX, 0.82),
            xytext=(13.5, 0.55),
            arrowprops=dict(arrowstyle="->", lw=1.8, color=SIGNAL_BLUE),
            color=SIGNAL_BLUE,
            fontsize=LABEL_SIZE - 3,
            ha="center",
        )
        ax.annotate(
            r"local $n=4$",
            xy=(TASK4_CLICK_INDEX, 0.70),
            xytext=(26.5, 0.47),
            arrowprops=dict(arrowstyle="->", lw=1.8, color=WINDOW_GREEN),
            color=WINDOW_GREEN,
            fontsize=LABEL_SIZE - 3,
            ha="center",
        )


def export_task4_sketch() -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.20, top=0.84)
    xmax = (TASK4_N_WINDOWS - 1) * TASK4_HOP_SIZE + TASK4_WINDOW_LENGTH - 1
    draw_sample_grid(ax, 0, xmax, step=1)
    draw_rectangular_stft_windows(ax)
    style_task4_axis(ax, "Aufgabe 4: Lokaler Analyseblock eines Klicks")
    fig.savefig(OUTPUT_DIR / "04_aufgabe_klick_stft_fenster_skizze.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def export_task4_solution_sketch() -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.20, top=0.84)
    xmax = (TASK4_N_WINDOWS - 1) * TASK4_HOP_SIZE + TASK4_WINDOW_LENGTH - 1
    draw_sample_grid(ax, 0, xmax, step=1)
    draw_rectangular_stft_windows(ax, annotate_solution=True)
    style_task4_axis(ax, "Aufgabe 4: Musterloesung zur Klick-Position")
    fig.savefig(OUTPUT_DIR / "04_loesung_klick_stft_fenster_skizze.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def main() -> None:
    clear_output_dir()
    export_task3_sketch()
    export_task3_solution_sketch()
    export_task4_sketch()
    export_task4_solution_sketch()
    print(f"PNG storyboard exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
