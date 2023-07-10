import random
import time
from datetime import datetime

class Quiz:
    def __init__(self, filename):
        self.filename = filename
        self.total_questions = 0
        self.correct_answers = 0
        self.used_numbers = set()
        self.incorrect_responses = []
        self.start_time = time.time()

    def rand_num_gen(self):
        question_num = random.randint(1, 900)
        while question_num in self.used_numbers:
            question_num = random.randint(1, 900)
        return question_num

    def ask_question(self, question_num):
        with open(self.filename, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if f"QUESTION {question_num}" in line:
                question_index = i
                print("\n" + line)

                for j in range(question_index+1, len(lines)):
                    if "Correct Answer" in lines[j]:
                        correct_answer = lines[j].split(":")[1].strip()
                        break
                    print(lines[j].strip())

                user_answer = input("Enter your answer: ").strip()

                if user_answer == correct_answer:
                    self.correct_answers += 1
                    print("Correct!")
                else:
                    print(f"Incorrect! The correct answer is {correct_answer}")
                    self.incorrect_responses.append(f"QUESTION {question_num} - Incorrect answer: {user_answer}")

                self.total_questions += 1
                break

    def print_scores(self):
        score = self.correct_answers / self.total_questions * 100
        elapsed_time = time.time() - self.start_time
        print(f"Score: {self.correct_answers}/{self.total_questions} ({score:.2f}%)")
        print(f"Total time taken: {elapsed_time//3600:.0f} hours and {(elapsed_time%3600)//60:.0f} minutes")

    def save_incorrect_responses(self):
        if self.incorrect_responses:
            # Get the current date and time
            now = datetime.now()

            # Format it as a string
            date_time_str = now.strftime("%Y%m%d_%H%M%S")

            # Use it in the filename
            filename = f"incorrect_responses_{date_time_str}.txt"

            with open(filename, "w") as file:
                for response in self.incorrect_responses:
                    file.write(response + "\n")

    def run(self):
        keep_going = True
        while keep_going:
            question_num = self.rand_num_gen()
            self.used_numbers.add(question_num)

            self.ask_question(question_num)
            self.print_scores()

            keep_going = input("\nDo you want to continue? (y/n) ") == 'y'

        self.save_incorrect_responses()


if __name__ == '__main__':
    quiz = Quiz("aws_test.txt")
    quiz.run()
