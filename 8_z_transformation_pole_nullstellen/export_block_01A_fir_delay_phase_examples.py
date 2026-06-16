from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "01_delay_phase_zeitbereich" / "01A_sinus_durch_delay"

DPI = 200
FIGSIZE = (10.5, 4.2)
TITLE_SIZE = 26
FRAME_TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
OUTPUT_BLUE = "#2b7bbb"
SINE_GREY = "0.58"
REFERENCE_GREY = "0.76"
MARKER_ORANGE = "#d98c2f"

NUM_SAMPLES = 8
DELAY_VALUES = (1, 2)
PHASE_SAMPLE_POINTS = (0.0, 0.5, 1.0)

SIGNALS = (
    ("dc", "DC", 0.0, r"$\Omega=0$"),
    ("half_nyquist", "Half Nyquist", 0.5 * np.pi, r"$\Omega=\pi/2$"),
    ("nyquist", "Nyquist", np.pi, r"$\Omega=\pi$"),
)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.rglob("*.png"):
        image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def input_signal(omega: float) -> np.ndarray:
    n = np.arange(NUM_SAMPLES)
    return np.cos(omega * n)


def delayed_signal(omega: float, delay: int) -> np.ndarray:
    n = np.arange(NUM_SAMPLES)
    y = np.zeros(NUM_SAMPLES)
    valid = n >= delay
    y[valid] = np.cos(omega * (n[valid] - delay))
    return y


def continuous_signal(omega: float, *, delay: int = 0) -> tuple[np.ndarray, np.ndarray]:
    t = np.linspace(0.0, NUM_SAMPLES - 1, 1400)
    return t, np.cos(omega * (t - delay))


def phase_at(omega: float, delay: int) -> float:
    return -delay * omega


def phase_label(phase: float) -> str:
    if np.isclose(phase, 0.0):
        return r"$0$"
    ratio = phase / np.pi
    if np.isclose(ratio, -0.5):
        return r"$-\pi/2$"
    if np.isclose(ratio, -1.0):
        return r"$-\pi$"
    if np.isclose(ratio, -2.0):
        return r"$-2\pi$"
    return rf"${ratio:.1f}\pi$"


def style_signal_axis(ax, *, title: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=FRAME_TITLE_SIZE, pad=10)
    ax.set_xlim(-0.5, NUM_SAMPLES - 0.5)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks(np.arange(0, NUM_SAMPLES, 1))
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2, zorder=1)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def plot_stem(ax, values: np.ndarray, *, color: str, alpha: float, zorder: int, linestyle: str = "-") -> None:
    samples = np.arange(values.size)
    markerline, stemlines, baseline = ax.stem(samples, values)
    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor("white")
    markerline.set_markeredgewidth(0.8)
    markerline.set_markersize(7.5)
    markerline.set_alpha(alpha)
    markerline.set_zorder(zorder + 1)
    stemlines.set_color(color)
    stemlines.set_linewidth(2.4)
    stemlines.set_alpha(alpha)
    stemlines.set_linestyle(linestyle)
    stemlines.set_zorder(zorder)
    baseline.set_visible(False)


def add_legend_last(ax, *, location: str = "lower right") -> None:
    legend = ax.legend(loc=location, fontsize=15, frameon=True, framealpha=0.92)
    legend.set_zorder(100)


def export_input_frame(figure_number: int, delay: int, key: str, title: str, omega: float, omega_label: str) -> None:
    x = input_signal(omega)
    t, sine = continuous_signal(omega)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    ax.plot(t, sine, color=SINE_GREY, lw=2.4, alpha=0.88, label="input sinus")
    plot_stem(ax, x, color=SIGNAL_BLACK, alpha=1.0, zorder=4)
    style_signal_axis(
        ax,
        title=rf"{title}: input signal",
        ylabel=r"$x[n]$",
    )
    legend_location = "lower right" if key == "dc" else "upper right"
    add_legend_last(ax, location=legend_location)
    save_figure(fig, f"{figure_number:02d}_delay_d{delay}_{key}_input.png")


def export_output_frame(figure_number: int, delay: int, key: str, title: str, omega: float, omega_label: str) -> None:
    y = delayed_signal(omega, delay)
    phase = phase_at(omega, delay)
    t, input_sine = continuous_signal(omega)
    _, output_sine = continuous_signal(omega, delay=delay)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    ax.plot(t, input_sine, color=REFERENCE_GREY, lw=2.3, ls="--", alpha=0.88, label="input reference")
    valid_output = t >= delay
    ax.plot(t[valid_output], output_sine[valid_output], color=SINE_GREY, lw=2.4, alpha=0.92, label="output sinus")
    plot_stem(ax, y, color=OUTPUT_BLUE, alpha=1.0, zorder=5)
    style_signal_axis(
        ax,
        title=rf"{title}: output $y[n]=x[n-{delay}]$",
        ylabel=r"$y[n]$",
    )
    legend_location = "lower right" if key == "dc" else "upper right"
    add_legend_last(ax, location=legend_location)
    save_figure(fig, f"{figure_number:02d}_delay_d{delay}_{key}_output.png")


def style_phase_axis(ax) -> None:
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-2.15 * np.pi, 0.25 * np.pi)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1"])
    ax.set_yticks([-2.0 * np.pi, -1.5 * np.pi, -np.pi, -0.5 * np.pi, 0.0])
    ax.set_yticklabels([r"$-2\pi$", r"$-1.5\pi$", r"$-\pi$", r"$-\pi/2$", "0"])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Phase [rad]", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def phase_values(delay: int, omega_norm: np.ndarray | float) -> np.ndarray | float:
    return -delay * np.pi * omega_norm


def export_phase_build_sequence(delay: int, figure_number: int, *, previous_delay: int | None = None) -> int:
    omega_norm = np.linspace(0.0, 1.0, 600)
    points = np.array(PHASE_SAMPLE_POINTS)
    frame_indices = (0, 1, 3)

    for frame_index in frame_indices:
        fig, ax = plt.subplots(figsize=FIGSIZE)
        fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
        style_phase_axis(ax)

        if previous_delay is not None:
            ax.plot(
                omega_norm,
                phase_values(previous_delay, omega_norm),
                color=REFERENCE_GREY,
                lw=3.0,
                alpha=0.80,
                label=rf"$D={previous_delay}$",
                zorder=2,
            )

        visible_points = points[: min(frame_index + 1, len(points))]
        if frame_index == 1:
            partial_omega_norm = np.linspace(0.0, 0.5, 300)
            ax.plot(
                partial_omega_norm,
                phase_values(delay, partial_omega_norm),
                color=SYSTEM_GREEN,
                lw=3.2,
                zorder=4,
            )
        elif frame_index == 3:
            ax.plot(
                omega_norm,
                phase_values(delay, omega_norm),
                color=SYSTEM_GREEN,
                lw=3.2,
                label=rf"$D={delay}$",
                zorder=4,
            )

        ax.scatter(
            visible_points,
            phase_values(delay, visible_points),
            s=95,
            color=SYSTEM_GREEN,
            edgecolor="white",
            linewidth=0.9,
            clip_on=False,
            label=rf"$D={delay}$" if previous_delay is not None and frame_index < 3 else None,
            zorder=5,
        )

        if previous_delay is not None or frame_index == 3:
            add_legend_last(ax, location="upper right")

        save_figure(fig, f"{figure_number:02d}_delay_d{delay}_phase_build_{frame_index + 1:02d}.png")
        figure_number += 2 if frame_index == 1 else 1

    return figure_number


def main() -> None:
    clear_output_dir()
    figure_number = 1
    for delay in DELAY_VALUES:
        for key, title, omega, omega_label in SIGNALS:
            export_input_frame(figure_number, delay, key, title, omega, omega_label)
            figure_number += 1
            export_output_frame(figure_number, delay, key, title, omega, omega_label)
            figure_number += 1
        previous_delay = delay - 1 if delay > 1 else None
        figure_number = export_phase_build_sequence(delay, figure_number, previous_delay=previous_delay)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
