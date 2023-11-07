import os
import sys
utils_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(utils_dir)

from GlobalHandler import GlobalHandler

__all__ = ['GlobalHandler']
