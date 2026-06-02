# Task 4: Document Querying with LLM

## Overview
This project demonstrates how to use Large Language Models (LLMs) to query and extract information from documents. It tests the LLM's ability to understand document content, answer questions accurately, and identify when it doesn't have information (avoiding hallucinations).

## Files Created

### 1. **sample_document.txt**
- Employee handbook for ACME Technologies
- Contains company policies, benefits, working hours, leave policies, etc.
- 6,558 characters covering 9 sections

### 2. **document_query.py** (Automated Testing)
- Reads document and asks predefined test questions
- Tests different question types:
  - **FACTUAL**: Direct information from document
  - **NUMERICAL**: Specific numbers and amounts  
  - **SUMMARY**: Requires understanding and summarization
  - **NOT IN DOCUMENT**: Tests for hallucination
  - **INTERPRETATION**: Requires context understanding
  - **COMPLEX**: Multi-part questions

### 3. **interactive_query.py** (Interactive Mode)
- Allows you to ask your own questions
- Type questions and get real-time answers
- Type 'quit' or 'exit' to end session

## How It Works

### Process Flow:
```
1. Load Document → 2. Read Content → 3. User Question
                                           ↓
4. Create Prompt ← 5. Send to LLM ← 6. Add Context
                                           ↓
7. Get Response → 8. Display Answer → 9. Analyze Accuracy
```

### The Prompt Structure:
```
DOCUMENT CONTENT: [Full document text]
QUESTION: [User's question]
INSTRUCTIONS:
- Answer based ONLY on document content
- If not in document, say "The document does not contain this information"
- Be specific and cite relevant parts
- No assumptions or external information
```

## Test Questions & Expected Behavior

### ✅ FACTUAL Questions (Should Answer Correctly):
- "What are the working hours for regular employees?"
  - **Expected**: 9:00 AM to 6:00 PM, Monday to Friday
  
- "How many days of casual leave per year?"
  - **Expected**: 12 days

### 🔢 NUMERICAL Questions:
- "What is the health insurance coverage?"
  - **Expected**: ₹5 lakhs for employee, ₹5 lakhs for family

### 📝 SUMMARY Questions:
- "What types of leave are available?"
  - **Expected**: Should list Casual (12), Sick (12), Earned (18), Maternity (26 weeks), Paternity (2 weeks)

### ❌ NOT IN DOCUMENT (Test Hallucination):
- "What is the CEO's name?"
  - **Expected**: "The document does not contain this information"
  - **Hallucination**: Making up a name

- "What is the average salary?"
  - **Expected**: "The document does not contain this information"
  - **Hallucination**: Inventing a number

### 🧠 INTERPRETATION Questions:
- "What is the notice period for resignation?"
  - **Expected**: 2 months notice required

### 🎯 COMPLEX Questions:
- "What benefits can I use for attending a conference?"
  - **Expected**: Professional development budget ₹50,000/year, 2 conferences/year allowed

## Usage

### Automated Testing:
```bash
cd Task4
python document_query.py
```

This will:
- Load the document
- Ask 8 different questions
- Display all answers
- Show observations to make

### Interactive Mode:
```bash
cd Task4
python interactive_query.py
```

Then type your questions:
```
❓ Your Question: How many leaves can I take?
💡 Answer: [LLM provides answer based on document]

❓ Your Question: What is the gym reimbursement?
💡 Answer: [LLM provides answer based on document]
```

## Observations to Make

When running the system, observe:

### 1. **ACCURACY**
- ✅ Does LLM extract correct facts?
- ✅ Are numbers accurate?
- ✅ Are dates and names correct?

### 2. **HALLUCINATION**
- ❌ Does it make up information not in document?
- ✅ Does it admit when information is unavailable?
- ⚠️ Does it add "common knowledge" not in document?

### 3. **COMPREHENSION**
- Can it understand context?
- Can it summarize multiple related points?
- Can it interpret policies correctly?

### 4. **CITATION**
- Does it reference specific sections?
- Does it quote relevant parts?
- Is it specific or vague?

### 5. **CONSISTENCY**
- Are repeated questions answered the same way?
- Does it contradict itself?

### 6. **EDGE CASES**
- Questions with ambiguous wording
- Questions requiring calculations
- Questions combining multiple sections

## Example Expected Outputs

### Good Response (Accurate):
```
❓ Question: What are the working hours?
💡 Answer: According to Section 2, regular employees work from 9:00 AM 
to 6:00 PM, Monday to Friday, with a 1-hour lunch break from 1:00 PM 
to 2:00 PM, totaling 40 hours per week.
```

### Good Response (Admitting Unknown):
```
❓ Question: What is the CEO's salary?
💡 Answer: The document does not contain information about the CEO's 
salary or executive compensation.
```

### Bad Response (Hallucination):
```
❓ Question: What is the CEO's name?
💡 Answer: The CEO of ACME Technologies is Rajesh Kumar.
[THIS IS WRONG - name not in document]
```

## Document Formats Supported

The script can be extended to read multiple formats:

- **✅ TXT files**: Already implemented
- **📄 PDF files**: Add PyPDF2 library
  ```bash
  pip install PyPDF2
  ```
- **📝 DOCX files**: Add python-docx library
  ```bash
  pip install python-docx
  ```

## Key Takeaways

### LLM Strengths:
✅ Excellent at finding specific facts in documents  
✅ Good at summarizing information  
✅ Can understand context and relationships  
✅ Fast and scalable compared to manual reading  

### LLM Limitations:
⚠️ May hallucinate when pushed for unavailable information  
⚠️ Accuracy depends on prompt quality  
⚠️ May miss subtle nuances  
⚠️ Requires clear instructions to avoid assumptions  

### Best Practices:
1. **Explicit Instructions**: Tell LLM to only use document content
2. **Request Citations**: Ask for specific references
3. **Handle Unknowns**: Instruct to admit when information is unavailable
4. **Test Edge Cases**: Ask questions with no answers to test for hallucination
5. **Verify Critical Information**: Always verify important facts

## Prompt Engineering Tips

### What Works Well:
```
✅ "Based ONLY on the document..."
✅ "If information is not in the document, state so clearly"
✅ "Cite specific sections when answering"
✅ "Do not make assumptions or add external information"
```

### What to Avoid:
```
❌ "What do you know about..."
❌ Open-ended questions without context
❌ Not specifying to use only document content
❌ Not handling "unknown" scenarios
```

## Real-World Applications

1. **Customer Support**: Answer questions from product manuals
2. **Legal**: Extract information from contracts and policies
3. **HR**: Answer employee questions about policies
4. **Research**: Query academic papers and reports
5. **Compliance**: Check documents against regulations
6. **Education**: Study material Q&A systems

## API Considerations

- Script includes retry logic for rate limits
- Exponential backoff (1s, 2s, 4s, 8s, 16s)
- Handles 429 (rate limit) and 503 (unavailable) errors
- If API is experiencing high demand, retry after a few minutes

## Try It Yourself!

1. Run `python document_query.py` to see automated testing
2. Run `python interactive_query.py` to ask your own questions
3. Try questions where you know the answer
4. Try questions NOT in the document to test hallucination
5. Compare LLM responses with actual document content
6. Note patterns in correct vs incorrect responses

## Future Enhancements

- [ ] Add PDF support with PyPDF2
- [ ] Add Word document support with python-docx
- [ ] Implement document chunking for very large files
- [ ] Add conversation history for follow-up questions
- [ ] Implement confidence scores for answers
- [ ] Add source highlighting (which part of document was used)
- [ ] Create a web interface
- [ ] Support multiple documents simultaneously

---

**Note**: When API is experiencing high demand (503 errors), wait a few minutes and try again. The retry logic will automatically handle temporary issues.
