from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    This strategy focuses on a simple RSI and Bollinger Bands approach for trading a single instrument, "AAPL".
    The idea is to go long (buy) when the RSI is below 30 (indicating it's potentially oversold) and the close
    price is below the lower Bollinger Band, suggesting the price is low relative to recent volatility.
    We sell our position (i.e., have 0 allocation) when the RSI is above 70 (indicating potentially overbought conditions).
    """

    @property
    def assets(self):
        # Define which assets are involved in this strategy, here it's only "AAPL".
        return ["AAPL"]

    @property
    def interval(self):
        # Define the data interval for the strategy. "1day" is used for daily frequency analysis.
        return "1day"

    def run(self, data):
        """
        This method contains the core logic of the strategy to be executed at each interval.
        """
        # Initialize the default allocation to be 0 for AAPL. It means no position by default.
        aapl_stake = 0

        # Calculate RSI with a 14-day period for AAPL
        rsi_values = RSI("AAPL", data["ohlcv"], 14)
        
        # Calculate Bollinger Bands with a 20-day period and 2 standard deviations for AAPL
        aapl_bbands = BB("AAPL", data["ohlcv"], 20, 2)

        if len(data["ohlcv"]) >= 20:  # Ensure there's enough data for Bollinger Bands calculation
            current_price = data["ohlcv"][-1]["AAPL"]['close']  # Get the latest close price for AAPL

            # Buying Condition: RSI < 30 (oversold) and current price is below the lower Bollinger Band
            if rsi_values[-1] < 30 and current_price < aapl_bbands['lower'][-1]:
                log("Buying signal - RSI below 30 and price below lower BB")
                aapl_stake = 1  # Full allocation to AAPL

            # Selling Condition: RSI > 70 (overbought), indicating a good time to sell or avoid buying
            elif rsi_values[-1] > 70:
                log("Selling signal - RSI above 70")
                aapl_stake = 0  # 0 allocation to AAPL

        # Return the defined allocation for AAPL. If none of the conditions are met, it stays as initially defined (0).
        return TargetAllocation({"AAPL": aapl_stake})