from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "03_aliasing"
    / "03C_frequenzraster_und_aufloesung"
)

DPI = 200
SINGLE_FIGSIZE = (12.0, 4.4)
COMPARE_FIGSIZE = (12.0, 7.2)
TITLE_SIZE = 22
LABEL_SIZE = 18
TICK_SIZE = 17
LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86

SIGNAL_BLACK = "0.10"
SIGNAL_BLUE = "#2b7bbb"
SIGNAL_LIGHT_BLUE = "#bddcf3"
WINDOW_GREEN = "#66b77a"
WINDOW_LIGHT_GREEN = "#d7efde"
ACTIVE_RED = "crimson"
GRID_GREY = "0.75"
BOUNDARY_GREY = "0.72"
BIN_GREY = "0.55"
CURVE_GREY = "0.55"
INACTIVE_GREY = "0.65"

TIME_START = 0.0
REFERENCE_TIME_END = 1.5
SIGNAL_AMPLITUDE = 0.88
SIGNAL_FREQ_HZ = 2.0
SIGNAL_PHASE_RAD = 0.18 * np.pi
FREQ_DISPLAY_MAX_HZ = 16.0
AMPLITUDE_LIMIT = 1.15


def clear_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def make_config(fs_hz, n_samples):
    sample_indices = np.arange(n_samples)
    sample_period = 1.0 / fs_hz
    observation_time = n_samples / fs_hz
    sample_times = sample_indices * sample_period
    signal_samples = SIGNAL_AMPLITUDE * np.cos(2.0 * np.pi * SIGNAL_FREQ_HZ * sample_times + SIGNAL_PHASE_RAD)

    delta_f_hz = fs_hz / n_samples
    max_frequency = min(FREQ_DISPLAY_MAX_HZ, fs_hz)
    bin_frequencies = np.arange(0.0, max_frequency + 0.5 * delta_f_hz, delta_f_hz)

    return {
        "fs_hz": float(fs_hz),
        "n_samples": int(n_samples),
        "sample_period": sample_period,
        "observation_time": observation_time,
        "delta_f_hz": delta_f_hz,
        "sample_times": sample_times,
        "signal_samples": signal_samples,
        "bin_frequencies": bin_frequencies,
    }


def format_value(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def create_single_figure():
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=BOTTOM_MARGIN,
        top=TOP_MARGIN,
    )
    return fig, ax


def create_compare_figure(suptitle):
    fig, axes = plt.subplots(2, 2, figsize=COMPARE_FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.09, top=0.88, wspace=0.20, hspace=0.48)
    fig.suptitle(suptitle, fontsize=TITLE_SIZE, y=0.965)
    return fig, axes


def choose_time_ticks(xmax):
    if xmax <= 1.15:
        return np.arange(0.0, xmax + 1e-9, 0.2)
    if xmax <= 2.25:
        return np.arange(0.0, xmax + 1e-9, 0.5)
    return np.arange(0.0, xmax + 1e-9, 1.0)


def add_parameter_box(ax, cfg):
    ax.text(
        0.97,
        0.93,
        "\n".join(
            [
                rf"$f_s = {format_value(cfg['fs_hz'])}\,\mathrm{{Hz}}$",
                rf"$N = {cfg['n_samples']}$",
                rf"$T_{{obs}} = {format_value(cfg['observation_time'])}\,\mathrm{{s}}$",
                rf"$\Delta f = {format_value(cfg['delta_f_hz'])}\,\mathrm{{Hz}}$",
            ]
        ),
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=15,
        color=SIGNAL_BLACK,
        zorder=10,
        bbox=dict(boxstyle="round,pad=0.30", facecolor="white", edgecolor="0.78", alpha=1.0),
    )


def draw_time_window_annotation(ax, cfg):
    y_level = -0.96 * AMPLITUDE_LIMIT
    ax.annotate(
        "",
        xy=(0.0, y_level),
        xytext=(cfg["observation_time"], y_level),
        arrowprops=dict(arrowstyle="<->", lw=1.3, color=ACTIVE_RED),
    )
    ax.text(
        0.5 * cfg["observation_time"],
        y_level + 0.08,
        r"$T_{obs}$",
        color=ACTIVE_RED,
        fontsize=15,
        ha="center",
        va="bottom",
    )


def continuous_signal(time_values):
    return SIGNAL_AMPLITUDE * np.cos(2.0 * np.pi * SIGNAL_FREQ_HZ * time_values + SIGNAL_PHASE_RAD)


def display_sample_times(cfg, xmax):
    n_display = int(np.floor(xmax * cfg["fs_hz"] + 1e-9)) + 1
    display_indices = np.arange(n_display)
    display_times = display_indices * cfg["sample_period"]
    return display_indices, display_times


def draw_delta_f_annotation(ax, cfg):
    bins = cfg["bin_frequencies"]
    if bins.size < 3:
        return

    left = 2.0 * cfg["delta_f_hz"]
    right = 3.0 * cfg["delta_f_hz"]
    if right > FREQ_DISPLAY_MAX_HZ + 1e-9:
        left = bins[1]
        right = bins[2]
    y_level = 0.88
    ax.annotate(
        "",
        xy=(left, y_level),
        xytext=(right, y_level),
        arrowprops=dict(arrowstyle="<->", lw=1.3, color=ACTIVE_RED),
    )
    ax.text(
        0.5 * (left + right),
        y_level + 0.07,
        rf"$\Delta f = {format_value(cfg['delta_f_hz'])}\,\mathrm{{Hz}}$",
        color=ACTIVE_RED,
        fontsize=15,
        ha="center",
        va="bottom",
    )


def highlighted_bin_frequency(cfg):
    bin_index = int(round(SIGNAL_FREQ_HZ / cfg["delta_f_hz"]))
    return bin_index * cfg["delta_f_hz"]


def mirrored_bin_frequency(cfg):
    primary_frequency = highlighted_bin_frequency(cfg)
    return cfg["fs_hz"] - primary_frequency


def style_time_axis(ax, panel_title, xmax, show_ylabel):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(TIME_START, xmax)
    ax.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
    ax.set_xticks(choose_time_ticks(xmax))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    if panel_title:
        ax.set_title(panel_title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude" if show_ylabel else "", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_frequency_axis(ax, panel_title, show_ylabel):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(0.0, FREQ_DISPLAY_MAX_HZ)
    ax.set_ylim(0.0, 1.08)
    ax.set_xticks(np.arange(0.0, FREQ_DISPLAY_MAX_HZ + 1e-9, 2.0))
    ax.set_yticks([])
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    if panel_title:
        ax.set_title(panel_title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlabel("Frequency [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("DFT bins" if show_ylabel else "", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def draw_time_panel(
    ax,
    cfg,
    xmax,
    panel_title,
    show_ylabel,
    *,
    show_signal=True,
    show_samples=True,
    show_observation_window=True,
    show_tobs_annotation=True,
    show_parameter_box=False,
    signal_color=SIGNAL_BLACK,
    sample_mode="block_only",
):
    if show_observation_window:
        ax.axvspan(0.0, cfg["observation_time"], color=WINDOW_LIGHT_GREEN, alpha=0.55, zorder=0)
        ax.axvline(cfg["observation_time"], color=WINDOW_GREEN, lw=1.4, ls="--", zorder=1)
    if show_signal:
        dense_times = np.linspace(TIME_START, xmax, 3200)
        ax.plot(dense_times, continuous_signal(dense_times), color=signal_color, lw=2.1, zorder=2)
    if show_samples:
        display_indices, display_times = display_sample_times(cfg, xmax)
        display_values = continuous_signal(display_times)
        active_mask = display_indices < cfg["n_samples"]
        inactive_times = display_times[~active_mask]
        active_times = display_times[active_mask]
        active_values = display_values[active_mask]

        if sample_mode == "full_sequence":
            ax.vlines(
                display_times,
                ymin=0.0,
                ymax=display_values,
                color=SIGNAL_BLUE,
                lw=2.2,
                zorder=3,
            )
            ax.scatter(
                display_times,
                display_values,
                s=70,
                color=SIGNAL_BLUE,
                edgecolor="white",
                linewidth=0.9,
                zorder=4,
            )
        elif sample_mode == "windowed_sequence":
            ax.vlines(
                active_times,
                ymin=0.0,
                ymax=active_values,
                color=SIGNAL_BLUE,
                lw=2.2,
                zorder=3,
            )
            ax.scatter(
                active_times,
                active_values,
                s=70,
                color=SIGNAL_BLUE,
                edgecolor="white",
                linewidth=0.9,
                zorder=4,
            )
            if inactive_times.size:
                ax.scatter(
                    inactive_times,
                    np.zeros_like(inactive_times),
                    s=44,
                    color=INACTIVE_GREY,
                    edgecolor="white",
                    linewidth=0.8,
                    zorder=4,
                )
        else:
            ax.vlines(
                cfg["sample_times"],
                ymin=0.0,
                ymax=cfg["signal_samples"],
                color=SIGNAL_BLUE,
                lw=2.2,
                zorder=3,
            )
            ax.scatter(
                cfg["sample_times"],
                cfg["signal_samples"],
                s=70,
                color=SIGNAL_BLUE,
                edgecolor="white",
                linewidth=0.9,
                zorder=4,
            )
    if show_tobs_annotation:
        draw_time_window_annotation(ax, cfg)
    style_time_axis(ax, panel_title, xmax=xmax, show_ylabel=show_ylabel)
    if show_parameter_box:
        add_parameter_box(ax, cfg)


def draw_frequency_panel(
    ax,
    cfg,
    show_ylabel,
    *,
    panel_title="",
    show_bins=True,
    show_highlighted_bin=True,
    show_mirrored_bin=True,
    show_delta_f_annotation=True,
    show_parameter_box=False,
):
    highlighted_frequency = highlighted_bin_frequency(cfg)
    mirrored_frequency = mirrored_bin_frequency(cfg)
    if show_bins:
        ax.vlines(
            cfg["bin_frequencies"],
            ymin=0.0,
            ymax=0.72,
            color=BIN_GREY,
            lw=2.8,
            zorder=2,
        )
        ax.scatter(
            cfg["bin_frequencies"],
            np.full_like(cfg["bin_frequencies"], 0.72),
            s=72,
            color=BIN_GREY,
            edgecolor="white",
            linewidth=0.9,
            zorder=3,
        )
    if show_highlighted_bin and highlighted_frequency <= FREQ_DISPLAY_MAX_HZ + 1e-9:
        ax.vlines(
            [highlighted_frequency],
            ymin=0.0,
            ymax=0.72,
            color=SIGNAL_BLUE,
            lw=3.2,
            zorder=4,
        )
        ax.scatter(
            [highlighted_frequency],
            [0.72],
            s=82,
            color=SIGNAL_BLUE,
            edgecolor="white",
            linewidth=1.0,
            zorder=5,
        )
    if (
        show_mirrored_bin
        and mirrored_frequency <= FREQ_DISPLAY_MAX_HZ + 1e-9
        and abs(mirrored_frequency - highlighted_frequency) > 1e-9
    ):
        ax.vlines(
            [mirrored_frequency],
            ymin=0.0,
            ymax=0.72,
            color=SIGNAL_LIGHT_BLUE,
            lw=3.2,
            zorder=4,
        )
        ax.scatter(
            [mirrored_frequency],
            [0.72],
            s=82,
            color=SIGNAL_LIGHT_BLUE,
            edgecolor="white",
            linewidth=1.0,
            zorder=5,
        )
    if show_bins and show_delta_f_annotation:
        draw_delta_f_annotation(ax, cfg)
    style_frequency_axis(ax, panel_title=panel_title, show_ylabel=show_ylabel)
    if show_parameter_box:
        add_parameter_box(ax, cfg)


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def export_reference_series():
    cfg = make_config(fs_hz=16.0, n_samples=16)
    xmax = REFERENCE_TIME_END

    fig, ax = create_single_figure()
    draw_time_panel(
        ax,
        cfg,
        xmax=xmax,
        panel_title=r"Sampled signal sequence $x[n]$",
        show_ylabel=True,
        show_signal=True,
        show_samples=True,
        show_observation_window=False,
        show_tobs_annotation=False,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="full_sequence",
    )
    save_figure(fig, "01_endlicher_beobachtungsblock_mit_samples.png")

    fig, ax = create_single_figure()
    draw_time_panel(
        ax,
        cfg,
        xmax=xmax,
        panel_title=r"Observation duration $T_{obs}$",
        show_ylabel=True,
        show_signal=True,
        show_samples=True,
        show_observation_window=True,
        show_tobs_annotation=True,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    save_figure(fig, "02_beobachtungsdauer_t_obs.png")

    fig, ax = create_single_figure()
    draw_frequency_panel(
        ax,
        cfg,
        show_ylabel=True,
        panel_title=r"DFT bin grid from $T_{obs}$",
        show_bins=True,
        show_highlighted_bin=True,
        show_delta_f_annotation=True,
        show_parameter_box=False,
    )
    save_figure(fig, "03_dft_binraster_aus_t_obs.png")


def export_same_n_higher_sample_rate():
    reference_cfg = make_config(fs_hz=16.0, n_samples=16)
    higher_fs_cfg = make_config(fs_hz=32.0, n_samples=16)
    xmax = 1.5

    fig, axes = create_compare_figure("Same N, higher sample rate")
    draw_time_panel(
        axes[0, 0],
        reference_cfg,
        xmax=xmax,
        panel_title="Reference block",
        show_ylabel=True,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_time_panel(
        axes[0, 1],
        higher_fs_cfg,
        xmax=xmax,
        panel_title="Higher $f_s$",
        show_ylabel=False,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_frequency_panel(
        axes[1, 0],
        reference_cfg,
        show_ylabel=True,
        show_bins=False,
        show_highlighted_bin=False,
        show_mirrored_bin=False,
        show_delta_f_annotation=False,
    )
    draw_frequency_panel(
        axes[1, 1],
        higher_fs_cfg,
        show_ylabel=False,
        show_bins=False,
        show_highlighted_bin=False,
        show_mirrored_bin=False,
        show_delta_f_annotation=False,
    )
    save_figure(fig, "04_gleiches_n_hoehere_samplerate_frage.png")

    fig, axes = create_compare_figure("Same N, higher sample rate")
    draw_time_panel(
        axes[0, 0],
        reference_cfg,
        xmax=xmax,
        panel_title="Reference block",
        show_ylabel=True,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_time_panel(
        axes[0, 1],
        higher_fs_cfg,
        xmax=xmax,
        panel_title="Higher $f_s$",
        show_ylabel=False,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_frequency_panel(axes[1, 0], reference_cfg, show_ylabel=True, show_highlighted_bin=True)
    draw_frequency_panel(axes[1, 1], higher_fs_cfg, show_ylabel=False, show_highlighted_bin=True)
    save_figure(fig, "05_gleiches_n_hoehere_samplerate.png")


def export_same_sample_rate_longer_window():
    reference_cfg = make_config(fs_hz=16.0, n_samples=16)
    longer_window_cfg = make_config(fs_hz=16.0, n_samples=32)
    xmax = 2.5

    fig, axes = create_compare_figure("Same sample rate, longer observation")
    draw_time_panel(
        axes[0, 0],
        reference_cfg,
        xmax=xmax,
        panel_title="Reference block",
        show_ylabel=True,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_time_panel(
        axes[0, 1],
        longer_window_cfg,
        xmax=xmax,
        panel_title=r"Longer $T_{obs}$",
        show_ylabel=False,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_frequency_panel(
        axes[1, 0],
        reference_cfg,
        show_ylabel=True,
        show_bins=False,
        show_highlighted_bin=False,
        show_mirrored_bin=False,
        show_delta_f_annotation=False,
    )
    draw_frequency_panel(
        axes[1, 1],
        longer_window_cfg,
        show_ylabel=False,
        show_bins=False,
        show_highlighted_bin=False,
        show_mirrored_bin=False,
        show_delta_f_annotation=False,
    )
    save_figure(fig, "06_gleiche_samplerate_laengeres_fenster_frage.png")

    fig, axes = create_compare_figure("Same sample rate, longer observation")
    draw_time_panel(
        axes[0, 0],
        reference_cfg,
        xmax=xmax,
        panel_title="Reference block",
        show_ylabel=True,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_time_panel(
        axes[0, 1],
        longer_window_cfg,
        xmax=xmax,
        panel_title=r"Longer $T_{obs}$",
        show_ylabel=False,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_frequency_panel(axes[1, 0], reference_cfg, show_ylabel=True, show_highlighted_bin=True)
    draw_frequency_panel(axes[1, 1], longer_window_cfg, show_ylabel=False, show_highlighted_bin=True)
    save_figure(fig, "07_gleiche_samplerate_laengeres_fenster.png")


def export_same_observation_time():
    reference_cfg = make_config(fs_hz=16.0, n_samples=16)
    same_tobs_cfg = make_config(fs_hz=32.0, n_samples=32)
    xmax = 1.5

    fig, axes = create_compare_figure("Same observation time")
    draw_time_panel(
        axes[0, 0],
        reference_cfg,
        xmax=xmax,
        panel_title="16 Hz / 16 samples",
        show_ylabel=True,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_time_panel(
        axes[0, 1],
        same_tobs_cfg,
        xmax=xmax,
        panel_title="32 Hz / 32 samples",
        show_ylabel=False,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_frequency_panel(
        axes[1, 0],
        reference_cfg,
        show_ylabel=True,
        show_bins=False,
        show_highlighted_bin=False,
        show_mirrored_bin=False,
        show_delta_f_annotation=False,
    )
    draw_frequency_panel(
        axes[1, 1],
        same_tobs_cfg,
        show_ylabel=False,
        show_bins=False,
        show_highlighted_bin=False,
        show_mirrored_bin=False,
        show_delta_f_annotation=False,
    )
    save_figure(fig, "08_gleiche_beobachtungsdauer_gleiches_delta_f_frage.png")

    fig, axes = create_compare_figure("Same observation time")
    draw_time_panel(
        axes[0, 0],
        reference_cfg,
        xmax=xmax,
        panel_title="16 Hz / 16 samples",
        show_ylabel=True,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_time_panel(
        axes[0, 1],
        same_tobs_cfg,
        xmax=xmax,
        panel_title="32 Hz / 32 samples",
        show_ylabel=False,
        show_parameter_box=False,
        signal_color=CURVE_GREY,
        sample_mode="windowed_sequence",
    )
    draw_frequency_panel(axes[1, 0], reference_cfg, show_ylabel=True, show_highlighted_bin=True)
    draw_frequency_panel(axes[1, 1], same_tobs_cfg, show_ylabel=False, show_highlighted_bin=True)
    save_figure(fig, "09_gleiche_beobachtungsdauer_gleiches_delta_f.png")


def main():
    clear_output_dir()
    export_reference_series()
    export_same_n_higher_sample_rate()
    export_same_sample_rate_longer_window()
    export_same_observation_time()


if __name__ == "__main__":
    main()
