import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


def plot_equity_curve(
    equity_curve: pd.Series,
    benchmark: pd.Series | None = None,
    output_path: str | Path | None = None,
) -> None:
    """Plot equity curve with optional benchmark.
    
    Args:
        equity_curve: Series of portfolio values indexed by date
        benchmark: Optional benchmark series
        output_path: Path to save plot (if None, display interactively)
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={"height_ratios": [3, 1]})

    # Normalize to start at 1
    equity_normalized = equity_curve / equity_curve.iloc[0]

    # Plot equity curve
    ax1 = axes[0]
    ax1.plot(equity_normalized.index, equity_normalized.values, label="Strategy", linewidth=2)
    if benchmark is not None:
        benchmark_normalized = benchmark / benchmark.iloc[0]
        ax1.plot(benchmark_normalized.index, benchmark_normalized.values, label="Benchmark", linewidth=1, alpha=0.7)
    ax1.set_title("Equity Curve")
    ax1.set_ylabel("Normalized Value")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot drawdown
    ax2 = axes[1]
    rolling_max = equity_normalized.expanding().max()
    drawdown = (equity_normalized - rolling_max) / rolling_max * 100
    ax2.fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color="red")
    ax2.set_title("Drawdown")
    ax2.set_ylabel("Drawdown (%)")
    ax2.set_xlabel("Date")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        logger.info("Plot saved to %s", output_path)
    else:
        plt.show()

    plt.close()
