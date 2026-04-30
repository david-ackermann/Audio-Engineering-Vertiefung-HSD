from pathlib import Path
import sys

LECTURE_DIR = Path(__file__).resolve().parents[2] / "1_fourier_transformation"
if str(LECTURE_DIR) not in sys.path:
    sys.path.insert(0, str(LECTURE_DIR))

from fourier_phasor_core import *  # noqa: F401,F403


if __name__ == "__main__":
    main()
