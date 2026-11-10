import sys


def clear_screen():
    if not sys.stdout.isatty():
        return
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def render_table(headers: list[str], rows: list[list]) -> str:
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