#!/usr/bin/env python3
import os
import sys
import json
import re
import tempfile
import subprocess

# --- SYSTEM DIRECTORY SCATTER CONFIGURATION ---
STATE_FILE = "/dev/shm/immux_runtime_state.json"
HARDWARE_PROFILE_PATH = "./hardware_target.json"
COMMAND_RULES_PATH = "/etc/immsh/rules.json"

K8S_DEPLOYMENT_TEMPLATE = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: {APP_NAME}
  namespace: immux-appstore
  labels:
    tier: appstore-runtime
    distribution: dynamic-link
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: {APP_NAME}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {APP_NAME}
    spec:
      containers:
        - name: app-sandbox
          image: immux-registry/store-app-payload:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: DISPLAY
              value: ":0"
            - name: WAYLAND_DISPLAY
              value: "wayland-0"
            - name: GALLIUM_DRIVER
              value: "zink"
            - name: MESA_LOADER_DRIVER_OVERRIDE
              value: "zink"
            - name: VIRGL_DEBUG
              value: "use_vulkan"
            - name: PULSE_SERVER
              value: "unix:/tmp/pulse/native"
          resources:
            limits:
              cpu: "2"
              memory: 2Gi
            requests:
              cpu: "500m"
              memory: 512Mi
          volumeMounts:
            - name: x11-socket
              mountPath: /tmp/.X11-unix
              readOnly: true
            - name: wayland-socket
              mountPath: /run/user/1000
              readOnly: true
            - name: virgl-renderer-pipe
              mountPath: /dev/dri
            - name: pipewire-stream-socket
              mountPath: /tmp/pulse
            - name: isolated-shm
              mountPath: /dev/shm
      volumes:
        - name: x11-socket
          hostPath:
            path: /tmp/.X11-unix
            type: Directory
        - name: wayland-socket
          hostPath:
            path: /run/user/1000
            type: Directory
        - name: virgl-renderer-pipe
          hostPath:
            path: /dev/dri
            type: Directory
        - name: pipewire-stream-socket
          hostPath:
            path: /run/user/1000/pulse
            type: Directory
        - name: isolated-shm
          emptyDir:
            medium: Memory
            sizeLimit: 256Mi
"""

DEFAULT_STATE = {
    "system": {
        "mood": "calm",
        "time_of_day": "day",
        "narrative_stage": "k12_initialization"
    },
    "visuals": {
        "primary_color": "#1e1e2e",
        "accent_color": "#89b4fa",
        "opacity": 0.95,
        "animation_speed": "slow"
    }
}

# === MODULE 1: IN-MEMORY STATE ENGINE ===
def load_state():
    if not os.path.exists(STATE_FILE):
        return DEFAULT_STATE
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_STATE

def save_state(state):
    dir_name = os.path.dirname(STATE_FILE)
    os.makedirs(dir_name, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False) as tf:
        json.dump(state, tf, indent=2)
        temp_name = tf.name
    os.chmod(temp_name, 0o600)
    os.replace(temp_name, STATE_FILE)

def set_mood(mood):
    state = load_state()
    state["system"]["mood"] = mood

    if mood == "psychedelic":
        state["visuals"]["primary_color"] = "#311b92"
        state["visuals"]["accent_color"] = "#00e676"
        state["visuals"]["opacity"] = 0.85
        state["visuals"]["animation_speed"] = "pulsing_morph"
    elif mood == "alerted":
        state["visuals"]["primary_color"] = "#4a0000"
        state["visuals"]["accent_color"] = "#ff3333"
        state["visuals"]["opacity"] = 1.0
        state["visuals"]["animation_speed"] = "fast"
    else:
        state["visuals"] = DEFAULT_STATE["visuals"]

    save_state(state)
    print(f"✨ System mood shifted to [{mood.upper()}]. Shared memory state updated.")

# === MODULE 2: APP STORE & PACKAGE MANAGER (imm) ===
def install_app(app_name):
    if not re.match(r"^[a-zA-Z0-9_-]+$", app_name):
        print("❌ Error: Invalid application name format.")
        return False

    print(f"📦 Compiling dynamic container manifest template for '{app_name}'...")
    manifest_content = K8S_DEPLOYMENT_TEMPLATE.format(APP_NAME=app_name)

    # Process deployment directly through cluster stdin pipelines
    try:
        process = subprocess.Popen(["kubectl", "apply", "-f", "-"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=manifest_content)
        print(f"✅ '{app_name}' sandbox container pushed to target local cluster namespace.")
        return True
    except Exception as e:
        print(f"❌ Failed to interface with local cluster orchestration components: {e}")
        return False

# === MODULE 3: AUTOMATED SYSTEM INITIALIZATION ===
def execute_system_bootstrap():
    print("🚀 [Bootstrap] Running system-wide structural automation mappings...")

    # 1. Set runtime file permissions
    try:
        subprocess.run("chmod +x /scripts/*.sh /scripts/*.py /bin/imm /bin/immsh /usr/bin/immsh-health 2>/dev/null", shell=True)
        print("✓ Executable permissions synchronized across application binaries.")
    except Exception:
        pass

    # 2. Extract and bind from target profile configs
    if os.path.exists(HARDWARE_PROFILE_PATH):
        try:
            with open(HARDWARE_PROFILE_PATH, "r") as f:
                profile = json.load(f)
                print(f"⚙️ Target Spec Applied: {profile.get('system_profile', 'Unknown Profile')}")
        except Exception as e:
            print(f"⚠️ Unable to verify hardware configuration template metrics: {e}")

    # 3. Mount configurations and kick-off ISO assembly processes
    print("☸️ Verifying cluster core manifest alignment rules...")
    subprocess.run(["kubectl", "apply", "-f", "/manifests/rootsync.yaml", "--dry-run=client"], capture_output=True)

    if os.path.exists("/home/kali/build-immux-iso.sh"):
        print("🔨 Compiling bootable live Immux-OS ISO environment image...")
        subprocess.run(["bash", "/home/kali/build-immux-iso.sh"])
    else:
        print("⚠️ Build routine path '/home/kali/build-immux-iso.sh' unreachable. ISO compilation bypassed.")

# === EXECUTION COMMAND ROUTER ===
def print_help():
    print("Immux-OS Launcher Subsystem Interface [Yumi]")
    print("\nUsage:")
    print("  python3 Yumi.py bootstrap              - Perform full pipeline initial setup")
    print("  python3 Yumi.py mood <calm/alerted/..>  - Dynamically morph system mood layouts")
    print("  python3 Yumi.py install <app_name>     - Provision an isolated App Store container")
    print("  python3 Yumi.py state                  - Output active shared memory parameters")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    action = sys.argv[1]
    if action == "bootstrap":
        execute_system_bootstrap()
    elif action == "mood" and len(sys.argv) == 3:
        set_mood(sys.argv[2])
    elif action == "install" and len(sys.argv) == 3:
        install_app(sys.argv[2])
    elif action == "state":
        print(json.dumps(load_state(), indent=2))
    else:
        print_help()





def configure_sandbox_sockets(user_id=1000):
    print("🔌 [Yumi Engine] Mapping communication interface socket structures...")

    # Establish local runtime paths
    wayland_runtime = f"/run/user/{user_id}/wayland-0"
    pipewire_runtime = f"/run/user/{user_id}/pulse/native"

    # Ensure local sockets exist before initiating runtime linkage
    if not os.path.exists(wayland_runtime):
        print(f"⚠️ Wayland display interface socket unreachable at path: {wayland_runtime}")
    else:
        print(f"✓ Graphical path bound: {wayland_runtime}")

    if not os.path.exists(pipewire_runtime):
        print(f"⚠️ PipeWire communications server socket unreachable at path: {pipewire_runtime}")
    else:
        print(f"✓ Low-latency audio socket matched: {pipewire_runtime}")

    return {
        "WAYLAND_DISPLAY_PATH": wayland_runtime,
        "PIPEWIRE_SOCKET_PATH": pipewire_runtime
    }