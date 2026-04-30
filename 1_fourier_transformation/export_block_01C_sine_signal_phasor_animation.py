from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import MultipleLocator

import storyboard_paths as paths


OUTPUT_DIR = paths.PHASOR_INTRO_DIR
GIF_PATH = OUTPUT_DIR / "sine_signal_conjugate_pair.gif"
PREVIEW_T0_PATH = OUTPUT_DIR / "sine_signal_conjugate_pair_preview_t0.png"
PREVIEW_PATH = OUTPUT_DIR / "sine_signal_conjugate_pair_preview.png"

FPS = 12
FRAMES = 120
OMEGA = 1.0
T_END = 6.0 * np.pi
FIGSIZE = (13.5, 6.1)
FIG_DPI = 100
POS_COLOR = "tab:purple"
NEG_COLOR = "#26a043"
SUM_COLOR = "tab:blue"
TITLE_SIZE = 18
LABEL_SIZE = 15
TICK_SIZE = 12


# sin(omega t) = (1 / 2j) * (e^{j omega t} - e^{-j omega t})
#             = (-j/2) * e^{j omega t} + (j/2) * e^{-j omega t}

def build_animation():
    output_times = np.linspace(0.0, T_END, FRAMES)
    helix_times = np.linspace(0.0, T_END, 900)

    z_pos_all = (-0.5j) * np.exp(1j * OMEGA * helix_times)
    z_neg_all = (0.5j) * np.exp(-1j * OMEGA * helix_times)
    z_sum_all = z_pos_all + z_neg_all

    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.2])
    ax_complex = fig.add_subplot(grid[0, 0])
    ax_helix = fig.add_subplot(grid[0, 1], projection="3d")

    fig.subplots_adjust(left=0.055, right=0.955, top=0.90, bottom=0.08, wspace=0.18)

    unit_circle_t = np.linspace(0.0, 2.0 * np.pi, 500)
    ax_complex.plot(np.cos(unit_circle_t), np.sin(unit_circle_t), color="0.82", lw=2.2)
    ax_complex.axhline(0.0, color="0.75", lw=0.9)
    ax_complex.axvline(0.0, color="0.75", lw=0.9)

    pos_line, = ax_complex.plot([], [], color=POS_COLOR, lw=2.7, label=r"$-\frac{j}{2}e^{j\omega t}$")
    neg_line, = ax_complex.plot([], [], color=NEG_COLOR, lw=2.7, label=r"$\frac{j}{2}e^{-j\omega t}$")
    sum_line, = ax_complex.plot([], [], color=SUM_COLOR, lw=2.9, label=r"$\sin(\omega t)$")

    pos_tip, = ax_complex.plot([], [], "o", color=POS_COLOR, ms=7)
    neg_tip, = ax_complex.plot([], [], "o", color=NEG_COLOR, ms=7)
    sum_tip, = ax_complex.plot([], [], "o", color=SUM_COLOR, ms=7)

    pos_trace, = ax_complex.plot([], [], color=POS_COLOR, lw=1.4, alpha=0.45)
    neg_trace, = ax_complex.plot([], [], color=NEG_COLOR, lw=1.4, alpha=0.45)
    sum_trace, = ax_complex.plot([], [], color=SUM_COLOR, lw=1.6, alpha=0.55)

    ax_complex.set_xlim(-1.25, 1.25)
    ax_complex.set_ylim(-1.25, 1.25)
    ax_complex.set_aspect("equal", adjustable="box")
    ax_complex.grid(alpha=0.18)
    ax_complex.set_xlabel(r"Re$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax_complex.set_ylabel(r"Im$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax_complex.set_title("Sine signal as a phasor sum", pad=12, fontsize=TITLE_SIZE)
    ax_complex.tick_params(labelsize=TICK_SIZE)
    ax_complex.legend(loc="upper left", fontsize=12, framealpha=0.95)

    ax_helix.plot(helix_times, z_pos_all.real, z_pos_all.imag, color=POS_COLOR, lw=1.6, alpha=0.22)
    ax_helix.plot(helix_times, z_neg_all.real, z_neg_all.imag, color=NEG_COLOR, lw=1.6, alpha=0.22)
    ax_helix.plot(helix_times, z_sum_all.real, z_sum_all.imag, color=SUM_COLOR, lw=1.8, alpha=0.28)

    helix_pos_trace, = ax_helix.plot([], [], [], color=POS_COLOR, lw=2.2)
    helix_neg_trace, = ax_helix.plot([], [], [], color=NEG_COLOR, lw=2.2)
    helix_sum_trace, = ax_helix.plot([], [], [], color=SUM_COLOR, lw=2.4)

    helix_pos_point, = ax_helix.plot([], [], [], "o", color=POS_COLOR, ms=5.5)
    helix_neg_point, = ax_helix.plot([], [], [], "o", color=NEG_COLOR, ms=5.5)
    helix_sum_point, = ax_helix.plot([], [], [], "o", color=SUM_COLOR, ms=6.0)

    ax_helix.set_xlim(0.0, T_END)
    ax_helix.set_ylim(-1.1, 1.1)
    ax_helix.set_zlim(-1.1, 1.1)
    ax_helix.set_xlabel("t", fontsize=LABEL_SIZE, labelpad=10)
    ax_helix.set_ylabel(r"Re$\{\cdot\}$", color="tab:blue", fontsize=LABEL_SIZE, labelpad=12)
    ax_helix.set_zlabel(r"Im$\{\cdot\}$", color="tab:orange", fontsize=LABEL_SIZE, labelpad=6)
    ax_helix.yaxis.set_major_locator(MultipleLocator(0.5))
    ax_helix.zaxis.set_major_locator(MultipleLocator(0.5))
    ax_helix.tick_params(axis="x", labelsize=TICK_SIZE)
    ax_helix.tick_params(axis="y", colors="tab:blue", labelsize=TICK_SIZE)
    ax_helix.tick_params(axis="z", colors="tab:orange", labelsize=TICK_SIZE)
    ax_helix.set_title("Conjugate helices and sine sum", pad=12, fontsize=TITLE_SIZE)
    ax_helix.view_init(elev=24, azim=-62)

    def draw_state(current_t):
        z_pos = (-0.5j) * np.exp(1j * OMEGA * current_t)
        z_neg = (0.5j) * np.exp(-1j * OMEGA * current_t)
        z_sum = z_pos + z_neg

        past_mask = helix_times <= current_t
        past_times = helix_times[past_mask]
        past_pos = z_pos_all[past_mask]
        past_neg = z_neg_all[past_mask]
        past_sum = z_sum_all[past_mask]

        if not np.any(np.isclose(past_times, current_t)):
            past_times = np.append(past_times, current_t)
            past_pos = np.append(past_pos, z_pos)
            past_neg = np.append(past_neg, z_neg)
            past_sum = np.append(past_sum, z_sum)

        pos_line.set_data([0.0, z_pos.real], [0.0, z_pos.imag])
        neg_line.set_data([0.0, z_neg.real], [0.0, z_neg.imag])
        sum_line.set_data([0.0, z_sum.real], [0.0, z_sum.imag])

        pos_tip.set_data([z_pos.real], [z_pos.imag])
        neg_tip.set_data([z_neg.real], [z_neg.imag])
        sum_tip.set_data([z_sum.real], [z_sum.imag])

        pos_trace.set_data(past_pos.real, past_pos.imag)
        neg_trace.set_data(past_neg.real, past_neg.imag)
        sum_trace.set_data(past_sum.real, past_sum.imag)

        helix_pos_trace.set_data_3d(past_times, past_pos.real, past_pos.imag)
        helix_neg_trace.set_data_3d(past_times, past_neg.real, past_neg.imag)
        helix_sum_trace.set_data_3d(past_times, past_sum.real, past_sum.imag)

        helix_pos_point.set_data_3d([current_t], [z_pos.real], [z_pos.imag])
        helix_neg_point.set_data_3d([current_t], [z_neg.real], [z_neg.imag])
        helix_sum_point.set_data_3d([current_t], [z_sum.real], [z_sum.imag])

        return (
            pos_line,
            neg_line,
            sum_line,
            pos_tip,
            neg_tip,
            sum_tip,
            pos_trace,
            neg_trace,
            sum_trace,
            helix_pos_trace,
            helix_neg_trace,
            helix_sum_trace,
            helix_pos_point,
            helix_neg_point,
            helix_sum_point,
        )

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
