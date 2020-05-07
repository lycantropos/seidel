import sys

from hypothesis.strategies import SearchStrategy

Strategy = SearchStrategy

MAX_FLOAT_DIGITS_COUNT = sys.float_info.dig // 2
MAX_VALUE = 10 ** 6
MIN_VALUE = -MAX_VALUE
