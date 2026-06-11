from src.llm.prompt import create_prompt
import os
from dotenv import load_dotenv
from pathlib import Path
import os
from cloudflare import Cloudflare


def ask_llm(query: str) -> str:
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    prompt_system, prompt_user = create_prompt(query)
    client = Cloudflare(api_token=os.environ.get("CF_TOKEN"))
    account_id = os.environ.get("CF_ID")
    response = client.ai.run(
        account_id=account_id,
        model_name="@cf/meta/llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user},
        ],
        max_tokens=512,
    )
    return response["response"]
