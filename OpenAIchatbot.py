import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# Load environment variables
load_dotenv()

# LangSmith Tracking
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user question."),
        ("user", "Question: {question}"),
    ]
)


# Function to generate response
def generate_response(question, model, temperature, max_tokens):

    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    answer = chain.invoke({"question": question})

    return answer


# Streamlit UI
st.title("Q&A Chatbot with OpenAI")


# Sidebar Settings
st.sidebar.title("Model Settings")

model = st.sidebar.selectbox(
    "Select OpenAI Model",
    ["gpt-4o","gpt-4o-mini","gpt-4-turbo","gpt-3.5-turbo"]
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.5
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    min_value=50,
    max_value=300,
    value=150
)


# Main Chat Interface
st.write("Go ahead and ask any question!")

user_input = st.text_input("You:")


if user_input:
    response = generate_response(user_input, model, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter a question to get a response.")