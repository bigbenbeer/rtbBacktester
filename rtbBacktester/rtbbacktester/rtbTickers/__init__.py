import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

import Tickers
from TickerBaseclass import Ticker, TickerClassification
from ForexLotSizes import ForexLotSizes