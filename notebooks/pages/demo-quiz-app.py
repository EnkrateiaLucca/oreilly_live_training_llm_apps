import streamlit as st
import json
import csv
import io
import pandas as pd
import plotly.express as px
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
import hashlib

# Add OpenAI client initialization
client = OpenAI()

# Add Pydantic model for quiz structure
class QuizQuestion(BaseModel):
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., description="List of possible answers")
    correctAnswer: int = Field(..., description="Index of the correct answer (0-based)")

class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(..., description="List of quiz questions")

# Add function to generate quiz from content
def generate_quiz_from_content(content: str, num_questions: int = 5) -> List[dict]:
    response = client.beta.chat.completions.parse(
        model="gpt-4o",  # or your preferred model
        messages=[
            {
                "role": "system",
                "content": f"Generate a quiz with {num_questions} multiple-choice questions based on the following content. Each question should have 4 options."
            },
            {"role": "user", "content": content}
        ],
        response_format=Quiz
    )
    
    return response.choices[0].message.parsed.questions

# Add function to generate quiz identifier
def generate_quiz_id(questions):
    # Create a string representation of the questions
    quiz_str = json.dumps(questions, sort_keys=True)
    # Generate a hash of the quiz content
    return hashlib.md5(quiz_str.encode()).hexdigest()

# Initialize all session state variables at the start
if 'questions' not in st.session_state:
    st.session_state['questions'] = []
if 'quiz_started' not in st.session_state:
    st.session_state['quiz_started'] = False
if 'current_question' not in st.session_state:
    st.session_state['current_question'] = 0
if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'total_questions' not in st.session_state:
    st.session_state['total_questions'] = 0
if 'user_answers' not in st.session_state:
    st.session_state['user_answers'] = []
if 'current_quiz_id' not in st.session_state:
    st.session_state['current_quiz_id'] = None
if 'score_history' not in st.session_state:
    st.session_state['score_history'] = {}

st.title('Modern Quiz App')

# Add sidebar for AI quiz generation
with st.sidebar:
    use_ai_generation = st.checkbox("Generate Quiz with AI")
    
# Add AI quiz generation section
if use_ai_generation:
    st.subheader("Generate Quiz from Content")
    content = st.text_area("Paste your content here", height=200)
    num_questions = st.slider("Number of questions", min_value=3, max_value=10, value=5)
    
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            try:
                generated_questions = generate_quiz_from_content(content, num_questions)
                # Convert to the format expected by the app
                quiz_json = [
                    {
                        "question": q.question,
                        "options": q.options,
                        "correctAnswer": q.correctAnswer
                    } for q in generated_questions
                ]
                # Generate new quiz ID and reset score history for this quiz
                new_quiz_id = generate_quiz_id(quiz_json)
                st.session_state['current_quiz_id'] = new_quiz_id
                st.session_state['score_history'][new_quiz_id] = []
                
                st.session_state['questions'] = quiz_json
                st.session_state['total_questions'] = len(quiz_json)
                st.session_state['quiz_started'] = True
                st.session_state['current_question'] = 0
                st.session_state['score'] = 0
                st.session_state['user_answers'] = []
                st.rerun()
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")

uploaded_file = st.file_uploader('Choose a quiz JSON file', type=['json'])

if uploaded_file is not None and not st.session_state['quiz_started']:
    # Read the JSON file
    try:
        questions = json.load(uploaded_file)
        st.session_state['questions'] = questions
        st.session_state['total_questions'] = len(questions)
        # Generate new quiz ID and reset score history for this quiz
        new_quiz_id = generate_quiz_id(questions)
        if new_quiz_id != st.session_state['current_quiz_id']:
            st.session_state['current_quiz_id'] = new_quiz_id
            st.session_state['score_history'][new_quiz_id] = []
        
        if st.button('Start Quiz'):
            st.session_state['quiz_started'] = True
            st.session_state['current_question'] = 0
            st.session_state['score'] = 0
            st.session_state['user_answers'] = []
    except Exception as e:
        st.error('Error parsing file. Please ensure it\'s a valid JSON.')

if st.session_state['quiz_started']:
    current_q = st.session_state['current_question']
    questions = st.session_state['questions']
    total_q = st.session_state['total_questions']
    
    if current_q < total_q:
        question = questions[current_q]
        st.subheader(f"Question {current_q + 1}: {question['question']}")
        options = question['options']
        selection_key = f"question_{current_q}_selection"
        selected_option = st.radio("Select an option", options, key=selection_key)
        
        if st.button('Submit Answer'):
            # Get the selected option from session state
            selected_option = st.session_state[selection_key]
            # Store the user's answer
            st.session_state['user_answers'].append(selected_option)
            correct_answer = options[question['correctAnswer']]
            if selected_option == correct_answer:
                st.session_state['score'] += 1
            st.session_state['current_question'] += 1
            # Clear the selection for next question
            del st.session_state[selection_key]
            st.rerun()
    else:
        # Quiz is over, show results
        st.subheader('Quiz Results')
        score = st.session_state['score']
        total = st.session_state['total_questions']
        
        # Store score in history with percentage for current quiz
        score_percentage = (score / total) * 100
        current_quiz_id = st.session_state['current_quiz_id']
        st.session_state['score_history'][current_quiz_id].append({
            'attempt': len(st.session_state['score_history'][current_quiz_id]) + 1,
            'score': score_percentage
        })
        
        st.write(f"Score: {score} / {total} ({score_percentage:.1f}%)")
        
        # Add score history visualization for current quiz only
        current_history = st.session_state['score_history'][current_quiz_id]
        if len(current_history) > 1:  # Only show if there's more than one attempt
            st.subheader("Your Progress")
            history_df = pd.DataFrame(current_history)
            fig = px.line(history_df, x='attempt', y='score',
                         title='Score History',
                         labels={'attempt': 'Attempt Number', 'score': 'Score (%)'},
                         markers=True)
            fig.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig)

        # Add button to start new attempt
        if st.button('Start New Attempt'):
            st.session_state['current_question'] = 0
            st.session_state['score'] = 0
            st.session_state['user_answers'] = []
            st.rerun()

        # Show detailed feedback
        user_answers = st.session_state['user_answers']
        for idx, question in enumerate(questions):
            st.write(f"**Question {idx + 1}:** {question['question']}")
            st.write(f"**Your answer:** {user_answers[idx]}")
            correct_answer = question['options'][question['correctAnswer']]
            st.write(f"**Correct answer:** {correct_answer}")
            if user_answers[idx] == correct_answer:
                st.success('Correct')
            else:
                st.error('Incorrect')
            st.markdown("---")
        
        # Prepare CSV data
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Question', 'Your Answer', 'Correct Answer', 'Result'])
        for idx, question in enumerate(questions):
            user_answer = user_answers[idx]
            correct_answer = question['options'][question['correctAnswer']]
            is_correct = 'Correct' if user_answer == correct_answer else 'Incorrect'
            writer.writerow([question['question'], user_answer, correct_answer, is_correct])
        csv_data = output.getvalue()
        st.download_button(label='Download Results (CSV)', data=csv_data, file_name='quiz_results.csv', mime='text/csv')
