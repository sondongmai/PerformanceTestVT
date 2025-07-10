import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


def send_post_request(i, api_url):
    try:
        start = time.perf_counter()
        response = requests.post(api_url, json={"name": f"User{i}"}, timeout=5)
        elapsed = (time.perf_counter() - start) * 1000
        return response.status_code, elapsed
    except Exception:
        return "ERROR", 9999


def run_test(api_url, num_requests, max_workers, output_text):
    output_text.insert(tk.END, f"🔥 Sending {num_requests} requests with {max_workers} workers...\n")

    start_time = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_post_request, i, api_url) for i in range(num_requests)]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    total_time = time.time() - start_time

    success_count = sum(1 for status, _ in results if status == 201)
    lt_50ms_count = sum(1 for _, elapsed in results if elapsed < 50)
    total = len(results)

    success_pct = (success_count / total) * 100
    lt_50ms_pct = (lt_50ms_count / total) * 100

    output_text.insert(tk.END, "\n==== 📊 Load Test Report ====\n")
    output_text.insert(tk.END, f"Total Requests             : {total}\n")
    output_text.insert(tk.END, f"Successful (201)           : {success_count} ({success_pct:.2f}%)\n")
    output_text.insert(tk.END, f"< 50ms Response            : {lt_50ms_count} ({lt_50ms_pct:.2f}%)\n")
    output_text.insert(tk.END, f"Total Time Taken           : {total_time:.2f} s\n")
    output_text.insert(tk.END, "===================================\n")

    output_text.insert(tk.END, "\n==== ✅ Test Result Summary ====\n")
    if success_pct >= 99 and lt_50ms_pct >= 90:
        output_text.insert(tk.END, "✅ PASS: Success >= 99% and <50ms >= 90%\n")
    else:
        if success_pct < 99:
            output_text.insert(tk.END, f"❌ FAIL: Only {success_pct:.2f}% requests successful (< 99%)\n")
        if lt_50ms_pct < 90:
            output_text.insert(tk.END, f"❌ FAIL: Only {lt_50ms_pct:.2f}% requests < 50ms (< 90%)\n")
    output_text.insert(tk.END, "===================================\n\n")


def start_test(api_entry, num_req_entry, workers_entry, output_text):
    try:
        api_url = api_entry.get().strip()
        num_requests = int(num_req_entry.get())
        max_workers = int(workers_entry.get())

        if not api_url:
            raise ValueError("API URL cannot be empty.")

        output_text.delete(1.0, tk.END)
        threading.Thread(target=run_test, args=(api_url, num_requests, max_workers, output_text), daemon=True).start()

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


def create_gui():
    root = tk.Tk()
    root.title("🔥 Python Load Test Tool")
    root.geometry("700x500")

    # Inputs
    tk.Label(root, text="API URL:").pack()
    api_entry = tk.Entry(root, width=80)
    api_entry.insert(0, "http://127.0.0.1:5000/user")
    api_entry.pack(pady=5)

    tk.Label(root, text="Number of Requests:").pack()
    num_req_entry = tk.Entry(root)
    num_req_entry.insert(0, "1000")
    num_req_entry.pack(pady=5)

    tk.Label(root, text="Number of Workers (Threads):").pack()
    workers_entry = tk.Entry(root)
    workers_entry.insert(0, "100")
    workers_entry.pack(pady=5)

    # Button
    tk.Button(root, text="🚀 Start Load Test", command=lambda: start_test(api_entry, num_req_entry, workers_entry, output_text)).pack(pady=10)

    # Output log
    output_text = tk.Text(root, height=20, width=80, wrap="word")
    output_text.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()