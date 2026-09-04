# ====================================================================
# Immux-OS Master System Compilation Routine
# Target Environments: x86_64 / arm64 Hybrid Layer (Linux/Android/Win)
# ====================================================================

# Directories and Configurations
REPO_ROOT    := $(shell pwd)
BUILD_PACKAGE:= $(REPO_ROOT)/immux_config_package
SCRIPTS_DIR  := $(REPO_ROOT)/scripts
MANIFESTS_DIR:= $(REPO_ROOT)/manifests

.PHONY: all clean init-dirs build-bundle patch-launcher apply-hardware verify-security package-iso help

# Default Target: Run the entire system deployment compilation pipeline
all: init-dirs build-bundle patch-launcher apply-hardware verify-security package-iso
        @echo "🟢 [SUCCESS] Master compilation completed. Immux-OS is armed and ready."

# 1. Structure the foundational target tree
init-dirs:
        @echo "📁 [1/6] Structuring deployment compilation directories..."
        @mkdir -p $(BUILD_PACKAGE)/usr/bin
        @mkdir -p $(BUILD_PACKAGE)/var/run/immux
        @mkdir -p $(BUILD_PACKAGE)/etc/immsh
        @mkdir -p $(BUILD_PACKAGE)/scripts
        @mkdir -p $(MANIFESTS_DIR)

# 2. Package scripts, commands, and templates using the bundling engine
build-bundle: init-dirs
        @echo "📦 [2/6] Running automated package generation suite..."
        @python3 ./build_bundle.py
        @cp -r $(SCRIPTS_DIR)/* $(BUILD_PACKAGE)/scripts/ 2>/dev/null || true
        @cp $(REPO_ROOT)/etc/immsh/rules.json $(BUILD_PACKAGE)/etc/immsh/rules.json 2>/dev/null || true

# 3. Synchronize Yumi.py configurations and core container pipelines
patch-launcher: build-bundle
        @echo "🐍 [3/6] Injecting cluster and socket layout patches into Yumi.py launcher..."
        @chmod +x Yumi.py
        @python3 ./Yumi.py bootstrap

# 4. Bind drivers, low-latency audio frameworks, and environment properties
apply-hardware: patch-launcher
        @echo "⚙️ [4/6] Instantiating automated hardware targets and graphics profiles..."
        @if [ -f "./apply_hardware_profile.py" ]; then \
                python3 ./apply_hardware_profile.py; \
        else \
                echo "⚠️ apply_hardware_profile.py missing. Skipping hardware adjustments."; \
        fi

# 5. Run the integrity security suite (Dual-root enforcement & binfmt check)
verify-security: apply-hardware
        @echo "🛡️ [5/6] Launching sandboxing integrity validation testing..."
        @if [ -f "./validate_sysroot.py" ]; then \
                python3 ./validate_sysroot.py; \
        else \
                echo "⚠️ validate_sysroot.py missing. Bypassing partition safety audits."; \
        fi

# 6. Bake the operating system into a bootable ISO distribution file
package-iso: verify-security
        @echo "🔨 [6/6] Executing final live ISO environment baking routine..."
        @if [ -f "/home/kali/build-immux-iso.sh" ]; then \
                bash /home/kali/build-immux-iso.sh; \
        else \
                echo "ℹ️ ISO generator hook skipped. Configuration bundle completely prepared at: $(BUILD_PACKAGE)"; \
        fi

# Wipe generated distribution paths cleanly
clean:
        @echo "🧹 Cleaning up volatile targets and generated package files..."
        @rm -rf $(BUILD_PACKAGE)
        @rm -f $(BUILD_PACKAGE)/var/run/immux/sync_status.json
        @echo "✓ Clean phase executed completely."

# Self-documenting help utility
help:
        @echo "Immux-OS Makefile Command Interface Help"
        @echo "----------------------------------------"
        @echo "make              - Build and verify the entire system stack"
        @echo "make clean        - Wipe out compiled staging packages"
        @echo "make verify-security - Force audit the sysroot boundary and binfmt rules"