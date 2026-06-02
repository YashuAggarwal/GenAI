from google import genai
import time
import os
from dotenv import load_dotenv

# Load environment variables from parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(parent_dir, '.env'))

# Get API key from environment variable
api_key = os.getenv("API_Key")
if not api_key:
    raise ValueError("API_Key not found in .env file")

client = genai.Client(api_key=api_key)


def generate_with_retry(client, model, contents, max_retries=5):
    """Generate content with automatic retry logic"""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            return response
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "503" in error_str or "UNAVAILABLE" in error_str:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    error_type = "Rate limit" if "429" in error_str else "Service unavailable"
                    print(f"⚠️  {error_type} error. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Max retries exceeded. Please try again later.")
                    raise
            else:
                raise


def read_document(filepath):
    """Read document content"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def ask_question(document_content, question):
    """Ask a question about the document"""
    prompt = f"""
You are a helpful assistant that answers questions based on the provided document.

DOCUMENT CONTENT:
---
{document_content}
---

QUESTION: {question}

INSTRUCTIONS:
1. Answer based ONLY on the document content
2. If information is not in the document, state "The document does not contain this information"
3. Be specific and cite relevant parts
4. Keep answers concise and accurate
5. Do not make assumptions

ANSWER:
"""
    
    print("   🤔 Analyzing document...")
    
    response = generate_with_retry(
        client=client,
        model="gemini-flash-latest",
        contents=prompt
    )
    
    return response.text.strip()


def main():
    print("="*70)
    print("📄 INTERACTIVE DOCUMENT QUERY SYSTEM")
    print("="*70)
    
    # Load document
    document_path = "sample_document.txt"
    
    print(f"\n📂 Loading document: {document_path}")
    try:
        document_content = read_document(document_path)
        word_count = len(document_content.split())
        print(f"   ✅ Document loaded successfully")
        print(f"   📊 Stats: {len(document_content)} characters, ~{word_count} words")
    except Exception as e:
        print(f"❌ Error loading document: {e}")
        return
    
    print("\n" + "="*70)
    print("💬 You can now ask questions about the document!")
    print("   Type 'quit' or 'exit' to end the session")
    print("="*70)
    
    question_count = 0
    
    while True:
        print(f"\n{'─'*70}")
        user_question = input("❓ Your Question: ").strip()
        
        if user_question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thank you for using the Document Query System!")
            print(f"   Total questions asked: {question_count}")
            break
        
        if not user_question:
            print("   ⚠️  Please enter a question")
            continue
        
        question_count += 1
        
        try:
            answer = ask_question(document_content, user_question)
            print(f"\n💡 Answer:")
            print(f"   {answer}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("   Please try again")


if __name__ == "__main__":
    main()
