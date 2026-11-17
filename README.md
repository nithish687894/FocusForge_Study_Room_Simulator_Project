# FocusForge — Study Room Simulator

**A Tkinter holiday project**

FocusForge helps a student plan a balanced study day. It places study blocks and breaks on a visual timeline, totals the planned time, checks for schedule conflicts, and warns about a heavy study load.

## Run it

1. Install Python 3.10 or later with **Tcl/Tk** included.
2. Extract the project folder.
3. Open Command Prompt or PowerShell in this folder.
4. Run:

   ```powershell
   py -3 focusforge.py
   ```

The project uses only Python's standard library. It needs no `pip install` and works offline. `study_plan.json` stores the sample plan beside the Python file. The app saves changes there automatically.

To start with an empty plan, close the app and delete `study_plan.json`; the app creates it again when you add a block.

## What you can do

- Add, edit, and delete study or break blocks.
- Choose a subject, a start time, and a duration.
- Filter the table to study blocks or breaks.
- View study minutes, break minutes, total blocks, and plan status.
- See each block on an 08:00–20:00 timeline.
- Load the built-in demo schedule.
- Save and reload your plan as JSON.

## Smart checks

- Start times must be valid 24-hour times, from 08:00 to 20:00.
- Each block must last 5–240 minutes; a study block may last up to 120 minutes.
- The schedule check finds overlapping time ranges.
- A plan is marked **Heavy Load** above six study hours or when consecutive scheduled study exceeds two hours without a break.
- A gap in the schedule resets the consecutive-study counter.

These checks are planning hints for a classroom project. They do not make a medical or learning-science assessment.

## Logical modules

The code is kept in one beginner-friendly file, but its responsibilities are separated into logical sections:

| Module | Main responsibility | Main methods |
|---|---|---|
| Interface | Build the form, summary, table, timeline, and status area | `_build_shell`, `_field` |
| Input validation | Check time and duration before accepting a block | `_validate_form`, `_minutes` |
| Plan management | Add, update, remove, select, filter, and seed entries | `_add_task`, `_update_task`, `_delete_task`, `_select_task`, `_load_demo` |
| Schedule analysis | Find overlaps, total work, and identify long study runs | `_find_issues`, `_refresh` |
| Timeline drawing | Convert time ranges into horizontal positions and subject colors | `_draw_timeline` |
| Local storage | Read and write the plan as JSON | `_load`, `_save` |

## Data model

Each task is a Python dictionary with `id`, `subject`, `start`, `duration`, `kind`, and `end` fields. A list of these dictionaries is saved to `study_plan.json`. Times are displayed as `HH:MM`; the app converts them to minutes after midnight for comparisons.

## Demo sequence

1. Launch the app. The sample schedule appears automatically.
2. Point out the summary figures and the colored timeline.
3. Add a 20-minute block at 09:30 to see the overlap warning.
4. Change the start time to 13:00 and add it again to show that the warning clears.
5. Select a row, edit its duration, and save the change.
6. Close and reopen the app to show that JSON persistence works.

## Files

- `focusforge.py` — Tkinter application source
- `study_plan.json` — saved example schedule; app-managed
- `screenshots/` — representative sample output views
- `VIVA_GUIDE.md` — explanations, likely questions, and answers

