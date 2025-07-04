import asyncio
import aiohttp
import time

API_URL = "http://127.0.0.1:5000/user"
NUM_REQUESTS = 300_000

async def send_post(session, i, stats):
    start = time.perf_counter()
    try:
        async with session.post(API_URL, json={"name": f"User{i}"}, timeout=5) as resp:
            elapsed = (time.perf_counter() - start) * 1000  # ms
            if resp.status == 201:
                stats["success"] += 1
            else:
                stats["fail"] += 1
            stats["times"].append(elapsed)
    except Exception:
        stats["fail"] += 1
        stats["times"].append(9999)

async def send_all_requests():
    stats = {"success": 0, "fail": 0, "times": []}
    connector = aiohttp.TCPConnector(limit=0)  # Không giới hạn kết nối đồng thời
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [send_post(session, i, stats) for i in range(NUM_REQUESTS)]
        await asyncio.gather(*tasks)

    return stats

def print_report(stats, total_time):
    total = stats["success"] + stats["fail"]
    lt_50ms = len([t for t in stats["times"] if t < 50])

    print("\n==== 📊 Load Test Report ====")
    print(f"Total Requests      : {total}")
    print(f"✅ Successful (201) : {stats['success']} ({(stats['success'] / total) * 100:.2f}%)")
    print(f"❌ Failed           : {stats['fail']} ({(stats['fail'] / total) * 100:.2f}%)")
    print(f"<50ms Response      : {lt_50ms} ({(lt_50ms / total) * 100:.2f}%)")
    print(f"Total Time Taken    : {total_time:.2f} s")
    print("📈 Throughput       : {rps:.2f} requests/second".format(rps=total / total_time))

    if (stats['success'] / total) >= 0.99 and (lt_50ms / total) >= 0.9:
        print("✅ PASS: Success >= 99% & <50ms >= 90%")
    else:
        print("❌ FAIL: Không đạt tiêu chí performance")

if __name__ == "__main__":
    print(f"🚀 Sending {NUM_REQUESTS} requests concurrently (all at once)...")

    start = time.time()
    stats = asyncio.run(send_all_requests())
    duration = time.time() - start

    print_report(stats, duration)