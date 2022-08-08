"""Implement class for tracking jump sessions on a trampoline."""

from time import time
import requests
import json
import os

import telemetry
from loguru import logger

class Session:
    """Class for tracking jump sessions"""

    def __init__(self):
        self.starting_time = 0
#        self.ending_time = 0
        self.jump_count = 0
        self.time_of_last_jump = 0
        self.active = False

    def start(self):
        self.starting_time = time()
#        self.ending_time = 0
        self.jump_count = 0
        self.time_since_last_jump = 0
        self.active = True

    def add_jump(self):
        self.jump_count += 1
        self.time_of_last_jump = time()

    def log_stop_clear(self):
     #       self.ending_time = time()
        try:
            temp = os.popen("vcgencmd measure_temp").readline().replace(
                "temp=", "").replace("'C", "")
            log_string = f"e={round(self.time_of_last_jump-self.starting_time)}, j={self.jump_count}, t={temp}\n"
            telemetry.send_log_message(log_string)
        except:
            print("Error sending log packet from jsession.py")
            logger.warning("Error sending Splunk message from jsession.py")

        self.starting_time = 0
#        self.ending_time = 0
        self.jump_count = 0
        self.time_of_last_jump = 0
        self.active = False

#    def stats();
 #       return {'starting_time':self.starting_time, 'ending_time':self.ending_time, 'elapsed_time':(self.ending_time - self.starting_time), 'jump_count':self.jump_count, }
