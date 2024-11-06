# This file creates the database file (if it doesn't already exist), and allows the user to modify it.
import sqlite3

class Questions:
    def __init__(self, db_name="Quiz Questions.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """
        Creates tables for each subject if they don't already exist.
        """
        subjects = ["Math", "Science", "English", "History", "Geography"]
        with self.conn:
            for subject in subjects:
                self.conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {subject} (
                    id INTEGER PRIMARY KEY,
                    question TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    wrong_answer1 TEXT NOT NULL,
                    wrong_answer2 TEXT NOT NULL,
                    wrong_answer3 TEXT NOT NULL
                )''')

    def add_q(self, subject, question, correct_answer, wrong_answers):
        """
        Adds a question to the specified subject table.
        """
        subject = self.normalize_subject(subject)
        if not subject:
            return

        with self.conn:
            self.conn.execute(f'''
            INSERT INTO {subject} (question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3)
            VALUES (?, ?, ?, ?, ?)''', (question, correct_answer, wrong_answers[0], wrong_answers[1], wrong_answers[2]))
        print(f"\nQuestion added to {subject}\n")

    def remove_q(self, subject, q_id):
        """
        Removes a question from the specified subject table based on its ID.
        """
        subject = self.normalize_subject(subject)
        if not subject:
            return

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f'''
            DELETE FROM {subject} WHERE id = ?''', (q_id,))
            if cursor.rowcount == 0:
                print(f"\nNo question found with ID: {q_id} in {subject}\n")
            else:
                print(f"\nQuestion removed from {subject}\n")
                self.update_ids(subject)

    def update_ids(self, subject):
        """
        Updates the IDs of questions in the specified subject table to be sequential.
        """
        with self.conn:
            cursor = self.conn.cursor()
            questions = cursor.execute(f'''
            SELECT id, question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3 FROM {subject}
            ORDER BY id''').fetchall()

            # Clear table
            cursor.execute(f'DELETE FROM {subject}')

            # Reinsert questions with updated IDs
            for i, q in enumerate(questions, start=1):
                cursor.execute(f'''
                INSERT INTO {subject} (id, question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3)
                VALUES (?, ?, ?, ?, ?, ?)''', (i, q[1], q[2], q[3], q[4], q[5]))

    def read_q(self, subject=None):
        """
        Prints all questions in the specified subject table or all subjects if no subject is specified.
        """
        with self.conn:
            try:
                if subject:
                    subject = self.normalize_subject(subject)
                    if not subject:
                        return

                    questions = self.conn.execute(f"SELECT * FROM {subject}").fetchall()
                    if not questions:
                        print(f"\nNo questions found in {subject}\n")
                    else:
                        print(f"\nQuestions in {subject}:")
                        for q in questions:
                            print(q)
                        print()
                else:
                    for sub in ["Math", "Science", "English", "History", "Geography"]:
                        questions = self.conn.execute(f"SELECT * FROM {sub}").fetchall()
                        if not questions:
                            print(f"\nNo questions found in {sub}\n")
                        else:
                            print(f"\nQuestions in {sub}:")
                            for q in questions:
                                print(q)
                            print()
            except Exception as e:
                print(f"\nAn error occurred: {e}\n")

    def normalize_subject(self, subject):
        """
        Converts shorthand and case-insensitive subject input to the correct table name.
        """
        subject_map = {
            'm': 'Math',
            'math': 'Math',
            's': 'Science',
            'science': 'Science',
            'e': 'English',
            'english': 'English',
            'h': 'History',
            'history': 'History',
            'g': 'Geography',
            'geography': 'Geography'
        }
        normalized = subject_map.get(subject.lower())
        if not normalized:
            print(f"\nInvalid subject: {subject}\n")
        return normalized

def main():
    db = Questions()
    
    while True:
        print("\nQuiz Question Manager")
        print("1. Add Question")
        print("2. Remove Question")
        print("3. Read Questions")
        print("4. Exit")
        
        choice = input("\nChoose an option: ")
        
        if choice == '1':
            subject = input("\nEnter subject (or shorthand letter): ")
            question = input("Enter question: ")
            correct_answer = input("Enter correct answer: ")
            wrong_answers = [
                input("Enter wrong answer 1: "),
                input("Enter wrong answer 2: "),
                input("Enter wrong answer 3: ")
            ]
            db.add_q(subject, question, correct_answer, wrong_answers)
        
        elif choice == '2':
            subject = input("\nEnter subject (or shorthand letter): ")
            q_id = int(input("Enter question ID to remove: "))
            db.remove_q(subject, q_id)
        
        elif choice == '3':
            subject = input("\nEnter subject to read (leave blank for all, or use shorthand letter): ")
            if subject.strip() == "":
                subject = None
            db.read_q(subject)
        
        elif choice == '4':
            print("\nExiting Quiz Question Manager.")
            break
        
        else:
            print("\nInvalid option. Please try again.\n")

if __name__ == "__main__":
    main()
