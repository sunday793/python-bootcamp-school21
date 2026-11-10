import sys


def clear_screen():
    """
    Clear the terminal using ANSI escape codes.

    No external process is spawned (unlike os.system), and it works
    on Linux, macOS, and Windows 10+ terminals.
    """
    # '\033' is ESC.
    #   '[2J' clears the whole screen
    #   '[H'  moves the cursor to the top-left corner
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def render_table(headers: list[str], rows: list[list]) -> str:
    """Draw an ASCII table with centered cells."""
    widths = [
        max(len(str(headers[i])), max((len(str(r[i])) for r in rows), default=0)) + 2
        for i in range(len(headers))
    ]
    sep = "+" + "+".join("-" * w for w in widths) + "+"
    lines = [sep]
    lines.append("|" + "|".join(str(headers[i]).center(widths[i]) for i in range(len(headers))) + "|")
    lines.append(sep)
    for r in rows:
        lines.append("|" + "|".join(str(r[i]).center(widths[i]) for i in range(len(headers))) + "|")
    lines.append(sep)
    return "\n".join(lines)


def render_students_during(students) -> str:
    """Live students table: In queue → Passed → Failed."""
    order = {"In queue": 0, "Passed": 1, "Failed": 2}
    rows = sorted(
        [[s.name, s.status.value] for s in students],
        key=lambda r: order.get(r[1], 3),
    )
    return render_table(["Student", "Status"], rows)


def render_examiners_during(examiners) -> str:
    """Live examiners table with current student / totals / work time."""
    rows = [
        [
            e.name,
            e.current_student or "-",
            e.total_students,
            e.failed_students,
            f"{e.work_time:.2f}",
        ]
        for e in examiners
    ]
    return render_table(
        ["Examiner", "Current student", "Total students", "Failed", "Work time"],
        rows,
    )