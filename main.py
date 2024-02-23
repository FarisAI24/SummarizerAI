from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import openai
import streamlit as st

# Load the environment variables
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Read all text files in the data directory
def read_files():
    text = ""
    # Get the current working directory
    dir = os.path.join(os.getcwd(), "data")
    for file in os.listdir(dir):
        # Check if the file is a text file
        if file.endswith(".txt"):
            with open(os.path.join(dir, file), "r") as f:
                # Read the file and append the content to the text variable
                text += f.read()
    return text

# Get response from OpenAI
def get_response(text):
    # Set the prompt
    prompt = f""" 
    You are an expert in summarizing text. You will be given a text delimited by four astericks. 
    Your task is to summarize the text. Make sure to capture the main points, key arguments,and any supporting evidence presented in the article.
    Your summary should be informative and well-structured, ideally consiting of 3-5 sentences.
    
    text: ****{text}****
    """
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
                "role": "system",
                "content": prompt
            }
        ]
    )
    return response["choices"][0]["message"]["content"]

def text_from_pdf(pdf):
    # Load PDF file
    reader = PdfReader(pdf)
    # Extract text from PDF
    text = ""
    for page in reader.pages:
        content += page.extract_text()
        # Check if the content is not empty
        if content:
            text += content
    return text

def main():
    st.set_page_config(
    page_title="Summarizer AI", 
    page_icon="📖",
    )

    st.title("Summarizer AI")
    st.write("This app uses the latest AI to summarize text and PDF files.")
    st.divider()

    # Options for the user to choose from
    options = ["Text", "PDF"]
    choice = st.radio("Choose Input Type", options)

    if choice == "Text":
        # Get the text from the user
        text = st.text_area("Enter the text you want to summarize", "")
        # Check if the user has entered text and clicked the button
        if st.button("Summarize") and text != "":
            # Get the response from OpenAI
            response = get_response(text)
            st.subheader("Summary")
            st.markdown(f"> {response}")
        else:
            st.error("Please enter the text you want to summarize.")
    else:
        # Get the PDF file from the user
        pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
        # Check if the user has uploaded a file and clicked the button
        if st.button("Summarize") and pdf is not None:
            # Get the text from the PDF file
            text = text_from_pdf(pdf)
            # Get the response from OpenAI
            response = get_response(text)
            st.subheader("Summary")
            st.markdown(f"> {response}")
        else:
            st.error("Please upload a PDF file.")
        
if __name__ == "__main__":
    main()