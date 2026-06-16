from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "02_am_modulation" / "02d_am_modulation_sine_carrier"

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (12.0, 4.8)

SIGNAL_BLACK = "0.10"
SPECTRUM_BLUE = "#2b7bbb"
MODULATION_VIOLET = "#7b4ab8"
REFERENCE_GREY = "0.55"
GRID_GREY = "0.75"

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17

SAMPLE_RATE_HZ = 48_000.0
DURATION_S = 20.0
DISPLAY_DURATION_MS = 25.0
CARRIER_FREQUENCY_HZ = 1_000.0
MODULATION_FREQUENCY_HZ = 200.0
ALPHA = 1.0
SINE_LINE_AMPLITUDE = 0.5
GAIN_DC_LINE_AMPLITUDE = 1.0
GAIN_SINE_LINE_AMPLITUDE = ALPHA / 2.0
OUTPUT_CARRIER_LINE_AMPLITUDE = 0.5
OUTPUT_SIDEBAND_LINE_AMPLITUDE = ALPHA / 4.0
SPECTRUM_X_LIMIT_KHZ = 1.6
SPECTRUM_X_TICK_STEP_KHZ = 0.4

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def style_time_axis(ax: plt.Axes, *, ylabel: str = "Amplitude") -> None:
    ax.set_xlabel("Time (ms)", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=REFERENCE_GREY, lw=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def style_line_spectrum_axis(ax: plt.Axes, *, x_limit_khz: float, y_limit: float = 1.1) -> None:
    ax.set_xlabel("Frequency (kHz)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Component amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=REFERENCE_GREY, lw=0.9)
    ax.set_xlim(-x_limit_khz, x_limit_khz)
    ax.set_ylim(0.0, y_limit)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_time_signal(
    time_s: np.ndarray,
    signal: np.ndarray,
    *,
    title: str,
    color: str,
    filename: str,
    y_limit: tuple[float, float],
    reference_y: float | None = None,
) -> Path:
    display_samples = int(round(DISPLAY_DURATION_MS * 1e-3 * SAMPLE_RATE_HZ))
    time_ms = 1000.0 * time_s[:display_samples]

    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    ax.plot(time_ms, signal[:display_samples], color=color, lw=2.4)
    if reference_y is not None:
        ax.axhline(reference_y, color=REFERENCE_GREY, lw=1.4, ls="--")
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DISPLAY_DURATION_MS)
    ax.set_ylim(*y_limit)
    ax.set_xticks(np.arange(0.0, DISPLAY_DURATION_MS + 0.1, 5.0))
    style_time_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_line_spectrum(
    lines_hz: list[tuple[float, float, str]],
    *,
    title: str,
    filename: str,
    x_limit_khz: float,
    x_tick_step_khz: float,
    y_limit: float = 1.1,
) -> Path:
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    for frequency_hz, amplitude, color in lines_hz:
        ax.vlines(frequency_hz / 1000.0, 0.0, amplitude, color=color, lw=3.6)

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xticks(np.arange(-x_limit_khz, x_limit_khz + 0.001, x_tick_step_khz))
    style_line_spectrum_axis(ax, x_limit_khz=x_limit_khz, y_limit=y_limit)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()

    time_s = np.arange(int(round(DURATION_S * SAMPLE_RATE_HZ))) / SAMPLE_RATE_HZ
    carrier = np.sin(2.0 * np.pi * CARRIER_FREQUENCY_HZ * time_s)
    modulation_sine = np.sin(2.0 * np.pi * MODULATION_FREQUENCY_HZ * time_s)
    am_gain = 1.0 + ALPHA * modulation_sine
    output = am_gain * carrier

    difference_hz = CARRIER_FREQUENCY_HZ - MODULATION_FREQUENCY_HZ
    sum_hz = CARRIER_FREQUENCY_HZ + MODULATION_FREQUENCY_HZ

    image_paths = [
        save_time_signal(
            time_s,
            carrier,
            title="Carrier sine",
            color=SIGNAL_BLACK,
            filename="01_carrier_sine_time.png",
            y_limit=(-2.0, 2.0),
        ),
        save_line_spectrum(
            [
                (-CARRIER_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, SIGNAL_BLACK),
                (CARRIER_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, SIGNAL_BLACK),
            ],
            title="Carrier spectrum",
            filename="02_carrier_spectrum.png",
            x_limit_khz=SPECTRUM_X_LIMIT_KHZ,
            x_tick_step_khz=SPECTRUM_X_TICK_STEP_KHZ,
        ),
        save_time_signal(
            time_s,
            modulation_sine,
            title="Modulation sine",
            color=MODULATION_VIOLET,
            filename="03_modulation_sine_time.png",
            y_limit=(-2.0, 2.0),
        ),
        save_line_spectrum(
            [
                (-MODULATION_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, MODULATION_VIOLET),
                (MODULATION_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, MODULATION_VIOLET),
            ],
            title="Modulation spectrum",
            filename="04_modulation_spectrum.png",
            x_limit_khz=SPECTRUM_X_LIMIT_KHZ,
            x_tick_step_khz=SPECTRUM_X_TICK_STEP_KHZ,
        ),
        save_time_signal(
            time_s,
            am_gain,
            title="AM gain signal",
            color=MODULATION_VIOLET,
            filename="05_am_gain_signal_time.png",
            y_limit=(-2.0, 2.0),
            reference_y=1.0,
        ),
        save_line_spectrum(
            [
                (-MODULATION_FREQUENCY_HZ, GAIN_SINE_LINE_AMPLITUDE, MODULATION_VIOLET),
                (0.0, GAIN_DC_LINE_AMPLITUDE, MODULATION_VIOLET),
                (MODULATION_FREQUENCY_HZ, GAIN_SINE_LINE_AMPLITUDE, MODULATION_VIOLET),
            ],
            title="AM gain spectrum",
            filename="06_am_gain_spectrum_dc.png",
            x_limit_khz=SPECTRUM_X_LIMIT_KHZ,
            x_tick_step_khz=SPECTRUM_X_TICK_STEP_KHZ,
        ),
        save_time_signal(
            time_s,
            output,
            title="AM output",
            color=SPECTRUM_BLUE,
            filename="07_am_output_time.png",
            y_limit=(-2.0, 2.0),
        ),
        save_line_spectrum(
            [
                (-sum_hz, OUTPUT_SIDEBAND_LINE_AMPLITUDE, SPECTRUM_BLUE),
                (-CARRIER_FREQUENCY_HZ, OUTPUT_CARRIER_LINE_AMPLITUDE, SPECTRUM_BLUE),
                (-difference_hz, OUTPUT_SIDEBAND_LINE_AMPLITUDE, SPECTRUM_BLUE),
                (difference_hz, OUTPUT_SIDEBAND_LINE_AMPLITUDE, SPECTRUM_BLUE),
                (CARRIER_FREQUENCY_HZ, OUTPUT_CARRIER_LINE_AMPLITUDE, SPECTRUM_BLUE),
                (sum_hz, OUTPUT_SIDEBAND_LINE_AMPLITUDE, SPECTRUM_BLUE),
            ],
            title="Output spectrum",
            filename="08_am_output_spectrum_carrier_sidebands.png",
            x_limit_khz=SPECTRUM_X_LIMIT_KHZ,
            x_tick_step_khz=SPECTRUM_X_TICK_STEP_KHZ,
        ),
    ]

    for path in image_paths:
        print(path)


if __name__ == "__main__":
    main()
