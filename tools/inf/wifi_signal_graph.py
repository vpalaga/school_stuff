#!/usr/bin/env python3
"""
Live Wi-Fi signal strength graph (in percent, like netsh) for a given SSID.

Usage:
    python wifi_signal_graph.py "MyNetwork"
    python wifi_signal_graph.py "MyNetwork" --interval 1 --window 120

Requires:  pip install matplotlib
Windows:   uses `netsh` (built in)
Linux:     uses `nmcli` (NetworkManager)
macOS:     uses `airport` if present, otherwise CoreWLAN (pip install pyobjc-framework-CoreWLAN;
           the terminal/Python needs Location Services permission to see SSIDs)
"""

import argparse
import os
import platform
import re
import subprocess
import threading
import time
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ---------------------------------------------------------------- scanners --
def dbm_to_pct(dbm):
    """Convert dBm to a 0-100% quality (same mapping Windows uses)."""
    return max(0, min(100, 2 * (dbm + 100)))


DEBUG = False


def _run_netsh():
    raw = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        capture_output=True,
    ).stdout
    # netsh prints in the console's OEM code page; try that before giving up.
    for enc in ("utf-8", "oem", "cp1252"):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="ignore")


def scan_windows(ssid):
    out = _run_netsh()
    target = ssid.strip().casefold()
    best, current, seen = None, None, []
    for line in out.splitlines():
        m = re.match(r"\s*SSID\s+\d+\s*:\s?(.*)$", line)
        if m:
            current = m.group(1).strip()
            seen.append(current)
            continue
        m = re.match(r"\s*[^:]+:\s*(\d+)\s*%", line)  # "Signal : 87%"
        if m and current is not None and current.casefold() == target:
            val = int(m.group(1))
            best = val if best is None else max(best, val)  # strongest AP/BSSID
    if best is None and DEBUG:
        print(f"[debug] looking for {ssid!r}; netsh reported SSIDs: {seen!r}")
        if not seen:
            print("[debug] no SSIDs parsed. Raw netsh output:\n" + out[:1500])
    return best


def scan_linux(ssid):
    out = subprocess.run(
        ["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi", "list", "--rescan", "yes"],
        capture_output=True, text=True, errors="ignore",
    ).stdout
    best = None
    for line in out.splitlines():
        name, _, sig = line.rpartition(":")
        name = name.replace("\\:", ":")
        if name == ssid and sig.isdigit():
            val = int(sig)
            best = val if best is None else max(best, val)
    return best


AIRPORT = ("/System/Library/PrivateFrameworks/Apple80211.framework/"
           "Versions/Current/Resources/airport")


def scan_macos(ssid):
    if os.path.exists(AIRPORT):
        out = subprocess.run([AIRPORT, "-s"], capture_output=True,
                             text=True, errors="ignore").stdout
        best = None
        for line in out.splitlines():
            m = re.match(r"^\s*(.*?)\s+((?:[0-9a-f]{1,2}:){5}[0-9a-f]{1,2})\s+(-\d+)\s", line, re.I)
            if m and m.group(1) == ssid:
                rssi = int(m.group(3))
                best = rssi if best is None else max(best, rssi)
        return None if best is None else dbm_to_pct(best)
    # Newer macOS: use CoreWLAN through pyobjc
    import CoreWLAN  # type: ignore
    iface = CoreWLAN.CWWiFiClient.sharedWiFiClient().interface()
    nets, _ = iface.scanForNetworksWithName_error_(ssid, None)
    if not nets:
        return None
    return dbm_to_pct(max(n.rssiValue() for n in nets))


def get_scanner():
    system = platform.system()
    if system == "Windows":
        return scan_windows
    if system == "Linux":
        return scan_linux
    if system == "Darwin":
        return scan_macos
    raise SystemExit(f"Unsupported OS: {system}")


# -------------------------------------------------------------------- main --
def main():
    ap = argparse.ArgumentParser(description="Live Wi-Fi signal strength graph")
    ap.add_argument("ssid", help="Name of the network to monitor")
    ap.add_argument("--interval", type=float, default=1.0,
                    help="Seconds between scans (default 1)")
    ap.add_argument("--window", type=int, default=60,
                    help="Seconds of history shown on the graph (default 60)")
    ap.add_argument("--debug", action="store_true",
                    help="Print the SSIDs the scanner sees when yours isn't found")
    args = ap.parse_args()
    global DEBUG
    DEBUG = args.debug

    scan = get_scanner()
    max_points = max(2, int(args.window / args.interval))
    times = deque(maxlen=max_points)
    values = deque(maxlen=max_points)  # percent, or NaN when SSID not seen
    lock = threading.Lock()
    stop = threading.Event()
    start = time.time()

    def worker():
        # Scanning can take seconds, so keep it off the GUI thread.
        while not stop.is_set():
            t0 = time.time()
            try:
                value = scan(args.ssid)
            except Exception as exc:
                print(f"Scan error: {exc}")
                value = None
            with lock:
                times.append(time.time() - start)
                values.append(float("nan") if value is None else value)
            stop.wait(max(0.0, args.interval - (time.time() - t0)))

    threading.Thread(target=worker, daemon=True).start()

    # ---- plot setup
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.canvas.manager.set_window_title(f"Signal strength: {args.ssid}")
    (line,) = ax.plot([], [], lw=2, color="#1f77b4", marker="o", ms=3)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Signal strength (%)")
    ax.set_xlabel("Time (s)")
    ax.grid(alpha=0.3)

    # Quality bands
    ax.axhspan(70, 100, color="green", alpha=0.08)
    ax.axhspan(40, 70, color="yellow", alpha=0.08)
    ax.axhspan(0, 40, color="red", alpha=0.08)

    title = ax.set_title(f'"{args.ssid}"')
    stats = ax.text(0.01, 0.03, "", transform=ax.transAxes, family="monospace",
                    bbox=dict(boxstyle="round", fc="white", alpha=0.8))

    def update(_frame):
        with lock:
            xs, ys = list(times), list(values)
        if not xs:
            return line, title, stats
        line.set_data(xs, ys)
        ax.set_xlim(max(0, xs[-1] - args.window), max(args.window, xs[-1]))

        valid = [y for y in ys if y == y]  # drop NaN
        if ys[-1] == ys[-1]:
            title.set_text(f'"{args.ssid}"   {ys[-1]:.0f}%')
        else:
            title.set_text(f'"{args.ssid}"   not found')
        if valid:
            stats.set_text(f"min {min(valid):.0f}%  max {max(valid):.0f}%  "
                           f"avg {sum(valid) / len(valid):.1f}%")
        return line, title, stats

    anim = FuncAnimation(fig, update, interval=500, blit=False,
                         cache_frame_data=False)
    try:
        plt.show()
    finally:
        stop.set()
    return anim


if __name__ == "__main__":
    main()