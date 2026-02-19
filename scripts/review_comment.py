import os
import google.generativeai as genai

def check_grammar_gemini(comment_body, api_key):
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Use a specific, capable model. 
    # In 2026, we assume 'gemini-1.5-pro' is standard/legacy and maybe 'gemini-2.0' exists, 
    # but 'gemini-1.5-pro-latest' is a safe, high-quality bet for "latest version" alias.
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
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
    
    # Gemini 1.5 style interaction
    # We combine system prompt and user input as Gemini doesn't always strictly use 'system' role in same way as OpenAI in basic chats,
    # but system_instruction is supported in newer SDKs. We'll use a direct prompt approach for robustness.
    full_prompt = f"{system_prompt}\n\nStudent's homework:\n{comment_body}"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error contacting Gemini Teacher: {str(e)}\n\n(Please check if your GEMINI_API_KEY is correct in Repo Settings)"

def main():
    comment_body = os.environ.get("COMMENT_BODY")
    api_key = os.environ.get("GEMINI_API_KEY")

    if not comment_body:
        print("No comment body found.")
        return

    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        # Create a dummy file to warn user in the PR comment if we wanted, but better to fail or log.
        # Let's write a warning message to the feedback file so the user sees it in the issue.
        with open('feedback_body.md', 'w') as f:
            f.write("⚠️ **AI 助教未启动**\n\n请在仓库 Settings -> Secrets -> Actions 里添加 `GEMINI_API_KEY`。\n(去 Google AI Studio 申请免费 Key)")
        return

    feedback = check_grammar_gemini(comment_body, api_key)
    
    with open('feedback_body.md', 'w') as f:
        f.write(feedback)

if __name__ == "__main__":
    main()
