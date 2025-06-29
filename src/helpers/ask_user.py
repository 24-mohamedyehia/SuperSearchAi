import requests
import json
from datetime import datetime
from .config import get_settings

LLM_API_KEY= get_settings().LLM_API_KEY
current_date = datetime.now().strftime("%Y-%m-%d")

def ask_user_for_clarification(user_question: str):
    """
    This function sends a request to the LLM to ask the user for clarification on their query.
    It formats the request with the current date and the user's question.
    """

    system_prompt = f"""
    Receive this query from the user with The current date is {current_date}.

    ### User Question:
    {user_question}

    ### Instructions:
    - If it's unclear, ask clarifying questions for user to get more detail to get the best search results.
    - ask all questions to user in one question. Don't ask more than 3 questions.
    - Avoid asking repetitive or obvious questions.
    - questions should be in numbered format.

    ### Format your answer exactly like this (JSON):
    {{
    "clarification": [
        {{ "question": "..." }},
        {{ "question": "..." }},
        {{ "question": "..." }}
    ]
    }}

    Do NOT include any other text, only valid JSON.
    Dont include any json format like ```json or ``` at the start or end of your response.
    ### Answer:
    """
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {"role": "system", "content": system_prompt},
            ],
            "temperature": 0.5
        })
    )
    
    try:
        raw_content = response.json()['choices'][0]['message']['content']
        result = json.loads(raw_content)  
        return result['clarification']
    except Exception as e:
        print("❌ Error while parsing LLM response:", e)
        return {"clarification": []}

