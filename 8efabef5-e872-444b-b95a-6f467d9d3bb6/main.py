from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming the strategy is focused on $PHO
        self.ticker = "PHO"

    @property
    def assets(self):
        # Define which assets this strategy is targeting
        return [self.ticker]

    @property
    def interval(self):
        # Define the data interval required for the strategy
        return "1day"

    def run(self, data):
        # Extract closing prices for $PHO
        closes = [i[self.ticker]["close"] for i in data["ohlcv"]]
        
        # Calculate the current and previous SMAs
        current_sma = SMA(self.ticker, data["ohlcv"], 50)[-1]  # Current 50-day SMA
        prev_sma = SMA(self.ticker, data["ohlcv"][:-1], 50)[-1]  # Previous 50-day SMA to compare
        
        # Determine if the SMA has dropped by 5% or more
        if prev_sma > current_sma and ((prev_sma - current_sma) / prev_sma) >= 0.05:
            log(f"SMA dropped by 5% or more. Current SMA: {current_sma}, Previous SMA: {prev_sma}")
            # Here would be the logic to buy $10,000 of $PHO
            # Since we can't specify dollar amounts directly in allocations, this part is abstract.
            # For illustration, we will set allocation to a nominal value indicating a buy signal.
            allocation_dict = {self.ticker: 1}  # This 1 is arbitrary and should be replaced
                                                # with logic to calculate the fraction of the
                                                # portfolio to invest $10,000 in $PHO.
        else:
            # No action is taken if the condition is not met
            allocation_dict = {self.ticker: 0}
        
        return TargetAllocation(allocation_dict)