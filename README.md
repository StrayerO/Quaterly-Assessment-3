# Quaterly-Assessment-3
A sample quiz to demonstrate GUI, database, class, and repository skills.

The "Quiz Question Manager.py" file will create a database file if one doesn't already exist, then it will allow you to interact with it. The way it's built is a little tedious, but it works. Here's how.
When you run the program, you will see four options. You will type the corrosponding number with that option in order to proceed.
    1 = Add a question.
    2 = Remove a question.
    3 = Print questions.
    4 = End the program.

Then, each section works in its own way. 
    1
        You will be asked to enter a subject. Type the subject (the word or just the first letter of the subject will do), then type the question. These are multiple choice questions, so it will then ask you to type the correct answer. Next, you'll type three options for incorrect answers.

    2
        You will be asked to enter a subject. Type the subject (the word or just the first letter of the subject will do), then type the number for the question to be deleted. When a question is added, it is given a sequencial ID. That corrosponds to its placement. For example, the first question added is question 1 with sequential ID 1. The second question added is question 2. If you want to remove question 1, simply type "1". All following questions will automatically update their sequential IDs, so question 2 will become question 1 and so on.
    3
        You will be asked to enter a subject. Type the subject (the word or just the first letter of the subject will do), or leave it blank and press enter. If you enter a subject, only questions from that subject will be printed. If you leave it blank, all questions from all subjects will be printed.
    4
        This simply exists the program.