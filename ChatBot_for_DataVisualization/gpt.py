import pandas as pd
import matplotlib.pyplot as plt
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")

# Load data
df = pd.read_csv("Students_Attitude_Dataset new.csv")

# Preprocess Likert scale responses
likert_cols = [col for col in df.columns if col.startswith("Q5.")]
likert_data = df[likert_cols]

likert_scale_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}
likert_numeric = likert_data.replace(likert_scale_map).infer_objects()

# Plot average Likert responses
plt.figure(figsize=(10, 6))
likert_numeric.mean().plot(kind='bar', color='skyblue')
plt.title("Average Likert Scale Responses per Question")
plt.ylabel("Average Score")
plt.xlabel("Question")
plt.ylim(1, 5)
plt.grid(axis='y')
plt.show()

# Create dataset summary
df_shape = df.shape
df_head = df.head(3).to_string()

likert_avg_str = ""
for question, avg_score in list(likert_numeric.mean().items())[:5]:
    likert_avg_str += f"{question}: {avg_score:.2f}\n"

# Build prompt template
prompt_template = ChatPromptTemplate.from_template(
    """
You are a helpful data assistant. Here is a summary of the dataset:

Shape: {shape}
Head:
{head}

Likert Averages:
{likert_avg}

Answer the following question about the dataset:
{question}
"""
)

# Initialize the Groq LLM
chat = ChatGroq(
    model="Gemma2-9b-It",
    api_key=api_key
)

# Initial user instruction
print("Dataset loaded. You can now ask questions about it. Type 'exit' to quit.\n")

# Chat loop
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Exiting chat. Goodbye!")
        break

    # Format and send prompt using template
    prompt = prompt_template.format_messages(
        shape=df_shape,
        head=df_head,
        likert_avg=likert_avg_str,
        question=user_input
    )
    response = chat.invoke(prompt)
    print("Groq:", response.content)
