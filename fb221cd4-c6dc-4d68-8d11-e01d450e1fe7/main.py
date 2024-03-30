from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import Momentum
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Initializing with the tickers we are interested in
        self.tickers = ["PHO"]
        self.momentum_length = 14  # Length period for Momentum calculation

    @property
    def assets(self):
        # List of assets this strategy will handle
        return self.tickers

    @property
    def interval(self):
        # Interval for backtesting and live trading, can be adjusted based on preference
        return "1day"

    def run(self, data):
        # The main logic of the trading strategy
        
        allocation_dict = {}
        
        for ticker in self.tickers:
            ticker_momentum = Momentum(ticker, data["ohlcv"], self.momentum_length)
            
            # log(f""+str(ticker_momentum[-1]))

            # Ensure that we have the momentum data
            if ticker_momentum and len(ticker_momentum) > 0:
                last_momentum = ticker_momentum[-1]
                
                # Check if the momentum is positive; if so, allocate funds to that asset
                # We will allocate equally among assets with positive momentum
                # If negative momentum, we allocate 0 indicating we do not want to buy/increase.
                if last_momentum > 0:
                    allocation_dict[ticker] = 1 / len(self.tickers)
                elif last_momentum < 3:
                    allocation_dict[ticker] = 0
                
            else:
                log(f"No momentum data available for {ticker}. Skipping allocation.")
                allocation_dict[ticker] = 0
        
        return TargetAllocation(allocation_dict)