from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.lines import Line2D


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "03_single_sideband_modulator" / "03b_ssb_hilbert_phasor_product"

INPUT_PREVIEW_PATH = OUTPUT_DIR / "01_direct_quadrature_inputs_preview.png"
INPUT_GIF_PATH = OUTPUT_DIR / "02_direct_quadrature_inputs.gif"
PRODUCT_INPUT_PATH = OUTPUT_DIR / "03_ssb_input_phasors_before_products.png"
PRODUCT_STEP_PATHS = [
    OUTPUT_DIR / "04_direct_product_sum_frequency.png",
    OUTPUT_DIR / "05_direct_product_difference_frequency.png",
    OUTPUT_DIR / "06_quadrature_product_sum_frequency_phase_inverted.png",
    OUTPUT_DIR / "07_quadrature_product_difference_frequency.png",
]
PAIR_PREVIEW_PATH = OUTPUT_DIR / "08_direct_and_quadrature_pair_sums_preview.png"
PAIR_GIF_PATH = OUTPUT_DIR / "09_direct_and_quadrature_pair_sums.gif"
USB_PREVIEW_PATH = OUTPUT_DIR / "10_usb_cancellation_preview.png"
USB_GIF_PATH = OUTPUT_DIR / "11_usb_cancellation_and_output.gif"
LSB_PREVIEW_PATH = OUTPUT_DIR / "12_lsb_cancellation_preview.png"
LSB_GIF_PATH = OUTPUT_DIR / "13_lsb_cancellation_and_output.gif"

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
HILBERT_CARRIER_POS_COLOR = CARRIER_POS_COLOR
HILBERT_CARRIER_NEG_COLOR = CARRIER_NEG_COLOR
HILBERT_MOD_POS_COLOR = MOD_POS_COLOR
HILBERT_MOD_NEG_COLOR = MOD_NEG_COLOR
QUADRATURE_SUM_COLOR = "#d27a2c"
QUADRATURE_DIFF_COLOR = "#e7ad73"
INPUT_GREY = "0.70"
DIRECT_SUM_GREEN = "#1f7a3f"
DIRECT_DIFF_GREEN = "#86b996"
OUTPUT_BLUE = "#0b4f9c"
CANCEL_GREY = "0.62"
MARKER_COLOR = "tab:red"
BASELINE_COLOR = "0.78"
GRID_ALPHA = 0.18

TITLE_SIZE = 18
LABEL_SIZE = 15
TICK_SIZE = 12
SUPTITLE_SIZE = 24
COMPLEX_LIMIT = 1.15
AMPLITUDE_LIMITS = (-1.1, 1.1)
PREVIEW_T = 0.18 * T_END

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


DIRECT_INPUTS = [
    ("x_pos", r"$X_+$", r"$+\omega_x$", CARRIER_POS_COLOR),
    ("x_neg", r"$X_-$", r"$-\omega_x$", CARRIER_NEG_COLOR),
    ("m_pos", r"$M_+$", r"$+\omega_m$", MOD_POS_COLOR),
    ("m_neg", r"$M_-$", r"$-\omega_m$", MOD_NEG_COLOR),
]

QUADRATURE_INPUTS = [
    ("xh_pos", r"$\hat{X}_+$", r"$+\omega_x-\pi/2$", HILBERT_CARRIER_POS_COLOR),
    ("xh_neg", r"$\hat{X}_-$", r"$-\omega_x+\pi/2$", HILBERT_CARRIER_NEG_COLOR),
    ("mh_pos", r"$\hat{M}_+$", r"$+\omega_m-\pi/2$", HILBERT_MOD_POS_COLOR),
    ("mh_neg", r"$\hat{M}_-$", r"$-\omega_m+\pi/2$", HILBERT_MOD_NEG_COLOR),
]

PRODUCT_TERMS = [
    ("d_sum_pos", ("x_pos", "m_pos"), r"$X_+M_+$", r"$+\omega_x+\omega_m$", DIRECT_SUM_GREEN),
    ("d_diff_pos", ("x_pos", "m_neg"), r"$X_+M_-$", r"$+\omega_x-\omega_m$", DIRECT_DIFF_GREEN),
    ("q_sum_pos", ("xh_pos", "mh_pos"), r"$\hat{X}_+\hat{M}_+$", r"$+\omega_x+\omega_m+\pi$", QUADRATURE_SUM_COLOR),
    ("q_diff_pos", ("xh_pos", "mh_neg"), r"$\hat{X}_+\hat{M}_-$", r"$+\omega_x-\omega_m$", QUADRATURE_DIFF_COLOR),
]

ALL_PRODUCT_PHASORS = [
    ("d_sum_pos", r"$X_+M_+$", DIRECT_SUM_GREEN),
    ("d_sum_neg", r"$X_-M_-$", DIRECT_SUM_GREEN),
    ("d_diff_pos", r"$X_+M_-$", DIRECT_DIFF_GREEN),
    ("d_diff_neg", r"$X_-M_+$", DIRECT_DIFF_GREEN),
    ("q_sum_pos", r"$\hat{X}_+\hat{M}_+$", QUADRATURE_SUM_COLOR),
    ("q_sum_neg", r"$\hat{X}_-\hat{M}_-$", QUADRATURE_SUM_COLOR),
    ("q_diff_pos", r"$\hat{X}_+\hat{M}_-$", QUADRATURE_DIFF_COLOR),
    ("q_diff_neg", r"$\hat{X}_-\hat{M}_+$", QUADRATURE_DIFF_COLOR),
]


def signal_components(times):
    times = np.asarray(times)
    x_pos = 0.5 * np.exp(1j * OMEGA_X * times)
    x_neg = 0.5 * np.exp(-1j * OMEGA_X * times)
    m_pos = 0.5 * np.exp(1j * OMEGA_M * times)
    m_neg = 0.5 * np.exp(-1j * OMEGA_M * times)

    # Hilbert/quadrature signals: sin(wt)
    xh_pos = -0.5j * np.exp(1j * OMEGA_X * times)
    xh_neg = 0.5j * np.exp(-1j * OMEGA_X * times)
    mh_pos = -0.5j * np.exp(1j * OMEGA_M * times)
    mh_neg = 0.5j * np.exp(-1j * OMEGA_M * times)

    return {
        "x_pos": x_pos,
        "x_neg": x_neg,
        "m_pos": m_pos,
        "m_neg": m_neg,
        "xh_pos": xh_pos,
        "xh_neg": xh_neg,
        "mh_pos": mh_pos,
        "mh_neg": mh_neg,
        "x": x_pos + x_neg,
        "m": m_pos + m_neg,
        "xh": xh_pos + xh_neg,
        "mh": mh_pos + mh_neg,
    }


def product_components(times):
    values = signal_components(times)
    d_sum_pos = values["x_pos"] * values["m_pos"]
    d_sum_neg = values["x_neg"] * values["m_neg"]
    d_diff_pos = values["x_pos"] * values["m_neg"]
    d_diff_neg = values["x_neg"] * values["m_pos"]

    q_sum_pos = values["xh_pos"] * values["mh_pos"]
    q_sum_neg = values["xh_neg"] * values["mh_neg"]
    q_diff_pos = values["xh_pos"] * values["mh_neg"]
    q_diff_neg = values["xh_neg"] * values["mh_pos"]

    direct_sum_pair = d_sum_pos + d_sum_neg
    direct_diff_pair = d_diff_pos + d_diff_neg
    quadrature_sum_pair = q_sum_pos + q_sum_neg
    quadrature_diff_pair = q_diff_pos + q_diff_neg
    direct_product = direct_sum_pair + direct_diff_pair
    quadrature_product = quadrature_sum_pair + quadrature_diff_pair

    usb_sum = direct_sum_pair - quadrature_sum_pair
    usb_diff = direct_diff_pair - quadrature_diff_pair
    usb = direct_product - quadrature_product
    lsb_sum = direct_sum_pair + quadrature_sum_pair
    lsb_diff = direct_diff_pair + quadrature_diff_pair
    lsb = direct_product + quadrature_product

    return {
        "d_sum_pos": d_sum_pos,
        "d_sum_neg": d_sum_neg,
        "d_diff_pos": d_diff_pos,
        "d_diff_neg": d_diff_neg,
        "q_sum_pos": q_sum_pos,
        "q_sum_neg": q_sum_neg,
        "q_diff_pos": q_diff_pos,
        "q_diff_neg": q_diff_neg,
        "direct_sum_pair": direct_sum_pair,
        "direct_diff_pair": direct_diff_pair,
        "quadrature_sum_pair": quadrature_sum_pair,
        "quadrature_diff_pair": quadrature_diff_pair,
        "direct_product": direct_product,
        "quadrature_product": quadrature_product,
        "usb_sum": usb_sum,
        "usb_diff": usb_diff,
        "usb": usb,
        "lsb_sum": lsb_sum,
        "lsb_diff": lsb_diff,
        "lsb": lsb,
    }


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


def setup_phasor_axis(ax, title, limit=COMPLEX_LIMIT, circle_radius=1.0):
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


def setup_time_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(T_START, T_END)
    ax.set_ylim(*AMPLITUDE_LIMITS)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def set_vector(line, tip, value):
    line.set_data([0.0, value.real], [0.0, value.imag])
    tip.set_data([value.real], [value.imag])


def draw_static_input_vectors(ax, current_values, active_keys=None):
    active_keys = set(current_values.keys()) if active_keys is None else set(active_keys)
    for key, label, phase_label, color in DIRECT_INPUTS + QUADRATURE_INPUTS:
        is_active = key in active_keys
        line_color = color if is_active else INPUT_GREY
        alpha = 1.0 if is_active else 0.24
        line_style = "-" if key in {item[0] for item in DIRECT_INPUTS} else "--"
        ax.plot(
            [0.0, current_values[key].real],
            [0.0, current_values[key].imag],
            color=line_color,
            lw=2.9 if is_active else 1.8,
            alpha=alpha,
            ls=line_style,
            label=f"{label}: {phase_label}",
        )
        ax.plot([current_values[key].real], [current_values[key].imag], "o", color=line_color, ms=7, alpha=alpha)


def build_input_animation():
    time_dense = np.linspace(T_START, T_END, 1000)
    time_frames = np.linspace(T_START, T_END, FRAMES, endpoint=False)
    values = signal_components(time_dense)

    fig, ax_phasor, ax_signal = create_two_panel_figure("Direct and Hilbert/quadrature input phasors")
    setup_phasor_axis(ax_phasor, "Input phasors")
    setup_time_axis(ax_signal, r"$x(t)$, $m(t)$ and quadrature signals")

    ax_signal.plot(time_dense, values["x"].real, color=CARRIER_POS_COLOR, lw=2.5, label=r"$x(t)$")
    ax_signal.plot(time_dense, values["m"].real, color=MOD_POS_COLOR, lw=2.5, label=r"$m(t)$")
    ax_signal.plot(time_dense, values["xh"].real, color=HILBERT_CARRIER_POS_COLOR, lw=2.1, ls="--", label=r"$\hat{x}(t)$")
    ax_signal.plot(time_dense, values["mh"].real, color=HILBERT_MOD_POS_COLOR, lw=2.1, ls="--", label=r"$\hat{m}(t)$")
    add_legend(ax_signal, loc="upper right", fontsize=10.5)

    lines = {}
    tips = {}
    for key, label, phase_label, color in DIRECT_INPUTS + QUADRATURE_INPUTS:
        line_style = "-" if key in {item[0] for item in DIRECT_INPUTS} else "--"
        lines[key], = ax_phasor.plot([], [], color=color, lw=2.5, ls=line_style, label=f"{label}: {phase_label}")
        tips[key], = ax_phasor.plot([], [], "o", color=color, ms=6)
    add_legend(ax_phasor, loc="lower left", fontsize=9.1)

    signal_marker = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    signal_points = {
        key: ax_signal.plot([], [], "o", color=color, ms=6)[0]
        for key, color in [
            ("x", CARRIER_POS_COLOR),
            ("m", MOD_POS_COLOR),
            ("xh", HILBERT_CARRIER_POS_COLOR),
            ("mh", HILBERT_MOD_POS_COLOR),
        ]
    }

    def draw_state(current_t):
        current = signal_components(np.array([current_t]))
        artists = [signal_marker, *signal_points.values()]
        for key in lines:
            set_vector(lines[key], tips[key], current[key][0])
            artists.extend([lines[key], tips[key]])
        signal_marker.set_xdata([current_t, current_t])
        for key in signal_points:
            signal_points[key].set_data([current_t], [current[key][0].real])
        return tuple(artists)

    def update(frame_index):
        return draw_state(time_frames[frame_index])

    draw_state(PREVIEW_T)
    fig.savefig(INPUT_PREVIEW_PATH, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    animation = FuncAnimation(fig, update, frames=len(time_frames), interval=1000 / FPS, blit=False)
    return fig, animation


def save_product_input_overview():
    current = signal_components(np.array([PREVIEW_T]))
    time_dense = np.linspace(T_START, T_END, 1000)
    values = signal_components(time_dense)

    fig, ax_phasor, ax_signal = create_two_panel_figure("SSB input phasors before multiplication")
    setup_phasor_axis(ax_phasor, "Direct and quadrature branches")
    setup_time_axis(ax_signal, "Time signals")
    draw_static_input_vectors(ax_phasor, {key: current[key][0] for key, *_ in DIRECT_INPUTS + QUADRATURE_INPUTS})
    add_legend(ax_phasor, loc="lower left", fontsize=9.1)
    ax_signal.plot(time_dense, values["x"].real, color=CARRIER_POS_COLOR, lw=2.5, label=r"$x(t)$")
    ax_signal.plot(time_dense, values["m"].real, color=MOD_POS_COLOR, lw=2.5, label=r"$m(t)$")
    ax_signal.plot(time_dense, values["xh"].real, color=HILBERT_CARRIER_POS_COLOR, lw=2.1, ls="--", label=r"$\hat{x}(t)$")
    ax_signal.plot(time_dense, values["mh"].real, color=HILBERT_MOD_POS_COLOR, lw=2.1, ls="--", label=r"$\hat{m}(t)$")
    ax_signal.axvline(PREVIEW_T, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    add_legend(ax_signal, loc="upper right", fontsize=10.5)
    fig.savefig(PRODUCT_INPUT_PATH, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_product_step(path, product_key):
    current_inputs = signal_components(np.array([PREVIEW_T]))
    current_products = product_components(np.array([PREVIEW_T]))
    key, input_pair, product_label, freq_label, color = next(item for item in PRODUCT_TERMS if item[0] == product_key)

    fig, ax_phasor, ax_signal = create_two_panel_figure(fr"Product step: {product_label} $\rightarrow$ {freq_label}")
    setup_phasor_axis(ax_phasor, "Length product and phase sum")
    setup_time_axis(ax_signal, "Time signal")
    draw_static_input_vectors(
        ax_phasor,
        {input_key: current_inputs[input_key][0] for input_key, *_ in DIRECT_INPUTS + QUADRATURE_INPUTS},
        active_keys=set(input_pair),
    )
    product_value = current_products[key][0]
    ax_phasor.plot([0.0, product_value.real], [0.0, product_value.imag], color=color, lw=4.0, label=product_label)
    ax_phasor.plot([product_value.real], [product_value.imag], "o", color=color, ms=8)
    add_legend(ax_phasor, loc="lower left", fontsize=9.4)
    fig.savefig(path, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def build_pair_sums_animation():
    time_dense = np.linspace(T_START, T_END, 1000)
    time_frames = np.linspace(T_START, T_END, FRAMES, endpoint=False)
    values = product_components(time_dense)

    fig, ax_phasor, ax_signal = create_two_panel_figure("Direct product and Hilbert/quadrature product")
    setup_phasor_axis(ax_phasor, "Product pairs and pair sums")
    setup_time_axis(ax_signal, "Pair-sum time signals")

    ax_signal.plot(time_dense, values["direct_sum_pair"].real, color=DIRECT_SUM_GREEN, lw=2.7, label=r"$d_\Sigma(t)$")
    ax_signal.plot(time_dense, values["direct_diff_pair"].real, color=DIRECT_DIFF_GREEN, lw=2.7, label=r"$d_\Delta(t)$")
    ax_signal.plot(time_dense, values["quadrature_sum_pair"].real, color=QUADRATURE_SUM_COLOR, lw=2.7, ls="--", label=r"$q_\Sigma(t)$")
    ax_signal.plot(time_dense, values["quadrature_diff_pair"].real, color=QUADRATURE_DIFF_COLOR, lw=2.7, ls="--", label=r"$q_\Delta(t)$")
    add_legend(ax_signal, loc="upper right", fontsize=10.5)

    product_lines = {}
    product_tips = {}
    for key, label, color in ALL_PRODUCT_PHASORS:
        product_lines[key], = ax_phasor.plot([], [], color=color, lw=2.0, alpha=0.42, label=label)
        product_tips[key], = ax_phasor.plot([], [], "o", color=color, ms=5.3, alpha=0.42)

    pair_specs = [
        ("direct_sum_pair", r"$d_\Sigma(t)$", DIRECT_SUM_GREEN),
        ("direct_diff_pair", r"$d_\Delta(t)$", DIRECT_DIFF_GREEN),
        ("quadrature_sum_pair", r"$q_\Sigma(t)$", QUADRATURE_SUM_COLOR),
        ("quadrature_diff_pair", r"$q_\Delta(t)$", QUADRATURE_DIFF_COLOR),
    ]
    pair_lines = {}
    pair_tips = {}
    for key, label, color in pair_specs:
        pair_lines[key], = ax_phasor.plot([], [], color=color, lw=3.4, label=label)
        pair_tips[key], = ax_phasor.plot([], [], "o", color=color, ms=7)
    add_legend(ax_phasor, loc="lower left", fontsize=8.7)

    marker = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    points = {key: ax_signal.plot([], [], "o", color=color, ms=6)[0] for key, _label, color in pair_specs}

    def draw_state(current_t):
        current = product_components(np.array([current_t]))
        artists = [marker, *points.values()]
        for key, _label, _color in ALL_PRODUCT_PHASORS:
            set_vector(product_lines[key], product_tips[key], current[key][0])
            artists.extend([product_lines[key], product_tips[key]])
        for key, _label, _color in pair_specs:
            set_vector(pair_lines[key], pair_tips[key], current[key][0])
            points[key].set_data([current_t], [current[key][0].real])
            artists.extend([pair_lines[key], pair_tips[key]])
        marker.set_xdata([current_t, current_t])
        return tuple(artists)

    def update(frame_index):
        return draw_state(time_frames[frame_index])

    draw_state(PREVIEW_T)
    fig.savefig(PAIR_PREVIEW_PATH, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    animation = FuncAnimation(fig, update, frames=len(time_frames), interval=1000 / FPS, blit=False)
    return fig, animation


def build_ssb_cancellation_animation(mode):
    time_dense = np.linspace(T_START, T_END, 1000)
    time_frames = np.linspace(T_START, T_END, FRAMES, endpoint=False)
    values = product_components(time_dense)
    if mode == "usb":
        preview_path = USB_PREVIEW_PATH
        title = "USB: direct product minus quadrature product"
        output_key = "usb"
        surviving_key = "usb_sum"
        cancelled_key = "usb_diff"
        surviving_label = r"$y_\mathrm{USB}(t)$"
        cancelled_label = r"cancelled difference"
    else:
        preview_path = LSB_PREVIEW_PATH
        title = "LSB: direct product plus quadrature product"
        output_key = "lsb"
        surviving_key = "lsb_diff"
        cancelled_key = "lsb_sum"
        surviving_label = r"$y_\mathrm{LSB}(t)$"
        cancelled_label = r"cancelled sum"

    fig, ax_phasor, ax_signal = create_two_panel_figure(title)
    setup_phasor_axis(ax_phasor, "Sideband cancellation")
    setup_time_axis(ax_signal, "SSB output")

    ax_signal.plot(time_dense, values[cancelled_key].real, color=CANCEL_GREY, lw=2.2, ls="--", label=cancelled_label)
    ax_signal.plot(time_dense, values[output_key].real, color=OUTPUT_BLUE, lw=3.2, label=surviving_label)
    add_legend(ax_signal, loc="upper right", fontsize=11)

    reference_specs = [
        ("direct_sum_pair", r"$d_\Sigma$", DIRECT_SUM_GREEN),
        ("direct_diff_pair", r"$d_\Delta$", DIRECT_DIFF_GREEN),
        ("quadrature_sum_pair", r"$q_\Sigma$", QUADRATURE_SUM_COLOR),
        ("quadrature_diff_pair", r"$q_\Delta$", QUADRATURE_DIFF_COLOR),
    ]
    ref_lines = {}
    ref_tips = {}
    for key, label, color in reference_specs:
        ref_lines[key], = ax_phasor.plot([], [], color=color, lw=2.2, alpha=0.35, label=label)
        ref_tips[key], = ax_phasor.plot([], [], "o", color=color, ms=5.5, alpha=0.35)
    cancel_line, = ax_phasor.plot([], [], color=CANCEL_GREY, lw=2.8, ls="--", label=cancelled_label)
    cancel_tip, = ax_phasor.plot([], [], "o", color=CANCEL_GREY, ms=6)
    output_line, = ax_phasor.plot([], [], color=OUTPUT_BLUE, lw=4.0, label=surviving_label)
    output_tip, = ax_phasor.plot([], [], "o", color=OUTPUT_BLUE, ms=8)
    add_legend(ax_phasor, loc="lower left", fontsize=8.9)

    marker = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    cancel_point, = ax_signal.plot([], [], "o", color=CANCEL_GREY, ms=6)
    output_point, = ax_signal.plot([], [], "o", color=OUTPUT_BLUE, ms=7)

    def draw_state(current_t):
        current = product_components(np.array([current_t]))
        artists = [marker, cancel_point, output_point]
        for key, _label, _color in reference_specs:
            set_vector(ref_lines[key], ref_tips[key], current[key][0])
            artists.extend([ref_lines[key], ref_tips[key]])
        set_vector(cancel_line, cancel_tip, current[cancelled_key][0])
        set_vector(output_line, output_tip, current[output_key][0])
        marker.set_xdata([current_t, current_t])
        cancel_point.set_data([current_t], [current[cancelled_key][0].real])
        output_point.set_data([current_t], [current[output_key][0].real])
        artists.extend([cancel_line, cancel_tip, output_line, output_tip])
        return tuple(artists)

    def update(frame_index):
        return draw_state(time_frames[frame_index])

    draw_state(PREVIEW_T)
    fig.savefig(preview_path, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    animation = FuncAnimation(fig, update, frames=len(time_frames), interval=1000 / FPS, blit=False)
    return fig, animation


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*"):
        if old_file.suffix.lower() in {".png", ".gif"}:
            old_file.unlink()

    saved_paths = []

    input_fig, input_animation = build_input_animation()
    input_animation.save(str(INPUT_GIF_PATH.resolve()), writer=PillowWriter(fps=FPS))
    plt.close(input_fig)
    saved_paths.extend([INPUT_PREVIEW_PATH, INPUT_GIF_PATH])

    save_product_input_overview()
    saved_paths.append(PRODUCT_INPUT_PATH)

    for path, (product_key, *_rest) in zip(PRODUCT_STEP_PATHS, PRODUCT_TERMS):
        save_product_step(path, product_key)
        saved_paths.append(path)

    pair_fig, pair_animation = build_pair_sums_animation()
    pair_animation.save(str(PAIR_GIF_PATH.resolve()), writer=PillowWriter(fps=FPS))
    plt.close(pair_fig)
    saved_paths.extend([PAIR_PREVIEW_PATH, PAIR_GIF_PATH])

    usb_fig, usb_animation = build_ssb_cancellation_animation("usb")
    usb_animation.save(str(USB_GIF_PATH.resolve()), writer=PillowWriter(fps=FPS))
    plt.close(usb_fig)
    saved_paths.extend([USB_PREVIEW_PATH, USB_GIF_PATH])

    lsb_fig, lsb_animation = build_ssb_cancellation_animation("lsb")
    lsb_animation.save(str(LSB_GIF_PATH.resolve()), writer=PillowWriter(fps=FPS))
    plt.close(lsb_fig)
    saved_paths.extend([LSB_PREVIEW_PATH, LSB_GIF_PATH])

    for path in saved_paths:
        print(path)


if __name__ == "__main__":
    main()
