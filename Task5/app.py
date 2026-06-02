"""
Streamlit application for Natural Language to SQL conversion.
Main entry point for the application.
"""

import streamlit as st
import pandas as pd
from db import initialize_database, get_database_schema
from gemini_client import GeminiClient
from sql_executor import SQLExecutor


# Page configuration
st.set_page_config(
    page_title="Natural Language to SQL",
    page_icon="🔍",
    layout="wide"
)


@st.cache_resource
def init_app():
    """
    Initialize application components.
    This function is cached to avoid reinitializing on every rerun.
    
    Returns:
        Tuple of (GeminiClient, SQLExecutor, database_schema)
    """
    # Initialize database
    initialize_database()
    
    # Get database schema
    schema = get_database_schema()
    
    # Initialize Gemini client
    try:
        gemini_client = GeminiClient()
    except ValueError as e:
        st.error(f"Failed to initialize Gemini client: {e}")
        st.stop()
    
    # Initialize SQL executor
    sql_executor = SQLExecutor()
    
    return gemini_client, sql_executor, schema


def main():
    """Main application function."""
    
    # Title and description
    st.title("🔍 Natural Language to SQL Query System")
    st.markdown("""
    Ask questions about the sales database in plain English, and get SQL queries and results instantly.
    
    **Available Tables:**
    - `customer`: Customer information (customer_id, name, email, join_date)
    - `sales`: Sales transactions (sale_id, customer_id, product, amount, sale_date)
    """)
    
    # Initialize application components
    gemini_client, sql_executor, schema = init_app()
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input section
        st.subheader("📝 Ask Your Question")
        
        # Text input for natural language query
        user_question = st.text_area(
            "Enter your question in natural language:",
            height=100,
            placeholder="e.g., What are the total sales in the last 3 days?\nWho are the top 5 customers by sales amount?\nShow me all sales for laptops."
        )
        
        # Submit button
        submit_button = st.button("🚀 Generate SQL & Execute", type="primary", use_container_width=True)
    
    with col2:
        # Example questions section
        st.subheader("💡 Example Questions")
        examples = [
            "Show all customers",
            "What are the total sales in the last 3 days?",
            "Who are the top 5 customers by total sales amount?",
            "List all sales for laptops",
            "What is the average sale amount?",
            "Show sales above $100",
            "Count the number of sales per product"
        ]
        
        for example in examples:
            if st.button(example, key=example, use_container_width=True):
                # Set the example as the input
                st.session_state['example_question'] = example
                st.rerun()
    
    # Handle example question selection
    if 'example_question' in st.session_state:
        user_question = st.session_state['example_question']
        del st.session_state['example_question']
    
    # Process query when submit button is clicked
    if submit_button and user_question:
        with st.spinner("🤔 Generating SQL query..."):
            # Generate SQL using Gemini
            generated_sql = gemini_client.generate_sql(user_question, schema)
        
        if generated_sql:
            # Display generated SQL
            st.subheader("📋 Generated SQL Query")
            st.code(generated_sql, language="sql")
            
            with st.spinner("⚙️ Executing query..."):
                # Execute the SQL query
                success, results, column_names, error = sql_executor.execute_query(generated_sql)
            
            if success:
                # Display results
                st.subheader("✅ Query Results")
                
                if results:
                    # Convert results to DataFrame for better display
                    df = pd.DataFrame(results, columns=column_names)
                    
                    # Display as interactive table
                    st.dataframe(df, use_container_width=True)
                    
                    # Show result count
                    st.info(f"📊 Total rows returned: {len(results)}")
                    
                    # Optional: Show formatted text version
                    with st.expander("View as formatted text"):
                        formatted_results = sql_executor.format_results(results, column_names)
                        st.text(formatted_results)
                else:
                    st.warning("⚠️ No results found for the query")
            else:
                # Display error
                st.error(f"❌ Query execution failed: {error}")
        else:
            st.error("❌ Failed to generate SQL query. Please check your Gemini API configuration.")
    
    elif submit_button and not user_question:
        st.warning("⚠️ Please enter a question before submitting.")
    
    # Footer with database schema
    with st.expander("📚 View Database Schema"):
        st.text(schema)
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This application uses **Google Gemini API** to convert natural language questions 
        into SQL queries and execute them against a SQLite database.
        
        **Features:**
        - Natural language to SQL conversion
        - Secure query validation
        - Interactive results display
        - Real-time query execution
        
        **Tech Stack:**
        - Python
        - Streamlit
        - Google Gemini API
        - SQLite
        """)
        
        st.header("🔒 Security")
        st.markdown("""
        Only **SELECT** queries are allowed. 
        All INSERT, UPDATE, DELETE, and DROP operations are blocked.
        """)


if __name__ == "__main__":
    main()
