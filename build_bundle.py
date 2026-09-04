#!/usr/bin/env python3
import os
import sys
import shutil
import json

TARGET_DIR = "./immux_config_package"
PATHS = [
    f"{TARGET_DIR}/usr/bin",
    f"{TARGET_DIR}/var/run/immux",
    f"{TARGET_DIR}/.github/workflows",
    f"{TARGET_DIR}/etc/immsh"
]

def build_package():
    print("📦 \033[1mInitializing Immux-OS Configuration Bundler...\033[0m")

    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)
    for path in PATHS:
        os.makedirs(path, exist_ok=True)

    sync_seed = {
        "status": "Synced",
        "commit": "cf83bc7a1290bb1c11700fa32491e38c92842100",
        "drift": "0 commits behind upstream (Main-Cluster)"
    }

    with open(f"{TARGET_DIR}/var/run/immux/sync_status.json", "w") as f:
        json.dump(sync_seed, f, indent=4)

    print(f"\033[1;32m✓ Environment layout bundled inside: {TARGET_DIR}/\033[0m")

if __name__ == "__main__":
    build_package()
EOF

