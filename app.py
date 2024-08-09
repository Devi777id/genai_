import os
import json
import traceback
import pandas as pd
import sys
from dotenv import load_dotenv
from src.mcqgenr.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenr.mcqgen import generate_evaluate_chain
from src.mcqgenr.logger import logging

# Loading json file
with open(r"C:\Users\hp\genai\response.json", 'r') as file:
    RESPONSE_JSON = json.load(file)

# Creating a title for the app
st.title('MCQs Generator')

# Create a form using st.form
with st.form("user_inputs"):
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF or text file")

    # Input fields
    mcq_count = st.number_input("Number of MCQs", min_value=3, max_value=50)

    # Subject
    subject = st.text_input("Insert subject", max_chars=20)

    # Quiz tone
    tone = st.text_input("Complexity level of questions", max_chars=20, placeholder="simple")
    
    # Add button
    button = st.form_submit_button("Create MCQs")

# Check if the button is clicked
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Loading..."):
        try:
            text = read_file(uploaded_file)
            # Count tokens
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,  # Changed from "number" to "numbers"
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
        except Exception as e:
            st.error("Error occurred")
            traceback.print_exception(type(e), e, e.__traceback__)
        else:
            st.write(f"Total tokens used: {cb.total_tokens}")
            if isinstance(response, dict):
                # Extract quiz from response
                quiz = response.get("Quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = range(1, len(df) + 1)  # Correctly set the DataFrame index
                        st.table(df)
                        # Display the review in the text area
                        st.text_area(label="Review", value=response.get('review', 'No review available'))
                    else:
                        st.error("Error in table data")
                else:
                    st.write(response)
