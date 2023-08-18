from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import streamlit as st


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
    - 1. What is a binary search tree?
    - 2. How are binary search trees implemented?
    
    - Answers: 
        1. A binary search tree is a data structure that is used to store data in a sorted manner.
        2. Binary search trees are implemented using linked lists.
"""
    prompt = PromptTemplate.from_template(template)
    prompt.format(num_questions=3, quiz_type="multiple-choice", quiz_context="Data Structures in Python Programming")
    
    return prompt


def create_quiz_chain(prompt_template,llm):
    return LLMChain(llm=llm, prompt=prompt_template)

def split_questions_answers(quiz_response):
    """"""
    questions = quiz_response.split("Answers:")[0]
    answers = quiz_response.split("Answers:")[1]
    return questions, answers


def main():
    st.title("Quiz App")
    st.write("This app generates a quiz based on a given context.")
    prompt_template = create_the_quiz_prompt_template()
    llm = ChatOpenAI()
    chain = create_quiz_chain(prompt_template,llm)
    context = st.text_area("Enter the concept/context for the quiz")
    num_questions = st.number_input("Enter the number of questions",min_value=1,max_value=10,value=3)
    quiz_type = st.selectbox("Select the quiz type",["multiple-choice","true-false", "open-ended"])
    if st.button("Generate Quiz"):
        quiz_response = chain.run(num_questions=num_questions, quiz_type=quiz_type, quiz_context=context)
        st.write("Quiz Generated!")        
        questions,answers = split_questions_answers(quiz_response)
        st.session_state.answers = answers
        st.session_state.questions = questions
        st.write(questions)
    if st.button("Show Answers"):
        st.write(st.session_state.questions)
        st.write("----")
        st.write(st.session_state.answers)
        

if __name__=="__main__":
    main()




