import time

from tests.prod import test_performance


def test_stability(image_paths):
    start_time = time.time()
    for path in image_paths:
        try:
            test_performance(path)
        except Exception as e:
            print(f"[ERROR] Stability test failed for {path}: {e}")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time for stability test: {total_time:.2f} seconds")

# Список зображень для тесту
image_queue = [f"image_{i}.jpg" for i in range(1, 101)]
test_stability(image_queue)
