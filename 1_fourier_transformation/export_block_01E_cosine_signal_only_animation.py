from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import MultipleLocator

import storyboard_paths as paths


OUTPUT_DIR = paths.PHASOR_INTRO_DIR
GIF_PATH = OUTPUT_DIR / "cosine_signal_only.gif"
PREVIEW_T0_PATH = OUTPUT_DIR / "cosine_signal_only_preview_t0.png"
PREVIEW_PATH = OUTPUT_DIR / "cosine_signal_only_preview.png"

FPS = 12
FRAMES = 120
OMEGA = 1.0
T_END = 6.0 * np.pi
FIGSIZE = (13.5, 6.1)
FIG_DPI = 100
COS_COLOR = "tab:blue"
TITLE_SIZE = 18
LABEL_SIZE = 15
TICK_SIZE = 12


def build_animation():
    output_times = np.linspace(0.0, T_END, FRAMES)
    dense_times = np.linspace(0.0, T_END, 900)
    cos_values = np.cos(OMEGA * dense_times)

    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.2])
    ax_complex = fig.add_subplot(grid[0, 0])
    ax_plane = fig.add_subplot(grid[0, 1], projection="3d")

    fig.subplots_adjust(left=0.055, right=0.955, top=0.90, bottom=0.08, wspace=0.18)

    unit_circle_t = np.linspace(0.0, 2.0 * np.pi, 500)
    ax_complex.plot(np.cos(unit_circle_t), np.sin(unit_circle_t), color="0.82", lw=2.2)
    ax_complex.axhline(0.0, color="0.75", lw=0.9)
    ax_complex.axvline(0.0, color="0.75", lw=0.9)
    phasor_line, = ax_complex.plot([], [], color=COS_COLOR, lw=2.8)
    phasor_tip, = ax_complex.plot([], [], "o", color=COS_COLOR, ms=8)
    phasor_trace, = ax_complex.plot([], [], color=COS_COLOR, lw=1.7, alpha=0.55)
    ax_complex.set_xlim(-1.25, 1.25)
    ax_complex.set_ylim(-1.25, 1.25)
    ax_complex.set_aspect("equal", adjustable="box")
    ax_complex.grid(alpha=0.18)
    ax_complex.set_xlabel(r"Re$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax_complex.set_ylabel(r"Im$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax_complex.set_title(r"Cosine phasor $z(t)=\cos(\omega t)$", pad=12, fontsize=TITLE_SIZE)
    ax_complex.tick_params(labelsize=TICK_SIZE)

    ax_plane.plot(dense_times, cos_values, np.zeros_like(dense_times), color="0.85", lw=1.8)
    plane_trace, = ax_plane.plot([], [], [], color=COS_COLOR, lw=2.6)
    plane_marker, = ax_plane.plot([], [], [], "o", color=COS_COLOR, ms=6)
    plane_stem, = ax_plane.plot([], [], [], color=COS_COLOR, lw=1.9, alpha=0.9)
    ax_plane.set_xlim(0.0, T_END)
    ax_plane.set_ylim(-1.1, 1.1)
    ax_plane.set_zlim(-1.1, 1.1)
    ax_plane.set_xlabel("t", fontsize=LABEL_SIZE, labelpad=10)
    ax_plane.set_ylabel(r"Re$\{\cdot\}$", color=COS_COLOR, fontsize=LABEL_SIZE, labelpad=12)
    ax_plane.set_zlabel(r"Im$\{\cdot\}$", color="tab:orange", fontsize=LABEL_SIZE, labelpad=6)
    ax_plane.yaxis.set_major_locator(MultipleLocator(0.5))
    ax_plane.zaxis.set_major_locator(MultipleLocator(0.5))
    ax_plane.tick_params(axis="x", labelsize=TICK_SIZE)
    ax_plane.tick_params(axis="y", colors=COS_COLOR, labelsize=TICK_SIZE)
    ax_plane.tick_params(axis="z", colors="tab:orange", labelsize=TICK_SIZE)
    ax_plane.set_title("Cosine in the t-Re plane", pad=12, fontsize=TITLE_SIZE)
    ax_plane.view_init(elev=24, azim=-62)

    def draw_state(current_t):
        current_value = np.cos(OMEGA * current_t)
        past_mask = dense_times <= current_t
        past_times = dense_times[past_mask]
        past_values = cos_values[past_mask]

        if not np.any(np.isclose(past_times, current_t)):
            past_times = np.append(past_times, current_t)
            past_values = np.append(past_values, current_value)

        phasor_line.set_data([0.0, current_value], [0.0, 0.0])
        phasor_tip.set_data([current_value], [0.0])
        phasor_trace.set_data(past_values, np.zeros_like(past_values))

        plane_trace.set_data_3d(past_times, past_values, np.zeros_like(past_times))
        plane_marker.set_data_3d([current_t], [current_value], [0.0])
        plane_stem.set_data_3d([current_t, current_t], [0.0, current_value], [0.0, 0.0])

        return phasor_line, phasor_tip, phasor_trace, plane_trace, plane_marker, plane_stem

    def update(frame_index):
        return draw_state(output_times[frame_index])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    draw_state(0.0)
    fig.canvas.draw()
    fig.canvas.print_png(str(PREVIEW_T0_PATH.resolve()))

    preview_t = T_END - np.pi / 4.0
    draw_state(preview_t)
    fig.canvas.draw()
    fig.canvas.print_png(str(PREVIEW_PATH.resolve()))

    animation = FuncAnimation(fig, update, frames=len(output_times), interval=1000 / FPS, blit=False)
    return fig, animation


def main():
    fig, animation = build_animation()
    writer = PillowWriter(fps=FPS)
    animation.save(str(GIF_PATH.resolve()), writer=writer)
    plt.close(fig)
    print(f"Saved GIF to: {GIF_PATH}")
    print(f"Saved preview t=0 to: {PREVIEW_T0_PATH}")
    print(f"Saved preview to: {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
