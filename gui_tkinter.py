#!/usr/bin/env python3
"""
CV Generator - Tkinter GUI

Simple graphical interface for generating customized CVs.

Features:
- File pickers for master CV, template, and output
- Profile dropdown selection
- Generate button with progress indicator
- Log panel for status messages
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime
import threading

from cv_data_extractor import load_master_cv
from template_renderer import fill_template
from profile_loader import get_available_profiles


class CVGeneratorApp:
    """Main application window for CV Generator."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CV Generation System")
        self.root.geometry("700x500")
        self.root.minsize(600, 450)

        # Paths
        self.script_dir = Path(__file__).parent
        self.profiles_dir = self.script_dir / 'render_profiles'

        # Variables
        self.master_cv_path = tk.StringVar()
        self.template_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.selected_profile = tk.StringVar(value='balanced')
        self.is_generating = False

        # Load available profiles
        self.profiles = self._load_profiles()

        # Build UI
        self._create_widgets()

        # Log startup
        self.log("CV Generation System ready.")
        self.log(f"Profiles loaded: {len(self.profiles)}")

    def _load_profiles(self) -> dict:
        """Load available profiles from render_profiles directory."""
        profiles = {}
        profile_list = get_available_profiles(str(self.profiles_dir))
        for p in profile_list:
            profiles[p['id']] = p
        return profiles

    def _create_widgets(self):
        """Create all UI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="CV Generation System",
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # Master CV file picker
        ttk.Label(main_frame, text="Master CV:").grid(
            row=1, column=0, sticky="e", padx=(0, 10), pady=5
        )
        master_entry = ttk.Entry(main_frame, textvariable=self.master_cv_path)
        master_entry.grid(row=1, column=1, sticky="ew", pady=5)
        ttk.Button(
            main_frame,
            text="Browse...",
            command=self._browse_master_cv
        ).grid(row=1, column=2, padx=(10, 0), pady=5)

        # Template file picker
        ttk.Label(main_frame, text="Template:").grid(
            row=2, column=0, sticky="e", padx=(0, 10), pady=5
        )
        template_entry = ttk.Entry(main_frame, textvariable=self.template_path)
        template_entry.grid(row=2, column=1, sticky="ew", pady=5)
        ttk.Button(
            main_frame,
            text="Browse...",
            command=self._browse_template
        ).grid(row=2, column=2, padx=(10, 0), pady=5)

        # Profile dropdown
        ttk.Label(main_frame, text="Profile:").grid(
            row=3, column=0, sticky="e", padx=(0, 10), pady=5
        )
        profile_names = list(self.profiles.keys()) if self.profiles else ['balanced']
        profile_combo = ttk.Combobox(
            main_frame,
            textvariable=self.selected_profile,
            values=profile_names,
            state='readonly',
            width=20
        )
        profile_combo.grid(row=3, column=1, sticky="w", pady=5)

        # Output file picker
        ttk.Label(main_frame, text="Output:").grid(
            row=4, column=0, sticky="e", padx=(0, 10), pady=5
        )
        output_entry = ttk.Entry(main_frame, textvariable=self.output_path)
        output_entry.grid(row=4, column=1, sticky="ew", pady=5)
        ttk.Button(
            main_frame,
            text="Browse...",
            command=self._browse_output
        ).grid(row=4, column=2, padx=(10, 0), pady=5)

        # Generate button
        self.generate_btn = ttk.Button(
            main_frame,
            text="Generate CV",
            command=self._generate_cv
        )
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=20)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Helvetica', 10)
        )
        status_label.grid(row=6, column=0, columnspan=3, pady=(0, 5))

        # Log panel
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=(5, 0))
        main_frame.rowconfigure(7, weight=1)

        self.log_text = tk.Text(
            log_frame,
            height=10,
            wrap=tk.WORD,
            state='disabled',
            font=('Courier', 10)
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

    def log(self, message: str):
        """Add timestamped message to log panel."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def _browse_master_cv(self):
        """Open file dialog for master CV JSON."""
        filepath = filedialog.askopenfilename(
            title="Select Master CV JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            self.master_cv_path.set(filepath)
            self.log(f"Master CV: {Path(filepath).name}")

    def _browse_template(self):
        """Open file dialog for template DOCX."""
        filepath = filedialog.askopenfilename(
            title="Select Template",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )
        if filepath:
            self.template_path.set(filepath)
            self.log(f"Template: {Path(filepath).name}")

    def _browse_output(self):
        """Open save dialog for output DOCX."""
        filepath = filedialog.asksaveasfilename(
            title="Save CV As",
            defaultextension=".docx",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )
        if filepath:
            self.output_path.set(filepath)
            self.log(f"Output: {Path(filepath).name}")

    def _validate_inputs(self) -> bool:
        """Validate all required inputs are provided."""
        if not self.master_cv_path.get():
            messagebox.showerror("Missing Input", "Please select a Master CV JSON file.")
            return False
        if not self.template_path.get():
            messagebox.showerror("Missing Input", "Please select a Template file.")
            return False
        if not self.output_path.get():
            messagebox.showerror("Missing Input", "Please specify an Output file.")
            return False
        return True

    def _generate_cv(self):
        """Start CV generation in background thread."""
        if self.is_generating:
            return

        if not self._validate_inputs():
            return

        self.is_generating = True
        self.generate_btn.config(state='disabled')
        self.status_var.set("Generating...")

        # Run generation in background thread
        thread = threading.Thread(target=self._do_generate, daemon=True)
        thread.start()

    def _do_generate(self):
        """Perform actual CV generation (runs in background thread)."""
        try:
            # Step 1: Load master CV
            self.log("Loading master CV...")
            cv_data = load_master_cv(self.master_cv_path.get())
            self.log("Master CV loaded successfully.")

            # Step 2: Get profile path
            profile_id = self.selected_profile.get()
            if profile_id in self.profiles:
                profile_path = self.profiles[profile_id]['path']
            else:
                profile_path = str(self.profiles_dir / f"{profile_id}.json")
            self.log(f"Using profile: {profile_id}")

            # Step 3: Generate CV
            self.log("Rendering template...")
            fill_template(
                self.template_path.get(),
                cv_data,
                self.output_path.get(),
                profile_path
            )

            # Success
            self.log("CV generated successfully!")
            self.root.after(0, lambda: self._generation_complete(True))

        except FileNotFoundError as e:
            self.log(f"ERROR: {e}")
            self.root.after(0, lambda: self._generation_complete(False, str(e)))

        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            self.log(f"ERROR: {error_msg}")
            self.root.after(0, lambda: self._generation_complete(False, error_msg))

    def _generation_complete(self, success: bool, error_msg: str = None):
        """Handle generation completion (called on main thread)."""
        self.is_generating = False
        self.generate_btn.config(state='normal')

        if success:
            self.status_var.set("Done!")
            messagebox.showinfo(
                "Success",
                f"CV generated successfully!\n\nOutput: {self.output_path.get()}"
            )
        else:
            self.status_var.set("Error")
            messagebox.showerror(
                "Generation Failed",
                f"Failed to generate CV:\n\n{error_msg}"
            )


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = CVGeneratorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
