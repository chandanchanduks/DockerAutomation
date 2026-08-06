from framework.basetest import BaseTest


class WifiTest(BaseTest):

    def setup(self):

        super().setup()

        print("Open Settings")

        print("Navigate to WiFi")

    def test_enable_wifi(self, device):

        print("Checking WiFi Status")

        assert device["wifi"] == "Connected"

        print("WiFi Connected")

    def test_disable_wifi(self, device):

        assert device["wifi"] == "Disconnected"

    def test_connect_wifi(self, device):

        print("Connect WiFi")

    def teardown(self):

        print("Back to Home Screen")

        super().teardown()
