import logging
import sys

from app.database import SessionLocal, init_db
from app.strategy.double_low import run_double_low_strategy
from app.strategy.low_premium import run_low_premium_strategy
from app.strategy.params import DoubleLowParams, LowPremiumParams
from app.logging import setup_logging

logger = logging.getLogger(__name__)


def run_strategy(strategy_type: str = "double_low", top_n: int = 10):
    """Run specified strategy."""
    setup_logging()
    init_db()
    db = SessionLocal()

    try:
        logger.info("Running %s strategy (top %d)...", strategy_type, top_n)

        if strategy_type == "double_low":
            params = DoubleLowParams(top_n=top_n)
            df = run_double_low_strategy(db, params)
        elif strategy_type == "low_premium":
            params = LowPremiumParams(top_n=top_n)
            df = run_low_premium_strategy(db, params)
        else:
            logger.error("Unknown strategy type: %s", strategy_type)
            sys.exit(1)

        if df.empty:
            logger.warning("No bonds selected")
        else:
            print("\n=== Strategy Results ===")
            print(df.to_string(index=False))
            logger.info("Strategy completed: %d bonds selected", len(df))

    except Exception as e:
        logger.error("Strategy failed: %s", e)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run convertible bond strategy")
    parser.add_argument("--strategy", choices=["double_low", "low_premium"], default="double_low")
    parser.add_argument("--top-n", type=int, default=10)
    args = parser.parse_args()

    run_strategy(args.strategy, args.top_n)
