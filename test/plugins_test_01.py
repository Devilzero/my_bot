import os
import sys

sys.path.append(os.path.realpath(__file__ + "/../.."))

from utils.mirai_api import mirai
import unittest

class PluginsTesting(unittest.TestCase):
    def test_get_j3_info(self):
        from plugins.get_j3_info import mk_msg
        mk_msg


