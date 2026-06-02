"""
Unified Streamlit Application - Module 7
Combines all tasks (Task1-5) in a single interface with tabs
"""

import streamlit as st
import pandas as pd
import json
import os
import time
import csv
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Module 7 - All Tasks",
    page_icon="🚀",
    layout="wide"
)

# Initialize Gemini client
@st.cache_resource
def init_gemini_client():
    """Initialize Gemini client with retry logic"""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_Key")
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found in .env file!")
        st.stop()
    return genai.Client(api_key=api_key)

client = init_gemini_client()

# Utility function for retry logic
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
                    time.sleep(wait_time)
                else:
                    raise
            else:
                raise


# ============================================================================
# TASK 1: PROMPT ENGINEERING
# ============================================================================
def task1_prompts():
    st.header("📝 Task 1: Prompt Engineering Samples")
    st.markdown("""
    This section contains carefully crafted prompts for distributed SQL query optimization.
    """)
    
    prompts_path = os.path.join("Task1", "Prompts.txt")
    
    if os.path.exists(prompts_path):
        with open(prompts_path, 'r', encoding='utf-8') as f:
            prompts_content = f.read()
        
        st.text_area("Prompt Examples:", prompts_content, height=400)
        
        if st.download_button(
            label="📥 Download Prompts",
            data=prompts_content,
            file_name="prompts.txt",
            mime="text/plain"
        ):
            st.success("✅ Downloaded!")
    else:
        st.warning("⚠️ Prompts.txt not found in Task1 folder")


# ============================================================================
# TASK 2: LLM CHAT & JSON PARSING
# ============================================================================
def task2_llm_chat():
    st.header("💬 Task 2: LLM Chat & JSON Parsing")
    st.markdown("Analyze user activity data and get structured JSON responses.")
    
    # Default user activity
    default_activity = """User A logged in and purchased a laptop worth $1200.
User B logged in but did not make any purchase.
User C purchased a phone worth $800."""
    
    user_activity = st.text_area(
        "Enter User Activity Data:",
        value=default_activity,
        height=150
    )
    
    if st.button("🚀 Analyze Activity", key="task2_btn"):
        with st.spinner("🤔 Analyzing..."):
            prompt = f"""
Analyze the following user activity.

{user_activity}

Return ONLY valid JSON in the format below:

{{
    "summary": "",
    "total_users": 0,
    "purchasing_users": 0,
    "total_revenue": 0,
    "insights": [
        "",
        ""
    ]
}}
"""
            
            try:
                response = generate_with_retry(
                    client=client,
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                
                result = response.text.strip()
                
                # Extract JSON from markdown
                if result.startswith("```"):
                    result = result.replace("```json", "").replace("```", "").strip()
                
                data = json.loads(result)
                
                st.success("✅ Analysis Complete!")
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Users", data.get("total_users", 0))
                with col2:
                    st.metric("Purchasing Users", data.get("purchasing_users", 0))
                with col3:
                    st.metric("Total Revenue", f"${data.get('total_revenue', 0)}")
                
                # Display JSON
                st.subheader("📋 Structured Response")
                st.json(data)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ============================================================================
# TASK 3: DATA AUGMENTATION
# ============================================================================
def task3_data_augmentation():
    st.header("📊 Task 3: Data Augmentation with LLM")
    st.markdown("Generate synthetic data based on sample CSV data.")
    
    sample_csv_path = os.path.join("Task3", "sample_data.csv")
    
    if os.path.exists(sample_csv_path):
        # Display sample data
        df_sample = pd.read_csv(sample_csv_path)
        st.subheader("📄 Sample Data")
        st.dataframe(df_sample, use_container_width=True)
        
        num_records = st.slider("Number of records to generate:", 1, 20, 10)
        
        if st.button("🎲 Generate Synthetic Data", key="task3_btn"):
            with st.spinner(f"🤖 Generating {num_records} synthetic records..."):
                sample_data = df_sample.head(3).to_dict('records')
                columns = list(df_sample.columns)
                
                prompt = f"""
Generate {num_records} realistic synthetic e-commerce sales records for an Indian e-commerce platform.

COLUMNS: {', '.join(columns)}

SAMPLE DATA:
{json.dumps(sample_data, indent=2)}

INSTRUCTIONS:
- Use realistic Indian names (Priya Sharma, Arjun Nair, etc.)
- Product categories: Electronics, Fashion, Home & Kitchen, Books, Toys
- Price range: ₹100 to ₹50000
- Ensure data is statistically consistent with samples
- Return ONLY a valid JSON array with {num_records} records

FORMAT:
[
  {json.dumps(sample_data[0])},
  ...
]
"""
                
                try:
                    response = generate_with_retry(
                        client=client,
                        model="gemini-1.5-flash",
                        contents=prompt
                    )
                    
                    result = response.text.strip()
                    if result.startswith("```"):
                        result = result.replace("```json", "").replace("```", "").strip()
                    
                    generated_data = json.loads(result)
                    df_generated = pd.DataFrame(generated_data)
                    
                    st.success(f"✅ Generated {len(df_generated)} records!")
                    st.subheader("🎯 Generated Data")
                    st.dataframe(df_generated, use_container_width=True)
                    
                    # Download option
                    csv_data = df_generated.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv_data,
                        file_name="augmented_data.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ sample_data.csv not found in Task3 folder")


# ============================================================================
# TASK 4: DOCUMENT QUERY
# ============================================================================
def task4_document_query():
    st.header("📄 Task 4: Interactive Document Query")
    st.markdown("Ask questions about a document and get AI-powered answers.")
    
    doc_path = os.path.join("Task4", "sample_document.txt")
    
    if os.path.exists(doc_path):
        with open(doc_path, 'r', encoding='utf-8') as f:
            document_content = f.read()
        
        with st.expander("📖 View Document Content"):
            st.text_area("Document:", document_content, height=300)
        
        st.info(f"📊 Document Stats: {len(document_content)} characters, ~{len(document_content.split())} words")
        
        # Example questions
        st.subheader("💡 Example Questions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("What is this document about?", key="q1"):
                st.session_state['task4_question'] = "What is this document about?"
            if st.button("What are the main points?", key="q2"):
                st.session_state['task4_question'] = "What are the main points?"
        with col2:
            if st.button("Who is mentioned in the document?", key="q3"):
                st.session_state['task4_question'] = "Who is mentioned in the document?"
            if st.button("What are the key dates?", key="q4"):
                st.session_state['task4_question'] = "What are the key dates?"
        
        # Question input
        question = st.text_input(
            "❓ Your Question:",
            value=st.session_state.get('task4_question', ''),
            placeholder="e.g., What is the main topic of this document?"
        )
        
        if st.button("🔍 Get Answer", key="task4_btn") and question:
            with st.spinner("🤔 Analyzing document..."):
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

ANSWER:
"""
                
                try:
                    response = generate_with_retry(
                        client=client,
                        model="gemini-1.5-flash",
                        contents=prompt
                    )
                    
                    answer = response.text.strip()
                    
                    st.success("✅ Answer found!")
                    st.markdown("### 💡 Answer:")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ sample_document.txt not found in Task4 folder")


# ============================================================================
# TASK 5: NATURAL LANGUAGE TO SQL
# ============================================================================
def task5_nl_to_sql():
    st.header("🔍 Task 5: Natural Language to SQL")
    st.markdown("Convert natural language questions to SQL queries and execute them.")
    
    # Import Task5 modules
    try:
        import sys
        from pathlib import Path
        
        # Add Task5 to Python path
        task5_path = Path(__file__).parent / "Task5"
        if str(task5_path) not in sys.path:
            sys.path.insert(0, str(task5_path))
        
        from db import initialize_database, get_database_schema, get_connection
        from gemini_client import GeminiClient
        from sql_executor import SQLExecutor
        
        # Initialize components
        if 'db_initialized' not in st.session_state:
            initialize_database()
            st.session_state['db_initialized'] = True
        
        schema = get_database_schema()
        
        @st.cache_resource
        def get_gemini_client():
            return GeminiClient()
        
        @st.cache_resource
        def get_sql_executor():
            return SQLExecutor()
        
        gemini_client = get_gemini_client()
        sql_executor = get_sql_executor()
        
        # UI
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Ask Your Question")
            user_question = st.text_area(
                "Enter your question in natural language:",
                height=100,
                placeholder="e.g., What are the total sales in the last 3 days?"
            )
            submit_button = st.button("🚀 Generate SQL & Execute", type="primary", use_container_width=True)
        
        with col2:
            st.subheader("💡 Examples")
            examples = [
                "Show all customers",
                "Total sales in last 3 days?",
                "Top 5 customers by sales?",
                "List all laptop sales"
            ]
            for example in examples:
                if st.button(example, key=f"ex_{example}", use_container_width=True):
                    st.session_state['task5_question'] = example
                    st.rerun()
        
        if 'task5_question' in st.session_state:
            user_question = st.session_state['task5_question']
            del st.session_state['task5_question']
        
        if submit_button and user_question:
            with st.spinner("🤔 Generating SQL query..."):
                generated_sql = gemini_client.generate_sql(user_question, schema)
            
            if generated_sql:
                st.subheader("📋 Generated SQL")
                st.code(generated_sql, language="sql")
                
                with st.spinner("⚙️ Executing query..."):
                    success, results, column_names, error = sql_executor.execute_query(generated_sql)
                
                if success:
                    st.subheader("✅ Results")
                    if results:
                        df = pd.DataFrame(results, columns=column_names)
                        st.dataframe(df, use_container_width=True)
                        st.info(f"📊 Total rows: {len(results)}")
                    else:
                        st.warning("⚠️ No results found")
                else:
                    st.error(f"❌ Query failed: {error}")
            else:
                st.error("❌ Failed to generate SQL query")
        
        with st.expander("📚 View Database Schema"):
            st.text(schema)
            
    except ImportError as e:
        st.error(f"⚠️ Task5 modules not found: {str(e)}")
        st.info("Make sure Task5 folder contains: db.py, gemini_client.py, sql_executor.py")


# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    # Header
    st.title("🚀 Module 7 - Unified Application")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        st.markdown("""
        Select a task from the tabs to explore different LLM applications:
        
        - **Task 1**: Prompt Engineering
        - **Task 2**: LLM Chat & JSON
        - **Task 3**: Data Augmentation
        - **Task 4**: Document Query
        - **Task 5**: Natural Language to SQL
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info("Powered by Google Gemini API")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Task 1: Prompts",
        "💬 Task 2: LLM Chat",
        "📊 Task 3: Data Aug",
        "📄 Task 4: Doc Query",
        "🔍 Task 5: NL to SQL"
    ])
    
    with tab1:
        task1_prompts()
    
    with tab2:
        task2_llm_chat()
    
    with tab3:
        task3_data_augmentation()
    
    with tab4:
        task4_document_query()
    
    with tab5:
        task5_nl_to_sql()


if __name__ == "__main__":
    main()
