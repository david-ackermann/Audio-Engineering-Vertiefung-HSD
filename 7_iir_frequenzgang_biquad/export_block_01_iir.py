from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "01_iir"
OUTPUT_DIR = BLOCK_DIR

DPI = 200
FIGSIZE = (10.5, 4.2)
TITLE_SIZE = 26
FRAME_TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18
STABILITY_YLIM = (-0.25, 3.05)
STABILITY_YTICKS = [0.0, 1.0, 2.0, 3.0]

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
OUTPUT_BLUE = "#2b7bbb"
REFERENCE_GREY = "0.72"
FEEDBACK_LIGHT_BLUE = "#9ecdf2"
FS_HZ = 48_000.0
LOG_MIN_HZ = 20.0
LOG_MAX_HZ = FS_HZ / 2.0

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class IirConfig:
    output_subdir: str
    title_name: str
    pole: float
    equation: str
    output_formula: str
    impulse_ylim: tuple[float, float]
    impulse_yticks: list[float]


@dataclass(frozen=True)
class StabilityConfig:
    output_subdir: str
    title_name: str
    p: float
    ylim: tuple[float, float]
    yticks: list[float]


STABILITY_CONFIGS = (
    StabilityConfig(
        output_subdir="01B_stabil_impulsantwort",
        title_name="Stable: |p|<1",
        p=0.7,
        ylim=STABILITY_YLIM,
        yticks=STABILITY_YTICKS,
    ),
    StabilityConfig(
        output_subdir="01C_grenzstabil_impulsantwort",
        title_name="Marginal case: |p|=1",
        p=1.0,
        ylim=STABILITY_YLIM,
        yticks=STABILITY_YTICKS,
    ),
    StabilityConfig(
        output_subdir="01D_instabil_impulsantwort",
        title_name="Unstable: |p|>1",
        p=1.15,
        ylim=STABILITY_YLIM,
        yticks=STABILITY_YTICKS,
    ),
)


FILTER_CONFIGS = (
    IirConfig(
        output_subdir="01E_iir_p_plus_05",
        title_name="p=+0.5",
        pole=0.5,
        equation=r"$y[n]=0.5\,x[n]+0.5\,y[n-1]$",
        output_formula=r"0.5x[{n}]+0.5y[{prev}]",
        impulse_ylim=(-0.5, 0.5),
        impulse_yticks=[-0.5, 0.0, 0.5],
    ),
    IirConfig(
        output_subdir="01F_iir_p_minus_05",
        title_name="p=-0.5",
        pole=-0.5,
        equation=r"$y[n]=1.5\,x[n]-0.5\,y[n-1]$",
        output_formula=r"1.5x[{n}]-0.5y[{prev}]",
        impulse_ylim=(-1.7, 1.7),
        impulse_yticks=[-1.5, 0.0, 1.5],
    ),
)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.rglob("*.png"):
        image_file.unlink()
    for directory in sorted((path for path in BLOCK_DIR.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
        try:
            directory.rmdir()
        except OSError:
            pass


def set_output_dir(path: Path) -> None:
    global OUTPUT_DIR
    OUTPUT_DIR = path
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_figure_fixed_canvas(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def input_gain(pole: float) -> float:
    return 1.0 - pole


def iir_filter(x: np.ndarray, pole: float) -> np.ndarray:
    b0 = input_gain(pole)
    y = np.zeros_like(x, dtype=float)
    for n in range(x.size):
        previous = y[n - 1] if n > 0 else 0.0
        y[n] = b0 * x[n] + pole * previous
    return y


def impulse_response(pole: float, num_samples: int = 8) -> np.ndarray:
    n = np.arange(num_samples)
    return input_gain(pole) * pole**n


def dense_transfer_response(pole: float, num_points: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    omega = np.linspace(0.0, np.pi, num_points)
    response = input_gain(pole) / (1.0 - pole * np.exp(-1j * omega))
    return omega, response


def log_frequency_transfer_response(pole: float, num_points: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(LOG_MAX_HZ), num_points)
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    response = input_gain(pole) / (1.0 - pole * np.exp(-1j * omega))
    return frequency_hz, response


def group_delay_samples(omega: np.ndarray, response: np.ndarray) -> np.ndarray:
    phase = np.unwrap(np.angle(response))
    return -np.gradient(phase, omega)


def stability_impulse_response(p: float, num_samples: int = 8) -> np.ndarray:
    n = np.arange(num_samples)
    return p**n


def dirac_signal(num_samples: int = 8) -> np.ndarray:
    x = np.zeros(num_samples)
    x[0] = 1.0
    return x


def stem_sequence(
    ax,
    n: np.ndarray,
    values: np.ndarray,
    *,
    color: str,
    alpha: float = 1.0,
    marker_size: float = 8.0,
    line_width: float = 2.8,
    line_style: str = "-",
) -> None:
    if n.size == 0:
        return
    markerline, stemlines, baseline = ax.stem(n, values)
    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor("white")
    markerline.set_markeredgewidth(0.9)
    markerline.set_markersize(marker_size)
    markerline.set_alpha(alpha)
    stemlines.set_color(color)
    stemlines.set_linewidth(line_width)
    stemlines.set_alpha(alpha)
    stemlines.set_linestyle(line_style)
    baseline.set_color(SIGNAL_BLACK)
    baseline.set_linewidth(1.4)


def plot_partial_stems(
    ax,
    indices: np.ndarray,
    values: np.ndarray,
    *,
    color: str,
    marker_size: float = 7.0,
    alpha: float = 1.0,
    line_width: float = 2.2,
    line_style: str = "-",
    zorder: int = 3,
) -> None:
    if indices.size == 0:
        return
    ax.vlines(indices, 0.0, values, color=color, lw=line_width, alpha=alpha, linestyles=line_style, zorder=zorder)
    ax.scatter(
        indices,
        values,
        s=marker_size**2,
        color=color,
        edgecolor="white",
        linewidth=0.9,
        zorder=zorder + 1,
        alpha=alpha,
    )


def style_time_axis(
    ax,
    title: str,
    *,
    n_max: int,
    ylabel: str,
    ylim: tuple[float, float] = (-1.2, 1.2),
    yticks: list[float] | None = None,
    title_size: int = TITLE_SIZE,
) -> None:
    if yticks is None:
        yticks = [-1.0, 0.0, 1.0]
    if title:
        ax.set_title(title, fontsize=title_size, pad=10)
    ax.set_xlim(-0.5, n_max + 0.5)
    ax.set_ylim(*ylim)
    ax.set_xticks(np.arange(0, n_max + 1, 1))
    ax.set_yticks(yticks)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def setup_sequence_axis(
    ax,
    *,
    title: str,
    ylabel: str,
    n_max: int,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    style_time_axis(
        ax,
        title,
        n_max=n_max,
        ylabel=ylabel,
        ylim=ylim,
        yticks=yticks,
        title_size=FRAME_TITLE_SIZE,
    )
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)


def add_output_subgrid(ax, config: IirConfig) -> None:
    if config.output_subdir != "01F_iir_p_minus_05":
        return
    ax.set_yticks([-2.0, -1.0, 1.0, 2.0], minor=True)
    ax.grid(which="minor", axis="y", alpha=0.16, linewidth=0.9)


def arrow(ax, xy_a: tuple[float, float], xy_b: tuple[float, float]) -> None:
    ax.add_patch(
        FancyArrowPatch(
            xy_a,
            xy_b,
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.8,
            color=SIGNAL_BLACK,
        )
    )


def block(ax, xy: tuple[float, float], text: str, *, width: float = 0.95, height: float = 0.58) -> None:
    rect = Rectangle(
        (xy[0] - width / 2, xy[1] - height / 2),
        width,
        height,
        facecolor="white",
        edgecolor=SIGNAL_BLACK,
        linewidth=1.7,
    )
    ax.add_patch(rect)
    ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=18)


def setup_stability_figure(config: StabilityConfig, *, title: str):
    values = stability_impulse_response(config.p)
    fig, ax_plot = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    style_time_axis(
        ax_plot,
        title,
        n_max=values.size - 1,
        ylabel=r"$h[n]$",
        ylim=config.ylim,
        yticks=config.yticks,
        title_size=FRAME_TITLE_SIZE,
    )
    ax_plot.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    return fig, ax_plot


def setup_dirac_figure(*, title: str):
    x = dirac_signal()
    fig, ax_plot = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    style_time_axis(
        ax_plot,
        title,
        n_max=x.size - 1,
        ylabel=r"$x[n]$",
        ylim=(-0.08, 1.10),
        yticks=[0.0, 0.5, 1.0],
        title_size=FRAME_TITLE_SIZE,
    )
    ax_plot.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    return fig, ax_plot


def plot_dirac_values(ax, x: np.ndarray, upto_index: int) -> None:
    n = np.arange(x.size)
    ax.vlines(n, 0.0, x, color=REFERENCE_GREY, lw=1.4, alpha=0.25, zorder=1)
    ax.scatter(n, x, s=36, color=REFERENCE_GREY, alpha=0.28, zorder=2)
    if upto_index >= 0:
        ax.axvline(upto_index, color="0.35", lw=1.6, ls="--", zorder=3)
        active = n <= upto_index
        plot_partial_stems(
            ax,
            n[active],
            x[active],
            color=SIGNAL_BLACK,
            marker_size=8.5,
            line_width=2.5,
            zorder=4,
        )
        plot_partial_stems(
            ax,
            np.array([upto_index]),
            np.array([x[upto_index]]),
            color=SIGNAL_BLACK,
            marker_size=11.0,
            line_width=3.1,
            zorder=5,
        )


def export_dirac_intro() -> None:
    x = dirac_signal()
    fig, ax_plot = setup_dirac_figure(title=r"Dirac impulse $x[n]=\delta[n]$")
    plot_dirac_values(ax_plot, x, -1)
    save_figure_fixed_canvas(fig, "01_dirac_start.png")


def export_dirac_step(step_index: int, figure_number: int) -> None:
    x = dirac_signal()
    fig, ax_plot = setup_dirac_figure(title=r"Dirac impulse $x[n]=\delta[n]$")
    plot_dirac_values(ax_plot, x, step_index)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_dirac_n_{step_index:02d}.png")


def export_dirac_final(figure_number: int) -> None:
    x = dirac_signal()
    fig, ax_plot = setup_dirac_figure(title=r"Dirac impulse $x[n]=\delta[n]$")
    plot_dirac_values(ax_plot, x, x.size - 1)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_dirac_ergebnis.png")


def export_dirac_series() -> None:
    set_output_dir(BLOCK_DIR / "01A_dirac_impuls")
    export_dirac_intro()
    for step_index in range(dirac_signal().size):
        export_dirac_step(step_index, step_index + 2)
    export_dirac_final(10)


def plot_stability_values(ax, values: np.ndarray, upto_index: int) -> None:
    n = np.arange(values.size)
    if upto_index >= 0:
        ax.axvline(upto_index, color="0.35", lw=1.6, ls="--", zorder=3)
        active = n <= upto_index
        plot_partial_stems(
            ax,
            n[active],
            values[active],
            color=SYSTEM_GREEN,
            marker_size=8.5,
            line_width=2.5,
            zorder=4,
        )
        plot_partial_stems(
            ax,
            np.array([upto_index]),
            np.array([values[upto_index]]),
            color=SYSTEM_GREEN,
            marker_size=11.0,
            line_width=3.1,
            zorder=5,
        )


def export_stability_intro(config: StabilityConfig) -> None:
    values = stability_impulse_response(config.p)
    fig, ax_plot = setup_stability_figure(config, title=config.title_name)
    plot_stability_values(ax_plot, values, -1)
    save_figure_fixed_canvas(fig, "01_stabilitaet_start.png")


def export_stability_step(config: StabilityConfig, step_index: int, figure_number: int) -> None:
    values = stability_impulse_response(config.p)
    fig, ax_plot = setup_stability_figure(config, title=config.title_name)
    plot_stability_values(ax_plot, values, step_index)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_stabilitaet_h_{step_index:02d}.png")


def export_stability_final(config: StabilityConfig, figure_number: int) -> None:
    values = stability_impulse_response(config.p)
    fig, ax_plot = setup_stability_figure(config, title=config.title_name)
    plot_stability_values(ax_plot, values, values.size - 1)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_stabilitaet_ergebnis.png")


def export_stability_envelope(config: StabilityConfig, figure_number: int) -> None:
    values = stability_impulse_response(config.p)
    n = np.arange(values.size)
    t = np.linspace(0.0, values.size - 1, 500)
    envelope = config.p**t

    fig, ax_plot = setup_stability_figure(config, title=rf"Envelope $p^n$, {config.title_name}")
    ax_plot.plot(t, envelope, color=SYSTEM_GREEN, lw=3.2, alpha=0.52, zorder=2)
    plot_partial_stems(
        ax_plot,
        n,
        values,
        color=SYSTEM_GREEN,
        marker_size=8.5,
        line_width=2.5,
        zorder=4,
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_stabilitaet_huellkurve_p_n.png")


def export_stability_series(config: StabilityConfig) -> None:
    set_output_dir(BLOCK_DIR / config.output_subdir)
    export_stability_intro(config)
    for step_index in range(stability_impulse_response(config.p).size):
        export_stability_step(config, step_index, step_index + 2)
    export_stability_final(config, 10)
    export_stability_envelope(config, 11)


def export_iir_structure(config: IirConfig) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title(f"First-order IIR, {config.title_name}", fontsize=TITLE_SIZE, pad=14)

    b0_label = f"{input_gain(config.pole):.1f}"
    pole_label = f"{config.pole:.1f}"

    ax.text(0.55, 3.0, r"$x[n]$", fontsize=23, va="center")
    arrow(ax, (1.05, 3.0), (1.85, 3.0))
    block(ax, (2.35, 3.0), rf"${b0_label}$")
    arrow(ax, (2.85, 3.0), (3.55, 3.0))
    ax.add_patch(Circle((4.0, 3.0), radius=0.34, facecolor="white", edgecolor=SIGNAL_BLACK, linewidth=1.8))
    ax.text(4.0, 3.0, r"$\Sigma$", ha="center", va="center", fontsize=23)
    arrow(ax, (4.35, 3.0), (8.2, 3.0))
    ax.text(8.35, 3.08, r"$y[n]$", fontsize=23, va="center")

    ax.plot([7.0, 7.0], [3.0, 1.55], color=SIGNAL_BLACK, lw=1.6)
    arrow(ax, (7.0, 1.55), (5.75, 1.55))
    block(ax, (5.0, 1.55), "delay")
    arrow(ax, (4.5, 1.55), (3.7, 1.55))
    block(ax, (3.2, 1.55), rf"${pole_label}$")
    arrow(ax, (3.2, 1.84), (3.85, 2.67))

    ax.text(5.0, 0.45, config.equation, ha="center", fontsize=25)
    save_figure_fixed_canvas(fig, "01_first_order_iir_structure.png")


def export_impulse_response(config: IirConfig) -> None:
    h = impulse_response(config.pole)
    n = np.arange(h.size)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN)
    style_time_axis(
        ax,
        "First-order IIR impulse response",
        n_max=n[-1],
        ylabel=r"$h[n]$",
        ylim=config.impulse_ylim,
        yticks=config.impulse_yticks,
    )
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    save_figure_fixed_canvas(fig, "02_first_order_iir_impulse_response.png")


def style_transfer_axis(
    ax,
    *,
    title: str,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(*ylim)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1"])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_log_frequency_axis(
    ax,
    *,
    title: str,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(LOG_MIN_HZ, LOG_MAX_HZ)
    ax.set_ylim(*ylim)
    ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 24000])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "24k"])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Frequency in Hz, $f_s=48\,\mathrm{kHz}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def export_transfer_magnitude(config: IirConfig) -> None:
    omega, response = dense_transfer_response(config.pole)
    magnitude = np.abs(response)
    if config.output_subdir == "01E_iir_p_plus_05":
        magnitude_ylim = (0.0, 1.08)
        magnitude_yticks = [0.0, 0.5, 1.0]
    else:
        magnitude_ylim = (-0.08, 3.15)
        magnitude_yticks = [0.0, 1.0, 2.0, 3.0]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, magnitude, color=SYSTEM_GREEN, lw=3.0)
    style_transfer_axis(
        ax,
        title="First-order IIR magnitude",
        ylabel="Magnitude",
        ylim=magnitude_ylim,
        yticks=magnitude_yticks,
    )
    save_figure_fixed_canvas(fig, "03_first_order_iir_magnitude_response.png")


def export_transfer_magnitude_db(config: IirConfig) -> None:
    omega, response = dense_transfer_response(config.pole)
    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(response), 1e-3))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, magnitude_db, color=SYSTEM_GREEN, lw=3.0)
    style_transfer_axis(
        ax,
        title="First-order IIR magnitude [dB]",
        ylabel="Magnitude [dB]",
        ylim=(-12.0, 12.0),
        yticks=[-12, -6, 0, 6, 12],
    )
    save_figure_fixed_canvas(fig, "04_first_order_iir_magnitude_response_db.png")


def export_transfer_magnitude_db_log_frequency(config: IirConfig) -> None:
    frequency_hz, response = log_frequency_transfer_response(config.pole)
    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(response), 1e-3))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz, magnitude_db, color=SYSTEM_GREEN, lw=3.0)
    style_log_frequency_axis(
        ax,
        title="First-order IIR magnitude [dB], log frequency",
        ylabel="Magnitude [dB]",
        ylim=(-12.0, 12.0),
        yticks=[-12, -6, 0, 6, 12],
    )
    save_figure_fixed_canvas(fig, "05_first_order_iir_magnitude_response_db_log_frequency.png")


def export_transfer_phase(config: IirConfig, filename: str = "05_first_order_iir_phase_response.png") -> None:
    omega, response = dense_transfer_response(config.pole)
    phase = np.unwrap(np.angle(response))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, phase, color=SYSTEM_GREEN, lw=3.0)
    style_transfer_axis(
        ax,
        title="First-order IIR phase",
        ylabel="Phase [rad]",
        ylim=(-np.pi / 2.0 - 0.15, np.pi / 2.0 + 0.15),
        yticks=[-np.pi / 2.0, -np.pi / 4.0, 0.0, np.pi / 4.0, np.pi / 2.0],
    )
    ax.set_yticklabels([r"$-\pi/2$", r"$-\pi/4$", "0", r"$\pi/4$", r"$\pi/2$"])
    save_figure_fixed_canvas(fig, filename)


def export_transfer_phase_log_frequency(config: IirConfig) -> None:
    frequency_hz, response = log_frequency_transfer_response(config.pole)
    phase = np.unwrap(np.angle(response))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz, phase, color=SYSTEM_GREEN, lw=3.0)
    style_log_frequency_axis(
        ax,
        title="First-order IIR phase, log frequency",
        ylabel="Phase [rad]",
        ylim=(-np.pi / 2.0 - 0.15, np.pi / 2.0 + 0.15),
        yticks=[-np.pi / 2.0, -np.pi / 4.0, 0.0, np.pi / 4.0, np.pi / 2.0],
    )
    ax.set_yticklabels([r"$-\pi/2$", r"$-\pi/4$", "0", r"$\pi/4$", r"$\pi/2$"])
    save_figure_fixed_canvas(fig, "07_first_order_iir_phase_response_log_frequency.png")


def export_transfer_group_delay(config: IirConfig) -> None:
    omega, response = dense_transfer_response(config.pole)
    delay = group_delay_samples(omega, response)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, delay, color=SYSTEM_GREEN, lw=3.0)
    style_transfer_axis(
        ax,
        title="First-order IIR group delay",
        ylabel="Group delay [samples]",
        ylim=(-0.5, 1.2),
        yticks=[-0.5, 0.0, 0.5, 1.0],
    )
    save_figure_fixed_canvas(fig, "08_first_order_iir_group_delay.png")


def export_transfer_group_delay_log_frequency(config: IirConfig) -> None:
    frequency_hz, response = log_frequency_transfer_response(config.pole)
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    delay = group_delay_samples(omega, response)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz, delay, color=SYSTEM_GREEN, lw=3.0)
    style_log_frequency_axis(
        ax,
        title="First-order IIR group delay, log frequency",
        ylabel="Group delay [samples]",
        ylim=(-0.5, 1.2),
        yticks=[-0.5, 0.0, 0.5, 1.0],
    )
    save_figure_fixed_canvas(fig, "09_first_order_iir_group_delay_log_frequency.png")


def input_sequences(num_samples: int = 8) -> dict[str, tuple[str, np.ndarray]]:
    n = np.arange(num_samples)
    return {
        "dc": ("DC input", np.ones(num_samples)),
        "nyquist": (r"Nyquist input, $\Omega/\pi=1$", (-1.0) ** n),
        "half_nyquist": (r"Half-Nyquist input, $\Omega/\pi=0.5$", np.cos(0.5 * np.pi * n)),
    }


def continuous_input(sequence_key: str, t: np.ndarray) -> np.ndarray | None:
    if sequence_key == "dc":
        return np.ones_like(t)
    if sequence_key == "nyquist":
        return np.cos(np.pi * t)
    if sequence_key == "half_nyquist":
        return np.cos(0.5 * np.pi * t)
    raise ValueError(f"Unknown sequence key: {sequence_key}")


def steady_state_output_curve(config: IirConfig, sequence_key: str, t: np.ndarray) -> np.ndarray:
    if sequence_key == "dc":
        return np.ones_like(t)

    if sequence_key == "nyquist":
        omega = np.pi
    elif sequence_key == "half_nyquist":
        omega = 0.5 * np.pi
    else:
        raise ValueError(f"Unknown sequence key: {sequence_key}")

    response = input_gain(config.pole) / (1.0 - config.pole * np.exp(-1j * omega))
    return np.abs(response) * np.cos(omega * t + np.angle(response))


def steady_state_title(sequence_key: str) -> str:
    return "Output with steady-state counterpart"


def output_axis_limits(y: np.ndarray) -> tuple[tuple[float, float], list[float]]:
    y_min = float(np.min(y))
    y_max = float(np.max(y))
    if y_max > 1.2 and y_min >= 0.0:
        top = np.ceil(y_max)
        return (-0.35, top + 0.45), [0.0, top / 2.0, top]
    if y_min < -1.2 or y_max > 1.2:
        lower = np.floor(y_min)
        upper = np.ceil(y_max)
        return (lower - 0.4, upper + 0.4), [lower, 0.0, upper]
    return (-1.2, 1.2), [-1.0, 0.0, 1.0]


def export_full_input(
    *,
    sequence_key: str,
    sequence_title: str,
    x: np.ndarray,
    figure_number: int,
) -> None:
    n_all = np.arange(x.size)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    t_dense = np.linspace(0.0, x.size - 1, 600)
    continuous = continuous_input(sequence_key, t_dense)
    if continuous is not None:
        ax.plot(t_dense, continuous, color=REFERENCE_GREY, lw=2.6, zorder=1)
    plot_partial_stems(ax, n_all, x, color=SIGNAL_BLACK, marker_size=7.5, line_width=2.4)
    setup_sequence_axis(
        ax,
        title=f"{sequence_title}: full input signal",
        ylabel=r"$x[n]$",
        n_max=x.size - 1,
        ylim=(-1.2, 1.2),
        yticks=[-1.0, 0.0, 1.0],
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_input_full.png")


def export_input_sample_frame(
    *,
    sequence_key: str,
    sequence_title: str,
    x: np.ndarray,
    frame_index: int,
    figure_number: int,
) -> None:
    n_all = np.arange(x.size)
    previous_index = frame_index - 1

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    t_dense = np.linspace(0.0, x.size - 1, 600)
    continuous = continuous_input(sequence_key, t_dense)
    if continuous is not None:
        ax.plot(t_dense, continuous, color=REFERENCE_GREY, lw=2.2, zorder=1)
    plot_partial_stems(
        ax,
        n_all,
        x,
        color=SIGNAL_BLACK,
        marker_size=5.8,
        alpha=0.35,
        line_width=1.25,
    )
    if previous_index >= 0:
        plot_partial_stems(
            ax,
            np.array([previous_index]),
            np.array([x[previous_index]]),
            color=SIGNAL_BLACK,
            marker_size=7.8,
            alpha=0.78,
            line_width=2.1,
            line_style="--",
        )
    plot_partial_stems(
        ax,
        np.array([frame_index]),
        np.array([x[frame_index]]),
        color=SIGNAL_BLACK,
        marker_size=10.0,
        line_width=2.8,
    )
    ax.axvline(frame_index, color="0.35", lw=1.6, ls="--")
    setup_sequence_axis(
        ax,
        title=f"{sequence_title}: input sample n={frame_index}",
        ylabel=r"$x[n]$",
        n_max=x.size - 1,
        ylim=(-1.2, 1.2),
        yticks=[-1.0, 0.0, 1.0],
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_input_sample_{frame_index:02d}.png")


def export_empty_output(
    *,
    config: IirConfig,
    sequence_key: str,
    y: np.ndarray,
    ylim: tuple[float, float],
    yticks: list[float],
    figure_number: int,
) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    setup_sequence_axis(
        ax,
        title="",
        ylabel=r"$y[n]$",
        n_max=y.size - 1,
        ylim=ylim,
        yticks=yticks,
    )
    add_output_subgrid(ax, config)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_output_empty.png")


def recursion_terms(
    *,
    x: np.ndarray,
    y: np.ndarray,
    pole: float,
    frame_index: int,
) -> tuple[float, float]:
    input_term = input_gain(pole) * x[frame_index]
    previous_output = y[frame_index - 1] if frame_index > 0 else 0.0
    feedback_term = pole * previous_output
    return input_term, feedback_term


def plot_current_recursion_terms(
    ax,
    *,
    x: np.ndarray,
    y: np.ndarray,
    pole: float,
    frame_index: int,
    alpha: float = 0.68,
    marker_size: float = 5.3,
    line_width: float = 1.65,
) -> None:
    input_term, feedback_term = recursion_terms(
        x=x,
        y=y,
        pole=pole,
        frame_index=frame_index,
    )
    plot_partial_stems(
        ax,
        np.array([frame_index - 0.13, frame_index + 0.13]),
        np.array([input_term, feedback_term]),
        color=FEEDBACK_LIGHT_BLUE,
        marker_size=marker_size,
        alpha=alpha,
        line_width=line_width,
        zorder=2,
    )


def plot_recursion_term_history(
    ax,
    *,
    x: np.ndarray,
    y: np.ndarray,
    pole: float,
    upto_index: int,
) -> None:
    for frame_index in range(upto_index + 1):
        plot_current_recursion_terms(
            ax,
            x=x,
            y=y,
            pole=pole,
            frame_index=frame_index,
            alpha=0.42,
            marker_size=4.0,
            line_width=1.15,
        )


def export_output_sample_frame(
    *,
    config: IirConfig,
    sequence_key: str,
    x: np.ndarray,
    y: np.ndarray,
    frame_index: int,
    ylim: tuple[float, float],
    yticks: list[float],
    figure_number: int,
) -> None:
    n_all = np.arange(y.size)
    computed = n_all <= frame_index
    previous_index = frame_index - 1
    current_output = y[frame_index]
    formula = config.output_formula.format(n=frame_index, prev=previous_index)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    plot_current_recursion_terms(ax, x=x, y=y, pole=config.pole, frame_index=frame_index)
    plot_partial_stems(
        ax,
        n_all[computed],
        y[computed],
        color=OUTPUT_BLUE,
        marker_size=7.0,
        line_width=2.3,
        zorder=4,
    )
    plot_partial_stems(
        ax,
        np.array([frame_index]),
        np.array([current_output]),
        color=OUTPUT_BLUE,
        marker_size=10.0,
        line_width=3.0,
        zorder=5,
    )
    ax.axvline(frame_index, color="0.35", lw=1.6, ls="--")
    setup_sequence_axis(
        ax,
        title=rf"$y[{frame_index}]={formula}={current_output:+.2f}$",
        ylabel=r"$y[n]$",
        n_max=y.size - 1,
        ylim=ylim,
        yticks=yticks,
    )
    add_output_subgrid(ax, config)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_output_sample_{frame_index:02d}.png")


def export_output_final(
    *,
    config: IirConfig,
    sequence_key: str,
    y: np.ndarray,
    x: np.ndarray,
    ylim: tuple[float, float],
    yticks: list[float],
    figure_number: int,
) -> None:
    n_all = np.arange(y.size)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    settled_start = 4.0
    t_transient = np.linspace(0.0, min(settled_start, y.size - 1), 320)
    t_steady = np.linspace(settled_start, y.size - 1, 360)
    ax.plot(
        t_transient,
        steady_state_output_curve(config, sequence_key, t_transient),
        color=REFERENCE_GREY,
        lw=2.6,
        ls="--",
        zorder=1,
    )
    ax.plot(t_steady, steady_state_output_curve(config, sequence_key, t_steady), color=REFERENCE_GREY, lw=2.6, zorder=1)
    plot_recursion_term_history(ax, x=x, y=y, pole=config.pole, upto_index=y.size - 1)
    plot_partial_stems(
        ax,
        n_all,
        y,
        color=OUTPUT_BLUE,
        marker_size=7.5,
        line_width=2.4,
        zorder=4,
    )
    setup_sequence_axis(
        ax,
        title=steady_state_title(sequence_key),
        ylabel=r"$y[n]$",
        n_max=y.size - 1,
        ylim=ylim,
        yticks=yticks,
    )
    add_output_subgrid(ax, config)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_output_final.png")


def export_sequence_frames(config: IirConfig, start_figure_number: int = 6) -> None:
    figure_number = start_figure_number
    sequences = input_sequences()
    outputs = {
        sequence_key: iir_filter(x, config.pole)
        for sequence_key, (_, x) in sequences.items()
    }
    output_ylim, output_yticks = output_axis_limits(np.concatenate(tuple(outputs.values())))

    for sequence_key, (sequence_title, x) in sequences.items():
        y = outputs[sequence_key]
        export_full_input(
            sequence_key=sequence_key,
            sequence_title=sequence_title,
            x=x,
            figure_number=figure_number,
        )
        figure_number += 1
        export_empty_output(
            config=config,
            sequence_key=sequence_key,
            y=y,
            ylim=output_ylim,
            yticks=output_yticks,
            figure_number=figure_number,
        )
        figure_number += 1
        for frame_index in range(x.size):
            export_input_sample_frame(
                sequence_key=sequence_key,
                sequence_title=sequence_title,
                x=x,
                frame_index=frame_index,
                figure_number=figure_number,
            )
            figure_number += 1
            export_output_sample_frame(
                config=config,
                sequence_key=sequence_key,
                x=x,
                y=y,
                frame_index=frame_index,
                ylim=output_ylim,
                yticks=output_yticks,
                figure_number=figure_number,
            )
            figure_number += 1
        export_output_final(
            config=config,
            sequence_key=sequence_key,
            y=y,
            x=x,
            ylim=output_ylim,
            yticks=output_yticks,
            figure_number=figure_number,
        )
        figure_number += 1


def export_filter(config: IirConfig) -> None:
    set_output_dir(BLOCK_DIR / config.output_subdir)
    export_iir_structure(config)
    export_impulse_response(config)
    export_transfer_magnitude(config)
    export_transfer_magnitude_db(config)
    if config.output_subdir in {"01E_iir_p_plus_05", "01F_iir_p_minus_05"}:
        export_transfer_magnitude_db_log_frequency(config)
        export_transfer_phase(config, "06_first_order_iir_phase_response.png")
        export_transfer_phase_log_frequency(config)
        export_transfer_group_delay(config)
        export_transfer_group_delay_log_frequency(config)
        export_sequence_frames(config, start_figure_number=10)
    else:
        export_transfer_phase(config)
        export_sequence_frames(config)


def main() -> None:
    clear_output_dir()
    export_dirac_series()
    for config in STABILITY_CONFIGS:
        export_stability_series(config)
    for config in FILTER_CONFIGS:
        export_filter(config)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
