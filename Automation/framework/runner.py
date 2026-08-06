import os
import inspect
import importlib

from framework.result import Result
from framework.artifact import Artifact


class Runner:

    def __init__(self):

        self.result = Result()

        self.artifact = Artifact()

    def run(self, suite, device):

        suite = suite.lower()

        root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        folder = os.path.join(
            root,
            "tests",
            suite
        )

        print("\n" + "=" * 70)

        print(f"EXECUTING {suite.upper()} SUITE")

        print("=" * 70)

        for file in sorted(os.listdir(folder)):

            if not file.startswith("test_"):

                continue

            module = importlib.import_module(
                f"tests.{suite}.{file[:-3]}"
            )

            self.execute_module(module, device)

        self.result.summary()

        return self.result

    def execute_module(self, module, device):

        classes = inspect.getmembers(
            module,
            inspect.isclass
        )

        for _, cls in classes:

            self.execute_test_class(cls(), device)

    def execute_test_class(self, test, device):

        methods = inspect.getmembers(
            test,
            predicate=inspect.ismethod
        )

        for method_name, method in methods:

            if not method_name.startswith("test_"):

                continue

            testcase = f"{test.__class__.__name__}.{method_name}"

            print("\n" + "-" * 70)

            print(f"Running : {testcase}")

            print("-" * 70)

            try:

                test.setup()

                method(device)

                self.result.pass_test(testcase)

                print("STATUS : PASS")

            except Exception as e:

                screenshot, logfile = self.artifact.capture_failure(

                    testcase.replace(".", "_"),

                    str(e)

                )

                self.result.fail_test(

                    testcase,

                    f"{e}\nScreenshot : {screenshot}\nLog : {logfile}"

                )

                print("STATUS : FAIL")

            finally:

                test.teardown()
