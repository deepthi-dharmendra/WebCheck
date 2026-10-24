
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

import csv
import os
from datetime import datetime

def normalize_url(url):
    """Add HTTPS if the user does not provide a scheme."""
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.hostname:
        raise ValueError("Please enter a valid website URL.")

    return url


def check_website(url, timeout=5):
    """Check website reachability, HTTP status, and response time."""
    url = normalize_url(url)
    start = time.perf_counter()

    try:
        request = urllib.request.Request(
            url,
            method="GET",
            headers={"User-Agent": "WebCheck/1.0"},
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            status_code = response.status
            elapsed_ms = (time.perf_counter() - start) * 1000

            return {
                "url": url,
                "status_code": status_code,
                "response_time_ms": round(elapsed_ms, 2),
                "reachable": True,
                "available": 200 <= status_code < 400,
                "error": "",
            }

    except urllib.error.HTTPError as error:
        # The server responded, even though the HTTP status is an error.
        elapsed_ms = (time.perf_counter() - start) * 1000

        return {
            "url": url,
            "status_code": error.code,
            "response_time_ms": round(elapsed_ms, 2),
            "reachable": True,
            "available": False,
            "error": f"HTTP error: {error.code}",
        }

    except (urllib.error.URLError, TimeoutError, OSError) as error:
        elapsed_ms = (time.perf_counter() - start) * 1000
        reason = getattr(error, "reason", error)

        return {
            "url": url,
            "status_code": None,
            "response_time_ms": round(elapsed_ms, 2),
            "reachable": False,
            "available": False,
            "error": str(reason),
        }


def save_report(results):
    """Append monitoring results to a CSV report."""
    filename = "webcheck_report.csv"
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0

    fields = [
        "timestamp",
        "url",
        "status_code",
        "response_time_ms",
        "reachable",
        "available",
        "error",
    ]

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        for result in results:
            row = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                **result,
            }
            writer.writerow({key: row.get(key, "") for key in fields})

    print(f"\nReport saved to: {os.path.abspath(filename)}")

def main():
    url = input("Enter a website URL: ").strip()

    try:
        url = normalize_url(url)
        attempts = int(input("How many checks? (1-20): "))

        if not 1 <= attempts <= 20:
            print("Please enter a number between 1 and 20.")
            return

    except ValueError as error:
        print(f"Input error: {error}")
        return

    results = []

    print(f"\nMonitoring {url} ({attempts} checks)\n")

    for attempt in range(1, attempts + 1):
        result = check_website(url)
        results.append(result)

        status = result["status_code"]
        response_time = result["response_time_ms"]

        print(
            f"Check {attempt}/{attempts} | "
            f"HTTP: {status if status is not None else 'No response'} | "
            f"Time: {response_time} ms | "
            f"Reachable: {result['reachable']} | "
            f"Available: {result['available']}"
        )

        if result["error"]:
            print(f"  Details: {result['error']}")

        if attempt < attempts:
            time.sleep(1)

    reachable_count = sum(r["reachable"] for r in results)
    available_count = sum(r["available"] for r in results)

    response_times = [
        r["response_time_ms"]
        for r in results
        if r["reachable"] and r["response_time_ms"] is not None
    ]

    average_time = (
        sum(response_times) / len(response_times)
        if response_times
        else None
    )

    print("\n--- Monitoring Summary ---")
    print(f"Total checks: {attempts}")
    print(f"Server responses received: {reachable_count}")
    print(f"Available responses (HTTP 2xx-3xx): {available_count}")
    print(f"Unavailable checks: {attempts - available_count}")

    if average_time is not None:
        print(f"Average response time: {average_time:.2f} ms")
    else:
        print("Average response time: No server responses received")
    
    save_report(results)

if __name__ == "__main__":
    main()
