import os
import tkinter as tk
from tkinter import ttk, messagebox
import clips

RULES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expert_system_rules.clp")


class ExpertSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Information Management Expert System (CLIPS-powered)")
        self.geometry("500x560")
        self.resizable(False, False)

        self.env = clips.Environment()
        self.env.load(RULES_FILE)
        self.template = self.env.find_template("record")

        pad = {"padx": 12, "pady": 8}

        ttk.Label(self, text="Information Management Expert System",
                  font=("Segoe UI", 14, "bold")).pack(pady=(16, 2))
        ttk.Label(self, text="Powered by the real CLIPS inference engine (via clipspy)",
                  font=("Segoe UI", 9)).pack(pady=(0, 16))

        form = ttk.Frame(self)
        form.pack(**pad)

        ttk.Label(form, text="Record ID").grid(row=0, column=0, sticky="w", pady=6)
        self.record_id = ttk.Entry(form, width=25)
        self.record_id.insert(0, "R001")
        self.record_id.grid(row=0, column=1, pady=6)

        ttk.Label(form, text="Record Type").grid(row=1, column=0, sticky="w", pady=6)
        self.record_type = ttk.Combobox(form, width=22, state="readonly",
                                         values=["Document", "Customer-Data", "Report", "File"])
        self.record_type.current(0)
        self.record_type.grid(row=1, column=1, pady=6)

        ttk.Label(form, text="Years Since Last Update").grid(row=2, column=0, sticky="w", pady=6)
        self.years_since_update = ttk.Spinbox(form, from_=0, to=20, width=23)
        self.years_since_update.set(0)
        self.years_since_update.grid(row=2, column=1, pady=6)

        ttk.Label(form, text="Category").grid(row=3, column=0, sticky="w", pady=6)
        self.category = ttk.Combobox(form, width=22, state="readonly",
                                      values=["Personal", "Financial", "Operational", "Confidential"])
        self.category.current(0)
        self.category.grid(row=3, column=1, pady=6)

        ttk.Label(form, text="Access Level").grid(row=4, column=0, sticky="w", pady=6)
        self.access_level = ttk.Combobox(form, width=22, state="readonly",
                                          values=["Public", "Restricted", "Confidential"])
        self.access_level.current(0)
        self.access_level.grid(row=4, column=1, pady=6)

        ttk.Label(form, text="Completeness").grid(row=5, column=0, sticky="w", pady=6)
        self.completeness = ttk.Combobox(form, width=22, state="readonly",
                                          values=["Complete", "Incomplete"])
        self.completeness.current(0)
        self.completeness.grid(row=5, column=1, pady=6)

        ttk.Label(form, text="Verified").grid(row=6, column=0, sticky="w", pady=6)
        self.verified = ttk.Combobox(form, width=22, state="readonly",
                                      values=["TRUE", "FALSE"])
        self.verified.current(0)
        self.verified.grid(row=6, column=1, pady=6)

        ttk.Button(self, text="Evaluate with CLIPS", command=self.on_evaluate).pack(pady=16)

        self.result_frame = ttk.LabelFrame(self, text="CLIPS Inference Result")
        self.result_frame.pack(fill="x", padx=16, pady=(0, 16))

        self.needs_update_label = ttk.Label(self.result_frame, text="Needs Update: -")
        self.needs_update_label.pack(anchor="w", padx=10, pady=4)

        self.status_label = ttk.Label(self.result_frame, text="Status: -")
        self.status_label.pack(anchor="w", padx=10, pady=4)

        self.flagged_label = ttk.Label(self.result_frame, text="Flagged for Review: -")
        self.flagged_label.pack(anchor="w", padx=10, pady=4)

        self.fired_label = ttk.Label(self.result_frame, text="Rules Fired: -", wraplength=440, justify="left")
        self.fired_label.pack(anchor="w", padx=10, pady=4)

    def on_evaluate(self):
        try:
            self.env.reset()

            record_id = self.record_id.get().strip() or "R000"
            years = int(self.years_since_update.get())

            slots = {
                "record-id": clips.Symbol(record_id),
                "record-type": clips.Symbol(self.record_type.get().lower()),
                "years-since-update": years,
                "category": clips.Symbol(self.category.get().lower()),
                "access-level": clips.Symbol(self.access_level.get().lower()),
                "completeness": clips.Symbol(self.completeness.get().lower()),
                "verified": clips.Symbol(self.verified.get()),
            }
            self.template.assert_fact(**slots)

            fired_rules = []
            for activation in list(self.env.activations()):
                fired_rules.append(str(activation.name))

            self.env.run()

            result = None
            for f in self.env.facts():
                if f.template.name == "record" and str(f["record-id"]) == record_id:
                    result = dict(f)

            if result is None:
                messagebox.showerror("Error", "No result fact found.")
                return

            self.needs_update_label.config(text=f"Needs Update: {result['needs-update']}")
            self.status_label.config(text=f"Status: {result['status']}")
            self.flagged_label.config(text=f"Flagged for Review: {result['flagged-for-review']}")
            fired_text = ", ".join(fired_rules) if fired_rules else "none"
            self.fired_label.config(text=f"Rules Fired: {fired_text}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = ExpertSystemApp()
    app.mainloop()