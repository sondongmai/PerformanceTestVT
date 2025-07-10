# main.py

import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import API_CONFIGS
from payload_generator import PAYLOAD_FUNCTIONS

def send_request(i, url, method, payload_func_key=None):
    try:
        start = time.perf_counter()
        payload = None

        if payload_func_key and payload_func_key in PAYLOAD_FUNCTIONS:
            payload = PAYLOAD_FUNCTIONS[payload_func_key](i)

        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=payload, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, json=payload, timeout=5)
        else:
            return i, "UNSUPPORTED_METHOD", 9999

        elapsed = (time.perf_counter() - start) * 1000
        return i, response.status_code, elapsed

    except Exception as e:
        return i, f"EXCEPTION: {type(e).__name__}", 9999

def run_load_test(api_config):
    print(f"\n🔥 Testing API: {api_config['name']}")
    print(f"→ URL: {api_config['url']} [{api_config['method']}]")
    print(f"→ Sending {api_config['num_requests']} requests with {api_config['max_workers']} workers...")

    results = []
    start_time = time.time()
    error_logs = []

    os.makedirs("logs", exist_ok=True)
    error_log_file = f"logs/{api_config['name'].replace(' ', '_').lower()}_errors.log"

    with ThreadPoolExecutor(max_workers=api_config['max_workers']) as executor:
        futures = [
            executor.submit(
                send_request,
                i,
                api_config['url'],
                api_config['method'],
                api_config.get('payload_func')
            )
            for i in range(api_config['num_requests'])
        ]

        for future in as_completed(futures):
            i, status, elapsed = future.result()
            results.append((i, status, elapsed))

            if status not in [200, 201]:
                error_logs.append(f"[#{i}] Status: {status}, Time: {elapsed:.2f}ms")

    # Ghi lỗi vào file
    if error_logs:
        with open(error_log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(error_logs))
        print(f"❗ Logged {len(error_logs)} errors to {error_log_file}")

    # Phân tích
    total_time = time.time() - start_time
    total = len(results)
    success_count = sum(1 for _, status, _ in results if status in [200, 201])
    lt_50ms_count = sum(1 for _, _, elapsed in results if elapsed < 50)

    print("\n==== 📊 Load Test Report ====")
    print(f"Total Requests             : {total}")
    print(f"Successful (200/201)       : {success_count} ({(success_count/total)*100:.2f}%)")
    print(f"< 50ms Response            : {lt_50ms_count} ({(lt_50ms_count/total)*100:.2f}%)")
    print(f"Total Time Taken           : {total_time:.2f} s")
    print("===================================")

def main():
    for config in API_CONFIGS:
        run_load_test(config)

if __name__ == "__main__":
    main()