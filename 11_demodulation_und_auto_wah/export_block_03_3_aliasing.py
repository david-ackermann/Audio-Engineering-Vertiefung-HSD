from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


LECTURE_DIR = Path(__file__).resolve().parent
BASE_STORYBOARD_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "05_aliasing"
)
OUTPUT_DIR = BASE_STORYBOARD_DIR / "05A_48khz"
OUTPUT_DIR_48KHZ = BASE_STORYBOARD_DIR / "05A_48khz"
OUTPUT_DIR_96KHZ = BASE_STORYBOARD_DIR / "05B_96khz"
OUTPUT_DIR_192KHZ = BASE_STORYBOARD_DIR / "05C_192khz"
OUTPUT_DIR_384KHZ = BASE_STORYBOARD_DIR / "05D_384khz"

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (24.0, 4.8)

SIGNAL_BLACK = "0.10"
INPUT_LIGHT_GREY = "0.72"
OUTPUT_BLUE = "#2b7bbb"
FOLDBACK_BLUE = "#75b9df"
FILTER_GREEN = "#2f8f46"
REMOVED_GREY = "0.62"
SHIFTED_GREY = "0.58"
LIGHT_GREY = "0.86"
REFERENCE_GREY = "0.68"
GRID_GREY = "0.75"
NYQUIST_GREY = "0.35"

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
LEGEND_SIZE = 13

FS_HZ = 48_000.0
FS_ANALYSIS_HZ = FS_HZ * 16
NYQUIST_HZ = FS_HZ / 2.0

F0_HZ = 5_000.0
DURATION_S = 1.0
DISPLAY_DURATION_MS = 2.0
CLIP_THRESHOLD = 0.5
LOWPASS_CUTOFF_HZ = 24_000.0

BASE_SPECTRUM_LIMIT_HZ = 96_000.0
SPECTRUM_LIMIT_HZ = BASE_SPECTRUM_LIMIT_HZ
SPECTRUM_DB_FLOOR = -80.0
SPECTRUM_DB_CEILING = 9.0
SPECTRUM_Y_LIMIT = (SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING)
SPECTRUM_THRESHOLD = 10 ** (SPECTRUM_DB_FLOOR / 20.0)

COEFFICIENT_FFT_SIZE = 262_144
_CLIPPED_COEFFICIENT_CACHE: list[tuple[int, complex]] | None = None

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def hard_clip(signal: np.ndarray) -> np.ndarray:
    return np.clip(signal, -CLIP_THRESHOLD, CLIP_THRESHOLD)


def alias_frequency(frequency_hz: float, sample_rate_hz: float) -> float:
    wrapped = ((frequency_hz + sample_rate_hz / 2.0) % sample_rate_hz) - sample_rate_hz / 2.0
    return abs(wrapped)


def positive_two_sided_amplitude_at(signal: np.ndarray, sample_rate_hz: float, frequency_hz: float) -> float:
    spectrum = np.fft.rfft(signal)
    bin_index = int(round(frequency_hz * len(signal) / sample_rate_hz))
    if bin_index < 0 or bin_index >= len(spectrum):
        return 0.0
    return float(abs(spectrum[bin_index]) / len(signal))


def amplitude_to_db(amplitude: float) -> float:
    return max(SPECTRUM_DB_FLOOR, 20.0 * np.log10(max(float(amplitude), SPECTRUM_THRESHOLD)))


def lowpass_ideal(signal: np.ndarray, sample_rate_hz: float, cutoff_hz: float) -> np.ndarray:
    spectrum = np.fft.rfft(signal)
    frequencies_hz = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate_hz)
    spectrum[frequencies_hz > cutoff_hz] = 0.0
    return np.fft.irfft(spectrum, n=len(signal))


def merge_components(components: list[tuple[float, float]]) -> list[tuple[float, float]]:
    merged: dict[float, float] = {}
    for frequency_hz, amplitude in components:
        key = round(float(frequency_hz), 6)
        merged[key] = merged.get(key, 0.0) + float(amplitude)
    return sorted((frequency_hz, amplitude) for frequency_hz, amplitude in merged.items())


def style_time_axis(ax: plt.Axes) -> None:
    ax.set_xlabel("Time (ms)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=REFERENCE_GREY, lw=0.9)
    ax.set_xlim(0.0, DISPLAY_DURATION_MS)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks(np.arange(0.0, DISPLAY_DURATION_MS + 0.001, 0.5))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def style_spectrum_axis(
    ax: plt.Axes,
    *,
    shade_above_base_nyquist: bool = False,
    show_base_nyquist: bool = False,
    show_sample_rate_marker: bool = False,
    show_internal_nyquist: bool = False,
) -> None:
    ax.set_xlabel("Frequency (kHz)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Two-sided amplitude (dB)", fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.grid(True, which="minor", color=GRID_GREY, alpha=0.14)
    ax.axhline(0.0, color=REFERENCE_GREY, lw=0.9)
    ax.set_xlim(0.0, SPECTRUM_LIMIT_HZ / 1000.0)
    ax.set_ylim(*SPECTRUM_Y_LIMIT)
    spectrum_limit_khz = SPECTRUM_LIMIT_HZ / 1000.0
    major_tick_khz = 2.0 if spectrum_limit_khz <= 96.0 else 8.0
    minor_tick_khz = 1.0 if spectrum_limit_khz <= 96.0 else 4.0
    ax.set_xticks(np.arange(0.0, spectrum_limit_khz + 0.001, major_tick_khz))
    ax.set_xticks(np.arange(0.0, spectrum_limit_khz + 0.001, minor_tick_khz), minor=True)
    y_ticks = list(np.arange(SPECTRUM_DB_FLOOR, SPECTRUM_DB_CEILING + 0.001, 20.0))
    if not np.isclose(y_ticks[-1], SPECTRUM_DB_CEILING):
        y_ticks.append(SPECTRUM_DB_CEILING)
    ax.set_yticks(y_ticks)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    nyquist_khz = NYQUIST_HZ / 1000.0
    nyquist_visible = 0.0 <= nyquist_khz <= spectrum_limit_khz
    sample_rate_khz = FS_HZ / 1000.0
    sample_rate_visible = 0.0 <= sample_rate_khz <= spectrum_limit_khz

    if shade_above_base_nyquist and NYQUIST_HZ < SPECTRUM_LIMIT_HZ:
        ax.axvspan(NYQUIST_HZ / 1000.0, SPECTRUM_LIMIT_HZ / 1000.0, color=LIGHT_GREY, alpha=0.16, zorder=0)

    if show_base_nyquist and nyquist_visible:
        ax.axvline(nyquist_khz, color=NYQUIST_GREY, lw=1.3, ls="--", zorder=2)
        nyquist_text_x = nyquist_khz + 0.8
        nyquist_text_ha = "left"
        if nyquist_text_x > spectrum_limit_khz - 2.0:
            nyquist_text_x = nyquist_khz - 0.8
            nyquist_text_ha = "right"
        ax.text(
            nyquist_text_x,
            -5.0,
            rf"$f_s/2={nyquist_khz:.0f}\,\mathrm{{kHz}}$",
            fontsize=LEGEND_SIZE,
            color=NYQUIST_GREY,
            ha=nyquist_text_ha,
            va="top",
        )
    if show_sample_rate_marker and sample_rate_visible:
        ax.axvline(sample_rate_khz, color=NYQUIST_GREY, lw=1.0, ls=":", alpha=0.75, zorder=2)
        ax.text(
            sample_rate_khz - 0.8,
            SPECTRUM_DB_FLOOR + 8.0,
            rf"$f_s={sample_rate_khz:.0f}\,\mathrm{{kHz}}$",
            fontsize=LEGEND_SIZE,
            color=NYQUIST_GREY,
            ha="right",
            va="bottom",
        )

    if show_internal_nyquist:
        ax.axvline(NYQUIST_INTERNAL_HZ / 1000.0, color=NYQUIST_GREY, lw=1.3, ls=":", zorder=2)
        ax.text(
            NYQUIST_INTERNAL_HZ / 1000.0 - 1.2,
            SPECTRUM_DB_FLOOR + 8.0,
            r"$Lf_s/2=96\,\mathrm{kHz}$",
            fontsize=LEGEND_SIZE,
            color=NYQUIST_GREY,
            ha="right",
            va="bottom",
        )


def save_time_plot(
    time_s: np.ndarray,
    traces: list[tuple[np.ndarray, str, str, float, float]],
    *,
    title: str,
    filename: str,
    sample_rate_hz: float,
) -> Path:
    display_samples = int(round(DISPLAY_DURATION_MS * 1e-3 * sample_rate_hz))
    time_ms = 1000.0 * time_s[:display_samples]

    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    handles: list[Line2D] = []
    labels: list[str] = []
    for signal, label, color, lw, alpha in traces:
        ax.plot(time_ms, signal[:display_samples], color=color, lw=lw, alpha=alpha)
        handles.append(Line2D([0], [0], color=color, lw=lw, alpha=alpha))
        labels.append(label)

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    style_time_axis(ax)
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
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def draw_stems(
    ax: plt.Axes,
    components: list[tuple[float, float]],
    *,
    color: str,
    lw: float,
    alpha: float = 1.0,
    zorder: int = 4,
    linestyle: str = "-",
) -> None:
    for frequency_hz, amplitude in components:
        amplitude_db = amplitude_to_db(amplitude)
        ax.vlines(
            frequency_hz / 1000.0,
            SPECTRUM_DB_FLOOR,
            amplitude_db,
            color=color,
            lw=lw,
            alpha=alpha,
            zorder=zorder,
            linestyles=linestyle,
        )


def draw_styled_stems(
    ax: plt.Axes,
    components: list[tuple[float, float, str, str, float, float]],
    *,
    zorder: int = 6,
) -> None:
    for frequency_hz, amplitude, color, linestyle, lw, alpha in components:
        amplitude_db = amplitude_to_db(amplitude)
        ax.vlines(
            frequency_hz / 1000.0,
            SPECTRUM_DB_FLOOR,
            amplitude_db,
            color=color,
            lw=lw,
            alpha=alpha,
            zorder=zorder,
            linestyles=linestyle,
        )


def add_legend(ax: plt.Axes, legend_items: list[tuple[str, str, str]] | None) -> None:
    if not legend_items:
        return
    handles = [
        Line2D([0], [0], color=color, lw=3.2, ls=linestyle)
        for label, color, linestyle in legend_items
    ]
    labels = [label for label, _, _ in legend_items]
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


def draw_ideal_lowpass(ax: plt.Axes, cutoff_hz: float) -> None:
    cutoff_khz = cutoff_hz / 1000.0

    ax.plot(
        [0.0, cutoff_khz],
        [0.0, 0.0],
        color=FILTER_GREEN,
        lw=3.0,
        alpha=0.98,
        zorder=8,
    )
    ax.vlines(
        cutoff_khz,
        SPECTRUM_DB_FLOOR,
        0.0,
        color=FILTER_GREEN,
        lw=3.0,
        alpha=0.98,
        zorder=8,
    )


def save_spectrum_plot(
    *,
    title: str,
    filename: str,
    blue_components: list[tuple[float, float]] | None = None,
    black_components: list[tuple[float, float]] | None = None,
    grey_components: list[tuple[float, float]] | None = None,
    alias_components: list[tuple[float, float]] | None = None,
    folded_components: list[tuple[float, float, str, str, float, float]] | None = None,
    shade_above_base_nyquist: bool = False,
    show_base_nyquist: bool = False,
    show_sample_rate_marker: bool = False,
    show_internal_nyquist: bool = False,
    show_lowpass_filter: bool = False,
    legend_items: list[tuple[str, str, str]] | None = None,
) -> Path:
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    style_spectrum_axis(
        ax,
        shade_above_base_nyquist=shade_above_base_nyquist,
        show_base_nyquist=show_base_nyquist,
        show_sample_rate_marker=show_sample_rate_marker,
        show_internal_nyquist=show_internal_nyquist,
    )

    if grey_components:
        draw_stems(ax, grey_components, color=REMOVED_GREY, lw=4.4, alpha=0.76, zorder=3)
    if black_components:
        draw_stems(ax, black_components, color=SIGNAL_BLACK, lw=4.2, alpha=0.96, zorder=5)
    if alias_components:
        draw_stems(ax, alias_components, color=FOLDBACK_BLUE, lw=3.6, alpha=0.98, zorder=6, linestyle="--")
    if folded_components:
        draw_styled_stems(ax, folded_components, zorder=6)
    if blue_components:
        draw_stems(ax, blue_components, color=OUTPUT_BLUE, lw=3.4, alpha=0.98, zorder=7)
    if show_lowpass_filter:
        draw_ideal_lowpass(ax, min(LOWPASS_CUTOFF_HZ, SPECTRUM_LIMIT_HZ))

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def harmonic_components(signal: np.ndarray, sample_rate_hz: float) -> list[tuple[float, float, int]]:
    components: list[tuple[float, float, int]] = []
    for harmonic, coefficient in clipped_cosine_coefficients():
        frequency_hz = harmonic * F0_HZ
        if frequency_hz > SPECTRUM_LIMIT_HZ:
            continue
        amplitude = float(abs(coefficient))
        if amplitude >= SPECTRUM_THRESHOLD:
            components.append((frequency_hz, amplitude, harmonic))
    return components


def component_pairs(components: list[tuple[float, float, int]]) -> list[tuple[float, float]]:
    return [(frequency_hz, amplitude) for frequency_hz, amplitude, _ in components]


def clipped_cosine_coefficients() -> list[tuple[int, complex]]:
    global _CLIPPED_COEFFICIENT_CACHE

    if _CLIPPED_COEFFICIENT_CACHE is None:
        phase = 2.0 * np.pi * np.arange(COEFFICIENT_FFT_SIZE) / COEFFICIENT_FFT_SIZE
        clipped_period = hard_clip(np.cos(phase))
        coefficients = np.fft.rfft(clipped_period) / COEFFICIENT_FFT_SIZE
        _CLIPPED_COEFFICIENT_CACHE = [
            (harmonic, coefficients[harmonic])
            for harmonic in range(1, len(coefficients), 2)
            if abs(coefficients[harmonic]) >= SPECTRUM_THRESHOLD
        ]

    return _CLIPPED_COEFFICIENT_CACHE


def higher_harmonic_alias_components(
    sample_rate_hz: float,
    *,
    min_source_frequency_hz: float,
    max_alias_frequency_hz: float,
) -> list[tuple[float, float]]:
    alias_bins: dict[float, complex] = {}

    for harmonic, coefficient in clipped_cosine_coefficients():
        source_frequency_hz = harmonic * F0_HZ
        if source_frequency_hz <= min_source_frequency_hz:
            continue

        signed_alias_hz = ((source_frequency_hz + sample_rate_hz / 2.0) % sample_rate_hz) - sample_rate_hz / 2.0
        alias_frequency_hz = abs(signed_alias_hz)
        if alias_frequency_hz > max_alias_frequency_hz:
            continue

        contribution = coefficient if signed_alias_hz >= 0.0 else np.conj(coefficient)
        key = round(float(alias_frequency_hz), 6)
        alias_bins[key] = alias_bins.get(key, 0.0 + 0.0j) + contribution

    components = [
        (frequency_hz, abs(coefficient))
        for frequency_hz, coefficient in alias_bins.items()
        if abs(coefficient) >= SPECTRUM_THRESHOLD
    ]
    return sorted(components)


def foldback_target(frequency_hz: float, amplitude: float) -> tuple[float, float, int, str]:
    first_reflection_hz = 2.0 * NYQUIST_HZ - frequency_hz
    if 0.0 <= first_reflection_hz <= NYQUIST_HZ:
        return first_reflection_hz, amplitude, 1, "-"

    second_reflection_hz = abs(first_reflection_hz)
    if 0.0 <= second_reflection_hz <= NYQUIST_HZ:
        return second_reflection_hz, amplitude, 2, "--"

    third_reflection_hz = 2.0 * NYQUIST_HZ - second_reflection_hz
    if 0.0 <= third_reflection_hz <= NYQUIST_HZ:
        return third_reflection_hz, amplitude, 3, "-."

    return alias_frequency(frequency_hz, FS_HZ), amplitude, 3, "-."


def folded_component_targets(
    components: list[tuple[float, float, int]]
) -> list[tuple[float, float, int, str, int]]:
    targets: list[tuple[float, float, int, str, int]] = []
    for frequency_hz, amplitude, harmonic in components:
        target_hz, target_amplitude, stage, linestyle = foldback_target(frequency_hz, amplitude)
        targets.append((target_hz, target_amplitude, stage, linestyle, harmonic))
    return targets


def styled_fold_components(
    targets: list[tuple[float, float, int, str, int]],
    *,
    current_harmonic: int | None,
) -> list[tuple[float, float, str, str, float, float]]:
    styled: list[tuple[float, float, str, str, float, float]] = []
    for frequency_hz, amplitude, _stage, linestyle, harmonic in targets:
        is_current = harmonic == current_harmonic
        styled.append(
            (
                frequency_hz,
                amplitude,
                FOLDBACK_BLUE if is_current else SHIFTED_GREY,
                linestyle,
                4.2 if is_current else 3.2,
                0.98 if is_current else 0.62,
            )
        )
    return styled


def measured_components(signal: np.ndarray, sample_rate_hz: float, candidate_frequencies_hz: list[float]) -> list[tuple[float, float]]:
    components: list[tuple[float, float]] = []
    for frequency_hz in candidate_frequencies_hz:
        amplitude = positive_two_sided_amplitude_at(signal, sample_rate_hz, frequency_hz)
        if amplitude >= SPECTRUM_THRESHOLD:
            components.append((frequency_hz, amplitude))
    return merge_components(components)


def sampled_spectrum_components(signal: np.ndarray, sample_rate_hz: float) -> list[tuple[float, float]]:
    spectrum = np.fft.rfft(signal)
    frequencies_hz = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate_hz)
    components: list[tuple[float, float]] = []

    for frequency_hz, coefficient in zip(frequencies_hz, spectrum):
        if frequency_hz > min(NYQUIST_HZ, SPECTRUM_LIMIT_HZ):
            continue
        amplitude = float(abs(coefficient) / len(signal))
        if amplitude >= SPECTRUM_THRESHOLD:
            components.append((float(frequency_hz), amplitude))

    return components


def bandlimited_reconstruction(signal: np.ndarray, sample_rate_hz: float, evaluation_time_s: np.ndarray) -> np.ndarray:
    coefficients = np.fft.rfft(signal) / len(signal)
    frequencies_hz = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate_hz)
    output = np.full_like(evaluation_time_s, coefficients[0].real, dtype=float)

    for bin_index in range(1, len(coefficients)):
        coefficient = coefficients[bin_index]
        if abs(coefficient) < SPECTRUM_THRESHOLD:
            continue
        frequency_hz = frequencies_hz[bin_index]
        phase = np.exp(1j * 2.0 * np.pi * frequency_hz * evaluation_time_s)
        if bin_index == len(coefficients) - 1 and len(signal) % 2 == 0:
            output += np.real(coefficient * phase)
        else:
            output += 2.0 * np.real(coefficient * phase)

    return output


def sample_rate_label(sample_rate_hz: float) -> str:
    return f"{sample_rate_hz / 1000.0:.0f} kHz"


def sample_rate_tag(sample_rate_hz: float) -> str:
    return f"{sample_rate_hz / 1000.0:.0f}khz"


def export_series(*, sample_rate_hz: float, output_dir: Path) -> None:
    global OUTPUT_DIR, FS_HZ, FS_ANALYSIS_HZ, NYQUIST_HZ, SPECTRUM_LIMIT_HZ

    OUTPUT_DIR = output_dir
    FS_HZ = sample_rate_hz
    FS_ANALYSIS_HZ = FS_HZ * 16
    NYQUIST_HZ = FS_HZ / 2.0
    SPECTRUM_LIMIT_HZ = BASE_SPECTRUM_LIMIT_HZ

    fs_label = sample_rate_label(FS_HZ)
    fs_tag = sample_rate_tag(FS_HZ)
    spectrum_limit_tag = f"{int(round(SPECTRUM_LIMIT_HZ / 1000.0))}khz"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()

    n_base = int(round(DURATION_S * FS_HZ))
    n_analysis = int(round(DURATION_S * FS_ANALYSIS_HZ))

    time_base_s = np.arange(n_base) / FS_HZ
    time_analysis_s = np.arange(n_analysis) / FS_ANALYSIS_HZ

    x_base = np.cos(2.0 * np.pi * F0_HZ * time_base_s)
    y_base = hard_clip(x_base)

    x_analysis = np.cos(2.0 * np.pi * F0_HZ * time_analysis_s)
    y_analysis = hard_clip(x_analysis)
    display_samples_analysis = int(round(DISPLAY_DURATION_MS * 1e-3 * FS_ANALYSIS_HZ))
    y_alias_analysis = bandlimited_reconstruction(y_base, FS_HZ, time_analysis_s[:display_samples_analysis])
    y_lowpass_base = lowpass_ideal(y_base, FS_HZ, min(LOWPASS_CUTOFF_HZ, NYQUIST_HZ))
    y_lowpass_analysis = bandlimited_reconstruction(y_lowpass_base, FS_HZ, time_analysis_s[:display_samples_analysis])

    input_component = [(F0_HZ, 0.5)]
    ideal_components = harmonic_components(y_analysis, FS_ANALYSIS_HZ)
    below_base_nyquist = [component for component in ideal_components if component[0] <= NYQUIST_HZ]
    above_base_nyquist = [component for component in ideal_components if component[0] > NYQUIST_HZ]
    folded_targets = folded_component_targets(above_base_nyquist)

    alias_candidates = sorted({frequency_hz for frequency_hz, _amplitude, _stage, _linestyle, _harmonic in folded_targets})
    low_rate_alias_measured = measured_components(y_base, FS_HZ, alias_candidates)
    measured_alias_by_frequency = {round(frequency_hz, 6): amplitude for frequency_hz, amplitude in low_rate_alias_measured}
    measured_folded_targets = [
        (
            frequency_hz,
            measured_alias_by_frequency.get(round(frequency_hz, 6), amplitude),
            stage,
            linestyle,
            harmonic,
        )
        for frequency_hz, amplitude, stage, linestyle, harmonic in folded_targets
    ]
    higher_alias_nyquist_components = higher_harmonic_alias_components(
        FS_HZ,
        min_source_frequency_hz=SPECTRUM_LIMIT_HZ,
        max_alias_frequency_hz=min(NYQUIST_HZ, SPECTRUM_LIMIT_HZ),
    )

    fold_step_images = []
    previous_targets: list[tuple[float, float, int, str, int]] = []
    for step_index, target in enumerate(measured_folded_targets, start=6):
        target_hz, _target_amplitude, stage, _linestyle, harmonic = target
        fold_step_images.append(
            save_spectrum_plot(
                title=rf"Foldback step {step_index - 5}: $h={harmonic}$",
                filename=f"{step_index:02d}_fold_h{harmonic:02d}_to_{target_hz / 1000.0:.0f}khz.png",
                blue_components=component_pairs(below_base_nyquist),
                grey_components=component_pairs(above_base_nyquist),
                folded_components=styled_fold_components(previous_targets + [target], current_harmonic=harmonic)
                + [
                    (
                        harmonic * F0_HZ,
                        target[1],
                        FOLDBACK_BLUE,
                        target[3],
                        4.2,
                        0.98,
                    )
                ],
                shade_above_base_nyquist=True,
                show_base_nyquist=True,
                legend_items=[
                    ("representable", OUTPUT_BLUE, "-"),
                    ("above Nyquist", REMOVED_GREY, "-"),
                    ("current fold", FOLDBACK_BLUE, "-" if stage == 1 else "--" if stage == 2 else "-."),
                    ("already folded", SHIFTED_GREY, "-"),
                ],
            )
        )
        previous_targets.append(target)

    high_alias_index = 6 + len(fold_step_images)
    final_spectrum_index = high_alias_index + 1
    lowpass_spectrum_index = final_spectrum_index + 1
    raw_time_index = lowpass_spectrum_index + 1
    lowpass_time_index = raw_time_index + 1
    final_spectrum_title = (
        f"{fs_label} output: aliases below Nyquist"
        if measured_folded_targets or higher_alias_nyquist_components
        else f"{fs_label} output: no aliases below Nyquist"
    )
    higher_alias_title = (
        rf"{fs_label}: all aliases below $f_s/2$"
        if higher_alias_nyquist_components
        else rf"{fs_label}: no additional aliases below $f_s/2$"
    )
    low_order_folded_visible = [
        (frequency_hz, amplitude, SHIFTED_GREY, linestyle, 2.8, 0.52)
        for frequency_hz, amplitude, _stage, linestyle, _harmonic in measured_folded_targets
    ]
    higher_alias_nyquist_stems = [
        (frequency_hz, amplitude, FOLDBACK_BLUE, ":", 3.2, 0.96)
        for frequency_hz, amplitude in higher_alias_nyquist_components
    ]
    sampled_output_components = sampled_spectrum_components(y_base, FS_HZ)
    below_lowpass = [component for component in sampled_output_components if component[0] <= LOWPASS_CUTOFF_HZ]
    above_lowpass = [component for component in sampled_output_components if component[0] > LOWPASS_CUTOFF_HZ]

    image_paths = [
        save_time_plot(
            time_analysis_s,
            [(x_analysis, r"$x[n]$", SIGNAL_BLACK, 2.4, 0.96)],
            title="Input before NLT",
            filename="01_input_before_nlt_time.png",
            sample_rate_hz=FS_ANALYSIS_HZ,
        ),
        save_spectrum_plot(
            title="Input spectrum before NLT",
            filename=f"02_input_before_nlt_spectrum_to_{spectrum_limit_tag}.png",
            black_components=input_component,
            legend_items=[(r"$x[n]$", SIGNAL_BLACK, "-")],
        ),
        save_time_plot(
            time_analysis_s,
            [
                (x_analysis, r"$x[n]$", INPUT_LIGHT_GREY, 2.1, 0.82),
                (y_analysis, r"$y[n]$", OUTPUT_BLUE, 2.8, 0.98),
            ],
            title=r"Hard clipping, $T=0.5$",
            filename="03_hard_clipped_output_time.png",
            sample_rate_hz=FS_ANALYSIS_HZ,
        ),
        save_spectrum_plot(
            title="Hard clipping: harmonics without aliasing",
            filename=f"04_unaliased_harmonics_to_{spectrum_limit_tag}.png",
            blue_components=component_pairs(ideal_components),
            legend_items=[(r"$y[n]$", OUTPUT_BLUE, "-")],
        ),
        save_spectrum_plot(
            title=f"{fs_label} sampling: Nyquist boundary",
            filename=f"05_{fs_tag}_nyquist_boundary.png",
            blue_components=component_pairs(below_base_nyquist),
            grey_components=component_pairs(above_base_nyquist),
            shade_above_base_nyquist=True,
            show_base_nyquist=True,
            show_sample_rate_marker=True,
            legend_items=[
                ("representable", OUTPUT_BLUE, "-"),
                ("above Nyquist", REMOVED_GREY, "-"),
            ],
        ),
        *fold_step_images,
        save_spectrum_plot(
            title=higher_alias_title,
            filename=f"{high_alias_index:02d}_{fs_tag}_aliases_below_nyquist.png",
            blue_components=component_pairs(below_base_nyquist),
            grey_components=component_pairs(above_base_nyquist),
            folded_components=low_order_folded_visible + higher_alias_nyquist_stems,
            shade_above_base_nyquist=True,
            show_base_nyquist=True,
        ),
        save_spectrum_plot(
            title=final_spectrum_title,
            filename=f"{final_spectrum_index:02d}_{fs_tag}_aliased_output_spectrum.png",
            blue_components=sampled_output_components,
            shade_above_base_nyquist=True,
            show_base_nyquist=True,
        ),
        save_spectrum_plot(
            title=f"{fs_label}: 24 kHz lowpass after foldback",
            filename=f"{lowpass_spectrum_index:02d}_{fs_tag}_ideal_24khz_lowpass_spectrum.png",
            blue_components=below_lowpass,
            grey_components=above_lowpass,
            show_lowpass_filter=True,
            show_base_nyquist=True,
        ),
        save_time_plot(
            time_analysis_s,
            [
                (x_analysis, r"$x[n]$", INPUT_LIGHT_GREY, 2.1, 0.82),
                (y_alias_analysis, r"$y[n]$", OUTPUT_BLUE, 2.8, 0.98),
            ],
            title=f"{fs_label} output without lowpass",
            filename=f"{raw_time_index:02d}_{fs_tag}_output_without_lowpass_time.png",
            sample_rate_hz=FS_ANALYSIS_HZ,
        ),
        save_time_plot(
            time_analysis_s,
            [
                (x_analysis, r"$x[n]$", INPUT_LIGHT_GREY, 2.1, 0.82),
                (y_lowpass_analysis, r"$y[n]$", OUTPUT_BLUE, 2.8, 0.98),
            ],
            title=f"{fs_label} output after 24 kHz lowpass",
            filename=f"{lowpass_time_index:02d}_{fs_tag}_output_24khz_lowpass_time.png",
            sample_rate_hz=FS_ANALYSIS_HZ,
        ),
    ]

    for path in image_paths:
        print(path.relative_to(LECTURE_DIR))


def main() -> None:
    export_series(sample_rate_hz=48_000.0, output_dir=OUTPUT_DIR_48KHZ)
    export_series(sample_rate_hz=96_000.0, output_dir=OUTPUT_DIR_96KHZ)
    export_series(sample_rate_hz=192_000.0, output_dir=OUTPUT_DIR_192KHZ)
    export_series(sample_rate_hz=384_000.0, output_dir=OUTPUT_DIR_384KHZ)


if __name__ == "__main__":
    main()
