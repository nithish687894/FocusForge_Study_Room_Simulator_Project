import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
from pathlib import Path

APP_TITLE = "FocusForge | Study Room Simulator"
DATA_FILE = Path(__file__).with_name("study_plan.json")
BG = "#F2F5FA"
NAVY = "#18243A"
INK = "#202C40"
MUTED = "#68778D"
BLUE = "#4169E1"
TEAL = "#18A999"
AMBER = "#F0A53A"
RED = "#D95D5D"
WHITE = "#FFFFFF"

SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Computer Science", "English", "Biology", "Revision"]
COLORS = {"Mathematics": "#5478E7", "Physics": "#17A398", "Chemistry": "#E6A53A", "Computer Science": "#8867C4", "English": "#D86D83", "Biology": "#62A86A", "Revision": "#65758B", "Break": "#B7C4D6"}

class FocusForge(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x760")
        self.minsize(1020, 680)
        self.configure(bg=BG)
        self.tasks = []
        self.selected_id = None
        self._setup_style()
        self._build_shell()
        self._load()
        self._refresh()

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground=INK, rowheight=32, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#E8EDF5", foreground=NAVY, relief="flat", font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#DFE8FF")], foreground=[("selected", NAVY)])
        style.configure("TCombobox", padding=6)

    def _build_shell(self):
        header = tk.Frame(self, bg=NAVY, height=78)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="◈  FOCUSFORGE", bg=NAVY, fg=WHITE, font=("Segoe UI", 18, "bold")).pack(side="left", padx=28)
        tk.Label(header, text="STUDY ROOM SIMULATOR     •     PLAN WITH BALANCE", bg=NAVY, fg="#AEBBD0", font=("Segoe UI", 9, "bold")).pack(side="right", padx=28)

        self.main = tk.Frame(self, bg=BG)
        self.main.pack(fill="both", expand=True, padx=24, pady=18)
        tk.Label(self.main, text="Build a day that works for you", bg=BG, fg=INK, font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(self.main, text="Arrange study blocks, protect break time, and check your workload before the day begins.", bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 14))

        stats = tk.Frame(self.main, bg=BG)
        stats.pack(fill="x", pady=(0, 14))
        self.stat_labels = {}
        for key, title, color in [("study", "STUDY TIME", BLUE), ("break", "BREAK TIME", TEAL), ("blocks", "PLANNED BLOCKS", NAVY), ("load", "PLAN STATUS", AMBER)]:
            card = tk.Frame(stats, bg=WHITE, highlightbackground="#E1E7F0", highlightthickness=1)
            card.pack(side="left", fill="x", expand=True, padx=(0, 10))
            tk.Label(card, text=title, bg=WHITE, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(10, 1))
            value = tk.Label(card, text="—", bg=WHITE, fg=color, font=("Segoe UI", 17, "bold"))
            value.pack(anchor="w", padx=14, pady=(0, 10))
            self.stat_labels[key] = value

        content = tk.Frame(self.main, bg=BG)
        content.pack(fill="both", expand=True)
        left = tk.Frame(content, bg=WHITE, highlightbackground="#E1E7F0", highlightthickness=1, width=335)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)
        tk.Label(left, text="PLAN A BLOCK", bg=WHITE, fg=NAVY, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=17, pady=(16, 10))
        form = tk.Frame(left, bg=WHITE)
        form.pack(fill="x", padx=17)
        self.vars = {k: tk.StringVar() for k in ("subject", "start", "duration", "kind")}
        self.vars["subject"].set(SUBJECTS[0]); self.vars["start"].set("09:00"); self.vars["duration"].set("45"); self.vars["kind"].set("Study")
        self._field(form, "Subject", "subject", "combo", SUBJECTS)
        self._field(form, "Start time (24-hour, e.g. 09:00)", "start", "entry")
        self._field(form, "Duration in minutes", "duration", "entry")
        self._field(form, "Block type", "kind", "combo", ["Study", "Break"])
        self.add_btn = tk.Button(left, text="＋  Add to plan", command=self._add_task, bg=BLUE, fg=WHITE, activebackground="#3157CA", activeforeground=WHITE, relief="flat", font=("Segoe UI", 10, "bold"), pady=9, cursor="hand2")
        self.add_btn.pack(fill="x", padx=17, pady=(7, 4))
        tk.Button(left, text="Update selected block", command=self._update_task, bg="#EAF0FF", fg=BLUE, activebackground="#DCE6FF", relief="flat", font=("Segoe UI", 9, "bold"), pady=8, cursor="hand2").pack(fill="x", padx=17, pady=1)
        tk.Button(left, text="Delete selected block", command=self._delete_task, bg="#FFF0F0", fg=RED, activebackground="#FFE1E1", relief="flat", font=("Segoe UI", 9, "bold"), pady=8, cursor="hand2").pack(fill="x", padx=17, pady=1)
        tk.Button(left, text="Load demo day", command=self._load_demo, bg="#F0F3F8", fg=NAVY, activebackground="#E3E9F2", relief="flat", font=("Segoe UI", 9, "bold"), pady=8, cursor="hand2").pack(fill="x", padx=17, pady=(1, 5))
        tk.Label(left, text="SMART CHECKS", bg=WHITE, fg=NAVY, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=17, pady=(4, 2))
        self.advice = tk.Label(left, text="Add blocks to receive schedule feedback.", bg="#F4F7FB", fg=MUTED, justify="left", wraplength=280, padx=10, pady=10, font=("Segoe UI", 9))
        self.advice.pack(fill="x", padx=17, pady=(0, 16))

        right = tk.Frame(content, bg=BG)
        right.pack(side="left", fill="both", expand=True)
        tablebox = tk.Frame(right, bg=WHITE, highlightbackground="#E1E7F0", highlightthickness=1)
        tablebox.pack(fill="both", expand=True)
        tablehead = tk.Frame(tablebox, bg=WHITE)
        tablehead.pack(fill="x", padx=16, pady=(14, 8))
        tk.Label(tablehead, text="TODAY'S STUDY MAP", bg=WHITE, fg=NAVY, font=("Segoe UI", 11, "bold")).pack(side="left")
        self.filter_var = tk.StringVar(value="All blocks")
        filterbox = ttk.Combobox(tablehead, textvariable=self.filter_var, values=["All blocks", "Study only", "Breaks only"], state="readonly", width=13)
        filterbox.pack(side="right")
        filterbox.bind("<<ComboboxSelected>>", lambda e: self._refresh())
        cols = ("start", "end", "subject", "kind", "duration")
        self.tree = ttk.Treeview(tablebox, columns=cols, show="headings", selectmode="browse")
        for col, label, width in [("start", "START", 80), ("end", "END", 80), ("subject", "SUBJECT", 190), ("kind", "TYPE", 85), ("duration", "MIN", 70)]:
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="w" if col == "subject" else "center")
        self.tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.tree.bind("<<TreeviewSelect>>", self._select_task)
        timeline = tk.Frame(right, bg=WHITE, highlightbackground="#E1E7F0", highlightthickness=1)
        timeline.pack(fill="x", pady=(14, 0))
        tk.Label(timeline, text="VISUAL TIMELINE  ·  08:00–20:00", bg=WHITE, fg=NAVY, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=14, pady=(11, 2))
        self.canvas = tk.Canvas(timeline, height=75, bg=WHITE, highlightthickness=0)
        self.canvas.pack(fill="x", padx=12, pady=(0, 9))
        footer = tk.Frame(self.main, bg=BG)
        footer.pack(fill="x", pady=(10, 0))
        tk.Label(footer, text="Tip: click a row to edit or delete it  ·  Your plan is saved on this computer", bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(side="left")

    def _field(self, parent, label, key, kind, values=None):
        tk.Label(parent, text=label, bg=WHITE, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(4, 2))
        if kind == "combo":
            widget = ttk.Combobox(parent, textvariable=self.vars[key], values=values, state="readonly")
        else:
            widget = tk.Entry(parent, textvariable=self.vars[key], relief="solid", bd=1, font=("Segoe UI", 10), bg="#FCFDFE", fg=INK, insertbackground=INK)
        widget.pack(fill="x", ipady=2)

    def _minutes(self, value):
        return int(value.split(":")[0]) * 60 + int(value.split(":")[1])

    def _validate_form(self):
        try:
            start = self.vars["start"].get().strip()
            datetime.strptime(start, "%H:%M")
            duration = int(self.vars["duration"].get())
            if duration < 5 or duration > 240:
                raise ValueError("Duration must be between 5 and 240 minutes.")
            if self.vars["kind"].get() == "Study" and duration > 120:
                raise ValueError("A study block can be at most 120 minutes. Add a break and split it up.")
            begin = self._minutes(start)
            end = begin + duration
            if begin < 8*60 or end > 20*60:
                raise ValueError("Blocks must fit between 08:00 and 20:00.")
            kind = self.vars["kind"].get()
            subject = "Break" if kind == "Break" else self.vars["subject"].get()
            return {"subject": subject, "start": start, "duration": duration, "kind": kind, "end": end}
        except ValueError as exc:
            message = str(exc) or "Enter the start time as HH:MM, for example 09:00."
            messagebox.showerror("Check this block", message)
            return None

    def _add_task(self):
        task = self._validate_form()
        if not task: return
        task["id"] = str(datetime.now().timestamp())
        self.tasks.append(task)
        self._save(); self._refresh()

    def _update_task(self):
        if not self.selected_id:
            messagebox.showinfo("Select a block", "Click a row in the study map first."); return
        task = self._validate_form()
        if not task: return
        for i, old in enumerate(self.tasks):
            if old["id"] == self.selected_id:
                task["id"] = old["id"]; self.tasks[i] = task; break
        self._save(); self._refresh()

    def _delete_task(self):
        if not self.selected_id:
            messagebox.showinfo("Select a block", "Click a row in the study map first."); return
        self.tasks = [t for t in self.tasks if t["id"] != self.selected_id]
        self.selected_id = None
        self._save(); self._refresh()

    def _select_task(self, _event=None):
        selection = self.tree.selection()
        if not selection: return
        item_id = selection[0]
        task = next((t for t in self.tasks if t["id"] == item_id), None)
        if task:
            self.selected_id = item_id
            for key in ("subject", "start", "duration", "kind"):
                self.vars[key].set(str(task[key]))

    def _find_issues(self):
        ordered = sorted(self.tasks, key=lambda t: self._minutes(t["start"]))
        conflicts = []
        for a, b in zip(ordered, ordered[1:]):
            if a["end"] > self._minutes(b["start"]): conflicts.append((a,b))
        study = sum(t["duration"] for t in self.tasks if t["kind"] == "Study")
        longest = 0; run = 0; previous_end = None
        for t in ordered:
            begin = self._minutes(t["start"])
            if previous_end is not None and begin > previous_end:
                run = 0
            if t["kind"] == "Study":
                run += t["duration"]
                longest = max(longest, run)
            else:
                run = 0
            previous_end = t["end"]
        return conflicts, study, longest

    def _refresh(self):
        mode = self.filter_var.get() if hasattr(self, "filter_var") else "All blocks"
        for row in self.tree.get_children(): self.tree.delete(row)
        ordered = sorted(self.tasks, key=lambda t: self._minutes(t["start"]))
        for t in ordered:
            if mode == "Study only" and t["kind"] != "Study": continue
            if mode == "Breaks only" and t["kind"] != "Break": continue
            end = (datetime.min + timedelta(minutes=t["end"])).strftime("%H:%M")
            self.tree.insert("", "end", iid=t["id"], values=(t["start"], end, t["subject"], t["kind"], t["duration"]))
        conflicts, study, longest = self._find_issues()
        breaks = sum(t["duration"] for t in self.tasks if t["kind"] == "Break")
        self.stat_labels["study"].config(text=f"{study//60}h {study%60:02d}m")
        self.stat_labels["break"].config(text=f"{breaks} min")
        self.stat_labels["blocks"].config(text=str(len(self.tasks)))
        status = "OVERLAP" if conflicts else "BALANCED" if study <= 360 and longest <= 120 else "HEAVY LOAD"
        color = RED if conflicts else TEAL if status == "BALANCED" else AMBER
        self.stat_labels["load"].config(text=status, fg=color)
        notes = []
        if conflicts: notes.append(f"⚠ {len(conflicts)} time overlap(s) found. Move one of the overlapping blocks.")
        if study > 360: notes.append("⚠ More than 6 study hours: consider moving one block to another day.")
        if longest > 120: notes.append("⚠ Long study stretch: add a break between blocks.")
        if not notes and self.tasks: notes.append("✓ No overlaps. Your study load is within the 6-hour daily guide.")
        if not self.tasks: notes.append("Add study and break blocks. The simulator checks overlaps and workload as you go.")
        self.advice.config(text="\n\n".join(notes), fg=RED if conflicts or study > 360 or longest > 120 else TEAL if self.tasks else MUTED)
        self._draw_timeline(ordered)

    def _draw_timeline(self, tasks):
        c = self.canvas; c.delete("all")
        width = max(c.winfo_width(), 550); left, right = 36, width-16; y0, y1 = 26, 52
        c.create_rectangle(left, y0, right, y1, fill="#EDF1F7", outline="")
        span = 12*60
        for hour in range(8, 21, 2):
            x = left + (hour*60-480)/span*(right-left)
            c.create_line(x, y0-5, x, y1+3, fill="#CBD4E2")
            c.create_text(x, 66, text=f"{hour:02d}:00", fill=MUTED, font=("Segoe UI", 8))
        for t in tasks:
            x1 = left + (self._minutes(t["start"])-480)/span*(right-left)
            x2 = left + (t["end"]-480)/span*(right-left)
            c.create_rectangle(x1, y0+2, x2, y1-2, fill=COLORS.get(t["subject"], BLUE) if t["kind"] == "Study" else COLORS["Break"], outline="white", width=1)
            if x2-x1 > 38: c.create_text((x1+x2)/2, (y0+y1)/2, text=t["subject"][:9] if t["kind"] == "Study" else "Break", fill=WHITE if t["kind"] == "Study" else NAVY, font=("Segoe UI", 7, "bold"))

    def _load_demo(self):
        self.tasks = [
            {"id":"demo1","subject":"Mathematics","start":"09:00","duration":50,"kind":"Study","end":590},
            {"id":"demo2","subject":"Break","start":"09:50","duration":15,"kind":"Break","end":605},
            {"id":"demo3","subject":"Physics","start":"10:15","duration":50,"kind":"Study","end":665},
            {"id":"demo4","subject":"Computer Science","start":"11:30","duration":60,"kind":"Study","end":750},
            {"id":"demo5","subject":"Break","start":"12:30","duration":20,"kind":"Break","end":770},
            {"id":"demo6","subject":"Chemistry","start":"14:00","duration":60,"kind":"Study","end":900},
            {"id":"demo7","subject":"Revision","start":"16:00","duration":45,"kind":"Study","end":1005},
        ]
        self.selected_id = None; self._save(); self._refresh()

    def _save(self):
        try: DATA_FILE.write_text(json.dumps(self.tasks, indent=2), encoding="utf-8")
        except OSError as e: messagebox.showwarning("Save issue", f"Could not save the plan: {e}")

    def _load(self):
        try:
            if DATA_FILE.exists():
                self.tasks = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.tasks = []

if __name__ == "__main__":
    app = FocusForge()
    app.mainloop()



