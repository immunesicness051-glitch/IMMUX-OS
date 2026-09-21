    def assemble_sysroot(self):
        self.log("Assembling target OS tree layer architecture safely...")
        # Mirror structure locations into targeted build space with validation checks
        for folder in ["usr", "etc"]:
            source_folder = os.path.join(".", folder)
            if os.path.exists(source_folder) and os.listdir(source_folder):
                shutil.copytree(source_folder, os.path.join(self.sysroot, folder), dirs_exist_ok=True)
            else:
                # Creates empty fallback space inside build root instead of crashing the pipeline
                os.makedirs(os.path.join(self.sysroot, folder), exist_ok=True)
                self.log(f"Configured fallback structure for empty root path element: {folder}", "WARN")
