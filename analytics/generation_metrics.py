"""
Generation Metrics

Tracks ArchitectAI generation statistics.
"""

import time


class GenerationMetrics:

    def __init__(self):

        self.total_files = 0

        self.total_success = 0

        self.total_failed = 0

        self.total_time = 0

        self.start_time = None

    def start(self):

        self.start_time = time.perf_counter()

    def finish(
        self,
        success: bool = True,
    ):

        if self.start_time is None:
            return

        self.total_time += (
            time.perf_counter()
            - self.start_time
        )

        self.total_files += 1

        if success:

            self.total_success += 1

        else:

            self.total_failed += 1

        self.start_time = None

    @property
    def average_time(self):

        if self.total_files == 0:

            return 0

        return self.total_time / self.total_files

    def report(self):

        print()

        print("=" * 70)

        print("📊 ArchitectAI Generation Report")

        print("=" * 70)

        print(f"Files Generated : {self.total_files}")

        print(f"Successful      : {self.total_success}")

        print(f"Failed          : {self.total_failed}")

        print(f"Total Time      : {self.total_time:.2f} sec")

        print(f"Average/File    : {self.average_time:.2f} sec")

        print("=" * 70)