from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image, ImageSequence
from matplotlib.ticker import MultipleLocator

import export_block_03B_phase_shift_series as base
import storyboard_paths as paths


OUTPUT_DIR = paths.PHASE_SHIFT_SERIES_COS_NO_COMPONENTS_DIR
HELIX_GIF_PATH = OUTPUT_DIR / "04_phi_0_no_components_helix.gif"
HELIX_T0_PNG_PATH = OUTPUT_DIR / "04_phi_0_no_components_helix_t0.png"
HELIX_TMAX_PNG_PATH = OUTPUT_DIR / "04_phi_0_no_components_helix_tmax.png"
HELIX_SUM_ONLY_GIF_PATH = OUTPUT_DIR / "05_phi_0_no_components_helix_sum_only.gif"
HELIX_LIGHTBLUE_GIF_PATH = OUTPUT_DIR / "06_phi_0_no_components_helix_lightblue.gif"

COS_NO_COMPONENTS_CASE = {
    "prefix": "01",
    "slug": "phi_0_no_components",
    "mode": "constant",
    "phi": 0.0,
    "phase_title": r"Phase over time: $\varphi(t)=0^\circ$",
    "suptitle": r"Constant phase offset in $x(t)=\cos(\omega t)$",
    "signal_label": r"$\cos(\omega t)$",
    "spectrum_signal_title": r"Time signal $x(t)=\cos(\omega t)$",
}

HELIX_FIGSIZE = (13.8, 8.2)
HELIX_DPI = 120
HELIX_TITLE_SIZE = 24
HELIX_LABEL_SIZE = 20
HELIX_TICK_SIZE = 16
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"
LIGHTBLUE_SUM = "#8fc8ff"


def save_first_gif_frame_png(gif_path, png_path):
    with Image.open(gif_path) as gif:
        first_frame = next(ImageSequence.Iterator(gif)).convert("RGBA")
        first_frame.save(png_path)


def save_last_gif_frame_png(gif_path, png_path):
    with Image.open(gif_path) as gif:
        last_frame = None
        for frame in ImageSequence.Iterator(gif):
            last_frame = frame.convert("RGBA")
        if last_frame is None:
            raise RuntimeError(f"No frames found in {gif_path}")
        last_frame.save(png_path)


def crop_gif_whitespace_group(paths, threshold=250, pad=2):
    datasets = []
    bbox = None

    for path in paths:
        with Image.open(path) as gif:
            frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif)]
            durations = [frame.info.get("duration", gif.info.get("duration", 100)) for frame in ImageSequence.Iterator(gif)]
            loop = gif.info.get("loop", 0)
        datasets.append((path, frames, durations, loop))

        for frame in frames:
            rgb = np.asarray(frame.convert("RGB"))
            mask = np.any(rgb < threshold, axis=2)
            if not np.any(mask):
                continue
            rows, cols = np.where(mask)
            current = (cols.min(), rows.min(), cols.max() + 1, rows.max() + 1)
            if bbox is None:
                bbox = current
            else:
                bbox = (
                    min(bbox[0], current[0]),
                    min(bbox[1], current[1]),
                    max(bbox[2], current[2]),
                    max(bbox[3], current[3]),
                )

    if bbox is None:
        return

    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(datasets[0][1][0].width, x1 + pad)
    y1 = min(datasets[0][1][0].height, y1 + pad)

    for path, frames, durations, loop in datasets:
        cropped_frames = [frame.crop((x0, y0, x1, y1)).convert("P", palette=Image.ADAPTIVE) for frame in frames]
        cropped_frames[0].save(
            path,
            save_all=True,
            append_images=cropped_frames[1:],
            loop=loop,
            duration=durations,
            disposal=2,
        )


def build_overview_animation_no_components(case, data):
    fig, ax_complex, ax_signal, ax_phi = base.create_overview_figure(case)
    base.draw_background(case, data, ax_complex, ax_signal, ax_phi)
    ax_signal.lines[0].remove()
    ax_signal.legend(loc="upper right", fontsize=11, framealpha=0.95)

    sum_line, = ax_complex.plot([], [], color=base.SUM_COLOR, lw=2.9, label=r"$x(t)$")
    sum_tip, = ax_complex.plot([], [], "o", color=base.SUM_COLOR, ms=7)
    phase_text = ax_complex.text(-0.15, -0.24, r"$\varphi=+0^\circ$", color=base.PHASOR_PHASE_COLOR, fontsize=13)
    ax_complex.legend(loc="lower left", fontsize=10.5, framealpha=0.95)

    time_marker_signal = ax_signal.axvline(base.T_START, color=base.MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_signal_point, = ax_signal.plot([], [], "o", color=base.MARKER_COLOR, ms=8)
    time_marker_phi = ax_phi.axvline(base.T_START, color=base.MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_phi_point, = ax_phi.plot([], [], "o", color=base.MARKER_COLOR, ms=8)

    def draw_state(current_t):
        current_phi = float(base.phase_values(case, np.array([current_t]))[0])
        z_sum = np.cos(base.OMEGA * current_t + current_phi)
        signal_value = np.cos(base.OMEGA * current_t + current_phi)
        phi_value_deg = np.degrees(current_phi)

        sum_line.set_data([0.0, z_sum], [0.0, 0.0])
        sum_tip.set_data([z_sum], [0.0])
        phase_text.set_text(fr"$\varphi={base.format_phase_deg(phi_value_deg)}$")

        time_marker_signal.set_xdata([current_t, current_t])
        moving_signal_point.set_data([current_t], [signal_value])
        time_marker_phi.set_xdata([current_t, current_t])
        moving_phi_point.set_data([current_t], [phi_value_deg])

        return (
            sum_line,
            sum_tip,
            phase_text,
            time_marker_signal,
            moving_signal_point,
            time_marker_phi,
            moving_phi_point,
        )

    def update(frame_index):
        return draw_state(data["time_frames"][frame_index])

    animation = FuncAnimation(fig, update, frames=len(data["time_frames"]), interval=1000 / base.FPS, blit=False)
    return fig, animation, draw_state


def export_helix_variant(case, output_path, title, show_components, sum_color, sum_alpha, sum_lw, bg_sum_alpha):
    output_times = np.linspace(base.T_START, base.T_END, base.FRAMES, endpoint=False)
    helix_times = np.linspace(base.T_START, base.T_END, 900)
    phi_all = base.phase_values(case, helix_times)

    z_pos_all = 0.5 * np.exp(1j * (base.OMEGA * helix_times + phi_all))
    z_neg_all = 0.5 * np.exp(-1j * (base.OMEGA * helix_times + phi_all))
    z_sum_all = z_pos_all + z_neg_all

    fig = plt.figure(figsize=HELIX_FIGSIZE, dpi=HELIX_DPI, facecolor="white")
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.03, right=0.96, bottom=0.09, top=0.88)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("white")
    ax.set_box_aspect((3.9, 1.55, 1.55))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 1.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 1.0))

    if show_components:
        ax.plot(helix_times, z_pos_all.real, z_pos_all.imag, color=base.POS_COLOR, lw=1.5, alpha=0.20)
        ax.plot(helix_times, z_neg_all.real, z_neg_all.imag, color=base.NEG_COLOR, lw=1.5, alpha=0.20)
    ax.plot(helix_times, z_sum_all.real, z_sum_all.imag, color=sum_color, lw=1.8, alpha=bg_sum_alpha)

    if show_components:
        helix_pos_trace, = ax.plot([], [], [], color=base.POS_COLOR, lw=2.4)
        helix_neg_trace, = ax.plot([], [], [], color=base.NEG_COLOR, lw=2.4)
        helix_pos_point, = ax.plot([], [], [], "o", color=base.POS_COLOR, ms=5.5)
        helix_neg_point, = ax.plot([], [], [], "o", color=base.NEG_COLOR, ms=5.5)
    else:
        helix_pos_trace = helix_neg_trace = None
        helix_pos_point = helix_neg_point = None

    helix_sum_trace, = ax.plot([], [], [], color=sum_color, lw=sum_lw, alpha=sum_alpha)
    helix_sum_point, = ax.plot([], [], [], "o", color=sum_color, ms=6.0, alpha=min(1.0, max(sum_alpha, 0.65)))

    ax.set_xlim(base.T_START, base.T_END)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_locator(MultipleLocator(0.5))
    ax.set_xlabel("Time t [s]", fontsize=HELIX_LABEL_SIZE, labelpad=22)
    ax.set_ylabel(r"Re$\{\cdot\}$", fontsize=HELIX_LABEL_SIZE, color=RE_COLOR, labelpad=18)
    ax.set_zlabel(r"Im$\{\cdot\}$", fontsize=HELIX_LABEL_SIZE, color=IM_COLOR, labelpad=10)
    ax.set_title("", y=0.92, pad=-6, fontsize=HELIX_TITLE_SIZE)
    ax.tick_params(axis="x", labelsize=HELIX_TICK_SIZE, pad=4)
    ax.tick_params(axis="y", labelsize=HELIX_TICK_SIZE, colors=RE_COLOR, pad=4)
    ax.tick_params(axis="z", labelsize=HELIX_TICK_SIZE, colors=IM_COLOR, pad=4)
    ax.view_init(elev=24, azim=-62)

    def draw_state(current_t):
        z_pos = 0.5 * np.exp(1j * base.OMEGA * current_t)
        z_neg = 0.5 * np.exp(-1j * base.OMEGA * current_t)
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

        artists = []
        if show_components:
            helix_pos_trace.set_data_3d(past_times, past_pos.real, past_pos.imag)
            helix_neg_trace.set_data_3d(past_times, past_neg.real, past_neg.imag)
            helix_pos_point.set_data_3d([current_t], [z_pos.real], [z_pos.imag])
            helix_neg_point.set_data_3d([current_t], [z_neg.real], [z_neg.imag])
            artists.extend([helix_pos_trace, helix_neg_trace, helix_pos_point, helix_neg_point])

        helix_sum_trace.set_data_3d(past_times, past_sum.real, past_sum.imag)
        helix_sum_point.set_data_3d([current_t], [z_sum.real], [z_sum.imag])
        artists.extend([helix_sum_trace, helix_sum_point])
        return tuple(artists)

    animation = FuncAnimation(fig, lambda idx: draw_state(output_times[idx]), frames=len(output_times), interval=1000 / base.FPS, blit=False)
    writer = PillowWriter(fps=base.FPS)
    animation.save(str(output_path.resolve()), writer=writer)
    plt.close(fig)


def main():
    base.OUTPUT_DIR = OUTPUT_DIR
    base.build_overview_animation = build_overview_animation_no_components
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*"):
        if old_file.is_file():
            old_file.unlink()

    saved = list(base.export_case(COS_NO_COMPONENTS_CASE))
    export_helix_variant(
        COS_NO_COMPONENTS_CASE,
        HELIX_GIF_PATH,
        "",
        show_components=True,
        sum_color=base.SUM_COLOR,
        sum_alpha=1.0,
        sum_lw=2.8,
        bg_sum_alpha=0.24,
    )
    export_helix_variant(
        COS_NO_COMPONENTS_CASE,
        HELIX_SUM_ONLY_GIF_PATH,
        "",
        show_components=False,
        sum_color=base.SUM_COLOR,
        sum_alpha=1.0,
        sum_lw=2.8,
        bg_sum_alpha=0.24,
    )
    export_helix_variant(
        COS_NO_COMPONENTS_CASE,
        HELIX_LIGHTBLUE_GIF_PATH,
        "",
        show_components=True,
        sum_color=LIGHTBLUE_SUM,
        sum_alpha=0.55,
        sum_lw=2.6,
        bg_sum_alpha=0.0,
    )
    crop_gif_whitespace_group([HELIX_GIF_PATH, HELIX_SUM_ONLY_GIF_PATH, HELIX_LIGHTBLUE_GIF_PATH])
    save_first_gif_frame_png(HELIX_GIF_PATH, HELIX_T0_PNG_PATH)
    save_last_gif_frame_png(HELIX_GIF_PATH, HELIX_TMAX_PNG_PATH)
    saved.extend([HELIX_GIF_PATH, HELIX_T0_PNG_PATH, HELIX_TMAX_PNG_PATH, HELIX_SUM_ONLY_GIF_PATH, HELIX_LIGHTBLUE_GIF_PATH])
    print(f"Saved outputs to: {OUTPUT_DIR}")
    for path in saved:
        print(path)


if __name__ == "__main__":
    main()
