from pathlib import Path
import shutil

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.lines import Line2D
from PIL import Image, ImageChops, ImageSequence


OUTPUT_ROOT = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "05_herleitung_und_dualitaet"
    / "05B_rueckweg_zur_faltung"
)

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (11.0, 4.8)
SWEEP_FIGSIZE = (11.0, 7.8)
PHASOR_FIGSIZE = (6.8, 6.8)
HELIX_FIGSIZE = (14.2, 8.8)
TITLE_SIZE = 24
LABEL_SIZE = 20
TIME_FREQ_LABEL_SIZE = 23
TICK_SIZE = 17
LEGEND_SIZE = 13
HELIX_TITLE_SIZE = 25
HELIX_LABEL_SIZE = 21
HELIX_TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
FUTURE_GREY = "0.72"
SPECTRUM_BLUE = "tab:blue"
IMAG_ORANGE = "tab:orange"
WINDOW_GREEN = "#66b77a"
ACTIVE_RED = "crimson"
BASELINE_COLOR = "0.75"
GRID_ALPHA = 0.25
PHASOR_GRID_ALPHA = 0.22
HELIX_SUM_COLOR = "#de8d8d"

TIME_VALUES = np.linspace(-1.5, 1.5, 6250)
FREQ_STEP = 0.005
FREQ_VALUES_EXT = np.arange(-12.0, 12.0 + 0.5 * FREQ_STEP, FREQ_STEP)
DISPLAY_MASK = np.abs(FREQ_VALUES_EXT) <= 6.0
FREQ_VALUES = FREQ_VALUES_EXT[DISPLAY_MASK]
COMMON_TIME_XTICKS = np.arange(-1.0, 1.01, 0.5)
COMMON_FREQ_XTICKS = np.arange(-6.0, 6.01, 2.0)
TIME_AMPLITUDE_LIMIT = 2.0
TIME_VIEW_LIMIT = 1.5
REFERENCE_MAGNITUDE_LIMIT = 1.1509281561303313

PROBE_F = 2.0
SIGNAL_COMPONENTS = [
    ("cos", 1.00, 2.0, np.pi / 4.0),
    ("cos", 0.85, 5.0, -np.pi / 2.0),
]
WINDOW_HALF_WIDTH = 1.0
WINDOW_DURATION = 2.0 * WINDOW_HALF_WIDTH
ANIMATION_FRAME_COUNT = 121
ANIMATION_FPS = 12
GIF_HOLD_FIRST_MS = 900
GIF_HOLD_LAST_MS = 1200
KERNEL_PHASOR_LIMIT = 1.25
OUTPUT_DIR = OUTPUT_ROOT / "2Hz"


def clear_owned_outputs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT_DIR.glob("*"):
        if path.is_file() and path.suffix.lower() in {".png", ".gif"}:
            path.unlink()


def clear_root_file_outputs():
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT_ROOT.glob("*"):
        if path.is_file() and path.suffix.lower() in {".png", ".gif"}:
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def create_figure(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    if figsize == SPECTRUM_FIGSIZE:
        fig.subplots_adjust(left=0.09, right=0.99, bottom=0.14, top=0.90)
    elif figsize == PHASOR_FIGSIZE:
        fig.subplots_adjust(left=0.13, right=0.97, bottom=0.12, top=0.92)
    return fig, ax


def create_time_reference_figure():
    return plt.subplots(figsize=TIME_FIGSIZE)


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def save_animation(animation, filename):
    writer = PillowWriter(fps=ANIMATION_FPS)
    animation.save(str((OUTPUT_DIR / filename).resolve()), writer=writer)


def apply_standard_gif_timing(filename):
    gif_path = OUTPUT_DIR / filename
    with Image.open(gif_path) as gif:
        frames = [frame.convert("P", palette=Image.Palette.ADAPTIVE) for frame in ImageSequence.Iterator(gif)]
        loop = gif.info.get("loop", 0)

    durations = [int(round(1000 / ANIMATION_FPS))] * len(frames)
    if durations:
        durations[0] = GIF_HOLD_FIRST_MS
        durations[-1] = GIF_HOLD_LAST_MS

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        loop=loop,
        duration=durations,
        optimize=False,
        disposal=2,
    )


def render_figure_tight(fig):
    from io import BytesIO

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=DPI, bbox_inches="tight", facecolor="white")
    buffer.seek(0)
    with Image.open(buffer) as image:
        return image.convert("RGBA").copy()


def crop_gif_whitespace(filename, background=(255, 255, 255), tolerance=6):
    gif_path = OUTPUT_DIR / filename
    with Image.open(gif_path) as gif:
        frames = [frame.convert("RGB") for frame in ImageSequence.Iterator(gif)]
        durations = [frame.info.get("duration", gif.info.get("duration", int(1000 / ANIMATION_FPS))) for frame in ImageSequence.Iterator(gif)]
        loop = gif.info.get("loop", 0)

    union_bbox = None
    for frame in frames:
        bg = Image.new("RGB", frame.size, background)
        diff = ImageChops.difference(frame, bg)
        if tolerance > 0:
            diff = diff.point(lambda p: 0 if p <= tolerance else 255)
        bbox = diff.getbbox()
        if bbox is None:
            continue
        if union_bbox is None:
            union_bbox = bbox
        else:
            union_bbox = (
                min(union_bbox[0], bbox[0]),
                min(union_bbox[1], bbox[1]),
                max(union_bbox[2], bbox[2]),
                max(union_bbox[3], bbox[3]),
            )

    if union_bbox is None:
        return

    cropped_frames = [frame.crop(union_bbox) for frame in frames]
    cropped_frames[0].save(
        gif_path,
        save_all=True,
        append_images=cropped_frames[1:],
        loop=loop,
        duration=durations,
        optimize=False,
    )


def pad_gif_to_reference_size(gif_filename, reference_filename, background=(255, 255, 255)):
    gif_path = OUTPUT_DIR / gif_filename
    reference_path = OUTPUT_DIR / reference_filename
    with Image.open(reference_path) as ref:
        target_size = ref.size

    with Image.open(gif_path) as gif:
        frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif)]
        durations = [frame.info.get("duration", gif.info.get("duration", int(1000 / ANIMATION_FPS))) for frame in ImageSequence.Iterator(gif)]
        loop = gif.info.get("loop", 0)

    padded_frames = []
    for frame in frames:
        canvas = Image.new("RGBA", target_size, background + (255,))
        offset = (
            max(0, (target_size[0] - frame.width) // 2),
            max(0, (target_size[1] - frame.height) // 2),
        )
        canvas.alpha_composite(frame, dest=offset)
        padded_frames.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE))

    padded_frames[0].save(
        gif_path,
        save_all=True,
        append_images=padded_frames[1:],
        loop=loop,
        duration=durations,
        optimize=False,
        disposal=2,
    )


def save_manual_tight_gif(fig, update_func, filename, reference_filename):
    frames = []
    durations = []
    for frame_idx in range(len(ANIMATION_INDICES)):
        update_func(frame_idx)
        frames.append(render_figure_tight(fig))
        durations.append(int(round(1000 / ANIMATION_FPS)))

    durations[0] = GIF_HOLD_FIRST_MS
    durations[-1] = GIF_HOLD_LAST_MS
    gif_path = OUTPUT_DIR / filename
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )
    pad_gif_to_reference_size(filename, reference_filename)


def save_manual_tight_gif_auto(fig, update_func, filename, frame_indices):
    frames = []
    durations = []
    for frame_idx in range(len(frame_indices)):
        update_func(frame_idx)
        frames.append(render_figure_tight(fig))
        durations.append(int(round(1000 / ANIMATION_FPS)))

    durations[0] = GIF_HOLD_FIRST_MS
    durations[-1] = GIF_HOLD_LAST_MS
    max_width = max(frame.width for frame in frames)
    max_height = max(frame.height for frame in frames)
    padded_frames = []
    for frame in frames:
        canvas = Image.new("RGBA", (max_width, max_height), (255, 255, 255, 255))
        offset = ((max_width - frame.width) // 2, (max_height - frame.height) // 2)
        canvas.alpha_composite(frame, dest=offset)
        padded_frames.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE))

    gif_path = OUTPUT_DIR / filename
    padded_frames[0].save(
        gif_path,
        save_all=True,
        append_images=padded_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )


def save_last_gif_frame_as_png(gif_filename, png_filename):
    gif_path = OUTPUT_DIR / gif_filename
    png_path = OUTPUT_DIR / png_filename
    with Image.open(gif_path) as gif:
        frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif)]
    frames[-1].save(png_path)


def save_first_gif_frame_as_png(gif_filename, png_filename):
    gif_path = OUTPUT_DIR / gif_filename
    png_path = OUTPUT_DIR / png_filename
    with Image.open(gif_path) as gif:
        frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif)]
    frames[0].save(png_path)


def add_inset_legend(ax, handles, loc="upper right"):
    ax.legend(
        handles=handles,
        loc=loc,
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
        borderaxespad=0.6,
    )


def raw_signal_x_t(values):
    signal = np.zeros_like(values)
    for kind, amplitude, frequency_hz, phase_rad in SIGNAL_COMPONENTS:
        angle = 2.0 * np.pi * frequency_hz * values + phase_rad
        if kind == "cos":
            signal += amplitude * np.cos(angle)
        elif kind == "sin":
            signal += amplitude * np.sin(angle)
        else:
            raise ValueError(f"Unknown signal type: {kind}")
    return signal


def signal_x_t(values):
    return raw_signal_x_t(values)


def window_w_t(values):
    return (np.abs(values) <= WINDOW_HALF_WIDTH).astype(float)


def line_spectrum_from_components(components):
    line_map = {}
    for kind, amplitude, frequency_hz, phase_rad in components:
        if kind == "cos":
            positive = 0.5 * amplitude * np.exp(1j * phase_rad)
            negative = 0.5 * amplitude * np.exp(-1j * phase_rad)
        elif kind == "sin":
            positive = -0.5j * amplitude * np.exp(1j * phase_rad)
            negative = 0.5j * amplitude * np.exp(-1j * phase_rad)
        else:
            raise ValueError(f"Unknown signal type: {kind}")
        line_map[frequency_hz] = line_map.get(frequency_hz, 0.0 + 0.0j) + positive
        line_map[-frequency_hz] = line_map.get(-frequency_hz, 0.0 + 0.0j) + negative
    line_freqs = np.array(sorted(line_map.keys()), dtype=float)
    line_coeffs = np.array([line_map[freq] for freq in line_freqs], dtype=np.complex128)
    return line_freqs, line_coeffs


def continuous_ft(time_values, signal_values, freq_values, chunk_size=120):
    result = np.zeros_like(freq_values, dtype=np.complex128)
    for start in range(0, len(freq_values), chunk_size):
        stop = min(start + chunk_size, len(freq_values))
        freq_chunk = freq_values[start:stop]
        phase_matrix = np.exp(-1j * 2.0 * np.pi * freq_chunk[:, None] * time_values[None, :])
        integrand = phase_matrix * signal_values[None, :]
        result[start:stop] = np.trapezoid(integrand, time_values, axis=1)
    return result


def interp_complex(x_values, complex_values, x_target):
    real_part = np.interp(x_target, x_values, complex_values.real)
    imag_part = np.interp(x_target, x_values, complex_values.imag)
    return real_part + 1j * imag_part


SIGNAL_VALUES = signal_x_t(TIME_VALUES)
WINDOW_VALUES = window_w_t(TIME_VALUES)
OBSERVED_VALUES = SIGNAL_VALUES * WINDOW_VALUES
COS_BASIS = np.cos(2.0 * np.pi * PROBE_F * TIME_VALUES)
MINUS_SIN_BASIS = -np.sin(2.0 * np.pi * PROBE_F * TIME_VALUES)
REAL_PRODUCT = OBSERVED_VALUES * COS_BASIS
IMAG_PRODUCT = OBSERVED_VALUES * MINUS_SIN_BASIS
REAL_INTEGRAL = float(np.trapezoid(REAL_PRODUCT, TIME_VALUES))
IMAG_INTEGRAL = float(np.trapezoid(IMAG_PRODUCT, TIME_VALUES))
Y_FIXED_TIME = REAL_INTEGRAL + 1j * IMAG_INTEGRAL

KERNEL_REAL_VALUES = WINDOW_VALUES * COS_BASIS
KERNEL_IMAG_VALUES = WINDOW_VALUES * MINUS_SIN_BASIS

X_LINE_FREQS, X_LINE_COEFFS = line_spectrum_from_components(SIGNAL_COMPONENTS)
W_VALUES_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * FREQ_VALUES_EXT)
W_SHIFT_POS_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (FREQ_VALUES_EXT - PROBE_F))
W_SHIFT_NEG_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (FREQ_VALUES_EXT + PROBE_F))
KERNEL_REAL_SPECTRUM_EXT = 0.5 * (W_SHIFT_POS_EXT + W_SHIFT_NEG_EXT)
KERNEL_IMAG_SPECTRUM_COMPONENT_EXT = 0.5 * (W_SHIFT_POS_EXT - W_SHIFT_NEG_EXT)
G_VALUES_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (PROBE_F - FREQ_VALUES_EXT))
Y_VALUES_EXT = np.zeros_like(FREQ_VALUES_EXT, dtype=np.complex128)
for line_freq, line_coeff in zip(X_LINE_FREQS, X_LINE_COEFFS):
    Y_VALUES_EXT += line_coeff * WINDOW_DURATION * np.sinc(WINDOW_DURATION * (FREQ_VALUES_EXT - line_freq))

G_AT_LINE_FREQS = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (PROBE_F - X_LINE_FREQS))
WEIGHTED_LINE_COEFFS = X_LINE_COEFFS * G_AT_LINE_FREQS
Y_FIXED_FREQ = np.sum(WEIGHTED_LINE_COEFFS)

Y_VALUES = Y_VALUES_EXT[DISPLAY_MASK]
W_VALUES = W_VALUES_EXT[DISPLAY_MASK]
KERNEL_REAL_SPECTRUM = KERNEL_REAL_SPECTRUM_EXT[DISPLAY_MASK]
KERNEL_IMAG_SPECTRUM_COMPONENT = KERNEL_IMAG_SPECTRUM_COMPONENT_EXT[DISPLAY_MASK]
G_VALUES = G_VALUES_EXT[DISPLAY_MASK]

SIGNAL_LIMIT = TIME_AMPLITUDE_LIMIT
WINDOW_LIMIT = TIME_AMPLITUDE_LIMIT
PRODUCT_LIMIT = TIME_AMPLITUDE_LIMIT
KERNEL_TIME_LIMIT = TIME_AMPLITUDE_LIMIT
COMMON_SPECTRUM_LIMIT = 0.5 * np.ceil(
    2.0
    * 1.15
    * max(
        np.max(np.abs(np.real(X_LINE_COEFFS))),
        np.max(np.abs(np.imag(X_LINE_COEFFS))),
        np.max(np.abs(np.real(WEIGHTED_LINE_COEFFS))),
        np.max(np.abs(np.imag(WEIGHTED_LINE_COEFFS))),
        np.max(np.abs(W_VALUES)),
        np.max(np.abs(G_VALUES)),
        np.max(np.abs(Y_VALUES)),
        1e-6,
    )
)
REAL_SPECTRUM_LIMIT = COMMON_SPECTRUM_LIMIT
IMAG_SPECTRUM_LIMIT = COMMON_SPECTRUM_LIMIT
KERNEL_SPECTRUM_LIMIT = COMMON_SPECTRUM_LIMIT
MAGNITUDE_SPECTRUM_LIMIT = REFERENCE_MAGNITUDE_LIMIT
SIGNED_SPECTRUM_YTICKS = np.arange(-COMMON_SPECTRUM_LIMIT, COMMON_SPECTRUM_LIMIT + 0.001, 0.5)
MAGNITUDE_SPECTRUM_YTICKS = np.arange(0.0, COMMON_SPECTRUM_LIMIT + 0.001, 0.5)
COMPLEX_LIMIT = 1.15 * max(
    1.0,
    np.abs(Y_FIXED_TIME.real),
    np.abs(Y_FIXED_TIME.imag),
    np.abs(Y_FIXED_FREQ.real),
    np.abs(Y_FIXED_FREQ.imag),
    1e-6,
)
ANIMATION_INDICES = np.linspace(0, len(TIME_VALUES) - 1, ANIMATION_FRAME_COUNT).astype(int)
FREQ_ANIMATION_INDICES = np.linspace(0, len(FREQ_VALUES) - 1, ANIMATION_FRAME_COUNT).astype(int)


def first_sidelobe_offset_hz():
    sample_offsets = np.linspace(0.5001, 0.9999, 20000)
    sidelobe_values = np.abs(WINDOW_DURATION * np.sinc(WINDOW_DURATION * sample_offsets))
    return float(sample_offsets[np.argmax(sidelobe_values)])


def frequency_slug(value):
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return text.replace(".", "p")


def configure_series(probe_f, folder_name):
    global OUTPUT_DIR
    global PROBE_F
    global COS_BASIS
    global MINUS_SIN_BASIS
    global REAL_PRODUCT
    global IMAG_PRODUCT
    global REAL_INTEGRAL
    global IMAG_INTEGRAL
    global Y_FIXED_TIME
    global KERNEL_REAL_VALUES
    global KERNEL_IMAG_VALUES
    global W_SHIFT_POS_EXT
    global W_SHIFT_NEG_EXT
    global KERNEL_REAL_SPECTRUM_EXT
    global KERNEL_IMAG_SPECTRUM_COMPONENT_EXT
    global G_VALUES_EXT
    global Y_VALUES_EXT
    global G_AT_LINE_FREQS
    global WEIGHTED_LINE_COEFFS
    global Y_FIXED_FREQ
    global Y_VALUES
    global KERNEL_REAL_SPECTRUM
    global KERNEL_IMAG_SPECTRUM_COMPONENT
    global G_VALUES
    global COMPLEX_LIMIT

    OUTPUT_DIR = OUTPUT_ROOT / folder_name
    PROBE_F = probe_f

    COS_BASIS = np.cos(2.0 * np.pi * PROBE_F * TIME_VALUES)
    MINUS_SIN_BASIS = -np.sin(2.0 * np.pi * PROBE_F * TIME_VALUES)
    REAL_PRODUCT = OBSERVED_VALUES * COS_BASIS
    IMAG_PRODUCT = OBSERVED_VALUES * MINUS_SIN_BASIS
    REAL_INTEGRAL = float(np.trapezoid(REAL_PRODUCT, TIME_VALUES))
    IMAG_INTEGRAL = float(np.trapezoid(IMAG_PRODUCT, TIME_VALUES))
    Y_FIXED_TIME = REAL_INTEGRAL + 1j * IMAG_INTEGRAL

    KERNEL_REAL_VALUES = WINDOW_VALUES * COS_BASIS
    KERNEL_IMAG_VALUES = WINDOW_VALUES * MINUS_SIN_BASIS

    W_SHIFT_POS_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (FREQ_VALUES_EXT - PROBE_F))
    W_SHIFT_NEG_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (FREQ_VALUES_EXT + PROBE_F))
    KERNEL_REAL_SPECTRUM_EXT = 0.5 * (W_SHIFT_POS_EXT + W_SHIFT_NEG_EXT)
    KERNEL_IMAG_SPECTRUM_COMPONENT_EXT = 0.5 * (W_SHIFT_POS_EXT - W_SHIFT_NEG_EXT)
    G_VALUES_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (PROBE_F - FREQ_VALUES_EXT))
    Y_VALUES_EXT = np.zeros_like(FREQ_VALUES_EXT, dtype=np.complex128)
    for line_freq, line_coeff in zip(X_LINE_FREQS, X_LINE_COEFFS):
        Y_VALUES_EXT += line_coeff * WINDOW_DURATION * np.sinc(WINDOW_DURATION * (FREQ_VALUES_EXT - line_freq))

    G_AT_LINE_FREQS = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (PROBE_F - X_LINE_FREQS))
    WEIGHTED_LINE_COEFFS = X_LINE_COEFFS * G_AT_LINE_FREQS
    Y_FIXED_FREQ = np.sum(WEIGHTED_LINE_COEFFS)

    Y_VALUES = Y_VALUES_EXT[DISPLAY_MASK]
    KERNEL_REAL_SPECTRUM = KERNEL_REAL_SPECTRUM_EXT[DISPLAY_MASK]
    KERNEL_IMAG_SPECTRUM_COMPONENT = KERNEL_IMAG_SPECTRUM_COMPONENT_EXT[DISPLAY_MASK]
    G_VALUES = G_VALUES_EXT[DISPLAY_MASK]
    COMPLEX_LIMIT = 1.15 * max(
        1.0,
        np.abs(Y_FIXED_TIME.real),
        np.abs(Y_FIXED_TIME.imag),
        np.abs(Y_FIXED_FREQ.real),
        np.abs(Y_FIXED_FREQ.imag),
        1e-6,
    )


def style_time_axis(ax, title, y_limit, y_label="Amplitude"):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-TIME_VIEW_LIMIT, TIME_VIEW_LIMIT)
    ax.set_ylim(-y_limit, y_limit)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=TIME_FREQ_LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=TIME_FREQ_LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_window_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-TIME_VIEW_LIMIT, TIME_VIEW_LIMIT)
    ax.set_ylim(-WINDOW_LIMIT, WINDOW_LIMIT)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=TIME_FREQ_LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=TIME_FREQ_LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_signed_frequency_axis(ax, title, y_limit, y_label, x_label=r"Auxiliary frequency $\nu$ [Hz]"):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(FREQ_VALUES[0], FREQ_VALUES[-1])
    ax.set_ylim(-y_limit, y_limit)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel(x_label, fontsize=TIME_FREQ_LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=TIME_FREQ_LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_magnitude_frequency_axis(ax, title, y_limit, y_label="Magnitude", x_label="Frequency f [Hz]"):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(FREQ_VALUES[0], FREQ_VALUES[-1])
    ax.set_ylim(0.0, y_limit)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel(x_label, fontsize=TIME_FREQ_LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=TIME_FREQ_LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_complex_plane_axis(ax, title, x_label=r"Re$\{Y(f)\}$", y_label=r"Im$\{Y(f)\}$", limit=None):
    axis_limit = COMPLEX_LIMIT if limit is None else limit
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.axvline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-axis_limit, axis_limit)
    ax.set_ylim(-axis_limit, axis_limit)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=PHASOR_GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE + 2)
    ax.set_xlabel(x_label, fontsize=LABEL_SIZE + 2, color=SPECTRUM_BLUE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE + 2, color=IMAG_ORANGE)
    ax.tick_params(axis="x", colors=SPECTRUM_BLUE, labelsize=TICK_SIZE + 2)
    ax.tick_params(axis="y", colors=IMAG_ORANGE, labelsize=TICK_SIZE + 2)


def create_sweep_figure():
    fig, (ax_top, ax_bottom) = plt.subplots(
        2,
        1,
        figsize=SWEEP_FIGSIZE,
        gridspec_kw={"height_ratios": [1.0, 1.0]},
    )
    fig.subplots_adjust(left=0.09, right=0.99, bottom=0.08, top=0.93, hspace=0.58)
    return fig, ax_top, ax_bottom


def setup_time_kernel_animation_figure(title):
    fig, ax = create_time_reference_figure()
    style_time_axis(ax, title, KERNEL_TIME_LIMIT)
    return fig, ax


def draw_spectral_lines(ax, frequencies, values, color, lw=3.0, alpha=1.0):
    ax.vlines(frequencies, 0.0, values, color=color, lw=lw, alpha=alpha)


def export_signal_x_t():
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLACK, lw=2.2)
    style_time_axis(ax, r"Signal $x(t)$", SIGNAL_LIMIT)
    save_figure(fig, "01_signal_x_t.png")


def export_window_w_t():
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=2.6)
    style_window_axis(ax, r"Window $w(t)$")
    save_figure(fig, "02_window_w_t.png")


def export_observed_signal_x_obs_t():
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=FUTURE_GREY, lw=1.8)
    ax.plot(TIME_VALUES, OBSERVED_VALUES, color=SIGNAL_BLACK, lw=2.2)
    style_time_axis(ax, r"Observed signal $x_{obs}(t)=x(t)w(t)$", SIGNAL_LIMIT)
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.8, label=r"$x(t)$"),
            Line2D([0], [0], color=SIGNAL_BLACK, lw=2.2, label=r"$x_{obs}(t)$"),
        ],
        loc="upper left",
    )
    save_figure(fig, "03_observed_signal_x_obs_t.png")


def export_observed_with_basis(filename, basis_values, color, title, basis_label):
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, OBSERVED_VALUES, color=SIGNAL_BLACK, lw=2.2)
    ax.plot(TIME_VALUES, basis_values, color=color, lw=1.9, ls="--")
    style_time_axis(ax, title, SIGNAL_LIMIT)
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=SIGNAL_BLACK, lw=2.2, label=r"$x_{obs}(t)$"),
            Line2D([0], [0], color=color, lw=1.9, ls="--", label=basis_label),
        ],
        loc="upper left",
    )
    save_figure(fig, filename)


def export_product_plot(filename, values, color, title, y_label):
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, values, color=color, lw=2.2)
    style_time_axis(ax, title, PRODUCT_LIMIT, y_label)
    save_figure(fig, filename)


def export_integral_plot(filename, values, integral_value, color, title, y_label):
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, values, color=color, lw=2.1)
    ax.fill_between(
        TIME_VALUES,
        0.0,
        values,
        where=values >= 0.0,
        color=color,
        alpha=0.22,
        interpolate=True,
    )
    ax.fill_between(
        TIME_VALUES,
        0.0,
        values,
        where=values < 0.0,
        color="tab:red",
        alpha=0.16,
        interpolate=True,
    )
    ax.plot([TIME_VALUES[0], TIME_VALUES[-1]], [integral_value, integral_value], color=color, lw=2.0, ls="--")
    style_time_axis(ax, title, PRODUCT_LIMIT, y_label)
    save_figure(fig, filename)


def export_complex_value(filename, value, title):
    fig, ax = create_figure(PHASOR_FIGSIZE)
    ax.plot([0.0, value.real], [0.0, value.imag], color=ACTIVE_RED, lw=3.0)
    ax.plot([value.real], [value.imag], "o", color=ACTIVE_RED, ms=8)
    ax.plot([0.0, value.real], [0.0, 0.0], color=SPECTRUM_BLUE, lw=1.5, alpha=0.85)
    ax.plot([value.real, value.real], [0.0, value.imag], color=IMAG_ORANGE, lw=1.5, alpha=0.85)
    style_complex_plane_axis(ax, title)
    save_figure(fig, filename)


def export_complex_value_animation():
    fig, ax = create_figure(PHASOR_FIGSIZE)
    style_complex_plane_axis(ax, r"Complex value $Y(f)$")
    phasor_line, = ax.plot([], [], color=ACTIVE_RED, lw=3.0)
    phasor_point, = ax.plot([], [], "o", color=ACTIVE_RED, ms=8)
    real_projection, = ax.plot([], [], color=SPECTRUM_BLUE, lw=1.5, alpha=0.85)
    imag_projection, = ax.plot([], [], color=IMAG_ORANGE, lw=1.5, alpha=0.85)
    frequency_text = ax.text(
        0.97,
        0.95,
        "",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=LEGEND_SIZE + 1,
        bbox={"facecolor": "white", "edgecolor": "0.80", "alpha": 0.95},
    )

    def update(frame_idx):
        freq_idx = FREQ_ANIMATION_INDICES[frame_idx]
        current_f = FREQ_VALUES[freq_idx]
        current_value = Y_VALUES[freq_idx]

        phasor_line.set_data([0.0, current_value.real], [0.0, current_value.imag])
        phasor_point.set_data([current_value.real], [current_value.imag])
        real_projection.set_data([0.0, current_value.real], [0.0, 0.0])
        imag_projection.set_data([current_value.real, current_value.real], [0.0, current_value.imag])
        frequency_text.set_text(rf"$f={frequency_label(current_f)}$ Hz")
        return phasor_line, phasor_point, real_projection, imag_projection, frequency_text

    save_manual_tight_gif(
        fig,
        update,
        "15A_complex_value_Y_f_animation.gif",
        "15_complex_value_Y_f_from_frequency.png",
    )
    plt.close(fig)


def export_kernel_time_plot(filename, values, color, title, kernel_label, continuation_values=None, continuation_label=None):
    fig, ax = create_time_reference_figure()
    ax.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=1.8, alpha=0.8)
    ax.plot(TIME_VALUES, values, color=color, lw=2.2)
    if continuation_values is not None:
        outside_window = WINDOW_VALUES < 0.5
        continuation_plot_values = np.where(outside_window, continuation_values, np.nan)
        ax.plot(TIME_VALUES, continuation_plot_values, color=color, lw=1.8, ls="--", alpha=0.9)
    style_time_axis(ax, title, KERNEL_TIME_LIMIT)
    legend_handles = [
        Line2D([0], [0], color=WINDOW_GREEN, lw=1.8, label=r"$w(t)$"),
        Line2D([0], [0], color=color, lw=2.2, label=kernel_label),
    ]
    if continuation_values is not None and continuation_label is not None:
        legend_handles.append(
            Line2D([0], [0], color=color, lw=1.8, ls="--", label=continuation_label)
        )
    add_inset_legend(ax, legend_handles, loc="upper left")
    save_figure(fig, filename)


def export_kernel_basis_only_plot(filename, basis_values, color, title, basis_label):
    fig, ax = create_time_reference_figure()
    ax.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=2.2)
    ax.plot(TIME_VALUES, basis_values, color=color, lw=1.9, ls="--")
    style_time_axis(ax, title, KERNEL_TIME_LIMIT)
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.2, label=r"$w(t)$"),
            Line2D([0], [0], color=color, lw=1.9, ls="--", label=basis_label),
        ],
        loc="upper left",
    )
    save_figure(fig, filename)


def export_real_kernel_animation():
    fig, ax_time = setup_time_kernel_animation_figure(
        rf"Windowed real kernel at $f={frequency_label(PROBE_F)}$ Hz"
    )
    ax_time.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=1.8, alpha=0.85)
    ax_time.plot(TIME_VALUES, KERNEL_REAL_VALUES, color=SPECTRUM_BLUE, lw=2.2)
    current_time_line = ax_time.axvline(TIME_VALUES[0], color=ACTIVE_RED, lw=1.8, ls="--", alpha=0.55)
    current_time_point, = ax_time.plot([], [], "o", color=SPECTRUM_BLUE, ms=7)
    add_inset_legend(
        ax_time,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=1.8, label=r"$w(t)$"),
            Line2D([0], [0], color=SPECTRUM_BLUE, lw=2.2, label=r"$g_{f,\mathrm{real}}(t)$"),
        ],
        loc="upper left",
    )

    def update(frame_idx):
        sample_idx = ANIMATION_INDICES[frame_idx]
        current_t = TIME_VALUES[sample_idx]
        current_value = KERNEL_REAL_VALUES[sample_idx]
        current_time_line.set_xdata([current_t, current_t])
        current_time_point.set_data([current_t], [current_value])
        return current_time_line, current_time_point

    save_manual_tight_gif(fig, update, "05_windowed_real_kernel_g_f.gif", "03_windowed_real_kernel_g_f.png")
    plt.close(fig)
    save_last_gif_frame_as_png("05_windowed_real_kernel_g_f.gif", "05_windowed_real_kernel_g_f_t_max.png")


def export_imag_kernel_animation():
    fig, ax_time = setup_time_kernel_animation_figure(
        rf"Windowed imaginary kernel at $f={frequency_label(PROBE_F)}$ Hz"
    )
    ax_time.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=1.8, alpha=0.85)
    ax_time.plot(TIME_VALUES, KERNEL_IMAG_VALUES, color=IMAG_ORANGE, lw=2.2)
    current_time_line = ax_time.axvline(TIME_VALUES[0], color=ACTIVE_RED, lw=1.8, ls="--", alpha=0.55)
    current_time_point, = ax_time.plot([], [], "o", color=IMAG_ORANGE, ms=7)
    add_inset_legend(
        ax_time,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=1.8, label=r"$w(t)$"),
            Line2D([0], [0], color=IMAG_ORANGE, lw=2.2, label=r"$g_{f,\mathrm{imag}}(t)$"),
        ],
        loc="upper left",
    )

    def update(frame_idx):
        sample_idx = ANIMATION_INDICES[frame_idx]
        current_t = TIME_VALUES[sample_idx]
        current_value = KERNEL_IMAG_VALUES[sample_idx]
        current_time_line.set_xdata([current_t, current_t])
        current_time_point.set_data([current_t], [current_value])
        return current_time_line, current_time_point

    save_manual_tight_gif(fig, update, "06_windowed_imag_kernel_g_f.gif", "04_windowed_imag_kernel_g_f.png")
    plt.close(fig)
    save_last_gif_frame_as_png("06_windowed_imag_kernel_g_f.gif", "06_windowed_imag_kernel_g_f_t_max.png")


def export_complex_kernel_helix_animation():
    fig = plt.figure(figsize=HELIX_FIGSIZE, facecolor="white")
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(1.0)
    fig.subplots_adjust(left=0.03, right=0.96, bottom=0.08, top=0.90)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("white")
    ax.set_box_aspect((3.9, 1.55, 1.55))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 1.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 1.0))

    ax.plot(TIME_VALUES, KERNEL_REAL_VALUES, KERNEL_IMAG_VALUES, color=HELIX_SUM_COLOR, lw=2.8)
    ax.plot(TIME_VALUES, KERNEL_REAL_VALUES, np.zeros_like(TIME_VALUES), color=SPECTRUM_BLUE, lw=1.7, alpha=0.8)
    ax.plot(TIME_VALUES, np.zeros_like(TIME_VALUES), KERNEL_IMAG_VALUES, color=IMAG_ORANGE, lw=1.7, alpha=0.8)

    helix_trace, = ax.plot([], [], [], color=ACTIVE_RED, lw=2.2)
    helix_point, = ax.plot([], [], [], "o", color=ACTIVE_RED, ms=6)
    proj_im_line, = ax.plot([], [], [], color=IMAG_ORANGE, lw=1.6, alpha=0.9)
    proj_re_line, = ax.plot([], [], [], color=SPECTRUM_BLUE, lw=1.6, alpha=0.9)

    ax.set_xlim(TIME_VALUES[0], TIME_VALUES[-1])
    ax.set_ylim(-KERNEL_PHASOR_LIMIT, KERNEL_PHASOR_LIMIT)
    ax.set_zlim(-KERNEL_PHASOR_LIMIT, KERNEL_PHASOR_LIMIT)
    component_ticks = np.arange(-1.0, 1.01, 0.5)
    ax.set_yticks(component_ticks)
    ax.set_zticks(component_ticks)
    ax.set_xlabel("Time t [s]", fontsize=HELIX_LABEL_SIZE, labelpad=22)
    ax.set_ylabel(r"Re$\{g_f(t)\}$", fontsize=HELIX_LABEL_SIZE, color=SPECTRUM_BLUE, labelpad=18)
    ax.set_zlabel(r"Im$\{g_f(t)\}$", fontsize=HELIX_LABEL_SIZE, color=IMAG_ORANGE, labelpad=10)
    ax.set_title(r"Complex analysis kernel $g_f(t)$", y=0.92, pad=-6, fontsize=HELIX_TITLE_SIZE)
    ax.tick_params(axis="x", labelsize=HELIX_TICK_SIZE, pad=4)
    ax.tick_params(axis="y", labelsize=HELIX_TICK_SIZE, colors=SPECTRUM_BLUE, pad=4)
    ax.tick_params(axis="z", labelsize=HELIX_TICK_SIZE, colors=IMAG_ORANGE, pad=4)
    ax.view_init(elev=24, azim=-62)

    def update(frame_idx):
        sample_idx = ANIMATION_INDICES[frame_idx]
        t_trace = TIME_VALUES[: sample_idx + 1]
        re_trace = KERNEL_REAL_VALUES[: sample_idx + 1]
        im_trace = KERNEL_IMAG_VALUES[: sample_idx + 1]
        current_t = TIME_VALUES[sample_idx]
        current_re = KERNEL_REAL_VALUES[sample_idx]
        current_im = KERNEL_IMAG_VALUES[sample_idx]
        helix_trace.set_data(t_trace, re_trace)
        helix_trace.set_3d_properties(im_trace)
        helix_point.set_data([current_t], [current_re])
        helix_point.set_3d_properties([current_im])
        proj_im_line.set_data([current_t, current_t], [current_re, current_re])
        proj_im_line.set_3d_properties([0.0, current_im])
        proj_re_line.set_data([current_t, current_t], [0.0, current_re])
        proj_re_line.set_3d_properties([current_im, current_im])
        return helix_trace, helix_point, proj_im_line, proj_re_line

    animation = FuncAnimation(fig, update, frames=len(ANIMATION_INDICES), interval=1000 / ANIMATION_FPS, blit=False)
    save_animation(animation, "07_complex_kernel_helix.gif")
    plt.close(fig)
    apply_standard_gif_timing("07_complex_kernel_helix.gif")
    crop_gif_whitespace("07_complex_kernel_helix.gif")
    save_first_gif_frame_as_png("07_complex_kernel_helix.gif", "07_complex_kernel_helix_t_min.png")
    save_last_gif_frame_as_png("07_complex_kernel_helix.gif", "07_complex_kernel_helix_t_max.png")


def export_kernel_component_spectrum(filename, values, color, title, y_label):
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    ax.plot(FREQ_VALUES, values, color=color, lw=2.4)
    style_signed_frequency_axis(ax, title, KERNEL_SPECTRUM_LIMIT, y_label)
    save_figure(fig, filename)


def export_kernel_spectrum_formula():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    ax.axis("off")
    formula = (
        r"$G_f(\nu)=\mathcal{F}\{g_f(t)\}$" "\n"
        r"$=\mathcal{F}\{g_{f,\mathrm{real}}(t)\}+j\,\mathcal{F}\{g_{f,\mathrm{imag}}(t)\}$"
    )
    ax.text(
        0.5,
        0.54,
        formula,
        ha="center",
        va="center",
        fontsize=26,
        color=SIGNAL_BLACK,
        transform=ax.transAxes,
    )
    save_figure(fig, "07_kernel_spectrum_formula.png")


def export_real_spectrum_x_nu():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.real(X_LINE_COEFFS), SPECTRUM_BLUE, lw=3.2)
    style_signed_frequency_axis(
        ax,
        r"Real part of $X(\nu)$",
        REAL_SPECTRUM_LIMIT,
        r"Re$\{X(\nu)\}$",
    )
    add_inset_legend(
        ax,
        [Line2D([0], [0], color=SPECTRUM_BLUE, lw=2.2, label=r"Re$\{X(\nu)\}$")],
        loc="upper left",
    )
    save_figure(fig, "09_real_spectrum_X_nu.png")


def export_imag_spectrum_x_nu():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.imag(X_LINE_COEFFS), IMAG_ORANGE, lw=3.2)
    style_signed_frequency_axis(
        ax,
        r"Imaginary part of $X(\nu)$",
        IMAG_SPECTRUM_LIMIT,
        r"Im$\{X(\nu)\}$",
    )
    add_inset_legend(
        ax,
        [Line2D([0], [0], color=IMAG_ORANGE, lw=2.2, label=r"Im$\{X(\nu)\}$")],
        loc="upper left",
    )
    save_figure(fig, "10_imaginary_spectrum_X_nu.png")


def export_weighting_sweep_animation(
    filename,
    base_values,
    output_values,
    active_color,
    top_title,
    top_ylabel,
    bottom_title,
    bottom_ylabel,
    base_label,
    weighted_label,
):
    fig, ax_top, ax_bottom = create_sweep_figure()

    draw_spectral_lines(ax_top, X_LINE_FREQS, base_values, FUTURE_GREY, lw=2.2)
    kernel_line, = ax_top.plot(FREQ_VALUES, np.zeros_like(FREQ_VALUES), color=ACTIVE_RED, lw=2.1)
    weighted_lines = ax_top.vlines(X_LINE_FREQS, 0.0, np.zeros_like(X_LINE_FREQS), color=active_color, lw=3.2)
    current_freq_line_top = ax_top.axvline(FREQ_VALUES[0], color="0.65", lw=1.0)
    current_freq_text = ax_top.text(
        0.985,
        0.96,
        "",
        transform=ax_top.transAxes,
        ha="right",
        va="top",
        fontsize=LEGEND_SIZE,
        bbox={"facecolor": "white", "edgecolor": "0.80", "alpha": 0.95},
    )
    style_signed_frequency_axis(
        ax_top,
        top_title,
        COMMON_SPECTRUM_LIMIT,
        top_ylabel,
        x_label=r"Auxiliary frequency $\nu$ [Hz]",
    )
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.8, label=base_label),
            Line2D([0], [0], color=ACTIVE_RED, lw=2.0, label=r"$G_f(\nu)=W(f-\nu)$"),
            Line2D([0], [0], color=active_color, lw=2.2, label=weighted_label),
        ],
        loc="upper left",
    )

    ax_bottom.plot(FREQ_VALUES, output_values, color=FUTURE_GREY, lw=1.8)
    active_trace, = ax_bottom.plot([], [], color=active_color, lw=2.4)
    current_freq_line_bottom = ax_bottom.axvline(FREQ_VALUES[0], color="0.65", lw=1.0)
    current_value_line = ax_bottom.axhline(0.0, color=active_color, lw=1.8, ls="--", alpha=0.9)
    current_point, = ax_bottom.plot([], [], "o", color=ACTIVE_RED, ms=7)
    style_signed_frequency_axis(
        ax_bottom,
        bottom_title,
        COMMON_SPECTRUM_LIMIT,
        bottom_ylabel,
        x_label="Analysis frequency f [Hz]",
    )

    def update(frame_idx):
        freq_idx = FREQ_ANIMATION_INDICES[frame_idx]
        current_f = FREQ_VALUES[freq_idx]
        current_kernel = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (current_f - FREQ_VALUES))
        kernel_at_lines = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (current_f - X_LINE_FREQS))
        weighted_values = base_values * kernel_at_lines
        current_output = output_values[freq_idx]

        kernel_line.set_data(FREQ_VALUES, current_kernel)
        weighted_lines.set_segments(
            [((freq, 0.0), (freq, value)) for freq, value in zip(X_LINE_FREQS, weighted_values)]
        )
        current_freq_line_top.set_xdata([current_f, current_f])
        current_freq_line_bottom.set_xdata([current_f, current_f])
        current_freq_text.set_text(rf"$f={frequency_label(current_f)}$ Hz")

        active_trace.set_data(FREQ_VALUES[: freq_idx + 1], output_values[: freq_idx + 1])
        current_value_line.set_ydata([current_output, current_output])
        current_point.set_data([current_f], [current_output])
        return (
            kernel_line,
            weighted_lines,
            current_freq_line_top,
            current_freq_line_bottom,
            current_value_line,
            current_point,
            active_trace,
            current_freq_text,
        )

    save_manual_tight_gif_auto(fig, update, filename, FREQ_ANIMATION_INDICES)
    plt.close(fig)


def export_real_weighting_sweep_animation():
    export_weighting_sweep_animation(
        "10A_real_weighting_sweep.gif",
        np.real(X_LINE_COEFFS),
        np.real(Y_VALUES),
        SPECTRUM_BLUE,
        r"Real weighting by shifted window spectrum",
        r"Amplitude",
        r"Running real result Re$\{Y(f)\}$",
        r"Re$\{Y(f)\}$",
        r"Re$\{X(\nu)\}$",
        r"Re$\{X(\nu)\}W(f-\nu)$",
    )


def export_imag_weighting_sweep_animation():
    export_weighting_sweep_animation(
        "10B_imaginary_weighting_sweep.gif",
        np.imag(X_LINE_COEFFS),
        np.imag(Y_VALUES),
        IMAG_ORANGE,
        r"Imaginary weighting by shifted window spectrum",
        r"Amplitude",
        r"Running imaginary result Im$\{Y(f)\}$",
        r"Im$\{Y(f)\}$",
        r"Im$\{X(\nu)\}$",
        r"Im$\{X(\nu)\}W(f-\nu)$",
    )


def export_kernel_spectrum():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    ax.plot(FREQ_VALUES, W_VALUES, color=WINDOW_GREEN, lw=1.9)
    ax.plot(FREQ_VALUES, G_VALUES, color=ACTIVE_RED, lw=2.4)
    ax.axvline(PROBE_F, color="0.65", lw=1.0)
    style_signed_frequency_axis(
        ax,
        rf"Analysis kernel spectrum $G_f(\nu)=W({frequency_label(PROBE_F)}\,\mathrm{{Hz}}-\nu)$",
        KERNEL_SPECTRUM_LIMIT,
        r"$G_f(\nu)$",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=1.9, label=r"$W(\nu)$"),
            Line2D([0], [0], color=ACTIVE_RED, lw=2.4, label=r"$G_f(\nu)=W(f-\nu)$"),
        ],
        loc="upper left",
    )
    save_figure(fig, "08_analysis_kernel_spectrum_G_f_nu.png")


def export_kernel_spectrum_xi():
    g_xi_values = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (FREQ_VALUES + PROBE_F))

    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    ax.plot(FREQ_VALUES, W_VALUES, color=WINDOW_GREEN, lw=1.9)
    ax.plot(FREQ_VALUES, g_xi_values, color=ACTIVE_RED, lw=2.4)
    ax.axvline(-PROBE_F, color="0.65", lw=1.0)
    style_signed_frequency_axis(
        ax,
        rf"Analysis kernel spectrum $G_f(\xi)$",
        KERNEL_SPECTRUM_LIMIT,
        r"$G_f(\xi)$",
        x_label=r"Auxiliary frequency $\xi$ [Hz]",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=1.9, label=r"$W(\xi)$"),
            Line2D([0], [0], color=ACTIVE_RED, lw=2.4, label=r"$G_f(\xi)=W(f+\xi)$"),
        ],
        loc="upper left",
    )
    save_figure(fig, "08A_analysis_kernel_spectrum_G_f_xi.png")


def export_weighted_real_spectrum():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.real(X_LINE_COEFFS), FUTURE_GREY, lw=2.2)
    ax.plot(FREQ_VALUES, G_VALUES, color=ACTIVE_RED, lw=1.8)
    ax.axvline(PROBE_F, color="0.65", lw=1.0)
    draw_spectral_lines(ax, X_LINE_FREQS, np.real(WEIGHTED_LINE_COEFFS), SPECTRUM_BLUE, lw=3.2)
    style_signed_frequency_axis(
        ax,
        r"Real part of $X(\nu)G_f(\nu)$",
        REAL_SPECTRUM_LIMIT,
        r"Re$\{X(\nu)G_f(\nu)\}$",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.8, label=r"Re$\{X(\nu)\}$"),
            Line2D([0], [0], color=ACTIVE_RED, lw=1.8, label=r"$G_f(\nu)$"),
            Line2D([0], [0], color=SPECTRUM_BLUE, lw=2.2, label=r"Re$\{X(\nu)G_f(\nu)\}$"),
        ],
        loc="upper left",
    )
    save_figure(fig, "11_real_weighted_spectrum_XG.png")


def export_cumulative_sum_over_nu():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)

    weighted_real = np.real(WEIGHTED_LINE_COEFFS)
    weighted_imag = np.imag(WEIGHTED_LINE_COEFFS)
    cumulative_real = np.cumsum(weighted_real)
    cumulative_imag = np.cumsum(weighted_imag)

    draw_spectral_lines(ax, X_LINE_FREQS, weighted_real, SPECTRUM_BLUE, lw=2.0, alpha=0.35)
    draw_spectral_lines(ax, X_LINE_FREQS, weighted_imag, IMAG_ORANGE, lw=2.0, alpha=0.35)

    step_x = np.concatenate(([FREQ_VALUES[0]], X_LINE_FREQS, [FREQ_VALUES[-1]]))
    step_real = np.concatenate(([0.0], cumulative_real, [cumulative_real[-1]]))
    step_imag = np.concatenate(([0.0], cumulative_imag, [cumulative_imag[-1]]))

    ax.step(step_x, step_real, where="post", color=SPECTRUM_BLUE, lw=2.6)
    ax.step(step_x, step_imag, where="post", color=IMAG_ORANGE, lw=2.6)

    style_signed_frequency_axis(
        ax,
        r"Cumulative sum over $\nu$",
        max(REAL_SPECTRUM_LIMIT, IMAG_SPECTRUM_LIMIT),
        r"Cumulative value",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=SPECTRUM_BLUE, lw=2.6, label=r"cumulative Re$\{Y(f)\}$"),
            Line2D([0], [0], color=IMAG_ORANGE, lw=2.6, label=r"cumulative Im$\{Y(f)\}$"),
        ],
        loc="upper right",
    )
    save_figure(fig, "13_cumulative_sum_over_nu.png")


def export_weighted_real_spectrum_with_integral():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.real(X_LINE_COEFFS), FUTURE_GREY, lw=2.2)
    ax.plot(FREQ_VALUES, G_VALUES, color=ACTIVE_RED, lw=1.8)
    draw_spectral_lines(ax, X_LINE_FREQS, np.real(WEIGHTED_LINE_COEFFS), SPECTRUM_BLUE, lw=3.2)
    ax.plot(
        [FREQ_VALUES[0], FREQ_VALUES[-1]],
        [Y_FIXED_FREQ.real, Y_FIXED_FREQ.real],
        color=SPECTRUM_BLUE,
        lw=2.0,
        ls="--",
    )
    style_signed_frequency_axis(
        ax,
        r"Real part with sum value",
        REAL_SPECTRUM_LIMIT,
        r"Re$\{X(\nu)G_f(\nu)\}$",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.8, label=r"Re$\{X(\nu)\}$"),
            Line2D([0], [0], color=ACTIVE_RED, lw=1.8, label=r"$G_f(\nu)$"),
            Line2D([0], [0], color=SPECTRUM_BLUE, lw=2.2, label=r"Re$\{X(\nu)G_f(\nu)\}$"),
            Line2D([0], [0], color=SPECTRUM_BLUE, lw=2.0, ls="--", label=r"Re$\{Y(f)\}$"),
        ],
        loc="upper left",
    )
    save_figure(fig, "13_real_weighted_spectrum_XG_with_sum.png")


def export_weighted_imag_spectrum():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.imag(X_LINE_COEFFS), FUTURE_GREY, lw=2.2)
    ax.plot(FREQ_VALUES, G_VALUES, color=ACTIVE_RED, lw=1.8)
    draw_spectral_lines(ax, X_LINE_FREQS, np.imag(WEIGHTED_LINE_COEFFS), IMAG_ORANGE, lw=3.2)
    style_signed_frequency_axis(
        ax,
        r"Imaginary part of $X(\nu)G_f(\nu)$",
        IMAG_SPECTRUM_LIMIT,
        r"Im$\{X(\nu)G_f(\nu)\}$",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.8, label=r"Im$\{X(\nu)\}$"),
            Line2D([0], [0], color=ACTIVE_RED, lw=1.8, label=r"$G_f(\nu)$"),
            Line2D([0], [0], color=IMAG_ORANGE, lw=2.2, label=r"Im$\{X(\nu)G_f(\nu)\}$"),
        ],
        loc="upper left",
    )
    save_figure(fig, "12_imaginary_weighted_spectrum_XG.png")


def export_weighted_imag_spectrum_with_integral():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.imag(X_LINE_COEFFS), FUTURE_GREY, lw=2.2)
    ax.plot(FREQ_VALUES, G_VALUES, color=ACTIVE_RED, lw=1.8)
    draw_spectral_lines(ax, X_LINE_FREQS, np.imag(WEIGHTED_LINE_COEFFS), IMAG_ORANGE, lw=3.2)
    ax.plot(
        [FREQ_VALUES[0], FREQ_VALUES[-1]],
        [Y_FIXED_FREQ.imag, Y_FIXED_FREQ.imag],
        color=IMAG_ORANGE,
        lw=2.0,
        ls="--",
    )
    style_signed_frequency_axis(
        ax,
        r"Imaginary part with sum value",
        IMAG_SPECTRUM_LIMIT,
        r"Im$\{X(\nu)G_f(\nu)\}$",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.8, label=r"Im$\{X(\nu)\}$"),
            Line2D([0], [0], color=ACTIVE_RED, lw=1.8, label=r"$G_f(\nu)$"),
            Line2D([0], [0], color=IMAG_ORANGE, lw=2.2, label=r"Im$\{X(\nu)G_f(\nu)\}$"),
            Line2D([0], [0], color=IMAG_ORANGE, lw=2.0, ls="--", label=r"Im$\{Y(f)\}$"),
        ],
        loc="upper left",
    )
    save_figure(fig, "14_imaginary_weighted_spectrum_XG_with_sum.png")


def export_observed_magnitude_spectrum_summary():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    magnitude_values = np.abs(Y_VALUES)
    ax.plot(FREQ_VALUES, magnitude_values, color="0.5", lw=2.0, ls="--")
    probe_value = output_magnitude_at(PROBE_F)
    ax.vlines(PROBE_F, 0.0, probe_value, color=ACTIVE_RED, lw=2.5)
    ax.plot([PROBE_F], [probe_value], "o", color=ACTIVE_RED, ms=8)
    style_magnitude_frequency_axis(ax, r"Observed magnitude $|Y(f)|$", MAGNITUDE_SPECTRUM_LIMIT)
    save_figure(fig, "16_observed_magnitude_spectrum_Y_f.png")


def export_observed_magnitude_spectrum_animation():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    magnitude_values = np.abs(Y_VALUES)
    ax.plot(FREQ_VALUES, magnitude_values, color="0.5", lw=2.0, ls="--")
    traced_curve, = ax.plot([], [], color=SIGNAL_BLACK, lw=2.2)
    current_line = ax.vlines(FREQ_VALUES[0], 0.0, magnitude_values[0], color=ACTIVE_RED, lw=2.5)
    current_point, = ax.plot([], [], "o", color=ACTIVE_RED, ms=8)
    style_magnitude_frequency_axis(ax, r"Observed magnitude $|Y(f)|$", MAGNITUDE_SPECTRUM_LIMIT)

    def update(frame_idx):
        nonlocal current_line
        freq_idx = FREQ_ANIMATION_INDICES[frame_idx]
        current_f = FREQ_VALUES[freq_idx]
        current_mag = magnitude_values[freq_idx]

        traced_curve.set_data(FREQ_VALUES[: freq_idx + 1], magnitude_values[: freq_idx + 1])
        current_line.remove()
        current_line = ax.vlines(current_f, 0.0, current_mag, color=ACTIVE_RED, lw=2.5)
        current_point.set_data([current_f], [current_mag])
        return traced_curve, current_line, current_point

    save_manual_tight_gif(
        fig,
        update,
        "16A_observed_magnitude_projection.gif",
        "16_observed_magnitude_spectrum_Y_f.png",
    )
    plt.close(fig)


def output_magnitude_at(current_f):
    return float(np.interp(current_f, FREQ_VALUES, np.abs(Y_VALUES)))


def frequency_label(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}"


def export_series():
    clear_owned_outputs()
    export_kernel_basis_only_plot(
        "01_analysis_kernel_real_g_f.png",
        COS_BASIS,
        SPECTRUM_BLUE,
        rf"Real basis at $f={frequency_label(PROBE_F)}$ Hz",
        r"$\cos(2\pi f t)$",
    )
    export_kernel_basis_only_plot(
        "02_analysis_kernel_imag_g_f.png",
        MINUS_SIN_BASIS,
        IMAG_ORANGE,
        rf"Imaginary basis at $f={frequency_label(PROBE_F)}$ Hz",
        r"$-\sin(2\pi f t)$",
    )
    export_kernel_time_plot(
        "03_windowed_real_kernel_g_f.png",
        KERNEL_REAL_VALUES,
        SPECTRUM_BLUE,
        rf"Windowed real kernel at $f={frequency_label(PROBE_F)}$ Hz",
        r"$g_{f,\mathrm{real}}(t)$",
        continuation_values=COS_BASIS,
        continuation_label=r"$\cos(2\pi f t)$",
    )
    export_kernel_time_plot(
        "04_windowed_imag_kernel_g_f.png",
        KERNEL_IMAG_VALUES,
        IMAG_ORANGE,
        rf"Windowed imaginary kernel at $f={frequency_label(PROBE_F)}$ Hz",
        r"$g_{f,\mathrm{imag}}(t)$",
        continuation_values=MINUS_SIN_BASIS,
        continuation_label=r"$-\sin(2\pi f t)$",
    )
    export_real_kernel_animation()
    export_imag_kernel_animation()
    export_complex_kernel_helix_animation()
    export_kernel_spectrum_xi()
    export_kernel_spectrum()
    export_real_spectrum_x_nu()
    export_imag_spectrum_x_nu()
    export_weighted_real_spectrum()
    export_weighted_imag_spectrum()
    export_weighted_real_spectrum_with_integral()
    export_weighted_imag_spectrum_with_integral()
    export_complex_value(
        "15_complex_value_Y_f_from_frequency.png",
        Y_FIXED_FREQ,
        rf"Complex value $Y(f)$ at $f={frequency_label(PROBE_F)}$ Hz",
    )
    export_observed_magnitude_spectrum_summary()
    mismatch = abs(Y_FIXED_TIME - Y_FIXED_FREQ)
    print(f"PNG figures exported to: {OUTPUT_DIR}")
    print(f"|Y_time({PROBE_F:.1f}) - Y_freq({PROBE_F:.1f})| = {mismatch:.6e}")


def main():
    clear_root_file_outputs()
    sidelobe_probe_f = 2.0 + first_sidelobe_offset_hz()
    series_configs = [
        (2.0, "2Hz"),
        (5.0, "5Hz"),
        (-5.0, "-5Hz"),
        (0.0, "0Hz"),
        (sidelobe_probe_f, f"{frequency_slug(sidelobe_probe_f)}Hz_sidelobe_at_2Hz"),
    ]
    for probe_f, folder_name in series_configs:
        configure_series(probe_f, folder_name)
        export_series()


if __name__ == "__main__":
    main()
