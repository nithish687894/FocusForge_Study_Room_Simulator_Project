# FocusForge — Viva Guide

## 30-second project introduction

“My project is FocusForge, a study-room schedule simulator built with Python Tkinter. A student can add study sessions and breaks, see the day on a timeline, and save the plan locally. The app checks for invalid times, overlapping blocks, more than six study hours, and long study stretches without a break. I used Tkinter for the interface, Python lists and dictionaries for the schedule, and JSON for storage.”

## Project modules

- **Interface:** Form fields, buttons, summary values, filter, table, and timeline.
- **Input validation:** Parses 24-hour time, checks duration limits, and keeps blocks within 08:00–20:00.
- **Plan management:** Adds, updates, deletes, selects, filters, and loads a sample day.
- **Schedule analysis:** Sorts blocks by start time, detects overlaps, totals study and break minutes, and checks study load.
- **Timeline drawing:** Maps each block’s start/end time to a horizontal canvas position.
- **Storage:** Reads/writes the task list in `study_plan.json` using Python’s `json` module.

## Likely viva questions

### 1. Why did you choose this project?
It is more than a data-entry form: it combines scheduling, immediate feedback, a graphical timeline, input validation, and file storage in one student-useful application.

### 2. What is Tkinter?
Tkinter is Python’s standard interface to the Tcl/Tk GUI toolkit. It provides widgets such as windows, labels, buttons, entries, comboboxes, and canvases.

### 3. What is an event in this app?
An event is an action such as clicking **Add to plan**, selecting a row, or changing the filter. Tkinter connects these events to functions such as `_add_task`, `_select_task`, and `_refresh`.

### 4. How are events connected to functions?
A button uses `command=self._add_task`. A table selection or combobox change uses `bind`, for example `self.tree.bind("<<TreeviewSelect>>", self._select_task)`.

### 5. How do you detect overlapping sessions?
The app sorts blocks by their start time. It compares each block’s end with the next block’s start. If the earlier end is later than the next start, the two ranges overlap.

### 6. Why convert times into minutes?
Strings such as `09:30` are easy to display, but integer minutes make addition and comparison straightforward. `09:30` becomes 570 minutes after midnight.

### 7. How does the timeline work?
The canvas represents 08:00 to 20:00 as a horizontal range. The app converts a block’s start and end into x-coordinates, then draws a colored rectangle between them.

### 8. How is data stored?
The plan is a list of dictionaries. Python’s `json` module serializes the list to `study_plan.json`; the app reads the file at startup and writes it after changes.

### 9. What does `try/except` do in validation?
It handles invalid input, such as a non-numeric duration or malformed time. Instead of crashing, the app shows a message and rejects the block.

### 10. Why use `ttk.Treeview`?
It displays schedule records in aligned columns and supports selecting a row, which makes editing and deleting a chosen block simple.

### 11. What is the difference between `pack` and `grid`?
Both are Tkinter geometry managers. `pack` places widgets relative to available space; `grid` arranges them in rows and columns. This project mainly uses `pack` for its stacked page layout.

### 12. What are the limitations?
It stores one plan on one computer, has no account or cloud sync, and uses simple workload rules. It does not automatically optimize a schedule or send reminders.

### 13. What could you add next?
Multiple saved days, drag-to-move timeline blocks, weekly summaries, CSV export, configurable study limits, and reminders.

## Demonstration checklist

- [ ] Launch the app and identify the form, table, summary, and timeline.
- [ ] Load or keep the sample day.
- [ ] Add a 20-minute block at 09:30 and explain the overlap warning.
- [ ] Move it to a free time and show the warning clear.
- [ ] Select and update an existing block.
- [ ] Close and reopen the app to show saved data.

## Rubric mapping (15 marks)

- **GUI Design and Implementation — 5 marks:** Organized form, readable schedule table, summary metrics, filtering, color-coded timeline, and visible feedback.
- **Code Implementation and Event Handling — 5 marks:** Tkinter callbacks, validation, sorting, overlap detection, canvas drawing, and JSON persistence.
- **Viva — 5 marks:** Explain the modules, data model, event flow, time conversion, overlap logic, and one limitation/future improvement.

