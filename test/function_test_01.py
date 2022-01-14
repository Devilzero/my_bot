import os
import sys

sys.path.append(os.path.realpath(__file__ + "/../.."))

from utils.mirai_api import mirai
import unittest

class FunctionTesting(unittest.TestCase):
    def test_send_message(self):
        mirai.send_group_message("374664776", "Test")
        mirai.send_temp_message("374664776", "747761541", "Test")
