import csv
from flask import Flask, render_template, request, session, redirect, url_for
from googlesearch import search
# from flask_session import Session

class Chatbot:
    def __init__(self, csv_file):
        self.questions = []
        self.answers = []
        try:
            with open(csv_file, "r", encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:  # Ensure there are at least two columns
                        self.questions.append(row[0].strip().lower())  # Convert questions to lowercase
                        self.answers.append(row[1].strip())
        except FileNotFoundError:
            print(f"Error: The file {csv_file} was not found.")
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")

    def answer_question(self, question):
        question = question.lower().strip()
        for i, csv_question in enumerate(self.questions):
            csv_words = set(csv_question.split())
            user_words = set(question.split())
            if csv_words & user_words:  # Check if there's any common word
                return self.answers[i]
        return None

def google_search(query, num_results=1):
    try:
        search_results = list(search(query, stop=num_results))
        return search_results
    except Exception as e:
        print(f"An error occurred during Google search: {e}")
        return []

def get_google_search_result(query):
    search_results = google_search(query, num_results=1)
    if search_results:
        return search_results[0]  # Return the first search result URL
    else:
        return "I couldn't find any relevant information for your query."

def chatbot_response(chatbot, user_input):
    if user_input.lower() == 'exit':
        return "Goodbye!"
    else:
        csv_response = chatbot.answer_question(user_input)
        if csv_response:
            return csv_response
        else:
            response = get_google_search_result(user_input)
            return response

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a random secret key
app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

chatbot = Chatbot("chat_bot.csv")

@app.route('/')
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html', chat_history=session['chat_history'])

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['user_input']
    response = chatbot_response(chatbot, user_input)
    session['chat_history'].append({'user': user_input, 'bot': response})
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
