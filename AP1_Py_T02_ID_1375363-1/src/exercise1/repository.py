from models import Student, Examiner, Question, Gender


def _parse_line(line: str) -> tuple[str, Gender]:
    """Split a line like 'Stepan M' into (name, Gender)."""
    name, g = line.split()
    return name, Gender(g)


def load_examiners(path: str = "examiners.txt") -> list[Examiner]:
    with open(path, encoding="utf-8") as f:
        return [
            Examiner(*_parse_line(line.strip()))
            for line in f if line.strip()
        ]


def load_students(path: str = "students.txt") -> list[Student]:
    with open(path, encoding="utf-8") as f:
        return [
            Student(*_parse_line(line.strip()))
            for line in f if line.strip()
        ]


def load_questions(path: str = "questions.txt") -> list[Question]:
    with open(path, encoding="utf-8") as f:
        return [Question(line.strip()) for line in f if line.strip()]
