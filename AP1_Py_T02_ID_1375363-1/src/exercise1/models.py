import random
from enum import Enum

F = 1.618  # golden ratio


class Gender(Enum):
    MALE = "M"
    FEMALE = "F"


class Status(Enum):
    IN_QUEUE = "In queue"
    PASSED = "Passed"
    FAILED = "Failed"


class Mood(Enum):
    BAD = "bad"
    GOOD = "good"
    NEUTRAL = "neutral"


class Person:
    """Base class for both students and examiners."""

    def __init__(self, name: str, gender: Gender):
        self._name = name
        self._gender = gender

    @property
    def name(self) -> str:
        return self._name

    @property
    def gender(self) -> Gender:
        return self._gender

    def __repr__(self):
        return f"{self.__class__.__name__}({self._name}, {self._gender.value})"


class Question:
    """A question from the bank. Builds the golden-ratio word distribution."""

    def __init__(self, text: str):
        self._text = text
        self._words = text.split()

    @property
    def text(self) -> str:
        return self._text

    @property
    def words(self) -> list[str]:
        return self._words

    def _golden_probs(self) -> list[float]:
        """Golden-ratio probabilities for N words."""
        n = len(self._words)
        if n == 1:
            return [1.0]
        a = 1 / F
        probs = [a]
        remaining = 1 - a
        for _ in range(1, n - 1):
            p = remaining / F
            probs.append(p)
            remaining -= p
        probs.append(remaining)
        return probs

    def pick_word(self, gender: Gender) -> int:
        """Student/examiner picks a word index."""
        probs = self._golden_probs()
        if gender == Gender.FEMALE:
            probs = probs[::-1]  # girls prefer words closer to the end
        return random.choices(range(len(self._words)), weights=probs, k=1)[0]

    def examiner_correct_set(self) -> set[int]:
        """Examiner builds the set of correct answers (may be several)."""
        correct = set()
        while True:
            idx = self.pick_word(random.choice(list(Gender)))
            correct.add(idx)
            # 1/3 chance to pick another answer, or stop when all words are chosen
            if random.random() >= 1 / 3 or len(correct) == len(self._words):
                break
        return correct

    def evaluate(self, student: "Student") -> bool:
        """Did the student answer this question correctly?"""
        correct = self.examiner_correct_set()
        student_idx = self.pick_word(student.gender)
        return student_idx in correct

    def __repr__(self):
        return f"Question({self._text!r})"


class Student(Person):
    """A student. Stores their own result."""

    def __init__(self, name: str, gender: Gender):
        super().__init__(name, gender)
        self.status: Status = Status.IN_QUEUE
        self.finish_time: float = 0.0
        self.correct_questions: list[str] = []

    def mark(self, passed: bool, finish_time: float, correct_questions: list[str]):
        self.status = Status.PASSED if passed else Status.FAILED
        self.finish_time = finish_time
        self.correct_questions = correct_questions

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "finish_time": self.finish_time,
            "correct_questions": self.correct_questions,
        }


class Examiner(Person):
    """An examiner. Exam duration depends on the length of their name."""

    LUNCH_THRESHOLD = 30.0

    def __init__(self, name: str, gender: Gender):
        super().__init__(name, gender)
        self.total_students: int = 0
        self.failed_students: int = 0
        self.work_time: float = 0.0
        self.current_student: str | None = None
        self.on_break: bool = False
        self.finished: bool = False
        self._lunch_taken = False

    @property
    def exam_duration_range(self) -> tuple[float, float]:
        """E.g. Stepan (6 letters) → 5..7 seconds."""
        base = len(self.name)
        return (max(1.0, base - 1), base + 1)

    def exam_duration(self) -> float:
        lo, hi = self.exam_duration_range
        return random.uniform(lo, hi)

    def decide(self, student: Student, correct: int, incorrect: int) -> bool:
        """Pass/fail decision based on the examiner's mood."""
        roll = random.random()
        if roll < 1 / 8:
            return False              # bad mood — automatic fail
        if roll < 1 / 8 + 1 / 4:
            return True               # good mood — automatic pass
        return correct > incorrect    # neutral — compare performance

    def needs_lunch(self) -> bool:
        return not self._lunch_taken and self.work_time >= self.LUNCH_THRESHOLD

    def take_lunch(self) -> float:
        self._lunch_taken = True
        self.on_break = True
        duration = random.uniform(12, 18)
        return duration

    def to_dict(self) -> dict:
        return {
            "current_student": self.current_student,
            "total": self.total_students,
            "failed": self.failed_students,
            "work_time": self.work_time,
            "on_break": self.on_break,
            "finished": self.finished,
        }
