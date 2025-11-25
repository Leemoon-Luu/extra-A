# Extra-A: Student Gradebook CLI

This is a simple Python command-line application for managing a student gradebook.  
It was created for the **Extra-A (60–70)** task in the mini-portfolio.

## Features

- **Add a course**  
  - Stores: course code, course name, number of credits, semester, and score.
- **Update a course**  
  - Edit an existing course by its course code.
- **Delete a course**  
  - Remove a course entry from the gradebook.
- **View gradebook**  
  - Displays all courses in a clean tabular format.
- **GPA calculation**  
  - Computes **overall weighted GPA** and **GPA by semester**.  
  - The `score` is treated as grade points on a **0.0–4.0 scale**.  
    - Example: 4.0 = A, 3.0 = B, etc.
- **Persistent storage**  
  - All data is saved in `gradebook.json` and loaded automatically on startup.
- **Input validation**  
  - Prevents empty fields.
  - Rejects invalid credits (must be positive integer).
  - Rejects invalid scores (must be between 0.0 and 4.0).
  - Prevents duplicate course codes when adding new courses.

## Files

- `gradebook.py` – main CLI application.
- `gradebook.json` – data file (created automatically if it does not exist).
- `README.md` – this file.

## How to Run

1. Make sure you have **Python 3** installed.
2. Place `gradebook.py` and `gradebook.json` (optional) in the same folder.
3. Open a terminal in that folder and run:

```bash
python gradebook.py
