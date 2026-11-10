from repository import load_examiners, load_students, load_questions
from simulator import ExamSimulator


def main():
    # Load data from text files
    examiners = load_examiners()
    students = load_students()
    questions = load_questions()

    # Run the simulation
    sim = ExamSimulator(examiners, students, questions)
    sim.run()


if __name__ == "__main__":
    main()