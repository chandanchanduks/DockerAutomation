class Result:

    def __init__(self):

        self.total = 0
        self.passed = 0
        self.failed = 0

        self.details = []

    def pass_test(self, testcase):

        self.total += 1
        self.passed += 1

        self.details.append(
            f"PASS : {testcase}"
        )

    def fail_test(self, testcase, reason):

        self.total += 1
        self.failed += 1

        self.details.append(
            f"FAIL : {testcase}\n{reason}"
        )

    def summary(self):

        print("\n" + "=" * 70)

        print("TEST EXECUTION SUMMARY")

        print("=" * 70)

        print(f"Total  : {self.total}")
        print(f"Passed : {self.passed}")
        print(f"Failed : {self.failed}")

        print()

        for item in self.details:

            print(item)

            print("-" * 70)
