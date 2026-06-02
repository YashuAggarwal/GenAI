from google import genai
import json
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
    """
    Generate content with automatic retry logic for rate limits and server errors.
    Uses exponential backoff with a maximum of max_retries attempts.
    """
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            return response
        except Exception as e:
            error_str = str(e)
            # Check if it's a retryable error (429 rate limit or 503 unavailable)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "503" in error_str or "UNAVAILABLE" in error_str:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                    error_type = "Rate limit" if "429" in error_str else "Service unavailable"
                    print(f"   ⚠️  {error_type} error. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ Max retries ({max_retries}) exceeded. Please try again later.")
                    raise
            else:
                # Re-raise if it's not a retryable error
                raise


def read_txt_file(filepath):
    """Read a text file"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def read_pdf_file(filepath):
    """Read a PDF file"""
    try:
        import PyPDF2
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except ImportError:
        print("❌ PyPDF2 not installed. Install with: pip install PyPDF2")
        return None
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None


def read_docx_file(filepath):
    """Read a Word document"""
    try:
        import docx
        doc = docx.Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except ImportError:
        print("❌ python-docx not installed. Install with: pip install python-docx")
        return None
    except Exception as e:
        print(f"❌ Error reading DOCX: {e}")
        return None


def read_document(filepath):
    """Read document based on file extension"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return None
    
    extension = os.path.splitext(filepath)[1].lower()
    
    if extension == '.txt':
        return read_txt_file(filepath)
    elif extension == '.pdf':
        return read_pdf_file(filepath)
    elif extension in ['.docx', '.doc']:
        return read_docx_file(filepath)
    else:
        print(f"❌ Unsupported file format: {extension}")
        return None


def ask_question(document_content, question):
    """Ask a question about the document content"""
    
    prompt = f"""
You are a helpful assistant that answers questions based on the provided document.

DOCUMENT CONTENT:
---
{document_content}
---

QUESTION: {question}

INSTRUCTIONS:
1. Answer the question based ONLY on the information provided in the document
2. If the answer is not in the document, clearly state "The document does not contain this information"
3. Be specific and cite relevant parts of the document
4. Keep your answer concise and accurate
5. Do not make assumptions or add information not present in the document

ANSWER:
"""
    
    print(f"\n❓ Question: {question}")
    print("   🤔 Thinking...")
    
    response = generate_with_retry(
        client=client,
        model="gemini-flash-latest",
        contents=prompt
    )
    
    answer = response.text.strip()
    return answer


def main():
    print("="*70)
    print("📄 DOCUMENT QUERYING WITH LLM")
    print("="*70)
    
    # Document path
    document_path = "sample_document.txt"
    
    # Read document
    print(f"\n📂 Reading document: {document_path}")
    document_content = read_document(document_path)
    
    if not document_content:
        print("❌ Failed to read document. Exiting.")
        return
    
    print(f"   ✅ Document loaded successfully ({len(document_content)} characters)")
    print(f"   📊 Document preview (first 200 chars):")
    print(f"   {document_content[:200]}...")
    
    # Test questions
    print("\n" + "="*70)
    print("🧪 TESTING WITH DIFFERENT TYPES OF QUESTIONS")
    print("="*70)
    
    questions = [
        # Factual questions - easy to find in document
        {
            "type": "FACTUAL",
            "question": "What are the working hours for regular employees?"
        },
        {
            "type": "FACTUAL",
            "question": "How many days of casual leave are employees entitled to per year?"
        },
        {
            "type": "NUMERICAL",
            "question": "What is the health insurance coverage amount for employees?"
        },
        # Questions requiring understanding and summary
        {
            "type": "SUMMARY",
            "question": "What are the different types of leave available and how many days for each?"
        },
        # Questions that require information not in document (test for hallucination)
        {
            "type": "NOT IN DOCUMENT",
            "question": "What is the CEO's name of ACME Technologies?"
        },
        {
            "type": "NOT IN DOCUMENT", 
            "question": "What is the average salary of software engineers at ACME?"
        },
        # Questions requiring interpretation
        {
            "type": "INTERPRETATION",
            "question": "What is the notice period required for resignation?"
        },
        # Complex questions
        {
            "type": "COMPLEX",
            "question": "If I want to attend a technical conference, what benefits can I use and how much budget is available?"
        }
    ]
    
    # Ask questions
    for i, q_item in enumerate(questions, 1):
        print(f"\n{'─'*70}")
        print(f"Question {i}/{len(questions)} [{q_item['type']}]")
        print(f"{'─'*70}")
        
        answer = ask_question(document_content, q_item['question'])
        
        print(f"\n💡 Answer:")
        print(f"   {answer}")
    
    print("\n" + "="*70)
    print("✅ DOCUMENT QUERYING COMPLETED")
    print("="*70)
    
    # Observations section
    print("\n" + "="*70)
    print("🔍 OBSERVATIONS TO MAKE:")
    print("="*70)
    print("""
1. ACCURACY: Did the LLM answer factual questions correctly?
2. HALLUCINATION: Did it make up information for questions not in the document?
3. CITATION: Did it reference specific parts of the document?
4. COMPREHENSION: Could it summarize and interpret information?
5. LIMITATIONS: Did it admit when information was not available?
6. CONSISTENCY: Were answers consistent with document content?
    """)


if __name__ == "__main__":
    main()
