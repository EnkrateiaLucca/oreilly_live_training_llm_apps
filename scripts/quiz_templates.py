from langchain_core.prompts import ChatPromptTemplate

def create_multiple_choice_template():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'You are a quiz engine that generates\
            multiple-choice questions with answers according\
                to user input specifications.'),
        ('human', "Create a quiz with {num_questions} and this context {quiz_context}")
    ])
    
    return prompt

def create_true_false_template():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'You are a quiz engine that generates\
            true-false questions with answers according\
                to user input specifications.'),
        ('human', "Create a quiz with {num_questions} and this context {quiz_context}")
    ])
    
    return prompt

def create_open_ended_template():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'You are a quiz engine that generates\
            open-ended questions with answers according\
                to user input specifications.'),
        ('human', "Create a quiz with {num_questions} and this context {quiz_context}")
    ])
    
    return prompt