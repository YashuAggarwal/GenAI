# Natural Language to SQL Query System

A production-ready application that converts natural language questions into SQL queries using Google Gemini API and executes them against a SQLite database.

## 🌟 Features

- **Natural Language Processing**: Ask questions in plain English
- **Google Gemini Integration**: Powered by Google's latest Gemini 1.5 Flash model
- **Secure Query Execution**: Only SELECT queries allowed; all modifications blocked
- **Interactive UI**: Built with Streamlit for a smooth user experience
- **Real-time Results**: Instant query generation and execution
- **Sample Data**: Pre-populated database with customer and sales data

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get it from: https://makersuite.google.com/app/apikey)

## 🚀 Installation

### 1. Clone or Navigate to Project Directory

```bash
cd Task5
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Edit the `.env` file and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

**Important:** Never commit your actual API key to version control. The `.env` file should be added to `.gitignore`.

## 🗄️ Database Schema

The application uses SQLite with the following schema:

### Table: customer
| Column       | Type    | Description              |
|--------------|---------|--------------------------|
| customer_id  | INTEGER | Primary key              |
| name         | TEXT    | Customer full name       |
| email        | TEXT    | Customer email address   |
| join_date    | TEXT    | Join date (YYYY-MM-DD)   |

### Table: sales
| Column       | Type    | Description                    |
|--------------|---------|--------------------------------|
| sale_id      | INTEGER | Primary key                    |
| customer_id  | INTEGER | Foreign key to customer table  |
| product      | TEXT    | Product name                   |
| amount       | REAL    | Sale amount (dollars)          |
| sale_date    | TEXT    | Sale date (YYYY-MM-DD)         |

## 🎯 Usage

### Start the Application

```bash
streamlit run app.py
```

The application will:
1. Initialize the database (if not already created)
2. Populate with sample data
3. Open in your default browser (typically at http://localhost:8501)

### Example Questions

Try asking questions like:

- "Show all customers"
- "What are the total sales in the last 3 days?"
- "Who are the top 5 customers by total sales amount?"
- "List all sales for laptops"
- "What is the average sale amount?"
- "Show sales above $100"
- "Count the number of sales per product"
- "Show me customers who joined in 2024"

## 🏗️ Project Structure

```
Task5/
│
├── app.py                  # Streamlit application entry point
├── db.py                   # Database initialization and management
├── gemini_client.py        # Google Gemini API client
├── sql_executor.py         # SQL validation and execution
│
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
└── sales.db                # SQLite database (auto-generated)
```

## 🔧 Module Descriptions

### app.py
Main Streamlit application that provides the web interface. Handles user input, displays results, and coordinates between other modules.

### db.py
Database management module that:
- Creates SQLite database schema
- Initializes tables (customer, sales)
- Populates sample data with realistic dates
- Provides database connection utilities

### gemini_client.py
Google Gemini API integration that:
- Configures Gemini API with credentials
- Constructs prompts for SQL generation
- Converts natural language to SQL queries
- Extracts and cleans SQL from responses

### sql_executor.py
SQL validation and execution module that:
- Validates queries for security (blocks INSERT, UPDATE, DELETE, DROP)
- Prevents SQL injection attempts
- Executes SELECT queries safely
- Formats results in readable format

## 🔒 Security Features

- **Query Whitelist**: Only SELECT queries are allowed
- **Keyword Blocking**: INSERT, UPDATE, DELETE, DROP, ALTER operations are blocked
- **Injection Prevention**: Multiple statements are not allowed
- **Syntax Validation**: Basic syntax checks before execution
- **Environment Variables**: API keys stored securely in .env file

## 🛠️ Testing Individual Modules

You can test each module independently:

```bash
# Test database initialization
python db.py

# Test Gemini client (requires API key in .env)
python gemini_client.py

# Test SQL executor
python sql_executor.py
```

## 📦 Dependencies

- **streamlit**: Web application framework
- **google-genai**: Official Google Gemini API SDK (new version)
- **python-dotenv**: Environment variable management
- **pandas**: Data manipulation and display
- **sqlalchemy**: Database toolkit
- **protobuf**: Protocol buffer support

## ⚠️ Troubleshooting

### API Key Error
**Error**: `GEMINI_API_KEY not found in environment variables`

**Solution**: Make sure you've:
1. Created the `.env` file in the Task5 directory
2. Added your actual API key: `GEMINI_API_KEY=your_key_here`
3. The .env file is in the same directory as the Python files

### Module Not Found Error
**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**: 
```bash
pip install -r requirements.txt
```

### Database Not Created
**Error**: Database file not found or no data

**Solution**: The database is automatically created on first run. If issues persist:
```bash
python db.py
```

### Port Already in Use
**Error**: `Address already in use`

**Solution**: 
```bash
streamlit run app.py --server.port 8502
```

## 🎨 Customization

### Change Gemini Model

Edit `.env` file:
```env
GEMINI_MODEL=gemini-1.5-pro  # or any other available model
```

### Add More Sample Data

Edit the `sales` and `customers` lists in `db.py` and delete `sales.db` to regenerate.

### Modify UI Theme

Add to `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#FF4B4B"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"
```

## 📝 License

This project is created for educational purposes.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Check Python version (3.8+)

## 🔄 Version History

- **v1.0.0** (Initial Release)
  - Natural language to SQL conversion
  - Google Gemini API integration
  - Secure query execution
  - Interactive Streamlit UI
  - Sample database with realistic data

---

**Built with ❤️ using Google Gemini API and Streamlit**
