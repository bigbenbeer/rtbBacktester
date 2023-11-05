"""
This section is used to import the Ticker baseclass from the parent directory

"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TickerBaseclass import Ticker

