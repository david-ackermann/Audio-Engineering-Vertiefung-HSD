from pathlib import Path
import shutil
import warnings

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_ROOT_DIR = BASE_DIR / "png_storyboards" / "08_ir_messung_und_fensterung"
OUTPUT_DIR_HOCHTOENER = OUTPUT_ROOT_DIR / "08_hochtoener"
OUTPUT_DIR_TIEFTONER = OUTPUT_ROOT_DIR / "08_tieftöner"
OVERVIEW_SUBDIR = "08A_ir_ueberblick"
RECTANGULAR_SUBDIRS = [
    ("08B_ir_fensterung_mit_40ms_rechteckfenster", 40.0),
    ("08C_ir_fensterung_mit_20ms_rechteckfenster", 20.0),
    ("08D_ir_fensterung_mit_10ms_rechteckfenster", 10.0),
    ("08E_ir_fensterung_mit_5ms_rechteckfenster", 5.0),
    ("08F_ir_fensterung_mit_2ms_rechteckfenster", 2.0),
]
HAMMING_SUBDIRS = [
    ("08G_ir_fensterung_mit_40ms_hammingfenster", 40.0),
    ("08H_ir_fensterung_mit_20ms_hammingfenster", 20.0),
    ("08I_ir_fensterung_mit_10ms_hammingfenster", 10.0),
    ("08J_ir_fensterung_mit_5ms_hammingfenster", 5.0),
    ("08K_ir_fensterung_mit_2ms_hammingfenster", 2.0),
]
DATASET_CONFIGS = [
    {
        "root": OUTPUT_DIR_HOCHTOENER,
        "label": "Hochtöner",
        "wav_filename": "FF_HT.wav",
        "zoom_xlim": (2000.0, 6000.0),
        "zoom_ylim": (-20.0, -10.0),
    },
    {
        "root": OUTPUT_DIR_TIEFTONER,
        "label": "Tieftöner",
        "wav_filename": "FF_TT.wav",
        "zoom_xlim": (200.0, 600.0),
        "zoom_ylim": (-10.0, -3.0),
    },
]
DATASET_CONFIGS[0]["label"] = "Hochtoener"
DATASET_CONFIGS[1]["label"] = "Tieftoener"
DATASET_CONFIGS[1]["zoom_ylim"] = (-25.0, -15.0)

DPI = 200
FIGSIZE = (12.0, 4.4)
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86

SIGNAL_BLACK = "0.10"
SIGNAL_BLUE = "#2b7bbb"
HAMMING_ORANGE = "#d98c2f"
GRID_GREY = "0.75"
TIME_DB_FLOOR = -100.0
SPECTRUM_DB_FLOOR = -50.0
TIME_DISPLAY_DURATION_MS = 1000.0
PEAK_EXCERPT_HALF_WIDTH_MS = 10.0
SPECTRUM_DURATION_MS = 150.0
GATE_DISPLAY_DURATION_MS = 150.0
CURRENT_OUTPUT_DIR_08A = None
CURRENT_DATASET_LABEL = ""
CURRENT_ZOOM_XMIN_HZ = 2000.0
CURRENT_ZOOM_XMAX_HZ = 6000.0
CURRENT_ZOOM_YMIN_DB = -20.0
CURRENT_ZOOM_YMAX_DB = -10.0


def find_wav_file(filename):
    wav_path = DATA_DIR / filename
    if not wav_path.exists():
        raise RuntimeError(f"Expected WAV file {wav_path} to exist.")
    return wav_path


def dataset_title(title):
    if not CURRENT_DATASET_LABEL:
        return title
    return f"{CURRENT_DATASET_LABEL}: {title}"


def load_ir_signal(wav_path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sample_rate, signal = wavfile.read(wav_path)

    signal = np.asarray(signal, dtype=np.float64)
    if signal.ndim > 1:
        signal = signal[:, 0]

    peak = np.max(np.abs(signal))
    if peak > 0.0:
        signal = signal / peak

    return sample_rate, signal


def create_figure():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=BOTTOM_MARGIN,
        top=TOP_MARGIN,
    )
    return fig, ax


def create_zoom_figure():
    fig, ax = plt.subplots(figsize=(8.6, 3.0))
    fig.subplots_adjust(
        left=0.08,
        right=0.98,
        bottom=0.18,
        top=0.95,
    )
    return fig, ax


def save_figure(fig, output_dir, filename):
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def clear_output_dir():
    OUTPUT_ROOT_DIR.mkdir(parents=True, exist_ok=True)
    for child in OUTPUT_ROOT_DIR.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def style_time_axis(ax, title, time_end_ms, y_limits, y_ticks):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(0.0, time_end_ms)
    ax.set_ylim(*y_limits)
    ax.set_yticks(y_ticks)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [ms]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_centered_time_axis(ax, title, x_limits, y_limits, y_ticks):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.axvline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(*y_limits)
    ax.set_yticks(y_ticks)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time relative to peak [ms]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_absolute_time_excerpt_axis(ax, title, x_limits, y_limits, y_ticks):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(*y_limits)
    ax.set_yticks(y_ticks)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [ms]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_frequency_axis(ax, title, x_limits, x_ticks):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_xticks(x_ticks)
    ax.set_ylim(SPECTRUM_DB_FLOOR, 0.0)
    ax.set_yticks(np.arange(SPECTRUM_DB_FLOOR, 0.1, 10.0))
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [kHz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_log_frequency_axis(ax, title):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xscale("log")
    ax.set_xlim(20.0, 22050.0)
    ax.set_ylim(SPECTRUM_DB_FLOOR, 0.0)
    ax.set_yticks(np.arange(SPECTRUM_DB_FLOOR, 0.1, 10.0))
    ax.grid(alpha=0.25, which="both")
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def magnitude_to_db(magnitude, reference_magnitude):
    safe_reference = max(float(reference_magnitude), 1e-12)
    normalized = magnitude / safe_reference
    return 20.0 * np.log10(
        np.maximum(normalized, 10.0 ** (SPECTRUM_DB_FLOOR / 20.0))
    )


def compute_spectra(signal, sample_rate, reference_magnitude=None):
    fft_values = np.fft.fft(signal)
    fft_freqs = np.fft.fftfreq(len(signal), d=1.0 / sample_rate)
    fft_magnitude = np.abs(fft_values)

    fft_freqs_shifted_hz = np.fft.fftshift(fft_freqs)

    rfft_values = np.fft.rfft(signal)
    rfft_freqs_hz = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate)
    rfft_magnitude = np.abs(rfft_values)

    if reference_magnitude is None:
        reference_magnitude = max(np.max(fft_magnitude), np.max(rfft_magnitude), 1e-12)

    fft_db = magnitude_to_db(fft_magnitude, reference_magnitude)
    fft_db_shifted = np.fft.fftshift(fft_db)
    rfft_db = magnitude_to_db(rfft_magnitude, reference_magnitude)

    return fft_freqs_shifted_hz, fft_db_shifted, rfft_freqs_hz, rfft_db


def create_symmetric_rectangular_window(signal_length, peak_index, half_width_samples):
    window = np.zeros(signal_length, dtype=np.float64)
    start = max(0, peak_index - half_width_samples)
    stop = min(signal_length, peak_index + half_width_samples + 1)
    window[start:stop] = 1.0
    return window


def create_symmetric_hamming_window(signal_length, peak_index, half_width_samples):
    window = np.zeros(signal_length, dtype=np.float64)
    start = max(0, peak_index - half_width_samples)
    stop = min(signal_length, peak_index + half_width_samples + 1)
    active_length = max(0, stop - start)
    if active_length > 0:
        window[start:stop] = np.hamming(active_length)
    return window


def export_time_domain_linear(time_ms, signal, filename, title):
    fig, ax = create_figure()
    ax.plot(time_ms, signal, color=SIGNAL_BLUE, lw=1.6)
    style_time_axis(
        ax,
        dataset_title(title),
        float(time_ms[-1]),
        (-1.05, 1.05),
        np.arange(-1.0, 1.01, 0.5),
    )
    save_figure(fig, CURRENT_OUTPUT_DIR_08A, filename)


def export_time_domain_log(time_ms, signal, filename, title):
    fig, ax = create_figure()
    signal_db = 20.0 * np.log10(
        np.maximum(np.abs(signal), 10.0 ** (TIME_DB_FLOOR / 20.0))
    )
    ax.plot(time_ms, signal_db, color=SIGNAL_BLUE, lw=1.6)
    style_time_axis(
        ax,
        dataset_title(title),
        float(time_ms[-1]),
        (TIME_DB_FLOOR, 5.0),
        np.arange(TIME_DB_FLOOR, 1.0, 20.0),
    )
    save_figure(fig, CURRENT_OUTPUT_DIR_08A, filename)


def export_peak_excerpt(time_ms_absolute, signal, filename, title, logarithmic):
    fig, ax = create_figure()
    if logarithmic:
        values = 20.0 * np.log10(
            np.maximum(np.abs(signal), 10.0 ** (TIME_DB_FLOOR / 20.0))
        )
        ax.plot(time_ms_absolute, values, color=SIGNAL_BLUE, lw=1.6)
        style_absolute_time_excerpt_axis(
            ax,
            dataset_title(title),
            (float(time_ms_absolute[0]), float(time_ms_absolute[-1])),
            (TIME_DB_FLOOR, 5.0),
            np.arange(TIME_DB_FLOOR, 1.0, 20.0),
        )
    else:
        ax.plot(time_ms_absolute, signal, color=SIGNAL_BLUE, lw=1.6)
        style_absolute_time_excerpt_axis(
            ax,
            dataset_title(title),
            (float(time_ms_absolute[0]), float(time_ms_absolute[-1])),
            (-1.05, 1.05),
            np.arange(-1.0, 1.01, 0.5),
        )
    save_figure(fig, CURRENT_OUTPUT_DIR_08A, filename)


def export_bidirectional_spectrum(freq_hz, magnitude_db):
    fig, ax = create_figure()
    ax.plot(freq_hz / 1000.0, magnitude_db, color=SIGNAL_BLUE, lw=1.6)
    style_frequency_axis(
        ax,
        dataset_title("Bidirectional spectrum |H(f)|"),
        (-22.05, 22.05),
        np.arange(-20.0, 20.1, 5.0),
    )
    save_figure(fig, CURRENT_OUTPUT_DIR_08A, "05_ir_spectrum_bidirectional.png")


def export_one_sided_spectrum(freq_hz, magnitude_db):
    fig, ax = create_figure()
    ax.plot(freq_hz / 1000.0, magnitude_db, color=SIGNAL_BLUE, lw=1.6)
    style_frequency_axis(
        ax,
        dataset_title("One-sided spectrum |H(f)|"),
        (0.0, 22.05),
        np.arange(0.0, 20.1, 5.0),
    )
    save_figure(fig, CURRENT_OUTPUT_DIR_08A, "06_ir_spectrum_one_sided.png")


def export_one_sided_log_frequency_spectrum(freq_hz, magnitude_db):
    fig, ax = create_figure()
    valid = freq_hz >= 20.0
    ax.plot(freq_hz[valid], magnitude_db[valid], color=SIGNAL_BLUE, lw=1.6)
    style_log_frequency_axis(
        ax, dataset_title("One-sided spectrum |H(f)| with log frequency")
    )
    save_figure(fig, CURRENT_OUTPUT_DIR_08A, "07_ir_spectrum_one_sided_log_frequency.png")


def export_one_sided_log_frequency_zoom(freq_hz, magnitude_db):
    fig, ax = create_zoom_figure()
    valid = (freq_hz >= CURRENT_ZOOM_XMIN_HZ) & (freq_hz <= CURRENT_ZOOM_XMAX_HZ)
    ax.plot(freq_hz[valid], magnitude_db[valid], color=SIGNAL_BLUE, lw=1.8)
    ax.set_xscale("log")
    ax.set_xlim(CURRENT_ZOOM_XMIN_HZ, CURRENT_ZOOM_XMAX_HZ)
    ax.set_ylim(CURRENT_ZOOM_YMIN_DB, CURRENT_ZOOM_YMAX_DB)
    ax.set_xticks(np.linspace(CURRENT_ZOOM_XMIN_HZ, CURRENT_ZOOM_XMAX_HZ, 5))
    ax.set_yticks(np.arange(CURRENT_ZOOM_YMIN_DB, CURRENT_ZOOM_YMAX_DB + 0.1, 2.0))
    ax.grid(alpha=0.25, which="both")
    ax.tick_params(labelsize=TICK_SIZE)
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    save_figure(
        fig,
        CURRENT_OUTPUT_DIR_08A,
        "08_ir_spectrum_one_sided_log_frequency_zoom_2k_to_6k.png",
    )


def export_ir_with_window(output_dir, time_ms, signal, window, window_color, window_title):
    fig, ax = create_figure()
    ax.plot(time_ms, signal, color=SIGNAL_BLUE, lw=1.6, zorder=2)
    ax.plot(time_ms, window, color=window_color, lw=2.2, zorder=3)
    style_time_axis(
        ax,
        dataset_title(window_title),
        float(time_ms[-1]),
        (-1.05, 1.05),
        np.arange(-1.0, 1.01, 0.5),
    )
    save_figure(fig, output_dir, "01_ir_and_rectangular_gate.png")


def export_windowed_ir_time(
    output_dir,
    time_ms,
    original_signal,
    window,
    windowed_signal,
    window_color,
):
    fig, ax = create_figure()
    original_db = 20.0 * np.log10(
        np.maximum(np.abs(original_signal), 10.0 ** (TIME_DB_FLOOR / 20.0))
    )
    window_db = 20.0 * np.log10(
        np.maximum(window, 10.0 ** (TIME_DB_FLOOR / 20.0))
    )
    signal_db = 20.0 * np.log10(
        np.maximum(np.abs(windowed_signal), 10.0 ** (TIME_DB_FLOOR / 20.0))
    )
    ax.plot(time_ms, original_db, color="#bddcf3", lw=1.6, zorder=1)
    ax.plot(time_ms, window_db, color=window_color, lw=2.0, zorder=2)
    ax.plot(time_ms, signal_db, color=SIGNAL_BLACK, lw=1.6, zorder=3)
    style_time_axis(
        ax,
        dataset_title("Windowed IR |h_w(t)| in dB"),
        float(time_ms[-1]),
        (TIME_DB_FLOOR, 5.0),
        np.arange(TIME_DB_FLOOR, 1.0, 20.0),
    )
    save_figure(fig, output_dir, "02_windowed_ir_time_domain.png")


def export_window_and_ir_spectra(output_dir, freq_hz, window_db, ir_db, window_color):
    fig, ax = create_figure()
    valid = freq_hz >= 20.0
    ax.plot(freq_hz[valid], window_db[valid], color=window_color, lw=1.8, zorder=2)
    ax.plot(freq_hz[valid], ir_db[valid], color=SIGNAL_BLUE, lw=1.6, zorder=3)
    style_log_frequency_axis(ax, dataset_title("Window spectrum and IR spectrum"))
    ax.legend(
        ["Window", "IR"],
        loc="upper right",
        framealpha=0.95,
        fontsize=14,
    )
    save_figure(fig, output_dir, "03_window_spectrum_and_ir_spectrum.png")


def export_windowed_ir_spectrum_log(
    output_dir,
    freq_hz,
    original_db,
    windowed_db,
    rectangular_reference_db=None,
):
    fig, ax = create_figure()
    valid = freq_hz >= 20.0
    ax.plot(freq_hz[valid], original_db[valid], color="#bddcf3", lw=1.6, zorder=1)
    if rectangular_reference_db is not None:
        ax.plot(freq_hz[valid], rectangular_reference_db[valid], color="0.87", lw=1.6, zorder=2)
    ax.plot(freq_hz[valid], windowed_db[valid], color=SIGNAL_BLACK, lw=1.6, zorder=3)
    style_log_frequency_axis(ax, dataset_title("Windowed spectrum |H_w(f)|"))
    save_figure(fig, output_dir, "04_windowed_ir_spectrum_logarithmic.png")


def export_windowed_ir_spectrum_zoom(
    output_dir,
    freq_hz,
    original_db,
    windowed_db,
    rectangular_reference_db=None,
):
    fig, ax = create_zoom_figure()
    valid = (freq_hz >= CURRENT_ZOOM_XMIN_HZ) & (freq_hz <= CURRENT_ZOOM_XMAX_HZ)
    ax.plot(freq_hz[valid], original_db[valid], color="#bddcf3", lw=1.6, zorder=1)
    if rectangular_reference_db is not None:
        ax.plot(freq_hz[valid], rectangular_reference_db[valid], color="0.87", lw=1.6, zorder=2)
    ax.plot(freq_hz[valid], windowed_db[valid], color=SIGNAL_BLACK, lw=1.6, zorder=3)
    ax.set_xscale("log")
    ax.set_xlim(CURRENT_ZOOM_XMIN_HZ, CURRENT_ZOOM_XMAX_HZ)
    ax.set_ylim(CURRENT_ZOOM_YMIN_DB, CURRENT_ZOOM_YMAX_DB)
    ax.set_xticks(np.linspace(CURRENT_ZOOM_XMIN_HZ, CURRENT_ZOOM_XMAX_HZ, 5))
    ax.set_yticks(np.arange(CURRENT_ZOOM_YMIN_DB, CURRENT_ZOOM_YMAX_DB + 0.1, 2.0))
    ax.grid(alpha=0.25, which="both")
    ax.tick_params(labelsize=TICK_SIZE)
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    save_figure(fig, output_dir, "05_windowed_ir_spectrum_zoom_2k_to_6k.png")


def build_output_dir(root_dir, subdir_name):
    return root_dir / subdir_name


def export_overview_series(sample_rate, signal, peak_index):
    time_samples = min(len(signal), int(round(TIME_DISPLAY_DURATION_MS * 1e-3 * sample_rate)))
    spectrum_samples = min(
        len(signal), int(round(SPECTRUM_DURATION_MS * 1e-3 * sample_rate))
    )
    peak_excerpt_half_width_samples = int(
        round(PEAK_EXCERPT_HALF_WIDTH_MS * 1e-3 * sample_rate)
    )

    signal_spectrum = signal[:spectrum_samples]
    excerpt_start = max(0, peak_index - peak_excerpt_half_width_samples)
    excerpt_stop = min(len(signal), peak_index + peak_excerpt_half_width_samples + 1)
    excerpt_signal = signal[excerpt_start:excerpt_stop]
    excerpt_time_ms_absolute = (
        np.arange(excerpt_start, excerpt_stop) / sample_rate * 1000.0
    )

    time_ms_short = np.arange(len(signal_spectrum)) / sample_rate * 1000.0
    fft_freq_hz, fft_db, rfft_freq_hz, rfft_db = compute_spectra(signal, sample_rate)

    export_time_domain_linear(
        time_ms_short,
        signal_spectrum,
        "01_ir_time_domain_linear_150ms.png",
        "Impulse response h(t)",
    )
    export_time_domain_log(
        time_ms_short,
        signal_spectrum,
        "02_ir_time_domain_logarithmic_150ms.png",
        "Impulse response |h(t)| in dB",
    )
    export_peak_excerpt(
        excerpt_time_ms_absolute,
        excerpt_signal,
        "03_ir_excerpt_around_peak_linear.png",
        "IR around peak h(t)",
        logarithmic=False,
    )
    export_peak_excerpt(
        excerpt_time_ms_absolute,
        excerpt_signal,
        "04_ir_excerpt_around_peak_logarithmic.png",
        "IR around peak |h(t)| in dB",
        logarithmic=True,
    )
    export_bidirectional_spectrum(fft_freq_hz, fft_db)
    export_one_sided_spectrum(rfft_freq_hz, rfft_db)
    export_one_sided_log_frequency_spectrum(rfft_freq_hz, rfft_db)
    export_one_sided_log_frequency_zoom(rfft_freq_hz, rfft_db)

    return rfft_freq_hz, rfft_db, np.max(np.abs(np.fft.rfft(signal)))


def export_window_series(
    output_dir,
    gate_width_ms,
    window_kind,
    sample_rate,
    signal,
    peak_index,
    ir_db,
    ir_spectrum_reference,
):
    gate_display_samples = min(
        len(signal), int(round(GATE_DISPLAY_DURATION_MS * 1e-3 * sample_rate))
    )
    time_ms_gate = np.arange(gate_display_samples) / sample_rate * 1000.0

    desired_half_width_samples = int(round((gate_width_ms * 1e-3 * sample_rate) / 2.0))
    symmetric_half_width_samples = min(
        desired_half_width_samples,
        peak_index,
        len(signal) - peak_index - 1,
    )
    rectangular_window = create_symmetric_rectangular_window(
        len(signal),
        peak_index,
        symmetric_half_width_samples,
    )
    rectangular_windowed_signal = signal * rectangular_window

    if window_kind == "rectangular":
        active_window = rectangular_window
        window_color = "#66b77a"
        window_title = "IR and symmetric rectangular gate"
        reference_rectangular_db = None
    else:
        active_window = create_symmetric_hamming_window(
            len(signal),
            peak_index,
            symmetric_half_width_samples,
        )
        window_color = HAMMING_ORANGE
        window_title = "IR and symmetric Hamming window"
        _, _, _, reference_rectangular_db = compute_spectra(
            rectangular_windowed_signal,
            sample_rate,
            reference_magnitude=ir_spectrum_reference,
        )

    windowed_signal = signal * active_window
    _, _, window_rfft_freq_hz, window_rfft_db = compute_spectra(
        active_window,
        sample_rate,
    )
    _, _, windowed_rfft_freq_hz, windowed_rfft_db = compute_spectra(
        windowed_signal,
        sample_rate,
        reference_magnitude=ir_spectrum_reference,
    )

    export_ir_with_window(
        output_dir,
        time_ms_gate,
        signal[:gate_display_samples],
        active_window[:gate_display_samples],
        window_color,
        window_title,
    )
    export_windowed_ir_time(
        output_dir,
        time_ms_gate,
        signal[:gate_display_samples],
        active_window[:gate_display_samples],
        windowed_signal[:gate_display_samples],
        window_color,
    )
    export_window_and_ir_spectra(
        output_dir,
        window_rfft_freq_hz,
        window_rfft_db,
        ir_db,
        window_color,
    )
    export_windowed_ir_spectrum_log(
        output_dir,
        windowed_rfft_freq_hz,
        ir_db,
        windowed_rfft_db,
        rectangular_reference_db=reference_rectangular_db,
    )
    export_windowed_ir_spectrum_zoom(
        output_dir,
        windowed_rfft_freq_hz,
        ir_db,
        windowed_rfft_db,
        rectangular_reference_db=reference_rectangular_db,
    )


def export_dataset(dataset_config):
    global CURRENT_OUTPUT_DIR_08A, CURRENT_DATASET_LABEL
    global CURRENT_ZOOM_XMIN_HZ, CURRENT_ZOOM_XMAX_HZ
    global CURRENT_ZOOM_YMIN_DB, CURRENT_ZOOM_YMAX_DB

    CURRENT_DATASET_LABEL = dataset_config["label"]
    CURRENT_ZOOM_XMIN_HZ, CURRENT_ZOOM_XMAX_HZ = dataset_config["zoom_xlim"]
    CURRENT_ZOOM_YMIN_DB, CURRENT_ZOOM_YMAX_DB = dataset_config["zoom_ylim"]
    dataset_root = dataset_config["root"]
    CURRENT_OUTPUT_DIR_08A = build_output_dir(dataset_root, OVERVIEW_SUBDIR)

    wav_path = find_wav_file(dataset_config["wav_filename"])
    sample_rate, signal = load_ir_signal(wav_path)
    peak_index = int(np.argmax(np.abs(signal)))

    rfft_freq_hz, rfft_db, ir_spectrum_reference = export_overview_series(
        sample_rate, signal, peak_index
    )

    for subdir_name, gate_width_ms in RECTANGULAR_SUBDIRS:
        export_window_series(
            build_output_dir(dataset_root, subdir_name),
            gate_width_ms,
            "rectangular",
            sample_rate,
            signal,
            peak_index,
            rfft_db,
            ir_spectrum_reference,
        )

    for subdir_name, gate_width_ms in HAMMING_SUBDIRS:
        export_window_series(
            build_output_dir(dataset_root, subdir_name),
            gate_width_ms,
            "hamming",
            sample_rate,
            signal,
            peak_index,
            rfft_db,
            ir_spectrum_reference,
        )

    print(f"WAV source: {wav_path}")
    print(f"PNG figures exported to: {dataset_root}")


def main():
    clear_output_dir()
    for dataset_config in DATASET_CONFIGS:
        export_dataset(dataset_config)


if __name__ == "__main__":
    main()
