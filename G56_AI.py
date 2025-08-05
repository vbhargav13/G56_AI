# 📦 Importing necessary libraries
import tkinter as tk                      # For GUI window and widgets
from tkinter import messagebox, filedialog  # For pop-up alerts and file upload
import csv                                # For reading the training CSV file

# 🌐 Global Variables
knowledge_base = {}  # Dictionary to store question-answer pairs after training
trained = False      # To track whether PyBot has been trained

# 🔁 Function to reset the bot's memory and interface
def reset_bot():
    global trained, knowledge_base
    trained = False
    knowledge_base = {}  # Clear all knowledge
    answer_label.config(text="🤖 I don't know this yet!", fg="black")
    reaction_label.config(text="")  # Clear emoji reaction
    messagebox.showinfo("Reset", "PyBot has been reset. Please train me again.")

# 🧠 Function to calculate how similar two questions are (basic AI logic)
def calculate_confidence(user_question, known_question):
    user_words = set(user_question.lower().split())      # Words typed by user
    known_words = set(known_question.lower().split())    # Words from CSV
    if not user_words or not known_words:
        return 0
    overlap = user_words.intersection(known_words)       # Common words
    confidence = int((len(overlap) / len(known_words)) * 100)  # % match
    return confidence

# 📁 Function to load and train PyBot from a CSV file
def train_bot():
    global trained, knowledge_base
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv")]  # Only allow .csv files
    )
    if not file_path:
        return  # If user cancels file selection
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)  # Read file with header: question, answer
            for row in reader:
                question = row['question'].strip().lower()
                answer = row['answer'].strip()
                knowledge_base[question] = answer
        trained = True
        messagebox.showinfo("Training Complete", "🎉 PyBot is now trained and ready!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file:\n{str(e)}")

# ❓ Function to get PyBot's answer and display it with style
def get_answer():
    global trained
    user_question = question_entry.get().strip().lower()  # Get and clean input

    if not user_question:
        messagebox.showwarning("Input Error", "Please type a question.")
        return

    if not trained:
        # If not trained yet
        answer_label.config(text="🤖 I don't know this yet! Please train me first.", fg="black")
        reaction_label.config(text="😕")
        return

    # 🧠 Find the best match from the trained questions
    best_match = None
    highest_confidence = 0

    for known_question in knowledge_base:
        confidence = calculate_confidence(user_question, known_question)
        if confidence > highest_confidence:
            highest_confidence = confidence
            best_match = known_question

    # 🎯 Decide on the final response and style
    if highest_confidence == 0:
        response = "🤖 Hmm... I don't know the answer to that yet."
    else:
        response = knowledge_base[best_match]

    # 🎨 Decide color and emoji based on confidence level
    if highest_confidence >= 80:
        color = "green"
        reaction = "🤩"  # High confidence = Excited
    elif highest_confidence >= 50:
        color = "orange"
        reaction = "🙂"  # Medium confidence = Happy
    else:
        color = "red"
        reaction = "😕"  # Low confidence = Unsure

    # 🖼️ Update GUI with response, color, font, and reaction
    answer_label.config(
        text=f"{response}\n\n🧠 Confidence: {highest_confidence}%",
        fg=color,
        font=("Arial", 12, "bold")
    )
    reaction_label.config(text=reaction, font=("Arial", 28))

# 🖼️ GUI setup
window = tk.Tk()
window.title("🤖 PyBot - AI Assistant for Kids")
window.geometry("550x450")

# 🏷️ Title
title = tk.Label(window, text="🎙️ Ask PyBot Anything!", font=("Arial", 16, "bold"))
title.pack(pady=10)

# ✏️ Entry for user question
question_entry = tk.Entry(window, width=60, font=("Arial", 12))
question_entry.pack(pady=5)

# 📤 Label for displaying answers
answer_label = tk.Label(window, text="🤖 I don't know this yet!", font=("Arial", 12), wraplength=500)
answer_label.pack(pady=15)

# 😲 Emoji face reaction (optional and fun!)
reaction_label = tk.Label(window, text="", font=("Arial", 28))
reaction_label.pack()

# 🔘 Buttons for Train, Ask, and Reset
train_button = tk.Button(window, text="📂 Train Me (Upload CSV)", command=train_bot, bg="lightgreen", font=("Arial", 11))
train_button.pack(pady=5)

ask_button = tk.Button(window, text="❓ Get Answer", command=get_answer, bg="lightblue", font=("Arial", 11))
ask_button.pack(pady=5)

reset_button = tk.Button(window, text="🔁 Reset", command=reset_bot, bg="lightcoral", font=("Arial", 11))
reset_button.pack(pady=5)

# ▶️ Start the GUI event loop
window.mainloop()
