import multiprocessing as mp
import time
import random

from models import Student, Examiner, Question, Status
import renderer


def examiner_worker(examiner: Examiner, queue, lock, shared_stats, questions: list[Question], start_time: float):
    """Worker function executed in a separate process for each examiner."""
    while True:
        # lunch break
        if examiner.needs_lunch():
            duration = examiner.take_lunch()
            with lock:
                shared_stats[examiner.name] = examiner.to_dict()
            time.sleep(duration)
            examiner.work_time += duration
            examiner.on_break = False
            with lock:
                shared_stats[examiner.name] = examiner.to_dict()
            continue

        # take the next student from the shared queue
        with lock:
            if queue.empty():
                examiner.current_student = None
                examiner.finished = True
                shared_stats[examiner.name] = examiner.to_dict()
                return
            student: Student = queue.get()
            examiner.current_student = student.name
            shared_stats[examiner.name] = examiner.to_dict()

        # run the exam
        duration = examiner.exam_duration()
        picked = random.sample(questions, min(3, len(questions)))  # 3 questions from the bank
        correct = 0
        incorrect = 0
        correct_questions = []
        for q in picked:
            if q.evaluate(student):
                correct += 1
                correct_questions.append(q.text)
            else:
                incorrect += 1

        passed = examiner.decide(student, correct, incorrect)
        finish_time = time.time() - start_time
        student.mark(passed, finish_time, correct_questions)

        examiner.total_students += 1
        if not passed:
            examiner.failed_students += 1

        time.sleep(duration)
        examiner.work_time += duration
        examiner.current_student = None

        with lock:
            shared_stats[student.name] = student.to_dict()
            shared_stats[examiner.name] = examiner.to_dict()


class ExamSimulator:
    """Orchestrator: starts processes, refreshes the screen, collects results."""

    def __init__(self, examiners: list[Examiner], students: list[Student], questions: list[Question]):
        self.examiners = examiners
        self.students = students
        self.questions = questions
        self.manager = mp.Manager()
        self.queue = self.manager.Queue()
        self.lock = self.manager.Lock()
        self.shared_stats = self.manager.dict()

    # run

    def run(self):
        """Fill the shared queue with students and init stats"""
        for s in self.students:
            self.queue.put(s)
            self.shared_stats[s.name] = s.to_dict()

        for e in self.examiners:
            self.shared_stats[e.name] = e.to_dict()

        start_time = time.time()
        processes = [
            mp.Process(
                target=examiner_worker,
                args=(e, self.queue, self.lock, self.shared_stats, self.questions, start_time),
            )
            for e in self.examiners
        ]
        for p in processes:
            p.start()

        # Live refresh while at least one examiner is still working
        while any(p.is_alive() for p in processes):
            self._sync()
            self._render_during(start_time)
            time.sleep(0.5)

        for p in processes:
            p.join()

        total_time = time.time() - start_time
        self._sync()
        self._render_after(total_time)


    def _sync(self):
        """Copy data from the shared dict back into the objects."""
        for s in self.students:
            d = self.shared_stats.get(s.name, {})
            if d:
                s.status = Status(d["status"])
                s.finish_time = d["finish_time"]
                s.correct_questions = d["correct_questions"]
        for e in self.examiners:
            d = self.shared_stats.get(e.name, {})
            if d:
                e.current_student = d["current_student"]
                e.total_students = d["total"]
                e.failed_students = d["failed"]
                e.work_time = d["work_time"]
                e.on_break = d["on_break"]


    def _render_during(self, start_time: float):
        renderer.clear_screen()
        print(renderer.render_students_during(self.students))
        print(renderer.render_examiners_during(self.examiners))
        in_queue = sum(1 for s in self.students if s.status == Status.IN_QUEUE)
        print(f"\nRemaining in queue: {in_queue} out of {len(self.students)}")
        print(f"Time since exam started: {time.time() - start_time:.2f}")

    def _render_after(self, total_time: float):
        renderer.clear_screen()

        order = {"Passed": 0, "Failed": 1}
        rows = sorted(
            [[s.name, s.status.value] for s in self.students],
            key=lambda r: order.get(r[1], 2),
        )
        print(renderer.render_table(["Student", "Status"], rows))

        ex_rows = [
            [e.name, e.total_students, e.failed_students, f"{e.work_time:.2f}"]
            for e in self.examiners
        ]
        print(renderer.render_table(
            ["Examiner", "Total students", "Failed", "Work time"], ex_rows))

        print(f"\nTime from exam start to finish: {total_time:.2f}")

        passed = sorted(
            [(s.name, s.finish_time) for s in self.students if s.status == Status.PASSED],
            key=lambda x: x[1],
        )
        top_students = self._top_by(passed)

        ex_rates = sorted(
            [(e.name, e.failed_students / e.total_students if e.total_students else 1.0)
             for e in self.examiners],
            key=lambda x: x[1],
        )
        best_rate = ex_rates[0][1] if ex_rates else 1.0
        top_examiners = [n for n, r in ex_rates if abs(r - best_rate) < 1e-6 and r < 1.0]
        if not top_examiners:
            top_examiners = ["-"]

        failed = sorted(
            [(s.name, s.finish_time) for s in self.students if s.status == Status.FAILED],
            key=lambda x: x[1],
        )
        expelled = self._top_by(failed)

        best_questions = self._best_questions()

        top_students_str = ", ".join(top_students) if top_students else "-"
        top_examiners_str = ", ".join(top_examiners) if top_examiners else "-"
        expelled_str = ", ".join(expelled) if expelled else "-"
        best_questions_str = ", ".join(best_questions) if best_questions else "-"

        print("Top-performing students: " + top_students_str)
        print("Top examiners: " + top_examiners_str)
        print("Students to be expelled: " + expelled_str)
        print("Best questions: " + best_questions_str)

        total = len(self.students)
        passed_n = sum(1 for s in self.students if s.status == Status.PASSED)
        result = "Exam passed" if total and passed_n / total > 0.85 else "Exam failed"
        print(f"Result: {result}")


    @staticmethod
    def _top_by(pairs: list[tuple[str, float]]) -> list[str]:
        """Return all names tied for the best (minimum) value."""
        if not pairs:
            return []
        best = pairs[0][1]
        return [name for name, val in pairs if abs(val - best) < 1e-6]

    def _best_questions(self) -> list[str]:
        """Questions answered correctly by the highest number of students."""
        counter: dict[str, int] = {}
        for s in self.students:
            for q in s.correct_questions:
                counter[q] = counter.get(q, 0) + 1
        if not counter:
            return []
        best = max(counter.values())
        return [q for q, c in counter.items() if c == best]