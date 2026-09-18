from matplotlib import pyplot as plt
import os
from pathlib import Path

from pretty_plot.core import prettify


def test_all(test_case_example):
    fig, ax = plt.subplots()

    ax.plot([-1, 2, 3], [4, 5, 6], label="data")
    ax.set_title("Amazing results")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper left")

    prettify(fig, ax, **test_case_example.model_dump())

    fig.tight_layout()
    output_dir = Path("test_outputs")
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(output_dir / "test.svg")
