from pathlib import Path
from fractions import Fraction

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image, ImageSequence


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_diskrete_kreisfrequenz"
    / "04A"
    / "04A3_cos_sin_basisfunktionen"
)

DPI = 200
FIGSIZE = (13.2, 4.8)
FPS = 8
FRAMES_PER_SAMPLE = 6
EXPORT_GIFS = True

TITLE_SIZE = 22
SUBTITLE_SIZE = 18
LABEL_SIZE = 18
TICK_SIZE = 16

SIGNAL_BLUE = "#2b7bbb"
SIGNAL_ORANGE = "#d97a27"
GRID_GREY = "0.78"
SIGNAL_BLACK = "0.05"
DENSE_REFERENCE_GREY = "0.72"

N = 16
K_VALUES = (1, 4, 7, 9, 16)
SAMPLE_INDICES = np.arange(N, dtype=float)
DENSE_INDICES = np.linspace(0.0, N, 2401)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()
    for gif_file in OUTPUT_DIR.glob("*.gif"):
        gif_file.unlink()


def omega_fraction_latex(k: int) -> str:
    return omega_fraction_latex_for(k, N)


def omega_fraction_latex_for(k: int, block_length: int) -> str:
    frac = Fraction(2 * k, block_length).limit_denominator()
    numerator = frac.numerator
    denominator = frac.denominator
    sign = "-" if numerator < 0 else ""
    numerator = abs(numerator)

    if numerator == 0:
        return "0"
    if denominator == 1:
        if numerator == 1:
            return rf"{sign}\pi"
        return rf"{sign}{numerator}\pi"
    if numerator == 1:
        return rf"{sign}\frac{{\pi}}{{{denominator}}}"
    return rf"{sign}\frac{{{numerator}\pi}}{{{denominator}}}"


def bin_title_latex(k: int) -> str:
    return rf"$k = {k}$"


def figure_title(k: int) -> str:
    return rf"DFT analysis basis: {bin_title_latex(k)}, $\Omega_{{{k}}} = {omega_fraction_latex(k)}$"


def figure_title_for(k: int, block_length: int) -> str:
    return (
        rf"DFT analysis basis: $k = {k}$, $N = {block_length}$, "
        rf"$\Omega_{{{k}}} = {omega_fraction_latex_for(k, block_length)}$"
    )


def cosine_dense(k: int):
    return np.cos(2.0 * np.pi * k * DENSE_INDICES / N)


def cosine_samples(k: int):
    return np.cos(2.0 * np.pi * k * SAMPLE_INDICES / N)


def minus_sine_dense(k: int):
    return -np.sin(2.0 * np.pi * k * DENSE_INDICES / N)


def minus_sine_samples(k: int):
    return -np.sin(2.0 * np.pi * k * SAMPLE_INDICES / N)


def cosine_dense_for(k: int, block_length: int, dense_indices: np.ndarray):
    return np.cos(2.0 * np.pi * k * dense_indices / block_length)


def cosine_samples_for(k: int, block_length: int, sample_indices: np.ndarray):
    return np.cos(2.0 * np.pi * k * sample_indices / block_length)


def minus_sine_dense_for(k: int, block_length: int, dense_indices: np.ndarray):
    return -np.sin(2.0 * np.pi * k * dense_indices / block_length)


def minus_sine_samples_for(k: int, block_length: int, sample_indices: np.ndarray):
    return -np.sin(2.0 * np.pi * k * sample_indices / block_length)


def style_axis(ax, *, title: str, show_ylabel: bool, block_length: int = N) -> None:
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.axvline(block_length, color=GRID_GREY, lw=1.0, ls=":")
    ax.set_xlim(-0.35, block_length + 0.35)
    ax.set_ylim(-1.15, 1.15)
    tick_step = 2 if block_length <= 16 else 4
    ax.set_xticks(np.arange(0, block_length + 1, tick_step))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=SUBTITLE_SIZE, pad=8)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude" if show_ylabel else "", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def draw_component(
    ax,
    dense_values,
    sample_values,
    *,
    color: str,
    dense_indices: np.ndarray = DENSE_INDICES,
    sample_indices: np.ndarray = SAMPLE_INDICES,
) -> None:
    ax.plot(dense_indices, dense_values, color=color, lw=2.3, ls="--", alpha=0.72, zorder=1)
    ax.vlines(sample_indices, 0.0, sample_values, color=color, lw=2.2, zorder=2)
    ax.scatter(
        sample_indices,
        sample_values,
        s=78,
        color=color,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
    )


def stem_segments(sample_indices: np.ndarray, sample_values: np.ndarray) -> list[list[tuple[float, float]]]:
    return [[(sample_index, 0.0), (sample_index, sample_value)] for sample_index, sample_value in zip(sample_indices, sample_values)]


def sync_total_duration_ms(block_length: int) -> int:
    return int(round(block_length * FRAMES_PER_SAMPLE * 1000 / FPS))


def sync_frame_durations(frame_count: int, total_duration_ms: int) -> list[int]:
    base_duration = int(np.floor(total_duration_ms / frame_count / 10.0) * 10)
    durations = [base_duration] * frame_count
    remaining_ms = total_duration_ms - base_duration * frame_count

    for index in range(remaining_ms // 10):
        durations[index % frame_count] += 10

    return durations


def enforce_gif_duration(path: Path, total_duration_ms: int) -> None:
    image = Image.open(path)
    frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(image)]
    if not frames:
        return

    durations = sync_frame_durations(len(frames), total_duration_ms)

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=image.info.get("loop", 0),
        disposal=2,
    )


def visible_dense_segment(
    dense_indices: np.ndarray,
    dense_values: np.ndarray,
    progress: float,
) -> tuple[np.ndarray, np.ndarray]:
    visible = dense_indices <= progress
    x_values = dense_indices[visible]
    y_values = dense_values[visible]

    if len(x_values) == 0 or not np.isclose(x_values[-1], progress):
        y_progress = np.interp(progress, dense_indices, dense_values)
        x_values = np.append(x_values, progress)
        y_values = np.append(y_values, y_progress)

    return x_values, y_values


def export_basis_components_animation_for(k: int, block_length: int, filename: str) -> None:
    sample_indices = np.arange(block_length, dtype=float)
    dense_indices = np.linspace(0.0, block_length, 2401)
    frame_count = block_length * FRAMES_PER_SAMPLE
    progress_values = np.linspace(0.0, float(block_length), frame_count)

    cos_dense_values = cosine_dense_for(k, block_length, dense_indices)
    sin_dense_values = minus_sine_dense_for(k, block_length, dense_indices)
    cos_sample_values = cosine_samples_for(k, block_length, sample_indices)
    sin_sample_values = minus_sine_samples_for(k, block_length, sample_indices)

    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.80, wspace=0.20)
    fig.suptitle(
        figure_title_for(k, block_length) if block_length != N else figure_title(k),
        fontsize=TITLE_SIZE,
        y=0.96,
    )

    axes[0].plot(dense_indices, cos_dense_values, color=DENSE_REFERENCE_GREY, lw=2.3, ls="--", alpha=0.72, zorder=1)
    cos_reveal, = axes[0].plot([], [], color=SIGNAL_BLUE, lw=2.3, ls="--", alpha=0.95, zorder=2)
    cos_stems = axes[0].vlines([], 0.0, [], color=SIGNAL_BLUE, lw=2.2, zorder=3)
    cos_points = axes[0].scatter([], [], s=78, color=SIGNAL_BLUE, edgecolor="white", linewidth=1.0, zorder=4)
    style_axis(
        axes[0],
        title=rf"Cosine component: $\cos(\Omega_{{{k}}} n)$",
        show_ylabel=True,
        block_length=block_length,
    )

    axes[1].plot(dense_indices, sin_dense_values, color=DENSE_REFERENCE_GREY, lw=2.3, ls="--", alpha=0.72, zorder=1)
    sin_reveal, = axes[1].plot([], [], color=SIGNAL_ORANGE, lw=2.3, ls="--", alpha=0.95, zorder=2)
    sin_stems = axes[1].vlines([], 0.0, [], color=SIGNAL_ORANGE, lw=2.2, zorder=3)
    sin_points = axes[1].scatter([], [], s=78, color=SIGNAL_ORANGE, edgecolor="white", linewidth=1.0, zorder=4)
    style_axis(
        axes[1],
        title=rf"Sine component: $-\sin(\Omega_{{{k}}} n)$",
        show_ylabel=False,
        block_length=block_length,
    )

    def draw_state(frame_index: int):
        progress = progress_values[frame_index]
        sample_count = min(block_length, int(np.floor(progress)) + 1)
        visible_indices = sample_indices[:sample_count]
        visible_cos_values = cos_sample_values[:sample_count]
        visible_sin_values = sin_sample_values[:sample_count]
        visible_cos_x, visible_cos_y = visible_dense_segment(dense_indices, cos_dense_values, progress)
        visible_sin_x, visible_sin_y = visible_dense_segment(dense_indices, sin_dense_values, progress)

        cos_reveal.set_data(visible_cos_x, visible_cos_y)
        sin_reveal.set_data(visible_sin_x, visible_sin_y)
        cos_stems.set_segments(stem_segments(visible_indices, visible_cos_values))
        sin_stems.set_segments(stem_segments(visible_indices, visible_sin_values))
        cos_points.set_offsets(np.column_stack([visible_indices, visible_cos_values]))
        sin_points.set_offsets(np.column_stack([visible_indices, visible_sin_values]))

        return cos_reveal, cos_stems, cos_points, sin_reveal, sin_stems, sin_points

    draw_state(0)
    animation = FuncAnimation(
        fig,
        draw_state,
        frames=frame_count,
        interval=1000 / FPS,
        blit=False,
    )
    gif_path = OUTPUT_DIR / filename
    animation.save(str(gif_path.resolve()), writer=PillowWriter(fps=FPS))
    enforce_gif_duration(gif_path, sync_total_duration_ms(block_length))
    plt.close(fig)


def export_basis_components_animation(k: int) -> None:
    export_basis_components_animation_for(k, N, f"k{k:02d}_cos_sin_basis.gif")


def draw_component_initial(
    ax,
    dense_indices: np.ndarray,
    dense_values: np.ndarray,
    sample_value: float,
    *,
    color: str,
) -> None:
    ax.plot(dense_indices, dense_values, color=DENSE_REFERENCE_GREY, lw=2.3, ls="--", alpha=0.72, zorder=1)
    ax.vlines([0.0], 0.0, [sample_value], color=color, lw=2.2, zorder=2)
    ax.scatter(
        [0.0],
        [sample_value],
        s=78,
        color=color,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
    )


def export_basis_components_initial_for(k: int, block_length: int, filename: str) -> None:
    sample_indices = np.arange(block_length, dtype=float)
    dense_indices = np.linspace(0.0, block_length, 2401)

    cos_dense_values = cosine_dense_for(k, block_length, dense_indices)
    sin_dense_values = minus_sine_dense_for(k, block_length, dense_indices)
    cos_sample_values = cosine_samples_for(k, block_length, sample_indices)
    sin_sample_values = minus_sine_samples_for(k, block_length, sample_indices)

    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.80, wspace=0.20)
    fig.suptitle(
        figure_title_for(k, block_length) if block_length != N else figure_title(k),
        fontsize=TITLE_SIZE,
        y=0.96,
    )

    draw_component_initial(
        axes[0],
        dense_indices,
        cos_dense_values,
        cos_sample_values[0],
        color=SIGNAL_BLUE,
    )
    style_axis(
        axes[0],
        title=rf"Cosine component: $\cos(\Omega_{{{k}}} n)$",
        show_ylabel=True,
        block_length=block_length,
    )

    draw_component_initial(
        axes[1],
        dense_indices,
        sin_dense_values,
        sin_sample_values[0],
        color=SIGNAL_ORANGE,
    )
    style_axis(
        axes[1],
        title=rf"Sine component: $-\sin(\Omega_{{{k}}} n)$",
        show_ylabel=False,
        block_length=block_length,
    )

    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def export_basis_components_initial(k: int) -> None:
    export_basis_components_initial_for(k, N, f"k{k:02d}_cos_sin_basis_n0.png")


def draw_sampled_dc_overlay(ax, *, level: float) -> None:
    ax.plot(
        SAMPLE_INDICES,
        np.full_like(SAMPLE_INDICES, level, dtype=float),
        color=SIGNAL_BLACK,
        lw=2.8,
        zorder=5,
    )
    ax.scatter(
        SAMPLE_INDICES,
        np.full_like(SAMPLE_INDICES, level, dtype=float),
        s=94,
        facecolor="white",
        edgecolor=SIGNAL_BLACK,
        linewidth=1.4,
        zorder=6,
    )


def draw_k9_with_kminus7_overlay(ax, dense_func, sample_func, *, color: str) -> None:
    k_samples = 9
    k_overlay = -7
    samples = sample_func(k_samples)

    ax.plot(DENSE_INDICES, dense_func(k_samples), color=color, lw=2.3, ls="--", alpha=0.62, zorder=1)
    ax.plot(DENSE_INDICES, dense_func(k_overlay), color=SIGNAL_BLACK, lw=2.2, zorder=2)
    ax.vlines(SAMPLE_INDICES, 0.0, samples, color=color, lw=2.2, zorder=3)
    ax.scatter(
        SAMPLE_INDICES,
        samples,
        s=78,
        color=color,
        edgecolor="white",
        linewidth=1.0,
        zorder=4,
    )
    ax.scatter(
        SAMPLE_INDICES,
        samples,
        s=110,
        facecolor="none",
        edgecolor=SIGNAL_BLACK,
        linewidth=1.1,
        zorder=5,
    )


def export_basis_components(k: int) -> None:
    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.80, wspace=0.20)
    fig.suptitle(
        figure_title(k),
        fontsize=TITLE_SIZE,
        y=0.96,
    )

    draw_component(
        axes[0],
        cosine_dense(k),
        cosine_samples(k),
        color=SIGNAL_BLUE,
    )
    style_axis(
        axes[0],
        title=rf"Cosine component: $\cos(\Omega_{{{k}}} n)$",
        show_ylabel=True,
    )

    draw_component(
        axes[1],
        minus_sine_dense(k),
        minus_sine_samples(k),
        color=SIGNAL_ORANGE,
    )
    style_axis(
        axes[1],
        title=rf"Sine component: $-\sin(\Omega_{{{k}}} n)$",
        show_ylabel=False,
    )

    fig.savefig(OUTPUT_DIR / f"k{k:02d}_cos_sin_basis.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def export_basis_components_for(k: int, block_length: int, filename: str) -> None:
    sample_indices = np.arange(block_length, dtype=float)
    dense_indices = np.linspace(0.0, block_length, 2401)

    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.80, wspace=0.20)
    fig.suptitle(
        figure_title_for(k, block_length),
        fontsize=TITLE_SIZE,
        y=0.96,
    )

    draw_component(
        axes[0],
        cosine_dense_for(k, block_length, dense_indices),
        cosine_samples_for(k, block_length, sample_indices),
        color=SIGNAL_BLUE,
        dense_indices=dense_indices,
        sample_indices=sample_indices,
    )
    style_axis(
        axes[0],
        title=rf"Cosine component: $\cos(\Omega_{{{k}}} n)$",
        show_ylabel=True,
        block_length=block_length,
    )

    draw_component(
        axes[1],
        minus_sine_dense_for(k, block_length, dense_indices),
        minus_sine_samples_for(k, block_length, sample_indices),
        color=SIGNAL_ORANGE,
        dense_indices=dense_indices,
        sample_indices=sample_indices,
    )
    style_axis(
        axes[1],
        title=rf"Sine component: $-\sin(\Omega_{{{k}}} n)$",
        show_ylabel=False,
        block_length=block_length,
    )

    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def export_k16_sampled_dc_overlay() -> None:
    k = 16
    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.80, wspace=0.20)
    fig.suptitle(
        figure_title(k),
        fontsize=TITLE_SIZE,
        y=0.96,
    )

    draw_component(
        axes[0],
        cosine_dense(k),
        cosine_samples(k),
        color=SIGNAL_BLUE,
    )
    draw_sampled_dc_overlay(axes[0], level=1.0)
    style_axis(
        axes[0],
        title=r"Cosine component: sampled sequence",
        show_ylabel=True,
    )

    draw_component(
        axes[1],
        minus_sine_dense(k),
        minus_sine_samples(k),
        color=SIGNAL_ORANGE,
    )
    draw_sampled_dc_overlay(axes[1], level=0.0)
    style_axis(
        axes[1],
        title=r"Sine component: sampled sequence",
        show_ylabel=False,
    )

    fig.savefig(OUTPUT_DIR / "k16_sampled_dc_equivalent.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def export_k9_kminus7_support_overlay() -> None:
    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.80, wspace=0.20)
    fig.suptitle(
        figure_title(9),
        fontsize=TITLE_SIZE,
        y=0.96,
    )

    draw_k9_with_kminus7_overlay(
        axes[0],
        cosine_dense,
        cosine_samples,
        color=SIGNAL_BLUE,
    )
    style_axis(
        axes[0],
        title=r"Cosine component",
        show_ylabel=True,
    )

    draw_k9_with_kminus7_overlay(
        axes[1],
        minus_sine_dense,
        minus_sine_samples,
        color=SIGNAL_ORANGE,
    )
    style_axis(
        axes[1],
        title=r"Sine component",
        show_ylabel=False,
    )

    fig.savefig(OUTPUT_DIR / "k09_kminus7_same_support_samples.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def main() -> None:
    clear_output_dir()
    for k in K_VALUES:
        export_basis_components(k)
        export_basis_components_initial(k)
        if EXPORT_GIFS:
            export_basis_components_animation(k)
    export_k9_kminus7_support_overlay()
    export_k16_sampled_dc_overlay()
    export_basis_components_for(16, 32, "k16_n32_cos_sin_basis.png")
    export_basis_components_initial_for(16, 32, "k16_n32_cos_sin_basis_n0.png")
    if EXPORT_GIFS:
        export_basis_components_animation_for(16, 32, "k16_n32_cos_sin_basis.gif")
    print(f"PNG storyboard exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
