# This file allows the user to take a quiz.

import sqlite3
import tkinter as tk
from tkinter import ttk
import random

class QuizApp:
    def __init__(self, root, db_name="Quiz Questions.db"):
        self.conn = sqlite3.connect(db_name)
        self.root = root
        self.root.title("Quiz Application")
        self.subject = None
        self.questions = []
        self.user_answers = {}
        self.correct_answers = {}

        self.create_welcome_window()

    def create_welcome_window(self):
        """
        Creates the welcome window where the user can choose a subject and start the quiz.
        """
        self.clear_screen()
        
        welcome_label = tk.Label(self.root, text="Welcome to the Quiz Application!", font=("Arial", 18))
        welcome_label.pack(pady=20)
        
        subject_label = tk.Label(self.root, text="Choose a subject to start the quiz:", font=("Arial", 14))
        subject_label.pack(pady=10)
        
        subjects = ["Math", "Science", "English", "History", "Geography"]
        self.subject_var = tk.StringVar(value="Math")
        
        for subject in subjects:
            tk.Radiobutton(self.root, text=subject, variable=self.subject_var, value=subject, font=("Arial", 12)).pack(anchor=tk.W)
        
        start_button = tk.Button(self.root, text="Start Quiz", command=self.start_quiz, font=("Arial", 12))
        start_button.pack(pady=20)
    
    def start_quiz(self):
        """
        Starts the quiz by fetching questions and displaying the quiz window.
        """
        self.subject = self.subject_var.get()
        self.questions = self.get_questions(self.subject)
        self.user_answers = {}
        self.correct_answers = {question[0]: question[2] for question in self.questions}
        
        if not self.questions:
            tk.messagebox.showinfo("Info", f"No questions available for {self.subject}")
            return

        # Shuffle questions
        random.shuffle(self.questions)
        
        self.create_quiz_window()
    
    def get_questions(self, subject):
        """
        Fetches questions for the selected subject from the database.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT id, question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3 FROM {subject}")
        return cursor.fetchall()
    
    def create_scrollable_frame(self):
        """
        Creates a scrollable frame.
        """
        container = ttk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        return scrollable_frame
    
    def create_quiz_window(self):
        """
        Creates the quiz window with questions and answer choices.
        """
        self.clear_screen()
        
        scrollable_frame = self.create_scrollable_frame()
        
        for question in self.questions:
            q_id, q_text, correct_answer, *wrong_answers = question
            tk.Label(scrollable_frame, text=q_text, font=("Arial", 12)).pack(anchor=tk.W, pady=5)
            
            answer_var = tk.StringVar(value="None")
            self.user_answers[q_id] = answer_var
            
            answer_options = [correct_answer] + wrong_answers
            random.shuffle(answer_options)
            for answer in answer_options:
                tk.Radiobutton(scrollable_frame, text=answer, variable=answer_var, value=answer, font=("Arial", 10)).pack(anchor=tk.W)
        
        submit_button = tk.Button(self.root, text="Submit", command=self.submit_quiz, font=("Arial", 12))
        submit_button.pack(pady=20)
    
    def submit_quiz(self):
        """
        Submits the quiz, calculates the score, and displays the results.
        """
        score = sum(1 for q_id, answer in self.user_answers.items() if answer.get() == self.correct_answers[q_id])
        total_questions = len(self.questions)
        
        self.create_result_window(score, total_questions)
    
    def create_result_window(self, score, total_questions):
        """
        Creates the result window showing the user's score and answers.
        """
        self.clear_screen()
        
        result_label = tk.Label(self.root, text=f"You scored {score} out of {total_questions}", font=("Arial", 18))
        result_label.pack(pady=20)
        
        scrollable_frame = self.create_scrollable_frame()
        
        for question in self.questions:
            q_id, q_text, correct_answer, *wrong_answers = question
            user_answer = self.user_answers[q_id].get()
            tk.Label(scrollable_frame, text=f"Question: {q_text}", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
            tk.Label(scrollable_frame, text=f"Your answer: {user_answer}", font=("Arial", 10), fg="red" if user_answer != correct_answer else "green").pack(anchor=tk.W)
            tk.Label(scrollable_frame, text=f"Correct answer: {correct_answer}", font=("Arial", 10), fg="green").pack(anchor=tk.W, pady=5)
        
        result_frame = ttk.Frame(self.root)
        result_frame.pack(pady=20)
        
        retry_button = tk.Button(result_frame, text="Choose Another Quiz", command=self.create_welcome_window, font=("Arial", 12))
        retry_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        exit_button = tk.Button(result_frame, text="Exit", command=self.root.quit, font=("Arial", 12))
        exit_button.pack(side=tk.RIGHT, padx=20, pady=20)
    
    def clear_screen(self):
        """
        Clears all widgets from the root window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
