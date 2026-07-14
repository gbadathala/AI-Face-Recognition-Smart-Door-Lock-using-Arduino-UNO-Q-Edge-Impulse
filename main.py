# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l.
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC

ui = WebUI()

detection_stream = VideoObjectDetection(
    confidence=0.8,
    debounce_sec=0.0
)

ui.on_message(
    "override_th",
    lambda sid, threshold: detection_stream.override_threshold(threshold)
)

busy = False

def send_detections_to_ui(detections):

    global busy

    if busy:
        return

    for key, values in detections.items():

        for value in values:

            confidence = value.get("confidence", 0)

            entry = {
                "content": key,
                "confidence": confidence,
                "timestamp": datetime.now(UTC).isoformat()
            }

            ui.send_message("detection", message=entry)

            print("--------------------------------")
            print("Label      :", repr(key))
            print("Confidence :", confidence)

            if key.strip().lower() == "ganesh" and confidence >= 0.9:

                print("GANESH DETECTED")

                busy = True

                Bridge.call("set_led_state", True)

                busy = False

                return


detection_stream.on_detect_all(send_detections_to_ui)

App.run()
