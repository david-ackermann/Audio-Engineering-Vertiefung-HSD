from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = (
    OUTPUT_ROOT
    / "04_verschobene_impulsantwort"
    / "04A_shifted_ir_frequency_response"
)

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
DELAY_GREYS = {
    0: "0.30",
    1: "0.44",
    2: "0.58",
    3: "0.72",
}

MAX_DELAY = 4
TIME_SAMPLES = 18
NUM_FREQUENCIES = 4096

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


def reference_impulse_response(num_samples: int = 96) -> np.ndarray:
    """Stable recursive example used only as a smooth reference response."""
    b0 = 1.0
    a_coefficients = np.array([0.55, -0.12, 0.04, -0.01])
    h = np.zeros(num_samples)
    h[0] = b0
    for n in range(1, num_samples):
        feedback_sum = 0.0
        for r, a_r in enumerate(a_coefficients, start=1):
            if n - r >= 0:
                feedback_sum += a_r * h[n - r]
        h[n] = -feedback_sum
    return h


def dense_response(h: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    omega = np.linspace(0.0, np.pi, NUM_FREQUENCIES)
    n = np.arange(h.size)
    response = np.exp(-1j * np.outer(omega, n)) @ h
    return omega, response


def delayed_response(base_response: np.ndarray, omega: np.ndarray, delay: int) -> np.ndarray:
    return np.exp(-1j * delay * omega) * base_response


def shifted_impulse_response(h: np.ndarray, delay: int, num_samples: int) -> np.ndarray:
    shifted = np.zeros(num_samples)
    available = max(0, num_samples - delay)
    shifted[delay:] = h[:available]
    return shifted


def magnitude(response: np.ndarray) -> np.ndarray:
    return np.abs(response)


def unwrapped_phase(response: np.ndarray) -> np.ndarray:
    return np.unwrap(np.angle(response))


def style_time_axis(ax, *, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, TIME_SAMPLES - 0.5)
    ax.set_ylim(-1.08, 1.08)
    ax.set_xticks(np.arange(0, TIME_SAMPLES, 2))
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.4, zorder=1)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    style_common_axis(ax)


def style_magnitude_axis(ax, *, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.08)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    style_common_axis(ax)


def style_phase_axis(ax, *, title: str | None = None) -> None:
    if title:
        ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-4.25 * np.pi, 1.25 * np.pi)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([-4 * np.pi, -3 * np.pi, -2 * np.pi, -np.pi, 0, np.pi])
    ax.set_yticklabels([r"$-4\pi$", r"$-3\pi$", r"$-2\pi$", r"$-\pi$", "0", r"$\pi$"])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Phase [rad]", fontsize=LABEL_SIZE)
    style_common_axis(ax)


def style_common_axis(ax) -> None:
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def plot_stem(ax, samples: np.ndarray, values: np.ndarray, *, color: str, alpha: float, zorder: int) -> None:
    markerline, stemlines, baseline = ax.stem(samples, values)
    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor("white")
    markerline.set_markeredgewidth(0.9)
    markerline.set_markersize(8.0)
    markerline.set_alpha(alpha)
    markerline.set_zorder(zorder + 1)
    stemlines.set_color(color)
    stemlines.set_linewidth(2.8)
    stemlines.set_alpha(alpha)
    stemlines.set_zorder(zorder)
    baseline.set_visible(False)


def plot_time_history(ax, h: np.ndarray, delay: int) -> None:
    samples = np.arange(TIME_SAMPLES)
    active_values = shifted_impulse_response(h, delay, TIME_SAMPLES)
    plot_stem(ax, samples, active_values, color=SYSTEM_GREEN, alpha=1.0, zorder=4)


def plot_magnitude_response(ax, omega_norm: np.ndarray, response: np.ndarray) -> None:
    ax.plot(
        omega_norm,
        magnitude(response),
        color=SYSTEM_GREEN,
        lw=3.2,
        zorder=4,
    )


def plot_phase_history(ax, omega_norm: np.ndarray, responses: dict[int, np.ndarray], delay: int) -> None:
    for previous_delay in range(delay):
        ax.plot(
            omega_norm,
            unwrapped_phase(responses[previous_delay]),
            color=DELAY_GREYS[previous_delay],
            lw=2.6,
            alpha=0.88,
            zorder=2,
            label=rf"$r={previous_delay}$",
        )
    ax.plot(
        omega_norm,
        unwrapped_phase(responses[delay]),
        color=SYSTEM_GREEN,
        lw=3.2,
        zorder=4,
        label=rf"$r={delay}$",
    )


def export_time_frame(delay: int, h: np.ndarray, frame_number: int) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_time_history(ax, h, delay)
    style_time_axis(ax, title=rf"Delayed impulse response, $r={delay}$ samples")
    save_figure(fig, f"{frame_number:02d}_r{delay}_shifted_ir.png")


def export_magnitude_frame(delay: int, frame_number: int, omega_norm: np.ndarray, response: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_magnitude_response(ax, omega_norm, response)
    style_magnitude_axis(ax, title=rf"Magnitude response, $r={delay}$ samples")
    save_figure(fig, f"{frame_number:02d}_r{delay}_magnitude.png")


def export_phase_frame(delay: int, omega_norm: np.ndarray, responses: dict[int, np.ndarray], frame_number: int) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_phase_history(ax, omega_norm, responses, delay)
    style_phase_axis(ax, title=rf"Phase response, $r={delay}$ samples")
    ax.legend(loc="lower left", fontsize=15, frameon=True, framealpha=0.92)
    save_figure(fig, f"{frame_number:02d}_r{delay}_phase.png")


def main() -> None:
    clear_output_dir()
    h = reference_impulse_response()
    h = h / np.max(np.abs(h))
    omega, base_response = dense_response(h)
    base_response = base_response / np.max(np.abs(base_response))
    omega_norm = omega / np.pi
    responses = {
        delay: delayed_response(base_response, omega, delay)
        for delay in range(MAX_DELAY + 1)
    }

    frame_number = 1
    for delay in range(MAX_DELAY + 1):
        export_time_frame(delay, h, frame_number)
        frame_number += 1

        export_magnitude_frame(delay, frame_number, omega_norm, responses[delay])
        frame_number += 1

        export_phase_frame(delay, omega_norm, responses, frame_number)
        frame_number += 1

    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
