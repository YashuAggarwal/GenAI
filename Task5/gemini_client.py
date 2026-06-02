"""
Google Gemini API client module.
Handles configuration and SQL query generation using Gemini API.
"""

import os
from typing import Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path


class GeminiClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client with API key and model from environment variables."""
        # Load environment variables from parent directory's .env file
        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent
        env_path = parent_dir / ".env"
        load_dotenv(dotenv_path=env_path)
        
        # Get API key and model name from environment
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_Key")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please set it in the .env file."
            )
        
        # Configure Gemini API client
        self.client = genai.Client(api_key=self.api_key)
        print(f"✓ Gemini client initialized with model: {self.model_name}")
    
    def generate_sql(self, natural_language_query: str, database_schema: str) -> Optional[str]:
        """
        Convert natural language query to SQL using Gemini API.
        
        Args:
            natural_language_query: User's question in natural language
            database_schema: Database schema information
            
        Returns:
            Generated SQL query string, or None if generation fails
        """
        try:
            # Construct prompt for Gemini
            prompt = self._build_prompt(natural_language_query, database_schema)
            
            # Generate SQL using Gemini with retry logic
            import time
            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt
                    )
                    
                    # Extract SQL from response
                    sql_query = self._extract_sql(response.text)
                    return sql_query
                    
                except Exception as retry_error:
                    error_str = str(retry_error)
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        if attempt < 2:
                            wait_time = 2 ** attempt
                            print(f"Rate limit hit, retrying in {wait_time}s...")
                            time.sleep(wait_time)
                        else:
                            raise
                    else:
                        raise
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"✗ Error generating SQL: {e}")
            print(f"✗ Full error: {error_details}")
            return None
    
    def _build_prompt(self, natural_language_query: str, database_schema: str) -> str:
        """
        Build a comprehensive prompt for Gemini to generate SQL.
        
        Args:
            natural_language_query: User's question
            database_schema: Schema information
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert SQL query generator. Convert the natural language question into a valid SQLite SELECT query.

{database_schema}

IMPORTANT RULES:
1. Generate ONLY SELECT queries (no INSERT, UPDATE, DELETE, DROP, ALTER, CREATE)
2. Return ONLY the SQL query without any explanation, markdown formatting, or additional text
3. Do not include ```sql``` or any other code block formatting
4. The query must be valid SQLite syntax
5. Use proper JOIN syntax when querying multiple tables
6. Use appropriate WHERE clauses for filtering
7. For date comparisons, use date() function or direct string comparison
8. Return just the raw SQL query text

Natural Language Question:
{natural_language_query}

SQL Query:"""
        
        return prompt
    
    def _extract_sql(self, response_text: str) -> str:
        """
        Extract SQL query from Gemini's response.
        Removes markdown formatting and extra whitespace.
        
        Args:
            response_text: Raw response from Gemini
            
        Returns:
            Cleaned SQL query string
        """
        # Remove markdown code blocks if present
        sql = response_text.strip()
        
        # Remove ```sql and ``` markers
        if sql.startswith("```sql"):
            sql = sql[6:]
        elif sql.startswith("```"):
            sql = sql[3:]
        
        if sql.endswith("```"):
            sql = sql[:-3]
        
        # Clean up whitespace
        sql = sql.strip()
        
        return sql


def test_gemini_client():
    """Test function to verify Gemini client works correctly."""
    try:
        client = GeminiClient()
        
        # Test schema
        test_schema = """
        Table: customer
        - customer_id INTEGER PRIMARY KEY
        - name TEXT
        - email TEXT
        """
        
        # Test query
        test_query = "Show all customers"
        
        print(f"\nTest Query: {test_query}")
        sql = client.generate_sql(test_query, test_schema)
        print(f"Generated SQL: {sql}")
        
        return sql is not None
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the client when run directly
    success = test_gemini_client()
    if success:
        print("\n✓ Gemini client test passed")
    else:
        print("\n✗ Gemini client test failed")
