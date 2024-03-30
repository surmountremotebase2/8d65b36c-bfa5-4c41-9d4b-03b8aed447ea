from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "PHO"  # Ticker to be traded
    
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Initialize the stake in PHO as the existing allocation, if any
        current_allocation = data["holdings"].get(self.ticker, 0)

        # Calculating the 20-day SMA for PHO
        sma_current = SMA(self.ticker, data["ohlcv"], 20)[-1]
        sma_previous = SMA(self.ticker, data["ohlcv"], 20)[-20]

        log(f"SMA is " + str(sma_current))

        # Check if the current SMA has dropped more than 7% compared to the previous day
        if sma_current < sma_previous * 0.99:
            log("SMA dropped more than 5%, increasing PHO stake by 10%.")
            # Increase the stake in PHO by 10% more of the portfolio, constrained to not exceed 100%
            new_allocation = min(1, current_allocation + 0.1)
        else:
            # If the condition isn't met, maintain the current allocation
            new_allocation = current_allocation

        # Returning the new allocation as a TargetAllocation object
        return TargetAllocation({self.ticker: new_allocation})