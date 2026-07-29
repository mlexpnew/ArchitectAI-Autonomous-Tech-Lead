import time

from analytics.generation_metrics import GenerationMetrics


metrics = GenerationMetrics()

metrics.start()

time.sleep(1)

metrics.finish()

metrics.start()

time.sleep(2)

metrics.finish()

metrics.report()