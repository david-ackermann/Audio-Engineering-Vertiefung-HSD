from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "04_imd"
)
SINGLE_OUTPUT_DIR = OUTPUT_DIR / "04A_single_sine"
TWO_TONE_OUTPUT_DIR = OUTPUT_DIR / "04B_two_sine_mixture"

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (12.0, 4.8)

SIGNAL_BLACK = "0.10"
SPECTRUM_BLUE = "#2b7bbb"
TAYLOR_GREEN = "#0b6b3a"
TAYLOR_LIGHT_GREEN = "#78a98c"
POWER_TERM_COLORS = {
    2: "#c46a00",
    3: "#8b5ec7",
    4: "#0f8b8d",
    5: "#b13a72",
}
REFERENCE_GREY = "0.68"
LIGHT_GREY = "0.84"
GRID_GREY = "0.75"

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
LEGEND_SIZE = 14

SAMPLE_RATE_HZ = 48_000.0
DURATION_S = 1.0
DISPLAY_DURATION_MS = 10.0
SPECTRUM_SAMPLE_RATE_HZ = SAMPLE_RATE_HZ * 16
SPECTRUM_DURATION_S = 0.2
SINGLE_FREQUENCY_HZ = 2_000.0
FREQUENCY_1_HZ = 3_500.0
FREQUENCY_2_HZ = 4_500.0
SINGLE_AMPLITUDE = 1.0
TONE_AMPLITUDE = 0.5
CLIP_THRESHOLD = 0.65
TAYLOR_COEFFICIENTS = {
    1: 1.0,
    3: -1.0 / 3.0,
    5: 2.0 / 15.0,
    7: -17.0 / 315.0,
    9: 62.0 / 2835.0,
    11: -1382.0 / 155925.0,
    13: 21844.0 / 6081075.0,
    15: -929569.0 / 638512875.0,
}
TAYLOR_ORDERS = tuple(TAYLOR_COEFFICIENTS.keys())
POWER_TERM_ORDERS = tuple(POWER_TERM_COLORS.keys())
SPECTRUM_LIMIT_HZ = 20_000.0
SPECTRUM_DB_FLOOR = -80.0
SPECTRUM_DB_CEILING = 9.0
SPECTRUM_THRESHOLD = 10 ** (SPECTRUM_DB_FLOOR / 20.0)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dirs() -> None:
    for folder in (SINGLE_OUTPUT_DIR, TWO_TONE_OUTPUT_DIR):
        folder.mkdir(parents=True, exist_ok=True)
        for image_file in folder.glob("*.png"):
            image_file.unlink()

    # Remove old flat files from the previous Block 3B version.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()


def style_time_axis(ax: plt.Axes, *, y_limit: tuple[float, float]) -> None:
    ax.set_xlabel("Time (ms)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=REFERENCE_GREY, lw=0.9)
    ax.set_xlim(0.0, DISPLAY_DURATION_MS)
    ax.set_ylim(*y_limit)
    ax.set_xticks(np.arange(0.0, DISPLAY_DURATION_MS + 0.1, 5.0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def style_spectrum_axis(ax: plt.Axes, *, y_limit: tuple[float, float]) -> None:
    ax.set_xlabel("Frequency (kHz)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Two-sided amplitude (dB)", fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.grid(True, which="minor", color=GRID_GREY, alpha=0.14)
    ax.axhline(0.0, color=REFERENCE_GREY, lw=0.9)
    ax.set_xlim(0.0, SPECTRUM_LIMIT_HZ / 1000.0)
    ax.set_ylim(*y_limit)
    ax.set_xticks(np.arange(0.0, SPECTRUM_LIMIT_HZ / 1000.0 + 0.001, 2.0))
    ax.set_xticks(np.arange(0.0, SPECTRUM_LIMIT_HZ / 1000.0 + 0.001, 1.0), minor=True)
    y_ticks = list(np.arange(y_limit[0], y_limit[1] + 0.001, 20.0))
    if not np.isclose(y_ticks[-1], y_limit[1]):
        y_ticks.append(y_limit[1])
    ax.set_yticks(y_ticks)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_time_plot(
    output_dir: Path,
    time_s: np.ndarray,
    traces: list[tuple[np.ndarray, str, str, float, float, str]],
    *,
    title: str,
    y_limit: tuple[float, float],
    filename: str,
    legend: bool = False,
) -> Path:
    display_samples = int(round(DISPLAY_DURATION_MS * 1e-3 * SAMPLE_RATE_HZ))
    time_ms = 1000.0 * time_s[:display_samples]

    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    handles: list[Line2D] = []
    labels: list[str] = []
    for signal, label, color, lw, alpha, linestyle in traces:
        ax.plot(time_ms, signal[:display_samples], color=color, lw=lw, alpha=alpha, linestyle=linestyle)
        handles.append(Line2D([0], [0], color=color, lw=lw, alpha=alpha, linestyle=linestyle))
        labels.append(label)

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    style_time_axis(ax, y_limit=y_limit)
    if legend:
        legend_obj = ax.legend(
            handles,
            labels,
            loc="upper right",
            frameon=True,
            fontsize=LEGEND_SIZE,
            borderpad=0.45,
            labelspacing=0.35,
        )
        legend_obj.get_frame().set_facecolor("white")
        legend_obj.get_frame().set_edgecolor("none")
        legend_obj.get_frame().set_alpha(0.92)

    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = output_dir / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_line_spectrum(
    output_dir: Path,
    components: list[tuple[float, float, str, float]],
    *,
    title: str,
    y_limit: tuple[float, float],
    filename: str,
    reference_components: list[tuple[float, float]] | None = None,
    legend_entries: list[tuple[str, str, float]] | None = None,
) -> Path:
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    spectrum_floor = y_limit[0]

    if reference_components is not None:
        for frequency_hz, amplitude in reference_components:
            amplitude_db = amplitude_to_db(amplitude)
            ax.vlines(
                frequency_hz / 1000.0,
                spectrum_floor,
                amplitude_db,
                color=LIGHT_GREY,
                lw=3.4,
                alpha=0.85,
                zorder=1,
            )

    for frequency_hz, amplitude, color, lw in components:
        amplitude_db = amplitude_to_db(amplitude)
        ax.vlines(frequency_hz / 1000.0, spectrum_floor, amplitude_db, color=color, lw=lw, zorder=3)

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    style_spectrum_axis(ax, y_limit=y_limit)
    if legend_entries is not None:
        handles = [
            Line2D([0], [0], color=color, lw=lw, label=label)
            for label, color, lw in legend_entries
        ]
        legend_obj = ax.legend(
            handles=handles,
            loc="upper right",
            frameon=True,
            fontsize=LEGEND_SIZE,
            borderpad=0.45,
            labelspacing=0.35,
        )
        legend_obj.get_frame().set_facecolor("white")
        legend_obj.get_frame().set_edgecolor("none")
        legend_obj.get_frame().set_alpha(0.92)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = output_dir / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def amplitude_to_db(amplitude: float) -> float:
    return max(SPECTRUM_DB_FLOOR, 20.0 * np.log10(max(float(amplitude), SPECTRUM_THRESHOLD)))


def positive_side_two_sided_fft_components(
    signal: np.ndarray,
    *,
    sample_rate_hz: float,
    threshold: float,
) -> list[tuple[float, float]]:
    spectrum = np.fft.rfft(signal)
    frequencies_hz = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate_hz)
    amplitudes = np.abs(spectrum) / len(signal)
    keep = (frequencies_hz <= SPECTRUM_LIMIT_HZ) & (amplitudes >= threshold)
    return [
        (float(frequency), float(amplitude))
        for frequency, amplitude in zip(frequencies_hz[keep], amplitudes[keep])
    ]


def component_lines(
    pairs: list[tuple[float, float]],
    *,
    color: str,
    lw: float = 3.4,
) -> list[tuple[float, float, str, float]]:
    return [(frequency_hz, amplitude, color, lw) for frequency_hz, amplitude in pairs]


def taylor_tanh(signal: np.ndarray, order: int) -> np.ndarray:
    output = np.zeros_like(signal)
    for polynomial_order, coefficient in TAYLOR_COEFFICIENTS.items():
        if polynomial_order <= order:
            output += coefficient * signal**polynomial_order
    return output


def polynomial_nonlinearity(signal: np.ndarray) -> np.ndarray:
    return taylor_tanh(signal, TAYLOR_ORDERS[-1])


def hard_clip(signal: np.ndarray) -> np.ndarray:
    return np.clip(signal, -CLIP_THRESHOLD, CLIP_THRESHOLD)


def single_sine_signal(time_s: np.ndarray) -> np.ndarray:
    return SINGLE_AMPLITUDE * np.cos(2.0 * np.pi * SINGLE_FREQUENCY_HZ * time_s)


def two_tone_signals(time_s: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x1 = TONE_AMPLITUDE * np.cos(2.0 * np.pi * FREQUENCY_1_HZ * time_s)
    x2 = TONE_AMPLITUDE * np.cos(2.0 * np.pi * FREQUENCY_2_HZ * time_s)
    return x1, x2, x1 + x2


def power_term_label(order: int) -> str:
    return rf"$x^{order}[n]$"


def power_term_legend_entries() -> list[tuple[str, str, float]]:
    return [
        (power_term_label(order), POWER_TERM_COLORS[order], 3.0)
        for order in POWER_TERM_ORDERS
    ]


def export_power_term_overviews(
    output_dir: Path,
    time_s: np.ndarray,
    signal: np.ndarray,
    spectrum_signal: np.ndarray,
    input_components: list[tuple[float, float]],
    *,
    prefix: str,
    start_index: int,
    spectrum_y_limit: tuple[float, float],
) -> list[Path]:
    power_signals: dict[int, np.ndarray] = {}
    power_components_by_order: dict[int, list[tuple[float, float]]] = {}

    for order in POWER_TERM_ORDERS:
        power_signal = signal**order
        power_signals[order] = power_signal
        power_components = positive_side_two_sided_fft_components(
            spectrum_signal**order,
            sample_rate_hz=SPECTRUM_SAMPLE_RATE_HZ,
            threshold=SPECTRUM_THRESHOLD,
        )
        power_components_by_order[order] = power_components

    paths: list[Path] = []

    for order_index, order in enumerate(POWER_TERM_ORDERS):
        color = POWER_TERM_COLORS[order]
        figure_index = start_index + 2 * order_index
        paths += [
            save_time_plot(
                output_dir,
                time_s,
                [
                    (signal, r"$x[n]$", LIGHT_GREY, 2.0, 0.78, "--"),
                    (power_signals[order], power_term_label(order), color, 2.6, 0.96, "-"),
                ],
                title=f"Power term x^{order}",
                y_limit=(-1.2, 1.2),
                filename=f"{figure_index:02d}_{prefix}_power_{order:02d}_time.png",
                legend=True,
            ),
            save_line_spectrum(
                output_dir,
                component_lines(power_components_by_order[order], color=color, lw=3.0),
                title=f"Power term x^{order} spectrum",
                y_limit=spectrum_y_limit,
                filename=f"{figure_index + 1:02d}_{prefix}_power_{order:02d}_spectrum.png",
                reference_components=input_components,
                legend_entries=[(power_term_label(order), color, 3.0)],
            ),
        ]

    return paths


def export_taylor_build_time_plots(
    output_dir: Path,
    time_s: np.ndarray,
    signal: np.ndarray,
    *,
    prefix: str,
    start_index: int,
) -> list[Path]:
    paths: list[Path] = []
    previous_output: np.ndarray | None = None

    for offset, order in enumerate(TAYLOR_ORDERS):
        current_output = taylor_tanh(signal, order)
        filename = f"{start_index + offset:02d}_{prefix}_taylor_order_{order:02d}_time.png"

        if order == 1:
            traces = [
                (current_output, r"$y_1[n]=x[n]$", SIGNAL_BLACK, 2.7, 0.98, "-"),
            ]
        else:
            traces = [
                (signal, r"$x[n]$", LIGHT_GREY, 2.0, 0.78, "--"),
            ]
            if previous_output is not None:
                previous_label = rf"$y_{{{TAYLOR_ORDERS[offset - 1]}}}[n]$"
                traces.append((previous_output, previous_label, TAYLOR_LIGHT_GREEN, 2.2, 0.78, "--"))
            traces.append((current_output, rf"$y_{{{order}}}[n]$", SPECTRUM_BLUE, 2.8, 0.98, "-"))

        paths.append(
            save_time_plot(
                output_dir,
                time_s,
                traces,
                title=f"Taylor output: order {order}",
                y_limit=(-1.2, 1.2),
                filename=filename,
                legend=True,
            )
        )
        previous_output = current_output

    return paths


def export_single_sine(time_s: np.ndarray, spectrum_time_s: np.ndarray) -> list[Path]:
    x = single_sine_signal(time_s)
    x_spectrum = single_sine_signal(spectrum_time_s)
    y_poly = polynomial_nonlinearity(x)
    y_clip = hard_clip(x)
    y_poly_spectrum = polynomial_nonlinearity(x_spectrum)
    y_clip_spectrum = hard_clip(x_spectrum)

    input_components = [(SINGLE_FREQUENCY_HZ, 0.5 * SINGLE_AMPLITUDE)]
    polynomial_components = positive_side_two_sided_fft_components(
        y_poly_spectrum,
        sample_rate_hz=SPECTRUM_SAMPLE_RATE_HZ,
        threshold=SPECTRUM_THRESHOLD,
    )
    clipped_components = positive_side_two_sided_fft_components(
        y_clip_spectrum,
        sample_rate_hz=SPECTRUM_SAMPLE_RATE_HZ,
        threshold=SPECTRUM_THRESHOLD,
    )

    paths = [
        save_time_plot(
            SINGLE_OUTPUT_DIR,
            time_s,
            [(x, r"$x[n]$", SIGNAL_BLACK, 2.4, 0.96, "-")],
            title="Single sine input",
            y_limit=(-1.2, 1.2),
            filename="01_single_sine_input_time.png",
        ),
        save_line_spectrum(
            SINGLE_OUTPUT_DIR,
            component_lines(input_components, color=SIGNAL_BLACK),
            title="Single sine spectrum",
            y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
            filename="02_single_sine_input_spectrum.png",
        ),
    ]
    paths += export_taylor_build_time_plots(
        SINGLE_OUTPUT_DIR,
        time_s,
        x,
        prefix="single_sine",
        start_index=3,
    )
    paths += export_power_term_overviews(
        SINGLE_OUTPUT_DIR,
        time_s,
        x,
        x_spectrum,
        input_components,
        prefix="single_sine",
        start_index=11,
        spectrum_y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
    )
    paths += [
        save_line_spectrum(
            SINGLE_OUTPUT_DIR,
            component_lines(polynomial_components, color=TAYLOR_GREEN),
            title="Taylor output spectrum",
            y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
            filename="19_single_sine_taylor_order_15_spectrum.png",
            reference_components=input_components,
        ),
        save_time_plot(
            SINGLE_OUTPUT_DIR,
            time_s,
            [
                (x, r"$x[n]$", LIGHT_GREY, 2.0, 0.82, "--"),
                (y_clip, r"$y[n]=\operatorname{clip}(x[n])$", SPECTRUM_BLUE, 2.8, 0.98, "-"),
            ],
            title="Hard clipping output",
            y_limit=(-1.2, 1.2),
            filename="20_single_sine_hard_clipping_time.png",
            legend=True,
        ),
        save_line_spectrum(
            SINGLE_OUTPUT_DIR,
            component_lines(clipped_components, color=SPECTRUM_BLUE),
            title="Hard clipping spectrum",
            y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
            filename="21_single_sine_hard_clipping_spectrum.png",
            reference_components=input_components,
        ),
        save_line_spectrum(
            SINGLE_OUTPUT_DIR,
            component_lines(input_components, color=LIGHT_GREY, lw=3.4)
            + component_lines(polynomial_components, color=TAYLOR_GREEN, lw=2.4)
            + component_lines(clipped_components, color=SPECTRUM_BLUE, lw=1.9),
            title="Single sine component overview",
            y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
            filename="22_single_sine_component_overview.png",
        ),
    ]
    return paths


def export_two_tone(time_s: np.ndarray, spectrum_time_s: np.ndarray) -> list[Path]:
    x1, x2, x = two_tone_signals(time_s)
    _, _, x_spectrum = two_tone_signals(spectrum_time_s)
    y_poly = polynomial_nonlinearity(x)
    y_clip = hard_clip(x)
    y_poly_spectrum = polynomial_nonlinearity(x_spectrum)
    y_clip_spectrum = hard_clip(x_spectrum)

    input_components = [
        (FREQUENCY_1_HZ, 0.5 * TONE_AMPLITUDE),
        (FREQUENCY_2_HZ, 0.5 * TONE_AMPLITUDE),
    ]
    polynomial_components = positive_side_two_sided_fft_components(
        y_poly_spectrum,
        sample_rate_hz=SPECTRUM_SAMPLE_RATE_HZ,
        threshold=SPECTRUM_THRESHOLD,
    )
    clipped_components = positive_side_two_sided_fft_components(
        y_clip_spectrum,
        sample_rate_hz=SPECTRUM_SAMPLE_RATE_HZ,
        threshold=SPECTRUM_THRESHOLD,
    )

    paths = [
        save_time_plot(
            TWO_TONE_OUTPUT_DIR,
            time_s,
            [
                (x1, r"$x_1[n]$", LIGHT_GREY, 2.0, 0.92, "-"),
                (x2, r"$x_2[n]$", REFERENCE_GREY, 2.0, 0.90, "-"),
                (x, r"$x[n]$", SIGNAL_BLACK, 2.7, 0.98, "-"),
            ],
            title="Two-tone input",
            y_limit=(-1.2, 1.2),
            filename="01_two_tone_input_time.png",
            legend=True,
        ),
        save_line_spectrum(
            TWO_TONE_OUTPUT_DIR,
            component_lines(input_components, color=SIGNAL_BLACK),
            title="Two-tone input spectrum",
            y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
            filename="02_two_tone_input_spectrum.png",
        ),
    ]
    paths += export_taylor_build_time_plots(
        TWO_TONE_OUTPUT_DIR,
        time_s,
        x,
        prefix="two_tone",
        start_index=3,
    )
    paths += export_power_term_overviews(
        TWO_TONE_OUTPUT_DIR,
        time_s,
        x,
        x_spectrum,
        input_components,
        prefix="two_tone",
        start_index=11,
        spectrum_y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
    )
    paths += [
        save_line_spectrum(
            TWO_TONE_OUTPUT_DIR,
            component_lines(polynomial_components, color=TAYLOR_GREEN),
            title="Taylor output spectrum",
            y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
            filename="19_two_tone_taylor_order_15_spectrum.png",
            reference_components=input_components,
        ),
        save_time_plot(
            TWO_TONE_OUTPUT_DIR,
            time_s,
            [
                (x, r"$x[n]$", LIGHT_GREY, 2.0, 0.82, "--"),
                (y_clip, r"$y[n]=\operatorname{clip}(x[n])$", SPECTRUM_BLUE, 2.8, 0.98, "-"),
            ],
            title="Hard clipping output",
            y_limit=(-1.2, 1.2),
            filename="20_two_tone_hard_clipping_output_time.png",
            legend=True,
        ),
        save_line_spectrum(
            TWO_TONE_OUTPUT_DIR,
            component_lines(clipped_components, color=SPECTRUM_BLUE),
            title="Hard clipping spectrum",
            y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
            filename="21_two_tone_hard_clipping_spectrum.png",
            reference_components=input_components,
        ),
        save_line_spectrum(
            TWO_TONE_OUTPUT_DIR,
            component_lines(input_components, color=LIGHT_GREY, lw=3.4)
            + component_lines(polynomial_components, color=TAYLOR_GREEN, lw=2.4)
            + component_lines(clipped_components, color=SPECTRUM_BLUE, lw=1.9),
            title="IMD component overview",
            y_limit=(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING),
            filename="22_two_tone_imd_component_overview.png",
        ),
    ]
    return paths

def main() -> None:
    clear_output_dirs()
    time_s = np.arange(int(round(DURATION_S * SAMPLE_RATE_HZ))) / SAMPLE_RATE_HZ
    spectrum_time_s = np.arange(int(round(SPECTRUM_DURATION_S * SPECTRUM_SAMPLE_RATE_HZ))) / SPECTRUM_SAMPLE_RATE_HZ
    image_paths = export_single_sine(time_s, spectrum_time_s) + export_two_tone(time_s, spectrum_time_s)

    for path in image_paths:
        print(path.relative_to(LECTURE_DIR))


if __name__ == "__main__":
    main()
