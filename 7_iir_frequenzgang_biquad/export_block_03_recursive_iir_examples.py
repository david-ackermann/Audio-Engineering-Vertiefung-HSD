from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "03_rekursives_iir_mehrere_taps" / "03A_recursive_iir_frequency_examples"

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"

FS_HZ = 48_000.0
NYQUIST_HZ = FS_HZ / 2.0
LOG_MIN_HZ = 20.0

LINEAR_LABEL_POSITIONS = {
    "m2_low_frequency_emphasis": (0.48, 0.74),
}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class RecursiveIirExample:
    slug: str
    title: str
    poles: tuple[complex, ...]
    label_x: float
    label_y: float


EXAMPLES = (
    RecursiveIirExample(
        slug="m2_low_frequency_emphasis",
        title="M=2 Low-frequency emphasis",
        poles=(0.72, 0.55),
        label_x=0.055,
        label_y=0.10,
    ),
    RecursiveIirExample(
        slug="m2_high_frequency_emphasis",
        title="M=2 High-frequency emphasis",
        poles=(-0.72, -0.55),
        label_x=0.055,
        label_y=0.74,
    ),
    RecursiveIirExample(
        slug="m2_resonant_mode",
        title="M=2 Mid resonance",
        poles=(
            0.82 * np.exp(1j * 0.36 * np.pi),
            0.82 * np.exp(-1j * 0.36 * np.pi),
        ),
        label_x=0.055,
        label_y=0.10,
    ),
    RecursiveIirExample(
        slug="m4_two_broad_resonances",
        title="M=4 Two broad resonances",
        poles=(
            0.74 * np.exp(1j * 0.24 * np.pi),
            0.74 * np.exp(-1j * 0.24 * np.pi),
            0.82 * np.exp(1j * 0.62 * np.pi),
            0.82 * np.exp(-1j * 0.62 * np.pi),
        ),
        label_x=0.055,
        label_y=0.10,
    ),
    RecursiveIirExample(
        slug="m6_three_resonances",
        title="M=6 Three resonances",
        poles=(
            0.78 * np.exp(1j * 0.16 * np.pi),
            0.78 * np.exp(-1j * 0.16 * np.pi),
            0.84 * np.exp(1j * 0.43 * np.pi),
            0.84 * np.exp(-1j * 0.43 * np.pi),
            0.80 * np.exp(1j * 0.78 * np.pi),
            0.80 * np.exp(-1j * 0.78 * np.pi),
        ),
        label_x=0.055,
        label_y=0.06,
    ),
    RecursiveIirExample(
        slug="m8_complex_recursive_curve",
        title="M=8 Complex recursive curve",
        poles=(
            0.72 * np.exp(1j * 0.10 * np.pi),
            0.72 * np.exp(-1j * 0.10 * np.pi),
            0.80 * np.exp(1j * 0.28 * np.pi),
            0.80 * np.exp(-1j * 0.28 * np.pi),
            0.86 * np.exp(1j * 0.53 * np.pi),
            0.86 * np.exp(-1j * 0.53 * np.pi),
            0.84 * np.exp(1j * 0.82 * np.pi),
            0.84 * np.exp(-1j * 0.82 * np.pi),
        ),
        label_x=0.055,
        label_y=0.06,
    ),
)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.rglob("*.png"):
        image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def denominator_coefficients_from_poles(poles: tuple[complex, ...]) -> np.ndarray:
    coefficients = np.poly(np.asarray(poles, dtype=complex)).real
    coefficients[np.abs(coefficients) < 1e-12] = 0.0
    return coefficients[1:]


def response_from_frequency(frequency_hz: np.ndarray, b0: float, a_coefficients: np.ndarray) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    denominator = np.ones_like(omega, dtype=complex)
    for r, a_r in enumerate(a_coefficients, start=1):
        denominator += a_r * np.exp(-1j * r * omega)
    return b0 / denominator


def normalized_b0(a_coefficients: np.ndarray) -> float:
    frequency_hz = np.linspace(0.0, NYQUIST_HZ, 32768)
    response = response_from_frequency(frequency_hz, 1.0, a_coefficients)
    return 1.0 / np.max(np.abs(response))


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def coefficient_label(b0: float, a_coefficients: np.ndarray) -> str:
    if len(a_coefficients) == 2:
        return (
            rf"$b_0={b0:.3f}$, "
            rf"$a_1={a_coefficients[0]:+.2f}$, "
            rf"$a_2={a_coefficients[1]:+.2f}$"
        )

    lines = [rf"$b_0={b0:.3f}$"]
    for start in range(0, len(a_coefficients), 4):
        values = ", ".join(f"{value:+.2f}" for value in a_coefficients[start : start + 4])
        end = min(start + 4, len(a_coefficients))
        lines.append(rf"$[a_{start + 1},\ldots,a_{end}]=[{values}]$")
    return "\n".join(lines)


def add_coefficient_label(
    ax,
    example: RecursiveIirExample,
    b0: float,
    a_coefficients: np.ndarray,
    label_position: tuple[float, float] | None = None,
) -> None:
    label_x, label_y = label_position or (example.label_x, example.label_y)
    coefficient_text = ax.text(
        label_x,
        label_y,
        coefficient_label(b0, a_coefficients),
        transform=ax.transAxes,
        fontsize=14 if len(a_coefficients) > 4 else 17 if len(a_coefficients) > 2 else 19,
        color=SIGNAL_BLACK,
        ha="left",
        va="bottom",
    )
    coefficient_text.set_path_effects(
        [path_effects.withStroke(linewidth=4, foreground="white")]
    )


def style_common_axis(
    ax,
    example: RecursiveIirExample,
    b0: float,
    a_coefficients: np.ndarray,
    label_position: tuple[float, float] | None = None,
) -> None:
    ax.set_title(example.title, fontsize=TITLE_SIZE, pad=14)
    add_coefficient_label(ax, example, b0, a_coefficients, label_position)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_log_db_axis(ax, example: RecursiveIirExample, b0: float, a_coefficients: np.ndarray) -> None:
    ax.set_xscale("log")
    ax.set_xlim(LOG_MIN_HZ, NYQUIST_HZ)
    ax.set_ylim(-30.0, 2.0)
    ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
    ax.set_yticks([-30, -24, -18, -12, -6, 0])
    ax.set_xlabel(r"Frequency in Hz, $f_s=48\,\mathrm{kHz}$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude in dB", fontsize=LABEL_SIZE)
    style_common_axis(ax, example, b0, a_coefficients)


def style_linear_axis(ax, example: RecursiveIirExample, b0: float, a_coefficients: np.ndarray) -> None:
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.08)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    style_common_axis(
        ax,
        example,
        b0,
        a_coefficients,
        LINEAR_LABEL_POSITIONS.get(example.slug),
    )


def export_log_db_example(index: int, example: RecursiveIirExample) -> None:
    a_coefficients = denominator_coefficients_from_poles(example.poles)
    b0 = normalized_b0(a_coefficients)
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(NYQUIST_HZ), 4096)
    response = response_from_frequency(frequency_hz, b0, a_coefficients)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz, magnitude_db(response), color=SYSTEM_GREEN, lw=3.0)
    style_log_db_axis(ax, example, b0, a_coefficients)
    save_figure(fig, f"{index:02d}_{example.slug}_log_db.png")


def export_linear_example(index: int, example: RecursiveIirExample) -> None:
    a_coefficients = denominator_coefficients_from_poles(example.poles)
    b0 = normalized_b0(a_coefficients)
    frequency_hz = np.linspace(0.0, NYQUIST_HZ, 4096)
    response = response_from_frequency(frequency_hz, b0, a_coefficients)
    normalized_omega = frequency_hz / NYQUIST_HZ

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(normalized_omega, np.abs(response), color=SYSTEM_GREEN, lw=3.0)
    style_linear_axis(ax, example, b0, a_coefficients)
    save_figure(fig, f"{index:02d}_{example.slug}_linear_magnitude.png")


def main() -> None:
    clear_output_dir()
    for index, example in enumerate(EXAMPLES, start=1):
        export_log_db_example(index, example)
    for index, example in enumerate(EXAMPLES, start=1 + len(EXAMPLES)):
        export_linear_example(index, example)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
