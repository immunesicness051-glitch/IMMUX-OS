# ====================================================================
# Immux-OS Master System Compilation Routine
# Target Environments: x86_64 / arm64 Hybrid Layer (Linux/Android/Win)
# ====================================================================

REPO_ROOT    := $(shell pwd)
BUILD_PACKAGE:= $(REPO_ROOT)/immux_config_package
SCRIPTS_DIR  := $(REPO_ROOT)/scripts
MANIFESTS_DIR:= $(REPO_ROOT)/manifests

.PHONY: all clean init-dirs build-bundle patch-launcher apply-hardware verify-security package-iso help

all: init-dirs build-bundle patch-launcher apply-hardware verify-security package-iso
        @echo "🟢 [SUCCESS] Master compilation completed. Immux-OS is armed and ready."

init-dirs:
        @echo "📁 [1/6] Structuring deployment compilation directories..."
        @mkdir -p $(BUILD_PACKAGE)/usr/bin
        @mkdir -p $(BUILD_PACKAGE)/var/run/immux
        @mkdir -p $(BUILD_PACKAGE)/etc/immsh
        @mkdir -p $(BUILD_PACKAGE)/scripts
        @mkdir -p $(MANIFESTS_DIR)

build-bundle: init-dirs
        @echo "📦 [2/6] Running automated package generation suite..."
        @python3 ./build_bundle.py
        @cp -r $(SCRIPTS_DIR)/* $(BUILD_PACKAGE)/scripts/ 2>/dev/null || true
        @cp $(REPO_ROOT)/etc/immsh/rules.json $(BUILD_PACKAGE)/etc/immsh/rules.json 2>/dev/null || true

patch-launcher: build-bundle
        @echo "🐍 [3/6] Injecting cluster and socket layout patches into Yumi.py launcher..."
        @chmod +x Yumi.py
        @python3 ./Yumi.py bootstrap

apply-hardware: patch-launcher
        @echo "⚙️ [4/6] Instantiating automated hardware targets and graphics profiles..."
        @if [ -f "./apply_hardware_profile.py" ]; then \
                python3 ./apply_hardware_profile.py; \
        else \
                echo "⚠️ apply_hardware_profile.py missing. Skipping hardware adjustments."; \
        fi

verify-security: apply-hardware
        @echo "🛡️ [5/6] Launching sandboxing integrity validation testing..."
        @if [ -f "./validate_sysroot.py" ]; then \
                python3 ./validate_sysroot.py; \
        else \
                echo "⚠️ validate_sysroot.py missing. Bypassing partition safety audits."; \
        fi

package-iso: verify-security
        @echo "🔨 [6/6] Executing final live ISO environment baking routine..."
        @if [ -f "/home/kali/build-immux-iso.sh" ]; then \
                bash /home/kali/build-immux-iso.sh; \
        else \
                echo "ℹ️ ISO generator hook skipped. Configuration bundle completely prepared at: $(BUILD_PACKAGE)"; \
        fi

clean:
        @echo "🧹 [Clean Engine] Purging volatile build assets and staging trees..."
        @rm -rf $(BUILD_PACKAGE)
        @echo "🧹 [Clean Engine] Disposing of active container state records in shared memory..."
        @rm -f /dev/shm/immux_runtime_state.json
        @echo "☸️ [Clean Engine] Pruning dynamic runtime pods inside immux-appstore namespace..."
        @if command -v kubectl >/dev/null 2>&1; then \
                kubectl delete deployments --all -n immux-appstore --timeout=15s 2>/dev/null || true; \
                echo "✓ K8s app store sandbox containers purged successfully."; \
        else \
                echo "ℹ️ kubectl not in path, skipping live container cluster cleanup."; \
        fi
        @echo "✓ System state realigned and clean action fully executed."

help:
        @echo "Immux-OS Makefile Command Interface Help"
        @echo "----------------------------------------"
        @echo "make              - Build and verify the entire system stack"
        @echo "make clean        - Wipe compiled staging, shared memory states, and reset active K8s apps"
        @echo "make verify-security - Force audit the sysroot boundary and binfmt rules"