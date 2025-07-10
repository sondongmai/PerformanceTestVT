import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "http://127.0.0.1:5000/user"
NUM_REQUESTS = 300000
MAX_WORKERS = 10000  # số luồng tối đa tùy CPU/RAM

# Gửi 1 request POST với tên giả định
def send_post_request(i):
    try:
        start = time.perf_counter()
        response = requests.post(API_URL, json={"name": f"User{i}"}, timeout=5)
        elapsed = (time.perf_counter() - start) * 1000  # convert to milliseconds
        return response.status_code, elapsed
    except Exception:
        return "ERROR", 9999

def main():
    print(f"🔥 Sending {NUM_REQUESTS} requests with {MAX_WORKERS} workers...")

    start_time = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(send_post_request, i) for i in range(NUM_REQUESTS)]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    total_time = time.time() - start_time

    # Phân tích kết quả
    success_count = sum(1 for status, _ in results if status == 201)
    lt_50ms_count = sum(1 for _, elapsed in results if elapsed < 50)
    total = len(results)

    success_pct = (success_count / total) * 100
    lt_50ms_pct = (lt_50ms_count / total) * 100

    print("\n==== 📊 Load Test Report ====")
    print(f"Total Requests             : {total}")
    print(f"Successful (201)           : {success_count} ({success_pct:.2f}%)")
    print(f"< 50ms Response            : {lt_50ms_count} ({lt_50ms_pct:.2f}%)")
    print(f"Total Time Taken           : {total_time:.2f} s")
    print("===================================")

    # Điều kiện đánh giá
    print("\n==== ✅ Test Result Summary ====")
    if success_pct >= 99 and lt_50ms_pct >= 90:
        print("✅ PASS: Success >= 99% and <50ms >= 90%")
    else:
        if success_pct < 99:
            print(f"❌ FAIL: Only {success_pct:.2f}% requests successful (< 99%)")
        if lt_50ms_pct < 90:
            print(f"❌ FAIL: Only {lt_50ms_pct:.2f}% requests < 50ms (< 90%)")
    print("===================================")

if __name__ == "__main__":
    main()