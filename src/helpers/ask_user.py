import json
from datetime import datetime
from providers import MakeLLM, InintLMM
from helpers import load_prompt
import os

PORMPT_PATH = os.path.join(
    os.path.dirname(__file__),      
    "..",                           
    "prompts",
    "clarification_questions.yaml"
)
PORMPT_PATH = os.path.abspath(PORMPT_PATH)  
current_date = datetime.now().strftime("%Y-%m-%d")

def ask_user_for_clarification(user_question: str, llm_setting: InintLMM):
    """
    This function sends a request to the LLM to ask the user for clarification on their query.
    It formats the request with the current date and the user's question.
    """
    llm = MakeLLM(llm_setting).get_llm()

    system_prompt = load_prompt(
    PORMPT_PATH,
    current_date=current_date,
    user_question=user_question
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": system_prompt}
    ]

    try:
        response = llm.call(messages=messages)      # Make the LLM call with JSON response format
        response = response.strip().removeprefix("```json").removesuffix("```").strip() 
        response = json.loads(response)                     # Parse the JSON response
        return response['clarification']
    except Exception as e:
        print("❌ Error while parsing LLM response:", e)
        return None
