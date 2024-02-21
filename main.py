import random
import time
from datetime import datetime
from tkinter import Tk, Label, Button, Entry, StringVar

class QuizGUI:
    def __init__(self, quiz):
        self.quiz = quiz
        self.window = Tk()
        self.window.title("Quiz App")

        self.question_label = Label(self.window, text="", wraplength=400, justify="left")
        self.question_label.pack(pady=(10, 20))

        self.answer_var = StringVar()
        self.answer_entry = Entry(self.window, textvariable=self.answer_var)
        self.answer_entry.pack()

        self.submit_button = Button(self.window, text="Submit Answer", command=self.submit_answer)
        self.submit_button.pack(pady=(10, 10))

        self.feedback_label = Label(self.window, text="")
        self.feedback_label.pack(pady=(5, 10))

        self.score_label = Label(self.window, text="")
        self.score_label.pack(pady=(5, 10))

        self.next_button = Button(self.window, text="Next Question", command=self.next_question)
        self.next_button.pack(pady=(0, 10))

        self.retry_incorrect_button = Button(self.window, text="Retry Incorrect Questions", command=self.retry_incorrect)
        self.retry_incorrect_button.pack(pady=(10, 10))

        self.current_question_num = None

    def start_quiz(self):
        self.next_question()
        self.window.mainloop()

    def submit_answer(self):
        user_answer = self.answer_var.get().strip()
        correct, feedback = self.quiz.check_answer(self.current_question_num, user_answer)
        self.display_feedback(feedback)
        if correct:
            self.quiz.correct_answers += 1
            self.next_question()
        else:
            self.quiz.incorrect_responses.append(f"QUESTION {self.current_question_num} - Incorrect answer: {user_answer}")
            self.quiz.total_questions += 1
        self.update_score()
        self.answer_var.set("")

    def display_feedback(self, feedback):
        self.feedback_label.config(text=feedback)

    def next_question(self):
        if self.quiz.incorrect_questions_retry and self.quiz.retry_mode:
            self.current_question_num = self.quiz.incorrect_questions_retry.pop(0)
        else:
            self.current_question_num = self.quiz.rand_num_gen()
            self.quiz.used_numbers.add(self.current_question_num)
        question_text = self.quiz.get_question_text(self.current_question_num)
        self.question_label.config(text=question_text)
        self.answer_var.set("")
        self.display_feedback("")  # Clear feedback message

    def update_score(self):
        score_text = f"Score: {self.quiz.correct_answers}/{self.quiz.total_questions}"
        self.score_label.config(text=score_text)

    def retry_incorrect(self):
        if self.quiz.incorrect_responses:
            self.quiz.retry_mode = True
            self.quiz.prepare_retry_session()
            self.next_question()
        else:
            self.display_feedback("No incorrect answers to retry.")

class Quiz:
    def __init__(self, filename):
        self.filename = filename
        self.total_questions = 0
        self.correct_answers = 0
        self.used_numbers = set()
        self.incorrect_responses = []
        self.start_time = time.time()
        self.retry_mode = False
        self.incorrect_questions_retry = []

    def rand_num_gen(self):
        question_num = random.randint(1, 900)
        while question_num in self.used_numbers:
            question_num = random.randint(1, 900)
        return question_num

    def get_question_text(self, question_num):
        question_text = ""
        with open(self.filename, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if f"QUESTION {question_num}" in line:
                question_text += line.split("QUESTION")[1].strip() + "\n"

                for j in range(i+1, len(lines)):
                    if "Correct Answer" in lines[j]:
                        break
                    question_text += lines[j].strip() + "\n"
                break
        return question_text.strip()

    def check_answer(self, question_num, user_answer):
        with open(self.filename, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if f"QUESTION {question_num}" in line:
                for j in range(i+1, len(lines)):
                    if "Correct Answer" in lines[j]:
                        correct_answer = lines[j].split(":")[1].strip()
                        if user_answer.lower() == correct_answer.lower():
                            return True, "Correct! Moving to the next question."
                        else:
                            if not self.retry_mode:
                                self.incorrect_responses.append(f"QUESTION {question_num}")
                            return False, f"Incorrect! The correct answer is {correct_answer}."
        return False, "Error: Question not found."

    def prepare_retry_session(self):
        self.incorrect_questions_retry = [int(resp.split()[1]) for resp in self.incorrect_responses]
        self.incorrect_responses = []  # Clear incorrect responses for the retry session

if __name__ == '__main__':
    quiz = Quiz("aws_test.txt")
    quiz_gui = QuizGUI(quiz)
    quiz_gui.start_quiz()
