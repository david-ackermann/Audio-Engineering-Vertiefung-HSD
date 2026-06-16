from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_2C_DIR = OUTPUT_ROOT / "02_komplexe_exponentialsignale_lti" / "02C_delay_ir_frequenzbereich"

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
REFERENCE_GREY = "0.58"
LIGHT_GREY = "0.82"
BLUE = "#2b7bbb"
ORANGE = "#d98c2f"
PURPLE = "#7c6aa6"

NUM_FREQUENCIES = 4096
TIME_SAMPLES = 16

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    BLOCK_2C_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_2C_DIR.rglob("*.png"):
        image_file.unlink()


def save_figure(fig, block_dir: Path, filename: str) -> None:
    fig.savefig(block_dir / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def reference_impulse_response(num_samples: int = 96) -> np.ndarray:
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


def shifted_response(response: np.ndarray, omega: np.ndarray, delay: int) -> np.ndarray:
    return np.exp(-1j * delay * omega) * response


def shifted_ir(h: np.ndarray, delay: int, num_samples: int) -> np.ndarray:
    output = np.zeros(num_samples)
    output[delay:] = h[: num_samples - delay]
    return output


def style_common_axis(ax) -> None:
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_time_axis(ax, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, TIME_SAMPLES - 0.5)
    ax.set_ylim(-1.08, 1.08)
    ax.set_xticks(np.arange(0, TIME_SAMPLES, 2))
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.4, zorder=1)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    style_common_axis(ax)


def style_magnitude_axis(ax, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.08)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    style_common_axis(ax)


def style_phase_axis(ax, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-2.15 * np.pi, 0.35 * np.pi)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([-2 * np.pi, -1.5 * np.pi, -np.pi, -0.5 * np.pi, 0.0])
    ax.set_yticklabels([r"$-2\pi$", r"$-1.5\pi$", r"$-\pi$", r"$-0.5\pi$", "0"])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Phase [rad]", fontsize=LABEL_SIZE)
    style_common_axis(ax)


def plot_stem(ax, values: np.ndarray, *, color: str, alpha: float = 1.0, zorder: int = 3) -> None:
    n = np.arange(values.size)
    markerline, stemlines, baseline = ax.stem(n, values)
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


def normalized_magnitude(response: np.ndarray) -> np.ndarray:
    mag = np.abs(response)
    return mag / np.max(mag)


def export_time_original(h: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_stem(ax, h[:TIME_SAMPLES], color=SYSTEM_GREEN)
    style_time_axis(ax, r"Impulse response $h[n]$")
    save_figure(fig, BLOCK_2C_DIR, "01_impulse_response_h_n.png")


def export_time_delayed(h: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_stem(ax, h[:TIME_SAMPLES], color=REFERENCE_GREY, alpha=0.42, zorder=2)
    plot_stem(ax, shifted_ir(h, 1, TIME_SAMPLES), color=SYSTEM_GREEN, zorder=4)
    style_time_axis(ax, r"One-sample delay: $h[n-1]$")
    save_figure(fig, BLOCK_2C_DIR, "02_one_sample_delay_time.png")


def export_magnitude_base(omega_norm: np.ndarray, base_response: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega_norm, normalized_magnitude(base_response), color=SYSTEM_GREEN, lw=3.2)
    style_magnitude_axis(ax, r"Magnitude of $H(e^{j\Omega})$")
    save_figure(fig, BLOCK_2C_DIR, "03_magnitude_original.png")


def export_magnitude_delayed(omega_norm: np.ndarray, base_response: np.ndarray, delayed_response: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega_norm, normalized_magnitude(base_response), color=REFERENCE_GREY, lw=4.4, alpha=0.70, label=r"$H(e^{j\Omega})$")
    ax.plot(omega_norm, normalized_magnitude(delayed_response), color=SYSTEM_GREEN, lw=2.8, label=r"$e^{-j\Omega}H(e^{j\Omega})$")
    style_magnitude_axis(ax, "One-sample delay leaves magnitude unchanged")
    ax.legend(loc="lower right", fontsize=16, frameon=True, framealpha=0.92)
    save_figure(fig, BLOCK_2C_DIR, "04_magnitude_delay_overlay.png")


def export_phase_base(omega_norm: np.ndarray, base_response: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega_norm, np.unwrap(np.angle(base_response)), color=SYSTEM_GREEN, lw=3.2)
    style_phase_axis(ax, r"Phase of $H(e^{j\Omega})$")
    save_figure(fig, BLOCK_2C_DIR, "05_phase_original.png")


def export_phase_delayed(omega_norm: np.ndarray, base_response: np.ndarray, delayed_response: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega_norm, np.unwrap(np.angle(base_response)), color=REFERENCE_GREY, lw=3.0, alpha=0.72, label=r"$H(e^{j\Omega})$")
    ax.plot(omega_norm, np.unwrap(np.angle(delayed_response)), color=SYSTEM_GREEN, lw=3.2, label=r"$e^{-j\Omega}H(e^{j\Omega})$")
    ax.plot(omega_norm, -np.pi * omega_norm, color=ORANGE, lw=2.0, ls="--", alpha=0.95, label=r"extra phase: $-\Omega$")
    style_phase_axis(ax, "One-sample delay adds linear phase")
    ax.legend(loc="lower left", fontsize=15, frameon=True, framealpha=0.92)
    save_figure(fig, BLOCK_2C_DIR, "06_phase_delay_overlay.png")


def main() -> None:
    clear_output_dir()
    h = reference_impulse_response()
    omega, base_response = dense_response(h)
    delayed = shifted_response(base_response, omega, 1)
    omega_norm = omega / np.pi

    export_time_original(h)
    export_time_delayed(h)
    export_magnitude_base(omega_norm, base_response)
    export_magnitude_delayed(omega_norm, base_response, delayed)
    export_phase_base(omega_norm, base_response)
    export_phase_delayed(omega_norm, base_response, delayed)
    print(f"PNG figures exported to: {BLOCK_2C_DIR}")


if __name__ == "__main__":
    main()
