from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Initialize with the ticker we are interested in
        self.ticker = "PHO"
        # Set a flag to track if we've already purchased $PHO and are holding
        self.is_holding = False

    @property
    def assets(self):
        # List of assets this strategy will request data for
        return [self.ticker]

    @property
    def interval(self):
        # Data interval for SMA calculation and trading decisions
        return "1day"

    def run(self, data):
        # Retrieve the closing price history for $PHO
        closing_prices = [i[self.ticker]["close"] for i in data["ohlcv"]]
        # Calculate the 20-day SMA for $PHO
        sma_20 = SMA(self.ticker, data["ohlcv"], length=15)

        if len(closing_prices) < 20 or sma_20 is None:
            # Not enough data to make a decision
            return TargetAllocation({})

        latest_close = closing_prices[-1]
        sma_20_latest = sma_20[-1]

        # Calculate the drop percentage from the 20-day SMA
        drop_pct = ((sma_20_latest - latest_close) / sma_20_latest) * 100
        # drop_string = str(drop_pct)
        # log(f""+drop_string)

        # Check if $PHO has dropped more than 15% from its 20-day SMA
        if not self.is_holding and drop_pct < -5:
            # Purchase (or hold) a 100% allocation in $PHO
            self.is_holding = True
            self.purchase_price = latest_close
            log(f"Purchased at " + str(latest_close))
            return TargetAllocation({self.ticker: 1})
        
        # If we are holding $PHO, check if it has gained 20% from our purchase
        if self.is_holding:
            # Assume 'purchase_price' is tracked externally or through strategy state management
            purchase_price = self.purchase_price  # This line is illustrative; actual implementation may vary
            gain_pct = ((latest_close - purchase_price) / purchase_price) * 100

            # If $PHO has gained 20% or more, sell back to 0
            if gain_pct >= 20:
                self.is_holding = False
                return TargetAllocation({self.ticker: 0})

        # Default action if no conditions are met or if holding without hitting the target gain
        return TargetAllocation({})