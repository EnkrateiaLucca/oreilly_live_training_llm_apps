# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "streamlit==1.37.0",
#     "langchain>=1.0",
#     "langchain-openai",
#     "pydantic>=2",
# ]
# ///
"""
Improved Quiz App (v2)
======================

Run it (avoids the streamlit websocket hang on this machine by pinning 1.37.0):

    uv run --with "streamlit==1.37.0" streamlit run quiz_app_v2.py

What's new vs v1:
- Uses langchain's `create_agent` (LangChain 1.x) instead of a bare chain.
- Quiz questions are produced by a generator agent with structured output.
- Per-question AI feedback (a coaching agent) powered by gpt-5.4-mini.
- Interactive single-page flow: generate -> answer -> grade -> coached feedback.
"""
import os
from typing import List

import streamlit as st
from langchain.agents import create_agent
from pydantic import BaseModel, Field

MODEL = "openai:gpt-5.4-mini"


# --------------------------------------------------------------------------- #
# Structured schema the generator agent must return
# --------------------------------------------------------------------------- #
class MCQuestion(BaseModel):
    question: str = Field(description="The question text")
    alternatives: List[str] = Field(description="3-4 answer options")
    correct_index: int = Field(description="0-based index of the correct alternative")
    explanation: str = Field(description="Short explanation of why the answer is correct")


class Quiz(BaseModel):
    topic: str = Field(description="The quiz topic")
    questions: List[MCQuestion] = Field(description="The list of multiple-choice questions")


# --------------------------------------------------------------------------- #
# Agents (cached so they aren't rebuilt on every Streamlit rerun)
# --------------------------------------------------------------------------- #
@st.cache_resource(show_spinner=False)
def get_generator_agent():
    return create_agent(
        MODEL,
        system_prompt=(
            "You are a quiz engine. Generate clear, unambiguous multiple-choice "
            "questions for the requested topic and difficulty. Exactly one "
            "alternative per question must be correct."
        ),
        response_format=Quiz,
    )


@st.cache_resource(show_spinner=False)
def get_feedback_agent():
    return create_agent(
        MODEL,
        system_prompt=(
            "You are an encouraging tutor. Given a quiz result, give the learner "
            "concise, specific, motivating feedback in 2-4 sentences. Mention what "
            "they got right, gently address mistakes, and suggest one next step. "
            "Use markdown and at most one emoji."
        ),
    )


def generate_quiz(topic: str, num_questions: int, difficulty: str) -> Quiz:
    agent = get_generator_agent()
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": (
                f"Create {num_questions} {difficulty} multiple-choice questions "
                f"about: {topic}"
            ),
        }]
    })
    return result["structured_response"]


def coach_feedback(quiz: Quiz, user_answers: List[int], score: int) -> str:
    agent = get_feedback_agent()
    lines = [f"Topic: {quiz.topic}", f"Score: {score}/{len(quiz.questions)}", ""]
    for i, q in enumerate(quiz.questions):
        picked = q.alternatives[user_answers[i]] if user_answers[i] is not None else "(blank)"
        correct = q.alternatives[q.correct_index]
        mark = "correct" if user_answers[i] == q.correct_index else "WRONG"
        lines.append(f"Q{i+1} [{mark}]: {q.question}")
        lines.append(f"  picked: {picked} | correct: {correct}")
    result = agent.invoke({"messages": [{"role": "user", "content": "\n".join(lines)}]})
    return result["messages"][-1].content


# --------------------------------------------------------------------------- #
# UI
# --------------------------------------------------------------------------- #
def main():
    st.set_page_config(page_title="Quiz App v2", page_icon="🧠")
    st.title("🧠 Quiz App v2")
    st.caption("Powered by LangChain `create_agent` + gpt-5.4-mini")

    api_key = st.sidebar.text_input("OpenAI API key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    st.session_state.setdefault("quiz", None)
    st.session_state.setdefault("graded", False)

    # --- Quiz setup ------------------------------------------------------- #
    with st.sidebar:
        st.header("Setup")
        topic = st.text_area("Topic / context", value="The Roman Empire")
        num_questions = st.slider("Number of questions", 1, 10, 3)
        difficulty = st.select_slider(
            "Difficulty", options=["easy", "medium", "hard"], value="medium"
        )
        if st.button("Generate quiz", type="primary", use_container_width=True):
            if not os.environ.get("OPENAI_API_KEY"):
                st.error("Enter your OpenAI API key first.")
            else:
                with st.spinner("Generating quiz..."):
                    st.session_state.quiz = generate_quiz(topic, num_questions, difficulty)
                    st.session_state.graded = False

    quiz: Quiz = st.session_state.quiz
    if quiz is None:
        st.info("Set up your quiz in the sidebar and hit **Generate quiz**.")
        return

    # --- Answer the quiz -------------------------------------------------- #
    st.subheader(f"Quiz: {quiz.topic}")
    with st.form("quiz_form"):
        user_answers = []
        for i, q in enumerate(quiz.questions):
            choice = st.radio(
                f"**Q{i+1}. {q.question}**",
                options=list(range(len(q.alternatives))),
                format_func=lambda idx, q=q: q.alternatives[idx],
                index=None,
                key=f"q_{i}",
            )
            user_answers.append(choice)
        submitted = st.form_submit_button("Submit answers", type="primary")

    if submitted:
        if any(a is None for a in user_answers):
            st.warning("Please answer every question before submitting.")
            return
        st.session_state.graded = True
        st.session_state.user_answers = user_answers

    # --- Results + AI feedback ------------------------------------------- #
    if st.session_state.graded:
        user_answers = st.session_state.user_answers
        score = sum(a == q.correct_index for a, q in zip(user_answers, quiz.questions))
        st.metric("Score", f"{score} / {len(quiz.questions)}")
        st.progress(score / len(quiz.questions))

        for i, q in enumerate(quiz.questions):
            right = user_answers[i] == q.correct_index
            with st.expander(
                f"{'✅' if right else '❌'} Q{i+1}. {q.question}", expanded=not right
            ):
                st.write(f"**Your answer:** {q.alternatives[user_answers[i]]}")
                st.write(f"**Correct answer:** {q.alternatives[q.correct_index]}")
                st.info(q.explanation)

        st.divider()
        st.subheader("💬 Coach feedback")
        with st.spinner("Asking your AI tutor..."):
            st.markdown(coach_feedback(quiz, user_answers, score))


if __name__ == "__main__":
    main()
