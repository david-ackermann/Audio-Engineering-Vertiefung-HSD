from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = (
    OUTPUT_ROOT
    / "04_verschobene_impulsantwort"
    / "04B_weighted_shifted_spectra"
)

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
TERM_GREYS = {
    1: "0.30",
    2: "0.44",
    3: "0.58",
    4: "0.72",
}

B0 = 1.0
A_COEFFICIENTS = np.array([0.55, -0.12, 0.04, -0.01])
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
    h = np.zeros(num_samples)
    h[0] = B0
    for n in range(1, num_samples):
        feedback_sum = 0.0
        for r, a_r in enumerate(A_COEFFICIENTS, start=1):
            if n - r >= 0:
                feedback_sum += a_r * h[n - r]
        h[n] = -feedback_sum
    return h


def dense_response(h: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    omega = np.linspace(0.0, np.pi, NUM_FREQUENCIES)
    n = np.arange(h.size)
    response = np.exp(-1j * np.outer(omega, n)) @ h
    return omega, response


def shifted_response(base_response: np.ndarray, omega: np.ndarray, delay: int) -> np.ndarray:
    return np.exp(-1j * delay * omega) * base_response


def weighted_shifted_terms(base_response: np.ndarray, omega: np.ndarray) -> dict[int, np.ndarray]:
    return {
        delay: A_COEFFICIENTS[delay - 1] * shifted_response(base_response, omega, delay)
        for delay in range(1, A_COEFFICIENTS.size + 1)
    }


def magnitude(response: np.ndarray) -> np.ndarray:
    return np.abs(response)


def unwrapped_phase(response: np.ndarray) -> np.ndarray:
    return np.unwrap(np.angle(response))


def style_common_axis(ax) -> None:
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


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


def style_phase_axis(ax, *, title: str) -> None:
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


def term_label(delay: int) -> str:
    return rf"$r={delay}$, $a_{delay}={A_COEFFICIENTS[delay - 1]:+.2f}$"


def plot_weighted_terms(
    ax,
    omega_norm: np.ndarray,
    terms: dict[int, np.ndarray],
    *,
    quantity: str,
) -> None:
    for delay in range(1, A_COEFFICIENTS.size + 1):
        values = magnitude(terms[delay]) if quantity == "magnitude" else unwrapped_phase(terms[delay])
        ax.plot(
            omega_norm,
            values,
            color=TERM_GREYS[delay],
            lw=3.0,
            alpha=0.92,
            zorder=3,
            label=term_label(delay),
        )


def export_all_weighted_terms_magnitude(
    frame_number: int,
    omega_norm: np.ndarray,
    terms: dict[int, np.ndarray],
) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_weighted_terms(ax, omega_norm, terms, quantity="magnitude")
    style_magnitude_axis(ax, title="Weighted shifted spectra, magnitude")
    ax.legend(loc="upper left", fontsize=14, frameon=True, framealpha=0.92)
    save_figure(fig, f"{frame_number:02d}_weighted_terms_magnitude.png")


def export_all_weighted_terms_phase(
    frame_number: int,
    omega_norm: np.ndarray,
    terms: dict[int, np.ndarray],
) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_weighted_terms(ax, omega_norm, terms, quantity="phase")
    style_phase_axis(ax, title="Weighted shifted spectra, phase")
    ax.legend(loc="lower left", fontsize=14, frameon=True, framealpha=0.92)
    save_figure(fig, f"{frame_number:02d}_weighted_terms_phase.png")


def export_weighted_sum_magnitude(
    frame_number: int,
    omega_norm: np.ndarray,
    terms: dict[int, np.ndarray],
    weighted_sum: np.ndarray,
) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_weighted_terms(ax, omega_norm, terms, quantity="magnitude")
    ax.plot(
        omega_norm,
        magnitude(weighted_sum),
        color=SYSTEM_GREEN,
        lw=3.4,
        zorder=5,
        label="complex sum",
    )
    style_magnitude_axis(ax, title=r"Complex sum of weighted shifted spectra, magnitude")
    ax.legend(loc="upper left", fontsize=14, frameon=True, framealpha=0.92)
    save_figure(fig, f"{frame_number:02d}_weighted_sum_magnitude.png")


def export_weighted_sum_phase(
    frame_number: int,
    omega_norm: np.ndarray,
    terms: dict[int, np.ndarray],
    weighted_sum: np.ndarray,
) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_weighted_terms(ax, omega_norm, terms, quantity="phase")
    ax.plot(
        omega_norm,
        unwrapped_phase(weighted_sum),
        color=SYSTEM_GREEN,
        lw=3.4,
        zorder=5,
        label="complex sum",
    )
    style_phase_axis(ax, title=r"Complex sum of weighted shifted spectra, phase")
    ax.legend(loc="lower left", fontsize=14, frameon=True, framealpha=0.92)
    save_figure(fig, f"{frame_number:02d}_weighted_sum_phase.png")


def main() -> None:
    clear_output_dir()
    h = reference_impulse_response()
    h = h / np.max(np.abs(h))
    omega, base_response = dense_response(h)
    base_response = base_response / np.max(np.abs(base_response))
    omega_norm = omega / np.pi
    terms = weighted_shifted_terms(base_response, omega)

    frame_number = 1
    export_all_weighted_terms_magnitude(frame_number, omega_norm, terms)
    frame_number += 1
    export_all_weighted_terms_phase(frame_number, omega_norm, terms)
    frame_number += 1

    weighted_sum = np.sum(np.stack([terms[delay] for delay in range(1, A_COEFFICIENTS.size + 1)]), axis=0)
    export_weighted_sum_magnitude(frame_number, omega_norm, terms, weighted_sum)
    frame_number += 1
    export_weighted_sum_phase(frame_number, omega_norm, terms, weighted_sum)

    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
