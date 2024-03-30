from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the stock ticker you're interested in
        self.ticker = "PHO"

    @property
    def assets(self):
        # Return a list with the stock ticker
        return [self.ticker]

    @property
    def interval(self):
        # Define the interval at which the strategy should run, "1day" for daily.
        return "1day"

    def run(self, data):
        # Use the SMA function provided by Surmount to calculate the Simple Moving Average
        # The 'length' parameter determines the period over which the average is computed. Adjust it as needed.
        sma_length = 20  # Example: 20-day simple moving average
        sma_values = SMA(self.ticker, data["ohlcv"], sma_length)

        # Check if the SMA values list is not empty
        if sma_values and len(sma_values) > 0:
            # Log the most recent SMA value
            log(f"The {sma_length}-day SMA of {self.ticker} is: {sma_values[-1]}")
        else:
            # Log a message indicating that the SMA couldn't be calculated
            log(f"Could not calculate the {sma_length}-day SMA for {self.ticker}")

        # Since this strategy only logs the SMA value and doesn't actually trade,
        # We return an empty TargetAllocation object.
        return TargetAllocation({})