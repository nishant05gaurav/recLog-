import os
from dotenv import load_dotenv
from google import genai

# Loading environment variables from a .env file
load_dotenv()

# Retrieving the Gemini API key from a .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check the availability of API key
if not GEMINI_API_KEY:
    print("Missing Gemini API key in environment.")
    
# Initializing the Gemini client with the provided API key
client = genai.Client(api_key=GEMINI_API_KEY)

def generateSummary(markdownText):
    """
    Generate a concise 2-sentence professional summary of a technical article. This function takes a technical blog post, sends it to the Gemini API, and returns a clean, professional summary suitable for use in developer portfolios or metadata descriptions.

    Args:
        markdownText (str): The markdown content of the article.

    Returns:
        str: A 2-sentence summary of the article. If input is empty or an error
             occurs during generation, a fallback message is returned.
    """
    
    # Handling case - No Output
    if not markdownText:
        return "Sorry. Read the full article in DEV"
    
    # Summarization is in progress
    print(f'Gemini will summarise the article for you :)')
    
    # Construct the prompt with strict instructions for the model and limiting input to 3000 characters to avoid large requests
    prompt = f"You are a technical editor writing metadata for a developer portfolio. Read the following markdown text from a technical blog post. Write EXACTLY a 2-sentence summary of what the article covers. Make it sound professional, focusing on the problem solved and the technologies used. CRITICAL: Do NOT use introductory phrases like 'This article discusses' or 'Here is a summary'. Just output the 2 sentences directly. ARTICLE CONTENT: {markdownText[:3000]}"
    
    try:
        # Sending the prompt to the Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Returning the response
        return response.text.strip()
    
    except Exception as e:
        # Error for debugging purposes
        print(f"Summary generation failed: {e}")
        
        # Returning a fallback message if summarization fails
        return "Read the full article on my dev.to profile"