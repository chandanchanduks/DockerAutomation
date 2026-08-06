from framework.basetest import BaseTest


class CameraTest(BaseTest):

    def setup(self):

        super().setup()

        print("Launching Camera Application")

    def execute(self, device):

        print("Taking Picture")
