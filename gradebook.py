import json
import os

DATA_FILE = "gradebook.json"


def load_gradebook():
    """Load gradebook data from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            print("Warning: gradebook.json did not contain a list. Starting with an empty gradebook.")
            return []
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read gradebook.json. Starting with an empty gradebook.")
        return []


def save_gradebook(gradebook):
    """Save gradebook data to JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(gradebook, f, indent=4, ensure_ascii=False)
    except OSError:
        print("Error: could not save gradebook data.")


def find_course_index(gradebook, code):
    """Return index of course with given code (case-insensitive), or None."""
    code = code.strip().lower()
    for i, course in enumerate(gradebook):
        if course["code"].strip().lower() == code:
            return i
    return None


def input_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def input_positive_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value > 0:
                return value
            else:
                print("Value must be a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")


def input_score(prompt):
    """
    Score is treated as a numeric grade on a 0–100 scale.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if 0 <= value <= 100:
                return value
            else:
                print("Score must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")


def add_course(gradebook):
    print("\n=== Add a New Course ===")
    code = input_non_empty("Course code: ")

    if find_course_index(gradebook, code) is not None:
        print(f"Error: Course with code '{code}' already exists.")
        return

    name = input_non_empty("Course name: ")
    credits = input_positive_int("Number of credits: ")
    semester = input_non_empty("Semester (e.g., 2025-Fall): ")
    score = input_score("Score (0–100): ")

    course = {
        "code": code,
        "name": name,
        "credits": credits,
        "semester": semester,
        "score": score,
    }
    gradebook.append(course)
    save_gradebook(gradebook)
    print(f"Course '{code}' added successfully.\n")


def update_course(gradebook):
    print("\n=== Update a Course ===")
    code = input_non_empty("Enter course code to update: ")
    idx = find_course_index(gradebook, code)

    if idx is None:
        print(f"Error: No course found with code '{code}'.")
        return

    course = gradebook[idx]
    print(f"Current data for {course['code']}:")
    print(f"  Name    : {course['name']}")
    print(f"  Credits : {course['credits']}")
    print(f"  Semester: {course['semester']}")
    print(f"  Score   : {course['score']:.2f}")

    print("\nPress Enter to keep the current value.")

    new_name = input("New name (leave blank to keep current): ").strip()
    if new_name:
        course["name"] = new_name

    new_credits = input("New credits (leave blank to keep current): ").strip()
    if new_credits:
        try:
            credits = int(new_credits)
            if credits > 0:
                course["credits"] = credits
            else:
                print("Invalid credits. Keeping old value.")
        except ValueError:
            print("Invalid credits. Keeping old value.")

    new_sem = input("New semester (leave blank to keep current): ").strip()
    if new_sem:
        course["semester"] = new_sem

    new_score = input("New score 0–100 (leave blank to keep current): ").strip()
    if new_score:
        try:
            score = float(new_score)
            if 0 <= score <= 100:
                course["score"] = score
            else:
                print("Invalid score. Keeping old value.")
        except ValueError:
            print("Invalid score. Keeping old value.")

    gradebook[idx] = course
    save_gradebook(gradebook)
    print(f"Course '{course['code']}' updated successfully.\n")


def delete_course(gradebook):
    print("\n=== Delete a Course ===")
    code = input_non_empty("Enter course code to delete: ")
    idx = find_course_index(gradebook, code)

    if idx is None:
        print(f"Error: No course found with code '{code}'.")
        return

    course = gradebook[idx]
    confirm = input(f"Are you sure you want to delete '{course['code']} - {course['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        gradebook.pop(idx)
        save_gradebook(gradebook)
        print("Course deleted.\n")
    else:
        print("Delete cancelled.\n")


def view_gradebook(gradebook):
    print("\n=== Gradebook ===")
    if not gradebook:
        print("No courses in the gradebook yet.\n")
        return

    header = f"{'Code':<10} {'Name':<30} {'Cred':>4} {'Semester':<12} {'Score':>6}"
    print(header)
    print("-" * len(header))
    for c in gradebook:
        print(
            f"{c['code']:<10} {c['name']:<30} {c['credits']:>4} "
            f"{c['semester']:<12} {c['score']:>6.2f}"
        )
    print()


def calculate_overall_gpa(gradebook):
    """Here 'GPA' is really a weighted average score from 0–100."""
    total_credits = 0
    total_points = 0.0

    for c in gradebook:
        credits = c.get("credits", 0)
        score = c.get("score", 0.0)
        total_credits += credits
        total_points += score * credits

    if total_credits == 0:
        return None

    return total_points / total_credits


def calculate_gpa_by_semester(gradebook):
    """Weighted average score 0–100 by semester."""
    semester_stats = {}

    for c in gradebook:
        sem = c.get("semester", "N/A")
        credits = c.get("credits", 0)
        score = c.get("score", 0.0)

        if sem not in semester_stats:
            semester_stats[sem] = {"credits": 0, "points": 0.0}

        semester_stats[sem]["credits"] += credits
        semester_stats[sem]["points"] += score * credits

    gpa_by_sem = {}
    for sem, stats in semester_stats.items():
        if stats["credits"] > 0:
            gpa_by_sem[sem] = stats["points"] / stats["credits"]
        else:
            gpa_by_sem[sem] = None

    return gpa_by_sem


def show_gpa_summary(gradebook):
    print("\n=== Score Summary (0–100) ===")
    if not gradebook:
        print("No courses available to compute scores.\n")
        return

    overall = calculate_overall_gpa(gradebook)
    if overall is None:
        print("Could not compute average score (no valid credits).\n")
    else:
        print(f"Overall weighted average score: {overall:.2f}")

    gpa_sem = calculate_gpa_by_semester(gradebook)
    print("\nAverage score by semester:")
    for sem in sorted(gpa_sem.keys()):
        g = gpa_sem[sem]
        if g is None:
            print(f"  {sem}: N/A")
        else:
            print(f"  {sem}: {g:.2f}")
    print()


def print_menu():
    print("===================================")
    print(" Student Gradebook CLI")
    print("===================================")
    print("1. Add a course")
    print("2. Update a course")
    print("3. Delete a course")
    print("4. View gradebook")
    print("5. Show score summary")
    print("6. Exit")
    print("===================================")


def main():
    gradebook = load_gradebook()

    while True:
        print_menu()
        choice = input("Choose an option (1–6): ").strip()

        if choice == "1":
            add_course(gradebook)
        elif choice == "2":
            update_course(gradebook)
        elif choice == "3":
            delete_course(gradebook)
        elif choice == "4":
            view_gradebook(gradebook)
        elif choice == "5":
            show_gpa_summary(gradebook)
        elif choice == "6":
            print("Saving data and exiting...")
            save_gradebook(gradebook)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select from 1 to 6.\n")


if __name__ == "__main__":
    main()
