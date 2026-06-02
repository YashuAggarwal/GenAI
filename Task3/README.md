# Task 3: Data Generation & Augmentation with LLM

## Overview
This project demonstrates how to use Large Language Models (LLMs) to generate synthetic data for testing purposes when actual data is limited.

## Files
- **sample_data.csv** - Original dataset with 5 customer records
- **data_augmentation.py** - Main script that uses LLM to generate synthetic data
- **augmented_data.csv** - Output file containing original + synthetic data (15 records)

## How It Works

### 1. **Read Original Data**
The script reads the CSV file and loads existing records.

### 2. **Analyze Structure**
Analyzes the data structure (columns, data types, patterns).

### 3. **Generate Synthetic Data**
Uses Gemini LLM to generate realistic synthetic records that match the pattern and structure of the original data.

### 4. **Save Augmented Dataset**
Combines original and synthetic data into a new CSV file.

## Features

✅ **Automatic Data Analysis** - Understands your data structure automatically  
✅ **LLM-Powered Generation** - Creates realistic and diverse synthetic data  
✅ **Retry Logic** - Handles API rate limits with exponential backoff  
✅ **CSV Format** - Easy to integrate with existing workflows  
✅ **Configurable** - Adjust number of records to generate  

## Usage

```python
python data_augmentation.py
```

## Configuration

Edit these variables in `data_augmentation.py`:

```python
input_file = "sample_data.csv"              # Your source CSV file
output_file = "augmented_data.csv"          # Output filename
num_synthetic_records = 10                   # How many records to generate
```

## Use Cases

- **Testing** - Generate test data for QA and development
- **Machine Learning** - Augment training datasets
- **Demo/Prototyping** - Create realistic sample data quickly
- **Data Privacy** - Replace sensitive real data with synthetic alternatives

## Requirements

- Python 3.7+
- google-genai library
- python-dotenv
- API key in .env file

## Example Output

```
Original records: 5
Synthetic records: 10
Total records: 15
```

The LLM generates diverse, realistic data including:
- Various names, ages, and cities
- Realistic email addresses
- Different occupations
- Varied purchase amounts

## Notes

- Generated data is synthetic and fictional
- Data patterns match the original dataset
- Each generation is unique due to LLM creativity
- API usage is optimized with retry logic
