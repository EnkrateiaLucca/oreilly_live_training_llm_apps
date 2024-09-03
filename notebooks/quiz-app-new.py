import os
import sys
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser

# Set the default encoding to utf-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def create_the_quiz_prompt_template():
    template = """
    You are an expert quiz maker for technical fields. Let's think step by step and
    create a quiz with {num_questions} {quiz_type} questions about the following concept/content: {quiz_context}.

    The format of the quiz could be one of the following:
    - Multiple-choice: 
    - Questions:
        <Question1>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
        <Question2>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
        ....
    - Answers:
        <Answer1>: <a|b|c|d>
        <Answer2>: <a|b|c|d>
        ....
    Example:
    - Questions:
    - 1. What is the time complexity of a binary search tree?
        a. O(n)
        b. O(log n)
        c. O(n^2)
        d. O(1)
    - Answers: 
        1. b
    - True-false:
        - Questions:
            <Question1>: <True|False>
            <Question2>: <True|False>
            .....
        - Answers:
            <Answer1>: <True|False>
            <Answer2>: <True|False>
            .....
    Example:
    - Questions:
        - 1. What is a binary search tree?
        - 2. How are binary search trees implemented?
    - Answers:
        - 1. True
        - 2. False
    - Open-ended:
    - Questions:
        <Question1>:
        <Question2>:
    - Answers:    
        <Answer1>:
        <Answer2>:
    Example:
    Questions:
        - 1. What is a binary search tree?
        - 2. How are binary search trees implemented?
        
        - Answers: 
            1. A binary search tree is a data structure that is used to store data in a sorted manner.
            2. Binary search trees are implemented using linked lists.
    """
    prompt = ChatPromptTemplate.from_template(template)
    prompt.format(num_questions=3, quiz_type="multiple-choice", quiz_context="Data Structures in Python Programming")
    
    return prompt


def create_quiz_chain(prompt_template, llm, openai_api_key):
    return prompt_template | llm |  StrOutputParser()

def split_questions_answers(quiz_response):
    parts = quiz_response.split("- Answers:")
    if len(parts) < 2:
        print("Error: quiz_response does not contain '- Answers:' marker.")
        return [], {}
    
    questions_parts = parts[0].split("- Questions:")
    if len(questions_parts) < 2:
        print("Error: quiz_response does not contain '- Questions:' marker.")
        return [], {}
    
    questions_part = questions_parts[1]
    answers_part = parts[1]
    
    questions = [q.strip() for q in questions_part.split("\n") if q.strip() != ""]
    answers = [a.strip() for a in answers_part.split("\n") if a.strip() != ""]

    structured_questions = []
    for question in questions:
        if ':' in question:
            question_parts = question.split(":")
            q_text = question_parts[0].strip()
            q_options = ':'.join(question_parts[1:]).strip()
            structured_questions.append({"question": q_text, "options": q_options})
        else:
            print(f"Skipping malformed question: {question}")
    
    structured_answers = {}
    for answer in answers:
        question_num, correct_option = answer.split(".")
        structured_answers[question_num.strip()] = correct_option.strip()
    
    return structured_questions, structured_answers


def main():
    st.title("Quiz App")
    st.write("This app generates a quiz based on a given context.")

    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if openai_api_key != "":
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return

    prompt_template = create_the_quiz_prompt_template()
    llm = ChatOpenAI(temperature=0.0, model="gpt-4")
    chain = create_quiz_chain(prompt_template, llm, openai_api_key)

    context = st.text_area("Enter the concept/context for the quiz")
    num_questions = st.number_input("Enter the number of questions", min_value=1, max_value=10, value=3)
    quiz_type = st.selectbox("Select the quiz type", ["multiple-choice", "true-false", "open-ended"])

    if st.button("Generate Quiz"):
        quiz_response = chain.invoke({"quiz_type": quiz_type, "num_questions": num_questions, "quiz_context": context})
        structured_questions, structured_answers = split_questions_answers(quiz_response)

        user_answers = {}

        if quiz_type == "multiple-choice":
            for question in structured_questions:
                q_num = question["question"].split()[0]
                st.write(f'{question["question"]}:')
                for option in question["options"].split(","):
                    option_key = f"{q_num}_{option.strip()[0]}"
                    user_answers[option_key] = st.checkbox(option.strip(), key=option_key)

        st.session_state["user_answers"] = user_answers
        st.session_state["structured_questions"] = structured_questions
        st.session_state["correct_answers"] = structured_answers
        
    if st.button("Check Answers"):
        score = 0
        for q_num, correct_answer in st.session_state["correct_answers"].items():
            if st.session_state["user_answers"].get(f"{q_num}_{correct_answer}", False):
                score += 1
        
        total_questions = len(st.session_state["correct_answers"])
        st.success(f"Your score is {score}/{total_questions}!")

if __name__ == "__main__":
    main()