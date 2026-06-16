from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.lines import Line2D


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "02_am_modulation" / "02e_phasor_product_sum_difference"

INPUT_PREVIEW_PATH = OUTPUT_DIR / "01_two_signals_conjugate_pairs_preview.png"
INPUT_GIF_PATH = OUTPUT_DIR / "02_two_signals_conjugate_pairs.gif"
PRODUCT_INPUT_PATH = OUTPUT_DIR / "03_product_build_00_input_phasors.png"
PRODUCT_STEP_PATHS = [
    OUTPUT_DIR / "04_product_build_01_sum_positive.png",
    OUTPUT_DIR / "05_product_build_02_difference_positive.png",
    OUTPUT_DIR / "06_product_build_03_difference_negative.png",
    OUTPUT_DIR / "07_product_build_04_sum_negative.png",
]
ALL_PRODUCTS_PREVIEW_PATH = OUTPUT_DIR / "08_all_product_phasors_preview.png"
ALL_PRODUCTS_GIF_PATH = OUTPUT_DIR / "09_all_product_phasors.gif"
PAIR_PREVIEW_PATH = OUTPUT_DIR / "10_sum_difference_pairs_preview.png"
PAIR_GIF_PATH = OUTPUT_DIR / "11_sum_difference_pairs_and_output.gif"

FPS = 12
FRAMES = 180
T_START = 0.0
T_END = 4.0 * np.pi
FIGSIZE = (14.4, 7.8)
FIG_DPI = 120

OMEGA_X = 5.0
OMEGA_M = 1.0

CARRIER_POS_COLOR = "0.08"
CARRIER_NEG_COLOR = "0.48"
MOD_POS_COLOR = "#7a3db8"
MOD_NEG_COLOR = "#b57ae8"
INPUT_GREY = "0.68"
SUM_PAIR_GREEN = "#1f7a3f"
DIFF_PAIR_GREEN = "#86b996"
OUTPUT_BLUE = "#0b4f9c"
MARKER_COLOR = "tab:red"
BASELINE_COLOR = "0.78"
GRID_ALPHA = 0.18

TITLE_SIZE = 18
LABEL_SIZE = 15
TICK_SIZE = 12
SUPTITLE_SIZE = 24
PHASOR_COMPLEX_LIMIT = 1.25
AMPLITUDE_LIMITS = (-1.15, 1.15)
TIME_AXIS_BOX_ASPECT = 1.0 / 1.45
PRODUCT_PREVIEW_T = 0.18 * T_END
INPUT_PREVIEW_T = PRODUCT_PREVIEW_T

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


INPUT_COMPONENTS = [
    ("x_pos", r"$X_+$", r"$+\omega_x$", CARRIER_POS_COLOR),
    ("x_neg", r"$X_-$", r"$-\omega_x$", CARRIER_NEG_COLOR),
    ("m_pos", r"$M_+$", r"$+\omega_m$", MOD_POS_COLOR),
    ("m_neg", r"$M_-$", r"$-\omega_m$", MOD_NEG_COLOR),
]

PRODUCT_COMPONENTS = [
    ("sum_pos", ("x_pos", "m_pos"), r"$X_+M_+$", r"$+\omega_x+\omega_m$", SUM_PAIR_GREEN),
    ("diff_pos", ("x_pos", "m_neg"), r"$X_+M_-$", r"$+\omega_x-\omega_m$", DIFF_PAIR_GREEN),
    ("diff_neg", ("x_neg", "m_pos"), r"$X_-M_+$", r"$-\omega_x+\omega_m$", DIFF_PAIR_GREEN),
    ("sum_neg", ("x_neg", "m_neg"), r"$X_-M_-$", r"$-\omega_x-\omega_m$", SUM_PAIR_GREEN),
]


def wrap_phase_deg(phase_rad):
    phase_wrapped = (np.asarray(phase_rad) + np.pi) % (2.0 * np.pi) - np.pi
    return np.degrees(phase_wrapped)


def signal_components(times):
    times = np.asarray(times)
    x_pos = 0.5 * np.exp(1j * OMEGA_X * times)
    x_neg = 0.5 * np.exp(-1j * OMEGA_X * times)
    m_pos = 0.5 * np.exp(1j * OMEGA_M * times)
    m_neg = 0.5 * np.exp(-1j * OMEGA_M * times)
    return {
        "x_pos": x_pos,
        "x_neg": x_neg,
        "m_pos": m_pos,
        "m_neg": m_neg,
        "x": x_pos + x_neg,
        "m": m_pos + m_neg,
    }


def input_phase_values(times):
    return {
        "x_pos": wrap_phase_deg(OMEGA_X * times),
        "x_neg": wrap_phase_deg(-OMEGA_X * times),
        "m_pos": wrap_phase_deg(OMEGA_M * times),
        "m_neg": wrap_phase_deg(-OMEGA_M * times),
    }


def product_components(times):
    signal = signal_components(times)
    sum_pos = signal["x_pos"] * signal["m_pos"]
    diff_pos = signal["x_pos"] * signal["m_neg"]
    diff_neg = signal["x_neg"] * signal["m_pos"]
    sum_neg = signal["x_neg"] * signal["m_neg"]
    sum_pair = sum_pos + sum_neg
    diff_pair = diff_pos + diff_neg
    product = sum_pair + diff_pair
    return {
        "sum_pos": sum_pos,
        "diff_pos": diff_pos,
        "diff_neg": diff_neg,
        "sum_neg": sum_neg,
        "sum_pair": sum_pair,
        "diff_pair": diff_pair,
        "product": product,
    }


def create_three_panel_figure(suptitle):
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.45], height_ratios=[1.0, 0.68])
    ax_phasor = fig.add_subplot(grid[:, 0])
    ax_signal = fig.add_subplot(grid[0, 1])
    ax_phase = fig.add_subplot(grid[1, 1], sharex=ax_signal)
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.10, wspace=0.24, hspace=0.22)
    fig.suptitle(suptitle, fontsize=SUPTITLE_SIZE, y=0.965)
    return fig, ax_phasor, ax_signal, ax_phase


def create_two_panel_figure(suptitle):
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.45])
    ax_phasor = fig.add_subplot(grid[0, 0])
    ax_signal = fig.add_subplot(grid[0, 1])
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.10, wspace=0.24)
    fig.suptitle(suptitle, fontsize=SUPTITLE_SIZE, y=0.965)
    return fig, ax_phasor, ax_signal


def add_legend(ax, *, loc, fontsize, framealpha=0.95, max_rows=4, **kwargs):
    handles, labels = ax.get_legend_handles_labels()
    ncol = max(1, int(np.ceil(len(labels) / max_rows)))
    pad_count = ncol * max_rows - len(labels) if ncol > 1 else 0
    if pad_count:
        spacer_handle = Line2D([], [], linestyle="none", marker="", alpha=0.0)
        handles = [*handles, *([spacer_handle] * pad_count)]
        labels = [*labels, *(["\u00a0"] * pad_count)]

    legend = ax.legend(
        handles=handles,
        labels=labels,
        loc=loc,
        fontsize=fontsize,
        framealpha=framealpha,
        ncol=ncol,
        columnspacing=1.0,
        handlelength=2.0,
        handleheight=1.35,
        handletextpad=0.55,
        labelspacing=0.25,
        borderaxespad=0.45,
        **kwargs,
    )

    if pad_count:
        for text in legend.get_texts()[-pad_count:]:
            text.set_alpha(0.0)
        for handle in legend.legend_handles[-pad_count:]:
            handle.set_visible(False)

    return legend


def setup_phasor_axis(ax, title, limit, circle_radius=1.0):
    circle_t = np.linspace(0.0, 2.0 * np.pi, 500)
    ax.plot(circle_radius * np.cos(circle_t), circle_radius * np.sin(circle_t), color="0.86", lw=2.0)
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.axvline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=12, fontsize=TITLE_SIZE)
    ax.set_xlabel(r"Re$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Im$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def setup_time_axis(ax, title, y_limits):
    ax.set_box_aspect(TIME_AXIS_BOX_ASPECT)
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(T_START, T_END)
    ax.set_ylim(*y_limits)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def setup_phase_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(T_START, T_END)
    ax.set_ylim(-180.0, 180.0)
    ax.set_yticks([-180.0, -90.0, 0.0, 90.0, 180.0])
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Phase [deg]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def set_vector(line, tip, value):
    line.set_data([0.0, value.real], [0.0, value.imag])
    tip.set_data([value.real], [value.imag])


def build_two_signal_animation():
    time_dense = np.linspace(T_START, T_END, 1000)
    time_frames = np.linspace(T_START, T_END, FRAMES, endpoint=False)
    values = signal_components(time_dense)

    fig, ax_phasor, ax_signal = create_two_panel_figure(
        r"Two real signals as two conjugate phasor pairs"
    )
    setup_phasor_axis(ax_phasor, "Phasor sums", limit=PHASOR_COMPLEX_LIMIT, circle_radius=1.0)
    setup_time_axis(ax_signal, r"Real signals $x(t)$ and $m(t)$", AMPLITUDE_LIMITS)

    ax_signal.plot(time_dense, values["x"].real, color=CARRIER_POS_COLOR, lw=2.7, label=r"$x(t)=\cos(\omega_x t)$")
    ax_signal.plot(time_dense, values["m"].real, color=MOD_POS_COLOR, lw=2.7, label=r"$m(t)=\cos(\omega_m t)$")
    add_legend(ax_signal, loc="upper right", fontsize=11)

    phasor_lines = {}
    phasor_tips = {}
    for key, label, phase_label, color in INPUT_COMPONENTS:
        phasor_lines[key], = ax_phasor.plot([], [], color=color, lw=2.6, label=f"{label}: {phase_label}")
        phasor_tips[key], = ax_phasor.plot([], [], "o", color=color, ms=7)
    x_sum_line, = ax_phasor.plot([], [], color=CARRIER_POS_COLOR, lw=3.0, label=r"$x(t)$")
    x_sum_tip, = ax_phasor.plot([], [], "o", color=CARRIER_POS_COLOR, ms=7)
    m_sum_line, = ax_phasor.plot([], [], color=MOD_POS_COLOR, lw=3.0, label=r"$m(t)$")
    m_sum_tip, = ax_phasor.plot([], [], "o", color=MOD_POS_COLOR, ms=7)
    add_legend(ax_phasor, loc="lower left", fontsize=10.5)

    signal_marker = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    x_point, = ax_signal.plot([], [], "o", color=CARRIER_POS_COLOR, ms=7)
    m_point, = ax_signal.plot([], [], "o", color=MOD_POS_COLOR, ms=7)

    def draw_state(current_t):
        current = signal_components(np.array([current_t]))
        artists = []

        for key, _, _, _ in INPUT_COMPONENTS:
            value = current[key][0]
            set_vector(phasor_lines[key], phasor_tips[key], value)
            artists.extend([phasor_lines[key], phasor_tips[key]])

        set_vector(x_sum_line, x_sum_tip, current["x"][0])
        set_vector(m_sum_line, m_sum_tip, current["m"][0])

        signal_marker.set_xdata([current_t, current_t])
        x_point.set_data([current_t], [current["x"][0].real])
        m_point.set_data([current_t], [current["m"][0].real])

        artists.extend([x_sum_line, x_sum_tip, m_sum_line, m_sum_tip])
        artists.extend([signal_marker, x_point, m_point])
        return tuple(artists)

    def update(frame_index):
        return draw_state(time_frames[frame_index])

    draw_state(INPUT_PREVIEW_T)
    fig.savefig(INPUT_PREVIEW_PATH, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    animation = FuncAnimation(fig, update, frames=len(time_frames), interval=1000 / FPS, blit=False)
    return fig, animation


def draw_input_vectors(ax, current_values, active_keys=None, inactive_alpha=0.45):
    active_keys = set(current_values.keys()) if active_keys is None else set(active_keys)
    artists = {}
    for key, label, phase_label, color in INPUT_COMPONENTS:
        is_active = key in active_keys
        line_color = color if is_active else INPUT_GREY
        alpha = 1.0 if is_active else inactive_alpha
        line, = ax.plot(
            [0.0, current_values[key].real],
            [0.0, current_values[key].imag],
            color=line_color,
            lw=3.0 if is_active else 2.0,
            alpha=alpha,
            label=f"{label}: {phase_label}",
        )
        tip, = ax.plot([current_values[key].real], [current_values[key].imag], "o", color=line_color, ms=7, alpha=alpha)
        artists[key] = (line, tip)
    return artists


def save_input_product_overview():
    current_t = PRODUCT_PREVIEW_T
    time_dense = np.linspace(T_START, T_END, 1000)
    values = signal_components(time_dense)
    current = signal_components(np.array([current_t]))

    fig, ax_phasor, ax_signal = create_two_panel_figure("Input phasors before multiplication")
    setup_phasor_axis(ax_phasor, "Four rotating input phasors", PHASOR_COMPLEX_LIMIT, circle_radius=1.0)
    setup_time_axis(ax_signal, r"Real signals $x(t)$ and $m(t)$", AMPLITUDE_LIMITS)

    draw_input_vectors(ax_phasor, {key: current[key][0] for key, _, _, _ in INPUT_COMPONENTS})
    add_legend(ax_phasor, loc="lower left", fontsize=10.5)

    ax_signal.plot(time_dense, values["x"].real, color=CARRIER_POS_COLOR, lw=2.7, label=r"$x(t)$")
    ax_signal.plot(time_dense, values["m"].real, color=MOD_POS_COLOR, lw=2.7, label=r"$m(t)$")
    ax_signal.axvline(current_t, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    add_legend(ax_signal, loc="upper right", fontsize=11)

    fig.savefig(PRODUCT_INPUT_PATH, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_product_step(preview_path, product_key):
    current_t = PRODUCT_PREVIEW_T
    signal_current = signal_components(np.array([current_t]))
    product_current = product_components(np.array([current_t]))
    component = next(item for item in PRODUCT_COMPONENTS if item[0] == product_key)
    _, input_pair, product_label, freq_label, pair_color = component

    fig, ax_phasor, ax_signal = create_two_panel_figure(fr"Product step: {product_label} $\rightarrow$ {freq_label}")
    setup_phasor_axis(ax_phasor, "Length product and phase sum", PHASOR_COMPLEX_LIMIT, circle_radius=1.0)
    setup_time_axis(ax_signal, "Time signal", AMPLITUDE_LIMITS)

    draw_input_vectors(
        ax_phasor,
        {key: signal_current[key][0] for key, _, _, _ in INPUT_COMPONENTS},
        active_keys=set(input_pair),
        inactive_alpha=0.28,
    )
    product_value = product_current[product_key][0]
    product_line, = ax_phasor.plot(
        [0.0, product_value.real],
        [0.0, product_value.imag],
        color=pair_color,
        lw=4.0,
        label=fr"{product_label}: $0.25e^{{j(\varphi_1+\varphi_2)}}$",
    )
    product_tip, = ax_phasor.plot([product_value.real], [product_value.imag], "o", color=pair_color, ms=8)
    add_legend(ax_phasor, loc="lower left", fontsize=10.5)

    fig.savefig(preview_path, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    return product_line, product_tip


def build_all_products_animation():
    time_dense = np.linspace(T_START, T_END, 1000)
    time_frames = np.linspace(T_START, T_END, FRAMES, endpoint=False)
    values = product_components(time_dense)

    fig, ax_phasor, ax_signal = create_two_panel_figure("Two conjugate product pairs")
    setup_phasor_axis(ax_phasor, "Product pairs and pair sums", PHASOR_COMPLEX_LIMIT, circle_radius=1.0)
    setup_time_axis(ax_signal, "Pair-sum time signals", AMPLITUDE_LIMITS)

    ax_signal.plot(time_dense, values["sum_pair"].real, color=SUM_PAIR_GREEN, lw=3.0, label=r"$y_\Sigma(t)$")
    ax_signal.plot(time_dense, values["diff_pair"].real, color=DIFF_PAIR_GREEN, lw=3.0, label=r"$y_\Delta(t)$")
    add_legend(ax_signal, loc="upper right", fontsize=11)

    product_lines = {}
    product_tips = {}
    for key, _input_pair, label, freq_label, pair_color in PRODUCT_COMPONENTS:
        product_lines[key], = ax_phasor.plot([], [], color=pair_color, lw=2.6, alpha=0.62, label=f"{label}: {freq_label}")
        product_tips[key], = ax_phasor.plot([], [], "o", color=pair_color, ms=6, alpha=0.62)
    sum_line, = ax_phasor.plot([], [], color=SUM_PAIR_GREEN, lw=3.6, label=r"$y_\Sigma(t)$")
    sum_tip, = ax_phasor.plot([], [], "o", color=SUM_PAIR_GREEN, ms=8)
    diff_line, = ax_phasor.plot([], [], color=DIFF_PAIR_GREEN, lw=3.6, label=r"$y_\Delta(t)$")
    diff_tip, = ax_phasor.plot([], [], "o", color=DIFF_PAIR_GREEN, ms=8)
    add_legend(ax_phasor, loc="lower left", fontsize=10.5)

    signal_marker = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    sum_point, = ax_signal.plot([], [], "o", color=SUM_PAIR_GREEN, ms=7)
    diff_point, = ax_signal.plot([], [], "o", color=DIFF_PAIR_GREEN, ms=7)

    def draw_state(current_t):
        current = product_components(np.array([current_t]))
        artists = [signal_marker, sum_point, diff_point]
        for key, *_rest in PRODUCT_COMPONENTS:
            set_vector(product_lines[key], product_tips[key], current[key][0])
            artists.extend([product_lines[key], product_tips[key]])
        set_vector(sum_line, sum_tip, current["sum_pair"][0])
        set_vector(diff_line, diff_tip, current["diff_pair"][0])
        signal_marker.set_xdata([current_t, current_t])
        sum_point.set_data([current_t], [current["sum_pair"][0].real])
        diff_point.set_data([current_t], [current["diff_pair"][0].real])
        artists.extend([sum_line, sum_tip, diff_line, diff_tip])
        return tuple(artists)

    def update(frame_index):
        return draw_state(time_frames[frame_index])

    draw_state(PRODUCT_PREVIEW_T)
    fig.savefig(ALL_PRODUCTS_PREVIEW_PATH, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    animation = FuncAnimation(fig, update, frames=len(time_frames), interval=1000 / FPS, blit=False)
    return fig, animation


def build_pair_animation():
    time_dense = np.linspace(T_START, T_END, 1000)
    time_frames = np.linspace(T_START, T_END, FRAMES, endpoint=False)
    values = product_components(time_dense)

    fig, ax_phasor, ax_signal = create_two_panel_figure("Sum-frequency pair and difference-frequency pair")
    setup_phasor_axis(ax_phasor, "Conjugate pairs and real sums", PHASOR_COMPLEX_LIMIT, circle_radius=1.0)
    setup_time_axis(ax_signal, "Pair sums and total output", AMPLITUDE_LIMITS)

    ax_signal.plot(time_dense, values["sum_pair"].real, color=SUM_PAIR_GREEN, lw=2.6, label=r"$y_\Sigma(t)$")
    ax_signal.plot(time_dense, values["diff_pair"].real, color=DIFF_PAIR_GREEN, lw=2.6, label=r"$y_\Delta(t)$")
    ax_signal.plot(time_dense, values["product"].real, color=OUTPUT_BLUE, lw=3.2, label=r"$y(t)=y_\Sigma(t)+y_\Delta(t)$")
    add_legend(ax_signal, loc="upper right", fontsize=11)

    phasor_lines = {}
    phasor_tips = {}
    for key, _input_pair, label, freq_label, pair_color in PRODUCT_COMPONENTS:
        phasor_lines[key], = ax_phasor.plot([], [], color=pair_color, lw=2.4, alpha=0.72, label=f"{label}: {freq_label}")
        phasor_tips[key], = ax_phasor.plot([], [], "o", color=pair_color, ms=6, alpha=0.72)

    sum_line, = ax_phasor.plot([], [], color=SUM_PAIR_GREEN, lw=3.5, label=r"$y_\Sigma(t)$")
    sum_tip, = ax_phasor.plot([], [], "o", color=SUM_PAIR_GREEN, ms=8)
    diff_line, = ax_phasor.plot([], [], color=DIFF_PAIR_GREEN, lw=3.5, label=r"$y_\Delta(t)$")
    diff_tip, = ax_phasor.plot([], [], "o", color=DIFF_PAIR_GREEN, ms=8)
    output_line, = ax_phasor.plot([], [], color=OUTPUT_BLUE, lw=4.0, label=r"$y(t)$")
    output_tip, = ax_phasor.plot([], [], "o", color=OUTPUT_BLUE, ms=8)
    add_legend(ax_phasor, loc="lower left", fontsize=10.5)

    signal_marker = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    sum_point, = ax_signal.plot([], [], "o", color=SUM_PAIR_GREEN, ms=6)
    diff_point, = ax_signal.plot([], [], "o", color=DIFF_PAIR_GREEN, ms=6)
    output_point, = ax_signal.plot([], [], "o", color=OUTPUT_BLUE, ms=7)

    def draw_state(current_t):
        current = product_components(np.array([current_t]))
        artists = [signal_marker, sum_point, diff_point, output_point]

        for key, *_rest in PRODUCT_COMPONENTS:
            set_vector(phasor_lines[key], phasor_tips[key], current[key][0])
            artists.extend([phasor_lines[key], phasor_tips[key]])

        set_vector(sum_line, sum_tip, current["sum_pair"][0])
        set_vector(diff_line, diff_tip, current["diff_pair"][0])
        set_vector(output_line, output_tip, current["product"][0])

        signal_marker.set_xdata([current_t, current_t])
        sum_point.set_data([current_t], [current["sum_pair"][0].real])
        diff_point.set_data([current_t], [current["diff_pair"][0].real])
        output_point.set_data([current_t], [current["product"][0].real])

        artists.extend([sum_line, sum_tip, diff_line, diff_tip, output_line, output_tip])
        return tuple(artists)

    def update(frame_index):
        return draw_state(time_frames[frame_index])

    draw_state(PRODUCT_PREVIEW_T)
    fig.savefig(PAIR_PREVIEW_PATH, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    animation = FuncAnimation(fig, update, frames=len(time_frames), interval=1000 / FPS, blit=False)
    return fig, animation


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*"):
        if old_file.suffix.lower() in {".png", ".gif"}:
            old_file.unlink()

    saved_paths = []

    input_fig, input_animation = build_two_signal_animation()
    input_animation.save(str(INPUT_GIF_PATH.resolve()), writer=PillowWriter(fps=FPS))
    plt.close(input_fig)
    saved_paths.extend([INPUT_PREVIEW_PATH, INPUT_GIF_PATH])

    save_input_product_overview()
    saved_paths.append(PRODUCT_INPUT_PATH)

    for preview_path, (product_key, *_rest) in zip(PRODUCT_STEP_PATHS, PRODUCT_COMPONENTS):
        save_product_step(preview_path, product_key)
        saved_paths.append(preview_path)

    products_fig, products_animation = build_all_products_animation()
    products_animation.save(str(ALL_PRODUCTS_GIF_PATH.resolve()), writer=PillowWriter(fps=FPS))
    plt.close(products_fig)
    saved_paths.extend([ALL_PRODUCTS_PREVIEW_PATH, ALL_PRODUCTS_GIF_PATH])

    pair_fig, pair_animation = build_pair_animation()
    pair_animation.save(str(PAIR_GIF_PATH.resolve()), writer=PillowWriter(fps=FPS))
    plt.close(pair_fig)
    saved_paths.extend([PAIR_PREVIEW_PATH, PAIR_GIF_PATH])

    for path in saved_paths:
        print(path)


if __name__ == "__main__":
    main()
