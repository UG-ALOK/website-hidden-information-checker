
#!/usr/bin/env python3
# FIREWALL CRACKER | VOID KERNEL 12 FINAL EDITION

import os
import sys
import json
import time
import socket
import shutil
import threading
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime

# ==================== COLOR SYSTEM ====================

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[38;5;196m"
GOLD = "\033[38;5;220m"
WHITE = "\033[38;5;255m"
GREEN = "\033[38;5;82m"
CYAN = "\033[38;5;51m"
GRAY = "\033[38;5;245m"
MAGENTA = "\033[38;5;207m"
BLUE = "\033[38;5;39m"

APP_DIR = Path.home() / ".firewall_cracker"
CONFIG_DIR = APP_DIR / "config"
REPORT_DIR = APP_DIR / "reports"
PATHS_FILE = CONFIG_DIR / "paths.txt"

TIMEOUT = 4
MAX_PATHS = 100
MAX_HTTP_REQUESTS = 100
REQUEST_DELAY = 0.5

COMMON_PORTS = [
    21, 22, 25, 53, 80, 110, 143, 443, 445, 465,
    587, 993, 995, 1433, 3306, 3389, 5432, 5900,
    8080, 8443
]


# ==================== GENERAL UTILITIES ====================

def setup():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if not PATHS_FILE.exists():
        PATHS_FILE.write_text(
            "# CUSTOM PATHS: ONE PATH PER LINE\n"
            "# EXAMPLE: /admin\n"
            "# EXAMPLE: /dashboard\n",
            encoding="utf-8"
        )


def clear():
    os.system("clear")


def banner():
    clear()
    print(f"{RED}{BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║           Website Hidden Information Checker            ║")
    print("║         VOID KERNEL           ║")
    print("╚════════════════════════════════════════╝")
    print(f"{GOLD}       ★ DEVELOPED BY Ug-alok ★{RESET}")
    print(f"{CYAN}          PYTHON 3 | TERMUX EDITION{RESET}\n")


def divider():
    print(f"{GOLD}{'━' * 44}{RESET}")


def pause():
    input(f"\n{GOLD}PRESS ENTER TO CONTINUE...{RESET}")


def ask_url():
    while True:
        raw = input(f"{GOLD}TARGET URL: {WHITE}").strip()

        if not raw:
            print(f"{RED}ERROR: URL CANNOT BE EMPTY.{RESET}")
            continue

        if "://" not in raw:
            raw = "https://" + raw

        try:
            parsed = urllib.parse.urlsplit(raw)

            if (
                parsed.scheme not in ("http", "https")
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
            ):
                raise ValueError

            return raw.rstrip("/")

        except ValueError:
            print(f"{RED}ERROR: ENTER A VALID HTTP/HTTPS URL.{RESET}")


def host_label(url):
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname or "UNKNOWN"

    if parsed.port:
        host += f":{parsed.port}"

    return host


# ==================== ANIMATED SPINNER ====================

def spinner(stop_event, message="PROCESSING"):
    frames = ["✦", "✧", "★", "✧", "✦", "✧"]
    index = 0

    while not stop_event.is_set():
        frame = frames[index % len(frames)]

        sys.stdout.write(
            f"\r{GOLD}{BOLD}{frame} {MAGENTA}{message}{RESET}"
        )
        sys.stdout.flush()

        index += 1
        stop_event.wait(0.12)

    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


# ==================== HIDDEN REPORT STORAGE ====================

def save_report(name, data):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = REPORT_DIR / f"{name}_{stamp}"

    payload = {
        "application": "FIREWALL CRACKER",
        "edition": "VOID KERNEL 12",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        **data
    }

    (base.with_suffix(".json")).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    text_content = (
        "FIREWALL CRACKER - VOID KERNEL 12\n"
        f"REPORT: {name}\n"
        f"CREATED: {payload['created_at']}\n"
        + "=" * 44 + "\n"
        + json.dumps(payload, indent=2, ensure_ascii=False)
        + "\n"
    )

    (base.with_suffix(".txt")).write_text(
        text_content,
        encoding="utf-8"
    )

    # Hide filesystem paths from normal terminal output.
    print(f"{GREEN}{BOLD}✓ REPORT SAVED SUCCESSFULLY.{RESET}")


# ==================== HTTP REQUEST ====================

def request_once(url):
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": "VoidKernel12-Authorized-Test/1.0"
        }
    )

    started = time.perf_counter()

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            return {
                "status": response.status,
                "seconds": round(time.perf_counter() - started, 3),
                "result": "HTTP RESPONSE"
            }

    except urllib.error.HTTPError as exc:
        return {
            "status": exc.code,
            "seconds": round(time.perf_counter() - started, 3),
            "result": "HTTP ERROR RESPONSE"
        }

    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError):
        return {
            "status": None,
            "seconds": round(time.perf_counter() - started, 3),
            "result": "NO RESPONSE / CONNECTION ERROR"
        }


# ==================== ADMIN PANEL FINDER ====================

def edit_custom_paths():
    setup()

    if not shutil.which("nano"):
        print(f"{RED}NANO NOT INSTALLED. RUN: pkg install nano{RESET}")
        return False

    # Launch nano without printing the full configuration path.
    subprocess_result = os.spawnlp(
        os.P_WAIT, "nano", "nano", str(PATHS_FILE)
    )

    return subprocess_result == 0


def read_custom_paths():
    if not edit_custom_paths():
        return []

    paths = []

    try:
        for raw in PATHS_FILE.read_text(encoding="utf-8").splitlines():
            path = raw.strip()

            if not path or path.startswith("#"):
                continue

            if not path.startswith("/"):
                path = "/" + path

            if "://" in path or any(ch.isspace() for ch in path):
                continue

            if path not in paths:
                paths.append(path)

            if len(paths) >= MAX_PATHS:
                break

    except OSError:
        print(f"{RED}COULD NOT READ CUSTOM PATHS.{RESET}")

    return paths


def admin_panel_finder():
    banner()
    print(f"{GOLD}{BOLD}OPTION 1 - ADMIN PANEL FINDER{RESET}")
    divider()

    print(
        f"{GRAY}ONLY TEST WEBSITES YOU OWN OR ARE AUTHORIZED TO TEST.{RESET}\n"
    )

    target = ask_url()
    paths = read_custom_paths()

    if not paths:
        print(f"{RED}NO CUSTOM PATHS AVAILABLE.{RESET}")
        pause()
        return

    print(f"\n{CYAN}TARGET HOST: {host_label(target)}{RESET}")
    print(f"{CYAN}PATHS TO CHECK: {len(paths)}{RESET}\n")

    results = []

    for number, path in enumerate(paths, 1):
        stop_event = threading.Event()
        worker = threading.Thread(
            target=spinner,
            args=(stop_event, f"CHECKING PATH {number}/{len(paths)}"),
            daemon=True
        )
        worker.start()

        result = request_once(target + path)

        stop_event.set()
        worker.join(timeout=1)

        status = result["status"]

        if status in (401, 403):
            label = "ACCESS DENIED"
        elif status is not None:
            label = "RESPONSE - VERIFY MANUALLY"
        else:
            label = "NO RESPONSE"

        results.append({
            "path": path,
            "status": status,
            "seconds": result["seconds"],
            "result": label
        })

        status_text = str(status) if status is not None else "N/A"
        color = GREEN if status in (200, 301, 302) else GOLD

        print(
            f"{GOLD}[{number}/{len(paths)}]{RESET} "
            f"{WHITE}{path}{RESET} | "
            f"{color}{status_text}{RESET} | "
            f"{result['seconds']}s | "
            f"{MAGENTA}{label}{RESET}"
        )

    save_report("admin_panel_finder", {
        "target_host": host_label(target),
        "paths_checked": len(paths),
        "results": results
    })

    pause()


# ==================== SIDE-BY-SIDE REQUEST MENU ====================

def show_request_menu():
    print(f"\n{GOLD}{BOLD}REQUEST BATCH MENU - 1 TO 100{RESET}")
    divider()

    columns = 4
    cell_width = 25

    for start in range(1, 101, columns):
        cells = []

        for option in range(start, min(start + columns, 101)):
            planned = option * 20
            cell = (
                f"{GOLD}[{option}]{RESET} "
                f"{CYAN}{planned}{RESET} REQ"
            )
            cells.append(cell)

        print("    ".join(cells))

    divider()

    print(
        f"{GRAY}PLANNED BATCH = OPTION NUMBER x 20{RESET}"
    )
    print(
        f"{RED}ACTUAL HTTP TEST LIMIT = "
        f"{MAX_HTTP_REQUESTS} REQUESTS{RESET}"
    )


# ==================== HTTP REQUEST TESTER ====================

def http_request_tester():
    banner()
    print(f"{GOLD}{BOLD}OPTION 2 - HTTP REQUEST TESTER{RESET}")
    divider()

    print(
        f"{RED}WARNING: HIGH REQUEST VOLUMES MAY FAIL "
        f"OR OVERLOAD A SERVER.{RESET}"
    )
    print(
        f"{GRAY}USE ONLY SYSTEMS YOU OWN OR ARE AUTHORIZED TO TEST.{RESET}\n"
    )

    target = ask_url()
    show_request_menu()

    while True:
        try:
            selected = int(
                input(f"\n{GOLD}SELECT OPTION (1-100): {WHITE}").strip()
            )

            if 1 <= selected <= 100:
                break

        except ValueError:
            pass

        print(f"{RED}INVALID NUMBER. ENTER 1-100.{RESET}")

    planned = selected * 20
    actual = min(planned, MAX_HTTP_REQUESTS)

    print(f"\n{GOLD}SELECTED OPTION: {selected}{RESET}")
    print(f"{CYAN}PLANNED BATCH SIZE: {planned} REQUESTS{RESET}")
    print(f"{WHITE}ACTUAL TEST SIZE: {actual} REQUESTS{RESET}")

    if planned > MAX_HTTP_REQUESTS:
        print(
            f"{RED}SAFETY LIMIT APPLIED: "
            f"ONLY {MAX_HTTP_REQUESTS} REQUESTS WILL RUN.{RESET}"
        )

    results = []
    stop_event = threading.Event()
    worker = threading.Thread(
        target=spinner,
        args=(stop_event, "STARTING HTTP TEST"),
        daemon=True
    )
    worker.start()

    try:
        for number in range(1, actual + 1):
            result = request_once(target)
            result["request_number"] = number
            results.append(result)

            stop_event.set()
            worker.join(timeout=1)

            status = (
                str(result["status"])
                if result["status"] is not None else "NO RESPONSE"
            )

            color = GREEN if result["status"] is not None else RED

            print(
                f"{GOLD}[{number}/{actual}]{RESET} "
                f"{color}STATUS: {status}{RESET} | "
                f"{WHITE}TIME: {result['seconds']}s{RESET}"
            )

            if number < actual:
                time.sleep(REQUEST_DELAY)

            stop_event = threading.Event()
            worker = threading.Thread(
                target=spinner,
                args=(stop_event, "HTTP TEST RUNNING"),
                daemon=True
            )
            worker.start()

    finally:
        stop_event.set()
        worker.join(timeout=1)

    received = sum(
        1 for item in results if item["status"] is not None
    )
    failed = len(results) - received

    print(f"\n{GOLD}{BOLD}TEST SUMMARY{RESET}")
    divider()
    print(f"{WHITE}SELECTED OPTION: {selected}{RESET}")
    print(f"{CYAN}PLANNED REQUESTS: {planned}{RESET}")
    print(f"{WHITE}ATTEMPTED REQUESTS: {len(results)}{RESET}")
    print(f"{GREEN}HTTP RESPONSES: {received}{RESET}")
    print(f"{RED}NO RESPONSE / ERRORS: {failed}{RESET}")

    save_report("http_request_tester", {
        "target_host": host_label(target),
        "selected_option": selected,
        "planned_batch_size": planned,
        "actual_request_limit": actual,
        "requests_attempted": len(results),
        "responses_received": received,
        "failed_or_no_response": failed,
        "delay_seconds": REQUEST_DELAY,
        "results": results
    })

    pause()


# ==================== TARGET PORT CHECKER ====================

def target_port_checker():
    banner()
    print(f"{GOLD}{BOLD}OPTION 3 - TARGET PORT CHECKER{RESET}")
    divider()

    print(f"{GRAY}AUTHORIZED HOSTS ONLY.{RESET}\n")

    target = ask_url()
    parsed = urllib.parse.urlsplit(target)
    host = parsed.hostname

    try:
        addresses = sorted({
            item[4][0]
            for item in socket.getaddrinfo(
                host, None, type=socket.SOCK_STREAM
            )
        })

    except socket.gaierror:
        print(f"{RED}DNS LOOKUP FAILED.{RESET}")
        pause()
        return

    ports = [parsed.port] if parsed.port else COMMON_PORTS
    results = []

    print(f"{CYAN}HOST: {host_label(target)}{RESET}")
    print(f"{CYAN}ADDRESSES: {', '.join(addresses)}{RESET}\n")

    for number, port in enumerate(ports, 1):
        status = "CLOSED OR FILTERED"
        elapsed = 0.0

        stop_event = threading.Event()
        worker = threading.Thread(
            target=spinner,
            args=(stop_event, f"CHECKING PORT {port}"),
            daemon=True
        )
        worker.start()

        try:
            started = time.perf_counter()

            with socket.create_connection(
                (host, port), timeout=1.5
            ):
                elapsed = round(time.perf_counter() - started, 3)
                status = "OPEN"

        except OSError:
            pass

        finally:
            stop_event.set()
            worker.join(timeout=1)

        results.append({
            "port": port,
            "status": status,
            "seconds": elapsed
        })

        color = GREEN if status == "OPEN" else GRAY

        print(
            f"{GOLD}[{number}/{len(ports)}]{RESET} "
            f"PORT {port} | {color}{status}{RESET}"
        )

    save_report("target_port_checker", {
        "target_host": host_label(target),
        "resolved_addresses": addresses,
        "results": results
    })

    pause()


# ==================== REPORT VIEWER ====================

def view_reports():
    banner()
    print(f"{GOLD}{BOLD}SAVED REPORTS{RESET}")
    divider()

    files = sorted(
        REPORT_DIR.glob("*"),
        key=lambda item: item.stat().st_mtime,
        reverse=True
    )

    if not files:
        print(f"{GRAY}NO REPORTS FOUND.{RESET}")
    else:
        for item in files:
            print(f"{WHITE}{item.name}{RESET}")

    print(f"\n{GREEN}REPORTS STORED IN HIDDEN TERMUX STORAGE.{RESET}")
    pause()


# ==================== MAIN MENU ====================

def main():
    setup()

    while True:
        banner()

        print(f"{GOLD}{BOLD}MAIN MENU{RESET}")
        divider()

        print(f"{GOLD}[1] {WHITE}WEB ADMIN PANEL FINDER")
        print(f"{GOLD}[2] {WHITE}FACK REQUES")
        print(f"{GOLD}[3] {WHITE}TARGET PORT CHECKER")
        print(f"{GOLD}[4] {WHITE}VIEW SAVED REPORTS")
        print(f"{RED}[0] {WHITE}EXIT")

        divider()

        choice = input(f"{GOLD}SELECT OPTION: {WHITE}").strip()

        try:
            if choice == "1":
                admin_panel_finder()

            elif choice == "2":
                http_request_tester()

            elif choice == "3":
                target_port_checker()

            elif choice == "4":
                view_reports()

            elif choice == "0":
                print(f"{GOLD}EXITING FIREWALL CRACKER...{RESET}")
                break

            else:
                print(f"{RED}INVALID OPTION.{RESET}")
                time.sleep(0.8)

        except KeyboardInterrupt:
            print(f"\n{RED}OPERATION CANCELLED.{RESET}")
            time.sleep(0.8)

        except Exception as exc:
            print(
                f"\n{RED}ERROR: {type(exc).__name__}: {exc}{RESET}"
            )
            pause()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(f"\n{GOLD}EXITED.{RESET}")
