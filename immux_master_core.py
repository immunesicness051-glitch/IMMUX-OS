#!/usr/bin/env python3
import os
import sys
import json
import time
import datetime
import shutil
import subprocess

# --- SYSTEM DIRECTORIES & FILE PATHS ---
WORKSPACE = os.path.expanduser("~/immux_build_workspace/")
RULES_PATH = "/etc/immsh/command_rules.json"
ASSET_DB_PATH = "/etc/imm/installed_manifest.db"
SYSTEMD_BOOT_ENTRY = "/boot/immux_efi/loader/entries/immux-os-gki.conf"

class ImmuxMasterCore:
    def __init__(self):
        self.diurnal_phase = "DAYTIME"
        self.colors = {"border": "#006400", "bg": "#000A0A", "desc": "Emerald & Cyber Cyan"}
        self.load_database()

    def load_database(self):
        """Manages user custom tool configurations and skill progress."""
        if not os.path.exists(ASSET_DB_PATH):
            try:
                os.makedirs(os.path.dirname(ASSET_DB_PATH), exist_ok=True)
                initial_db = {
                    "base_apps": ["immsh", "imm-calc", "xplorer-remix", "imm-hospital"],
                    "custom_modules": {},
                    "guild_profiles": {
                        "medical_guild": {"level": 1, "xp": 0, "unlocked_modules": ["Basic Triage Assessment"]},
                        "law_guild": {"level": 1, "xp": 0, "unlocked_modules": ["Public Security Statutes"]},
                        "trades_guild": {"level": 1, "xp": 150, "unlocked_modules": ["Welding Core Physics"]}
                    }
                }
                with open(ASSET_DB_PATH, 'w') as f:
                    json.dump(initial_db, f, indent=2)
            except:
                pass

    def run_theme_pulse(self):
        """Calculates real-world hours to slowly shift desktop color schemes (<600MB)."""
        current_hour = datetime.datetime.now().hour
        if 5 <= current_hour < 12:
            self.colors = {"border": "#4B0082", "bg": "#0D001A", "desc": "Deep Indigo & Electric Blue (Morning)"}
        elif 12 <= current_hour < 18:
            self.colors = {"border": "#006400", "bg": "#000A0A", "desc": "Emerald & Deep Cyber Cyan (Day)"}
        else:
            self.colors = {"border": "#FF4500", "bg": "#120012", "desc": "Twilight Amber & Neon Magenta (Night)"}
        print(f"🌌 \033[94m[Theme-Engine]\033[0m Workspace borders configured to: {self.colors['desc']}")

    def open_hospital_triage(self):
        """Displays the clinical system resource and sandbox security telemetry charts."""
        print("\n\033[95m" + "="*75 + "\033[0m")
        print(" 🏥 \033[1mIMMUX-OS CLINICAL DIAGNOSTICS HOSPITAL\033[0m")
        print("=  Status: Active Monitoring | Core Security Layer: Unbroken")
        print("\033[95m" + "="*75 + "\033[0m")
        print(" ├── CPU Strain: [████████░░░░░░░░░░░░] 38% (Normal Scheduling)")
        print(" └── RAM Burden: [████████████░░░░░░░░] 54% (Clean Memory Alloc)")
        print("\033[91m [ACTIVE SANDBOX VECTORS]:\033[0m Zero anomalies. Isolation boundaries are sealed.")
        print("\033[95m" + "="*75 + "\033[0m\n")

    def run_yumi_emulation(self):
        """Simulates one-click streaming of 4MLinux Core ISO directly into a memory loop."""
        print("\n\033[94m[Yumi-Core]\033[0m Simulating One-Click Execution for 4MLinux-32.0-core.iso...")
        print(" ├── Target Endpoint: Internet Archive Stream Verified")
        print(" ├── Allocation: Virtual RAM loop storage compartment initialized")
        print(" └── \033[92mStatus: Successful. 4MLinux live shell viewport linked.\033[0m\n")

    def start_shell_simulator(self):
        """Launches the typo-correcting, user-forgiving command shell prompt."""
        print("\n\033[95m" + "="*75 + "\033[0m")
        print(" 🛡️  \033[1mIMMUX-OS SECURE FLEXIBLE SHELL SIMULATOR ACTIVE\033[0m")
        print("=  Type 'hospital', 'yumi', or 'exit' to navigate modules.")
        print("\033[95m" + "="*75 + "\033[0m\n")

        while True:
            prompt = f"\033[92mroot@immux\033[0m:\033[34m{os.getcwd()}\033[0m# "
            try:
                user_in = input(prompt).strip()
                if user_in == "exit":
                    break
                elif user_in in ["hospital", "hosp"]:
                    self.open_hospital_triage()
                elif user_in in ["yumi", "yumi.py"]:
                    self.run_yumi_emulation()
                elif user_in in ["instlal", "instll", "instal"]:
                    print("\033[93m[immsh]: Auto-correcting typo entry to 'install' verb...\033[0m")
                    print("[Immux-Sysadmin]: Usage: sudo imm install <package>")
                elif user_in == "ifconfig":
                    print("\033[93m[immsh]: Intercepted missing path. Located binary at '/sbin/ifconfig'. Running...\033[0m")
                    subprocess.run(["ifconfig"], capture_output=False)
                elif user_in == "":
                    continue
                else:
                    print(f"\033[91m[immsh]: Command '{user_in}' not found.\033[0m Type 'hospital' or 'yumi' to test tools.")
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    core = ImmuxMasterCore()
    core.run_theme_pulse()
    core.start_shell_simulator()