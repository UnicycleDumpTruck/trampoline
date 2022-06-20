#!/usr/bin/env python

import time
from jsession import Session
import automationhat

beam_was_broken = 0
beam_brake = 0
#session_count = 0
#session_start_time = 0
#session_end_time = 0
#session_elapsed time = 0
#session_last_jump_time = 0
#session_active = False
session = Session()

automationhat.enable_auto_lights(False)

if automationhat.is_automation_hat():
    automationhat.light.power.write(1)

while True:
    beam_brake = automationhat.input.one.read()
    if beam_brake:
        if beam_was_broken:
            continue
        beam_was_broken = 1
        session.add_jump()
        if not session.active:
            session.start()
        temperature = automationhat.analog.four.read()
        temperature = round(((((temperature -0.5) * 100) * 1.8) + 32), 1)
        print(f"Jump: {session.jump_count}, Temperature: {temperature}")
        
    else:
        beam_was_broken = 0
        if ((time.time() - session.time_of_last_jump) > 20):
            session.log_stop_clear()
    time.sleep(0.05)
