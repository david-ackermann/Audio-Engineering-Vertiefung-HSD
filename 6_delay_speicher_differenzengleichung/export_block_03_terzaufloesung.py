from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "03_terzaufloesung"

DPI = 200
FIGSIZE = (12.0, 4.8)
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
NOTE_SIZE = 15

SIGNAL_BLACK = "0.10"
SPECTRUM_BLUE = "#2b7bbb"
COMPARE_ORANGE = "#d98c2f"
WINDOW_GREEN = "#66b77a"
ACTIVE_RED = "crimson"
GRID_GREY = "0.72"

SAMPLE_RATE_HZ = 48_000.0
N_FFT = 4096
F_CENTER_HZ = 1000.0
F_LOW_HZ = F_CENTER_HZ / 2 ** (1 / 6)
F_HIGH_HZ = F_CENTER_HZ * 2 ** (1 / 6)
F_MIN_PLOT_HZ = 780.0
F_MAX_PLOT_HZ = 1240.0
ANNOTATION_Y_MAX = 1.58
BOUNDARY_LABEL_Y = 1.38
CENTER_LABEL_Y = 1.20

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def fft_frequencies() -> np.ndarray:
    return np.fft.rfftfreq(N_FFT, d=1.0 / SAMPLE_RATE_HZ)


def example_pressure_magnitude(frequencies_hz: np.ndarray) -> np.ndarray:
    x = np.log2(np.maximum(frequencies_hz, 1.0) / F_CENTER_HZ)
    magnitude = (
        0.78
        + 0.11 * np.cos(2.0 * np.pi * 1.35 * x)
        + 0.08 * np.exp(-0.5 * ((frequencies_hz - 1035.0) / 38.0) ** 2)
        - 0.05 * np.exp(-0.5 * ((frequencies_hz - 948.0) / 30.0) ** 2)
    )
    return np.clip(magnitude, 0.08, None)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()


def save_figure(fig: plt.Figure, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def hz_math(value: float) -> str:
    return rf"{value:.1f}\,\mathrm{{Hz}}"


def plot_fft_bins(
    ax: plt.Axes,
    frequencies_hz: np.ndarray,
    magnitude: np.ndarray,
    *,
    selected: np.ndarray | None = None,
    show_curve: bool = True,
) -> None:
    in_view = (frequencies_hz >= F_MIN_PLOT_HZ) & (frequencies_hz <= F_MAX_PLOT_HZ)
    if selected is None:
        selected = np.zeros_like(frequencies_hz, dtype=bool)

    if show_curve:
        f_dense = np.linspace(F_MIN_PLOT_HZ, F_MAX_PLOT_HZ, 900)
        ax.plot(
            f_dense,
            example_pressure_magnitude(f_dense),
            color=SIGNAL_BLACK,
            lw=2.1,
            alpha=0.88,
            label=r"$|p(f)|$",
        )

    grey_bins = in_view & ~selected
    ax.vlines(
        frequencies_hz[grey_bins],
        0.0,
        magnitude[grey_bins],
        color=GRID_GREY,
        lw=1.0,
        alpha=0.55,
        zorder=1,
    )
    ax.scatter(
        frequencies_hz[grey_bins],
        magnitude[grey_bins],
        s=24,
        color=GRID_GREY,
        edgecolors="white",
        linewidths=0.5,
        alpha=0.80,
        zorder=2,
    )

    selected_in_view = in_view & selected
    if np.any(selected_in_view):
        ax.vlines(
            frequencies_hz[selected_in_view],
            0.0,
            magnitude[selected_in_view],
            color=SPECTRUM_BLUE,
            lw=2.0,
            alpha=0.95,
            zorder=3,
        )
        ax.scatter(
            frequencies_hz[selected_in_view],
            magnitude[selected_in_view],
            s=58,
            color=SPECTRUM_BLUE,
            edgecolors="white",
            linewidths=0.8,
            zorder=4,
        )


def shade_terzband(ax: plt.Axes, *, alpha: float = 0.13) -> None:
    ax.axvspan(F_LOW_HZ, F_HIGH_HZ, color=WINDOW_GREEN, alpha=alpha, zorder=0)


def draw_boundary(ax: plt.Axes, frequency_hz: float, label: str, *, color: str = ACTIVE_RED) -> None:
    ax.axvline(frequency_hz, color=color, lw=2.6, ls="--", zorder=4)
    ax.text(
        frequency_hz,
        BOUNDARY_LABEL_Y,
        label,
        color=color,
        fontsize=NOTE_SIZE,
        ha="center",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor=color, linewidth=1.1),
        zorder=14,
    )


def draw_center(ax: plt.Axes) -> None:
    ax.axvline(F_CENTER_HZ, color=SIGNAL_BLACK, lw=1.7, ls=":", zorder=4)
    ax.text(
        F_CENTER_HZ,
        CENTER_LABEL_Y,
        rf"$f_c={F_CENTER_HZ:.0f}\,\mathrm{{Hz}}$",
        color=SIGNAL_BLACK,
        fontsize=NOTE_SIZE,
        ha="center",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="0.75", linewidth=1.0),
        zorder=14,
    )


def setup_axis(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(F_MIN_PLOT_HZ, F_MAX_PLOT_HZ)
    ax.set_ylim(0.0, ANNOTATION_Y_MAX)
    ax.set_xticks([800, 900, 1000, 1100, 1200])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_xlabel("Frequenz in Hz", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Betrag $|p(f_i)|$", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def add_text_box(ax: plt.Axes, text: str, *, loc: tuple[float, float] = (0.02, 0.82)) -> None:
    ax.text(
        loc[0],
        loc[1],
        text,
        transform=ax.transAxes,
        fontsize=NOTE_SIZE,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="0.80", linewidth=1.0),
        zorder=11,
    )


def selected_bin_mask(frequencies_hz: np.ndarray) -> np.ndarray:
    return (frequencies_hz >= F_LOW_HZ) & (frequencies_hz < F_HIGH_HZ)


def export_f_low_frame(frequencies_hz: np.ndarray, magnitude: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.17, top=0.84)
    plot_fft_bins(ax, frequencies_hz, magnitude)
    draw_center(ax)
    draw_boundary(ax, F_LOW_HZ, rf"$f_{{\mathrm{{low}},b}}={hz_math(F_LOW_HZ)}$")
    add_text_box(
        ax,
        rf"$f_{{\mathrm{{low}},b}}=\dfrac{{f_{{c,b}}}}{{2^{{1/6}}}}$"
        "\n"
        rf"$f_{{c,b}}={F_CENTER_HZ:.0f}\,\mathrm{{Hz}}$",
    )
    setup_axis(ax, r"Terzband: zuerst die untere Bandgrenze")
    save_figure(fig, "01_untere_terzbandgrenze_f_low.png")


def export_f_high_frame(frequencies_hz: np.ndarray, magnitude: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.17, top=0.84)
    shade_terzband(ax)
    plot_fft_bins(ax, frequencies_hz, magnitude)
    draw_center(ax)
    draw_boundary(ax, F_LOW_HZ, rf"$f_{{\mathrm{{low}},b}}={hz_math(F_LOW_HZ)}$")
    draw_boundary(ax, F_HIGH_HZ, rf"$f_{{\mathrm{{high}},b}}={hz_math(F_HIGH_HZ)}$")
    add_text_box(
        ax,
        rf"$f_{{\mathrm{{high}},b}}=f_{{c,b}}\cdot2^{{1/6}}$"
        "\n"
        rf"$\dfrac{{f_{{\mathrm{{high}},b}}}}{{f_{{\mathrm{{low}},b}}}}=2^{{1/3}}$",
    )
    setup_axis(ax, r"Terzband: obere Bandgrenze kommt dazu")
    save_figure(fig, "02_obere_terzbandgrenze_f_high.png")


def export_index_set_frame(frequencies_hz: np.ndarray, magnitude: np.ndarray, selected: np.ndarray) -> None:
    selected_indices = np.flatnonzero(selected)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.17, top=0.84)
    shade_terzband(ax, alpha=0.16)
    plot_fft_bins(ax, frequencies_hz, magnitude, selected=selected)
    draw_boundary(ax, F_LOW_HZ, r"$f_{\mathrm{low},b}$")
    draw_boundary(ax, F_HIGH_HZ, r"$f_{\mathrm{high},b}$")
    ax.annotate(
        "",
        xy=(F_LOW_HZ, 0.10),
        xytext=(F_HIGH_HZ, 0.10),
        arrowprops=dict(arrowstyle="<->", color=WINDOW_GREEN, lw=2.4),
    )
    ax.text(
        F_CENTER_HZ,
        0.13,
        rf"$\mathcal{{I}}_b$: {selected_indices[0]} bis {selected_indices[-1]}",
        color=WINDOW_GREEN,
        fontsize=NOTE_SIZE,
        ha="center",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=WINDOW_GREEN, linewidth=1.0),
        zorder=12,
    )
    add_text_box(
        ax,
        r"$\mathcal{I}_b=\left\{i\,\middle|\,"
        r"f_{\mathrm{low},b}\leq f_i<f_{\mathrm{high},b}\right\}$",
    )
    setup_axis(ax, r"Indexmenge: alle FFT-Bins innerhalb des Terzbandes")
    save_figure(fig, "03_indexmenge_terzband.png")


def export_multiple_values_frame(frequencies_hz: np.ndarray, magnitude: np.ndarray, selected: np.ndarray) -> None:
    selected_indices = np.flatnonzero(selected)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.17, top=0.84)
    shade_terzband(ax, alpha=0.17)
    plot_fft_bins(ax, frequencies_hz, magnitude, selected=selected, show_curve=False)
    draw_boundary(ax, F_LOW_HZ, r"$f_{\mathrm{low},b}$")
    draw_boundary(ax, F_HIGH_HZ, r"$f_{\mathrm{high},b}$")

    label_indices = list(selected_indices[::4])
    if selected_indices[-1] not in label_indices:
        label_indices.append(selected_indices[-1])
    for bin_index in label_indices:
        ax.text(
            frequencies_hz[bin_index],
            magnitude[bin_index] + 0.055,
            rf"$i={bin_index}$",
            color=SPECTRUM_BLUE,
            fontsize=12,
            ha="center",
            va="bottom",
            zorder=12,
        )

    add_text_box(
        ax,
        rf"$f_i=i\,\Delta f,\quad \Delta f=\dfrac{{f_s}}{{N}}={SAMPLE_RATE_HZ / N_FFT:.2f}\,\mathrm{{Hz}}$"
        "\n"
        rf"$N_b=|\mathcal{{I}}_b|={selected_indices.size}$ Werte im Terzband",
    )
    setup_axis(ax, r"Ein Terzband enthält mehrere Frequenzwerte")
    save_figure(fig, "04_mehrere_fft_bins_im_terzband.png")


def export_band_average_frame(frequencies_hz: np.ndarray, magnitude: np.ndarray, selected: np.ndarray) -> None:
    selected_indices = np.flatnonzero(selected)
    band_rms = float(np.sqrt(np.mean(magnitude[selected] ** 2)))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.17, top=0.84)
    shade_terzband(ax, alpha=0.17)
    plot_fft_bins(ax, frequencies_hz, magnitude, selected=selected)
    draw_boundary(ax, F_LOW_HZ, r"$f_{\mathrm{low},b}$")
    draw_boundary(ax, F_HIGH_HZ, r"$f_{\mathrm{high},b}$")
    ax.hlines(
        band_rms,
        F_LOW_HZ,
        F_HIGH_HZ,
        color=COMPARE_ORANGE,
        lw=3.0,
        zorder=6,
        label="Terzband-RMS",
    )
    ax.text(
        F_HIGH_HZ + 8.0,
        band_rms,
        "Bandwert",
        color=COMPARE_ORANGE,
        fontsize=NOTE_SIZE,
        ha="left",
        va="center",
        zorder=12,
    )
    add_text_box(
        ax,
        r"$A_b=10\log_{10}\left("
        r"\dfrac{1}{N_b}\sum_{i\in\mathcal{I}_b}|p(f_i)|^2"
        r"\right)$"
        "\n"
        rf"$N_b={selected_indices.size}$",
    )
    setup_axis(ax, r"Terzbandwert: energetische Mittelung über die Indexmenge")
    save_figure(fig, "05_terzbandwert_energetische_mittelung.png")


def main() -> None:
    clear_output_dir()
    frequencies_hz = fft_frequencies()
    magnitude = example_pressure_magnitude(frequencies_hz)
    selected = selected_bin_mask(frequencies_hz)

    export_f_low_frame(frequencies_hz, magnitude)
    export_f_high_frame(frequencies_hz, magnitude)
    export_index_set_frame(frequencies_hz, magnitude, selected)
    export_multiple_values_frame(frequencies_hz, magnitude, selected)
    export_band_average_frame(frequencies_hz, magnitude, selected)

    selected_indices = np.flatnonzero(selected)
    print(f"PNG figures exported to: {OUTPUT_DIR}")
    print(
        "Terzband example: "
        f"fc={F_CENTER_HZ:.1f} Hz, "
        f"flow={F_LOW_HZ:.1f} Hz, "
        f"fhigh={F_HIGH_HZ:.1f} Hz, "
        f"indices={selected_indices[0]}..{selected_indices[-1]}, "
        f"Nb={selected_indices.size}"
    )


if __name__ == "__main__":
    main()
