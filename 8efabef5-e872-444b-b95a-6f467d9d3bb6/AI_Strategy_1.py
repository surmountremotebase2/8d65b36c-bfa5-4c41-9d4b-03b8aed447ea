from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker of interest
        self.ticker = "PHO"
    
    @property
    def assets(self):
        # Define which assets are relevant for this strategy
        return [self.ticker]

    @property
    def interval(self):
        # Define the interval to use for data fetching
        return "1day"
    
    def run(self, data):
        # Get the OHLCV data for the ticker
        pho_data = data["ohlcv"]
        
        # Pre-check to ensure we have enough data points
        if len(pho_data) < 20:
            log(f"Not enough data to calculate SMA for {self.ticker}")
            return TargetAllocation({})
        
        # Calculate the 20-day SMA
        sma_20 = SMA(self.ticker, pho_data, 20)
        if not sma_20:
            log(f"SMA calculation failed for {self.ticker}")
            return TargetAllocation({})
        
        # Calculate the percentage drop in SMA; considering the last two SMA values
        sma_drop_pct = ((sma_20[-1] - sma_20[-2]) / sma_20[-2]) * 100
        
        # Check the condition for buying $PHO
        if sma_drop_pct < -5:
            log(f"SMA dropped by more than 5% for {self.ticker}. Initiating buy.")
            # Buying signal, with an allocation adjusted for the desired capital increase per buy signal
            # The allocation value is symbolic; actual capital allocation happens outside this logic.
            allocation_value = 1  # This is a proxy to signal buy; external mechanisms should handle the actual increment of 10k
        else:
            log(f"No significant drop in SMA for {self.ticker}.")
            allocation_value = 0

        return TargetAllocation({self.ticker: allocation_value})