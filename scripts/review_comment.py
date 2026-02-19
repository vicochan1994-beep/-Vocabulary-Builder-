import os
import json
import requests
import sys

def check_grammar(comment_body, api_key):
    # Determine API base URL and model based on available keys or defaults
    # Defaulting to a generic OpenAI-compatible endpoint (could be DeepSeek, Moonshot, etc.)
    base_url = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com")
    model = os.environ.get("LLM_MODEL", "deepseek-chat")
    
    system_prompt = """
You are a helpful, encouraging English teacher for a beginner student (Level A1/A2).
The student is trying to write sentences using specific vocabulary.
Your task:
1. Identify the English sentences in their text.
2. Check for grammar, spelling, and natural phrasing errors.
3. Provide corrections in a gentle, supportive way.
4. Explain the 'Why' simply (in Chinese).
5. Give a score (1-5 stars) and a short encouraging remark.

Format your response in Markdown. Keep it concise.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Student's homework:\n{comment_body}"}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(f"{base_url}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error contacting AI Teacher: {str(e)}\n\n(Please check if your LLM_API_KEY is active in Repo Settings > Secrets)"

def main():
    comment_body = os.environ.get("COMMENT_BODY")
    api_key = os.environ.get("LLM_API_KEY")

    error_message = ""
    feedback = ""

    if not comment_body:
        print("No comment body found.")
        return

    if not api_key:
        error_message = "⚠️ **AI Coach Config Error**: I cannot find the `LLM_API_KEY`. Please check your Repository Settings > Secrets. (找不到 Key，请检查设置)"
    else:
        # Call AI
        feedback = check_grammar(comment_body, api_key)
    
    # If feedback contains "Error", treat it as an error message
    if feedback.startswith("Error"):
        error_message = f"⚠️ **AI Connection Error**: {feedback}"
        feedback = ""

    # Prepare final content
    final_output = ""
    if error_message:
        final_output = error_message
    else:
        final_output = feedback

    # Always write to file if there is something to say
    if final_output:
        with open('feedback_body.md', 'w') as f:
            f.write(final_output)
            
    # Debug print
    print(f"Final output prepared: {final_output[:50]}...")

if __name__ == "__main__":
    main()
