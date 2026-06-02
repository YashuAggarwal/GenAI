from google import genai
import json
import time
import os
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
                    print(f"{error_type} error. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries ({max_retries}) exceeded. Please try again later.")
                    raise
            else:
                # Re-raise if it's not a retryable error
                raise


def read_csv_data(filename):
    """Read CSV file and return data as list of dictionaries"""
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


def analyze_data_structure(data):
    """Analyze the structure of existing data"""
    if not data:
        return None
    
    # Get column names and sample rows
    columns = list(data[0].keys())
    sample_rows = data[:min(3, len(data))]  # Get up to 3 sample rows
    
    return {
        'columns': columns,
        'sample_data': sample_rows,
        'total_records': len(data)
    }


def generate_synthetic_data(analysis, num_records=10):
    """Use LLM to generate synthetic data based on existing data structure"""
    
    columns = analysis['columns']
    sample_data = analysis['sample_data']
    
    # Create a detailed prompt for the LLM with Indian e-commerce context
    prompt = f"""
CONTEXT:
I am a data engineer working on a project where actual test data is limited.
I need to generate more realistic, statistically consistent data rows from an existing CSV file
to augment the dataset for testing and development purposes.

ROLE:
Act as a realistic data generator for Indian e-commerce sales data.

TASK:
Given a sample of existing CSV data, generate {num_records} additional rows that are statistically consistent with the sample.

SAMPLE DATA STRUCTURE:
Columns: {', '.join(columns)}

Sample Data:
{json.dumps(sample_data, indent=2)}

CONSTRAINTS:
- Use realistic Indian names (e.g., Priya Sharma, Arjun Nair, Ravi Kumar, Anjali Gupta)
- Use Indian cities (e.g., Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Pune, Kolkata)
- Use realistic product names for e-commerce (e.g., Laptop, Smartphone, Tablet, Headphones, TV, Washing Machine)
- Keep amounts in realistic ranges (Rs. 100 to Rs. 50,000)
- Use date formats matching the sample (YYYY-MM-DD)
- Ensure email formats are consistent (if applicable)
- Generate diverse and varied data across all fields
- Do NOT repeat existing values that should be unique
- Make the data statistically consistent with the sample patterns

OUTPUT FORMAT:
Return ONLY valid JSON in this exact format:

{{
    "records": [
        {{{', '.join([f'"{col}": "value"' for col in columns])}}},
        {{{', '.join([f'"{col}": "value"' for col in columns])}}}
    ]
}}

EXAMPLES:
If columns are: customer_id, name, city, product, amount, sale_date
Example output:
{{
    "records": [
        {{"customer_id": "51", "name": "Priya Sharma", "city": "Mumbai", "product": "Laptop", "amount": "45000", "sale_date": "2024-03-15"}},
        {{"customer_id": "52", "name": "Arjun Nair", "city": "Hyderabad", "product": "Smartphone", "amount": "22000", "sale_date": "2024-04-10"}}
    ]
}}

Generate {num_records} records now. Return pure JSON only, no markdown formatting or code blocks.
"""
    
    print(f"\n🔄 Generating {num_records} synthetic records using LLM...")
    
    response = generate_with_retry(
        client=client,
        model="gemini-flash-latest",
        contents=prompt
    )
    
    result = response.text.strip()
    
    # Try to extract JSON if wrapped in markdown code blocks
    if result.startswith("```"):
        result = result.replace("```json", "").replace("```", "").strip()
    
    try:
        data = json.loads(result)
        return data.get('records', [])
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON response: {e}")
        print(f"Raw response:\n{result}")
        return []


def save_augmented_data(original_data, synthetic_data, output_filename):
    """Save combined original and synthetic data to new CSV file"""
    
    if not synthetic_data:
        print("❌ No synthetic data to save")
        return
    
    # Combine original and synthetic data
    all_data = original_data + synthetic_data
    
    # Get column names from first record
    columns = list(all_data[0].keys())
    
    # Write to CSV
    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"\n✅ Augmented data saved to: {output_filename}")
    print(f"   Original records: {len(original_data)}")
    print(f"   Synthetic records: {len(synthetic_data)}")
    print(f"   Total records: {len(all_data)}")


def main():
    # Configuration
    input_file = "sample_data.csv"
    output_file = "augmented_data.csv"
    num_synthetic_records = 10
    
    print("="*60)
    print("📊 DATA AUGMENTATION WITH LLM")
    print("="*60)
    
    # Step 1: Read original CSV data
    print(f"\n📂 Reading data from: {input_file}")
    original_data = read_csv_data(input_file)
    print(f"   ✅ Loaded {len(original_data)} records")
    
    # Step 2: Analyze data structure
    print("\n🔍 Analyzing data structure...")
    analysis = analyze_data_structure(original_data)
    print(f"   ✅ Columns: {', '.join(analysis['columns'])}")
    
    # Step 3: Generate synthetic data using LLM
    synthetic_data = generate_synthetic_data(analysis, num_synthetic_records)
    
    if synthetic_data:
        print(f"   ✅ Generated {len(synthetic_data)} synthetic records")
        
        # Step 4: Save augmented data
        save_augmented_data(original_data, synthetic_data, output_file)
        
        # Display sample synthetic records
        print("\n📋 Sample synthetic records:")
        for i, record in enumerate(synthetic_data[:3], 1):
            print(f"   {i}. {record}")
    else:
        print("   ❌ Failed to generate synthetic data")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()