"""
SQL validation and execution module.
Validates and executes SQL queries with security checks.
"""

import re
import sqlite3
from typing import List, Tuple, Optional
from db import get_connection


class SQLExecutor:
    """Validates and executes SQL queries with security checks."""
    
    # Dangerous SQL keywords that should be blocked
    BLOCKED_KEYWORDS = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 
        'CREATE', 'TRUNCATE', 'REPLACE', 'GRANT', 'REVOKE',
        'EXEC', 'EXECUTE', 'PRAGMA'
    ]
    
    def __init__(self):
        """Initialize SQL executor."""
        pass
    
    def validate_sql(self, sql_query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate SQL query for security and syntax.
        
        Args:
            sql_query: SQL query string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if query is safe to execute
            - error_message: Error description if invalid, None if valid
        """
        if not sql_query or not sql_query.strip():
            return False, "SQL query is empty"
        
        # Convert to uppercase for keyword checking
        sql_upper = sql_query.upper()
        
        # Check for blocked keywords
        for keyword in self.BLOCKED_KEYWORDS:
            # Use word boundaries to avoid false positives
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                return False, f"Query contains blocked keyword: {keyword}"
        
        # Ensure query starts with SELECT
        sql_stripped = sql_query.strip()
        if not sql_stripped.upper().startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        # Check for multiple statements (basic SQL injection prevention)
        if ';' in sql_query[:-1]:  # Allow semicolon only at the end
            return False, "Multiple SQL statements are not allowed"
        
        # Basic syntax validation - check for balanced parentheses
        if sql_query.count('(') != sql_query.count(')'):
            return False, "Unbalanced parentheses in query"
        
        return True, None
    
    def execute_query(self, sql_query: str) -> Tuple[bool, Optional[List], Optional[List], Optional[str]]:
        """
        Execute validated SQL query.
        
        Args:
            sql_query: SQL query to execute
            
        Returns:
            Tuple of (success, results, column_names, error_message)
            - success: True if execution succeeded
            - results: List of result rows (list of tuples)
            - column_names: List of column names
            - error_message: Error description if failed, None if successful
        """
        # First validate the query
        is_valid, error_msg = self.validate_sql(sql_query)
        if not is_valid:
            return False, None, None, error_msg
        
        # Execute the query
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Execute the query
            cursor.execute(sql_query)
            
            # Fetch results
            results = cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            return True, results, column_names, None
            
        except sqlite3.Error as e:
            error_msg = f"SQL execution error: {str(e)}"
            return False, None, None, error_msg
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            return False, None, None, error_msg
            
        finally:
            if conn:
                conn.close()
    
    def format_results(self, results: List, column_names: List) -> str:
        """
        Format query results as a readable string.
        
        Args:
            results: List of result rows
            column_names: List of column names
            
        Returns:
            Formatted string representation of results
        """
        if not results:
            return "No results found for the query"
        
        # Calculate column widths
        col_widths = [len(name) for name in column_names]
        for row in results:
            for i, value in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(value)))
        
        # Build header
        header = " | ".join(name.ljust(col_widths[i]) for i, name in enumerate(column_names))
        separator = "-+-".join("-" * width for width in col_widths)
        
        # Build rows
        rows = []
        for row in results:
            row_str = " | ".join(str(value).ljust(col_widths[i]) for i, value in enumerate(row))
            rows.append(row_str)
        
        # Combine all parts
        result_str = f"{header}\n{separator}\n" + "\n".join(rows)
        
        return result_str


def test_sql_executor():
    """Test function to verify SQL executor works correctly."""
    executor = SQLExecutor()
    
    # Test valid query
    print("Test 1: Valid SELECT query")
    is_valid, error = executor.validate_sql("SELECT * FROM customer")
    print(f"Valid: {is_valid}, Error: {error}")
    assert is_valid, "Valid query should pass"
    
    # Test invalid query (INSERT)
    print("\nTest 2: Invalid INSERT query")
    is_valid, error = executor.validate_sql("INSERT INTO customer VALUES (1, 'test')")
    print(f"Valid: {is_valid}, Error: {error}")
    assert not is_valid, "INSERT query should be blocked"
    
    # Test invalid query (DROP)
    print("\nTest 3: Invalid DROP query")
    is_valid, error = executor.validate_sql("DROP TABLE customer")
    print(f"Valid: {is_valid}, Error: {error}")
    assert not is_valid, "DROP query should be blocked"
    
    # Test SQL injection attempt
    print("\nTest 4: SQL injection attempt")
    is_valid, error = executor.validate_sql("SELECT * FROM customer; DROP TABLE sales")
    print(f"Valid: {is_valid}, Error: {error}")
    assert not is_valid, "Multiple statements should be blocked"
    
    print("\n✓ All SQL executor tests passed")


if __name__ == "__main__":
    # Run tests when executed directly
    test_sql_executor()
