import os
from datetime import datetime


class Artifact:

    def __init__(self):

        root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.screenshot_dir = os.path.join(
            root,
            "artifacts",
            "screenshots"
        )

        self.log_dir = os.path.join(
            root,
            "artifacts",
            "logs"
        )

        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

    def capture_failure(self, testcase, error):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        screenshot = os.path.join(
            self.screenshot_dir,
            f"{testcase}_{timestamp}.png"
        )

        logfile = os.path.join(
            self.log_dir,
            f"{testcase}_{timestamp}.txt"
        )

        with open(screenshot, "w") as f:
            f.write("Dummy Screenshot")

        with open(logfile, "w") as f:
            f.write(error)

        return screenshot, logfile
