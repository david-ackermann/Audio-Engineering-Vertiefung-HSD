from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import MultipleLocator

import storyboard_paths as paths


OUTPUT_DIR = paths.PHASOR_INTRO_DIR
GIF_PATH = OUTPUT_DIR / "phasor_components_e_minus_jwt.gif"
PREVIEW_PATH = OUTPUT_DIR / "phasor_components_preview.png"

FPS = 12
FRAMES = 120
OMEGA = 1.0
T_END = 6.0 * np.pi
FIGSIZE = (13.5, 6.1)
FIG_DPI = 100
PHASOR_GREEN = "#26a043"
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"
TITLE_SIZE = 18
LABEL_SIZE = 15
TICK_SIZE = 12


def build_animation():
    output_times = np.linspace(0.0, T_END, FRAMES)
    helix_times = np.linspace(0.0, T_END, 900)
    helix_values = np.exp(-1j * OMEGA * helix_times)
    helix_re = helix_values.real
    helix_im = helix_values.imag
    zeros = np.zeros_like(helix_times)

    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.2])
    ax_complex = fig.add_subplot(grid[0, 0])
    ax_helix = fig.add_subplot(grid[0, 1], projection="3d")

    fig.subplots_adjust(left=0.055, right=0.955, top=0.90, bottom=0.08, wspace=0.18)

    unit_circle_t = np.linspace(0.0, 2.0 * np.pi, 500)
    ax_complex.plot(np.cos(unit_circle_t), np.sin(unit_circle_t), color="0.82", lw=2.2)
    ax_complex.axhline(0.0, color="0.75", lw=0.9)
    ax_complex.axvline(0.0, color="0.75", lw=0.9)
    phasor_line, = ax_complex.plot([], [], color=PHASOR_GREEN, lw=2.7)
    phasor_tip, = ax_complex.plot([], [], "o", color=PHASOR_GREEN, ms=8)
    phasor_trace, = ax_complex.plot([], [], color=PHASOR_GREEN, lw=1.6, alpha=0.55)
    phasor_re_line, = ax_complex.plot([], [], color=RE_COLOR, lw=2.0, alpha=0.95)
    phasor_im_line, = ax_complex.plot([], [], color=IM_COLOR, lw=2.0, alpha=0.95)
    ax_complex.set_xlim(-1.25, 1.25)
    ax_complex.set_ylim(-1.25, 1.25)
    ax_complex.set_aspect("equal", adjustable="box")
    ax_complex.grid(alpha=0.18)
    ax_complex.set_xlabel(r"Re$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax_complex.set_ylabel(r"Im$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax_complex.set_title(r"Phasor $z(t)=e^{-j\omega t}$", pad=12, fontsize=TITLE_SIZE)
    ax_complex.tick_params(labelsize=TICK_SIZE)

    ax_helix.plot(helix_times, helix_re, helix_im, color="0.85", lw=1.6)
    ax_helix.plot(helix_times, helix_re, zeros, color=RE_COLOR, lw=1.4, alpha=0.20)
    ax_helix.plot(helix_times, zeros, helix_im, color=IM_COLOR, lw=1.4, alpha=0.20)

    helix_trace, = ax_helix.plot([], [], [], color=PHASOR_GREEN, lw=2.1)
    re_trace, = ax_helix.plot([], [], [], color=RE_COLOR, lw=2.1)
    im_trace, = ax_helix.plot([], [], [], color=IM_COLOR, lw=2.1)
    helix_point, = ax_helix.plot([], [], [], "o", color=PHASOR_GREEN, ms=6)
    re_point, = ax_helix.plot([], [], [], "o", color=RE_COLOR, ms=5)
    im_point, = ax_helix.plot([], [], [], "o", color=IM_COLOR, ms=5)
    re_stem, = ax_helix.plot([], [], [], color=RE_COLOR, lw=2.0, alpha=0.95)
    im_stem, = ax_helix.plot([], [], [], color=IM_COLOR, lw=2.0, alpha=0.95)

    ax_helix.set_xlim(0.0, T_END)
    ax_helix.set_ylim(-1.1, 1.1)
    ax_helix.set_zlim(-1.1, 1.1)
    ax_helix.set_xlabel("t", fontsize=LABEL_SIZE, labelpad=10)
    ax_helix.set_ylabel(r"Re$\{\cdot\}$", color=RE_COLOR, fontsize=LABEL_SIZE, labelpad=12)
    ax_helix.set_zlabel(r"Im$\{\cdot\}$", color=IM_COLOR, fontsize=LABEL_SIZE, labelpad=6)
    ax_helix.yaxis.set_major_locator(MultipleLocator(0.5))
    ax_helix.zaxis.set_major_locator(MultipleLocator(0.5))
    ax_helix.tick_params(axis="x", labelsize=TICK_SIZE)
    ax_helix.tick_params(axis="y", colors=RE_COLOR, labelsize=TICK_SIZE)
    ax_helix.tick_params(axis="z", colors=IM_COLOR, labelsize=TICK_SIZE)
    ax_helix.set_title("Complex signal as a 3D helix", pad=12, fontsize=TITLE_SIZE)
    ax_helix.view_init(elev=24, azim=-62)

    def draw_state(current_t):
        current_value = np.exp(-1j * OMEGA * current_t)

        past_mask = helix_times <= current_t
        past_times = helix_times[past_mask]
        past_re_values = helix_re[past_mask]
        past_im_values = helix_im[past_mask]

        if not np.any(np.isclose(past_times, current_t)):
            past_times = np.append(past_times, current_t)
            past_re_values = np.append(past_re_values, current_value.real)
            past_im_values = np.append(past_im_values, current_value.imag)

        phasor_line.set_data([0.0, current_value.real], [0.0, current_value.imag])
        phasor_tip.set_data([current_value.real], [current_value.imag])
        phasor_trace.set_data(past_re_values, past_im_values)
        phasor_re_line.set_data([0.0, current_value.real], [0.0, 0.0])
        phasor_im_line.set_data([current_value.real, current_value.real], [0.0, current_value.imag])

        helix_trace.set_data_3d(past_times, past_re_values, past_im_values)
        re_trace.set_data_3d(past_times, past_re_values, np.zeros_like(past_times))
        im_trace.set_data_3d(past_times, np.zeros_like(past_times), past_im_values)
        helix_point.set_data_3d([current_t], [current_value.real], [current_value.imag])
        re_point.set_data_3d([current_t], [current_value.real], [0.0])
        im_point.set_data_3d([current_t], [0.0], [current_value.imag])
        re_stem.set_data_3d([current_t, current_t], [0.0, current_value.real], [0.0, 0.0])
        im_stem.set_data_3d([current_t, current_t], [0.0, 0.0], [0.0, current_value.imag])

        return (
            phasor_line,
            phasor_tip,
            phasor_trace,
            phasor_re_line,
            phasor_im_line,
            helix_trace,
            re_trace,
            im_trace,
            helix_point,
            re_point,
            im_point,
            re_stem,
            im_stem,
        )

    def update(frame_index):
        return draw_state(output_times[frame_index])

    preview_t = T_END
    draw_state(preview_t)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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
    print(f"Saved preview to: {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
