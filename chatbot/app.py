#!/usr/bin/env python3
import gradio as gr
from resume_parser import extract_resume_text
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Extract and save resume text
RESUME_TEXT = extract_resume_text("resume.pdf")
with open("resume_text.txt", "w", encoding="utf-8") as f:
    f.write(RESUME_TEXT)

def ask_resume(question):
    """
    Answers questions using Cohere's API with resume context
    """
    
    prompt = f"""Use this resume content to answer questions. 
    If information isn't available, say "Not mentioned in my resume."

    RESUME CONTENT:
    {RESUME_TEXT}

    QUESTION: {question}
    ANSWER:"""
    
    try:
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=300,
            temperature=0.1,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        return response.generations[0].text.strip()
        
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio interface
iface = gr.Interface(
    fn=ask_resume,
    inputs=gr.Textbox(label="Ask about my resume", placeholder="What are your skills?"),
    outputs=gr.Textbox(label="Answer"),
    examples=[
        ["What are your technical skills?"],
        ["Describe your most recent work experience"],
        ["What certifications do you have?"]
    ],
    title="Resume Assistant (Powered by Cohere)",
    description="Ask me anything about my professional background!",
    allow_flagging="never"
)

iface.launch(
    server_name="0.0.0.0",
    server_port=7860
)