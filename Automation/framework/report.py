import os
from datetime import datetime


class Report:

    def __init__(self):

        root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.report_dir = os.path.join(
            root,
            "reports"
        )

        os.makedirs(self.report_dir, exist_ok=True)

    def generate(self, result):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report = os.path.join(
            self.report_dir,
            f"report_{timestamp}.txt"
        )

        with open(report, "w") as f:

            f.write("=" * 60 + "\n")

            f.write("AUTOMATION REPORT\n")

            f.write("=" * 60 + "\n\n")

            f.write(f"Total  : {result.total}\n")
            f.write(f"Passed : {result.passed}\n")
            f.write(f"Failed : {result.failed}\n\n")

            f.write("=" * 60 + "\n")

            for item in result.details:

                f.write(item + "\n")

                f.write("-" * 60 + "\n")

        print(f"\nReport Generated : {report}")
