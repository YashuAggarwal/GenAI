# Module 7 - Unified LLM Applications Suite

A comprehensive Streamlit application that combines 5 different LLM-powered tasks in a single unified interface using Google Gemini API.

## 🌟 Features

### Task 1: Prompt Engineering
View and download carefully crafted prompts for distributed SQL query optimization.

### Task 2: LLM Chat & JSON Parsing
Analyze user activity data and receive structured JSON responses with insights and metrics.

### Task 3: Data Augmentation
Generate synthetic e-commerce data using LLM to augment existing datasets.

### Task 4: Interactive Document Query
Ask natural language questions about documents and get AI-powered answers.

### Task 5: Natural Language to SQL
Convert natural language questions into SQL queries and execute them against a SQLite database with customer and sales data.

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get it from: https://makersuite.google.com/app/apikey)

## 🚀 Installation

### 1. Clone or Navigate to Project Directory

```bash
cd Module_7
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
API_Key=your_actual_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

**Important:** The `.env` file is ignored by git to protect your API key.

## 🎯 Usage

### Start the Unified Application

```bash
streamlit run app.py
```

The application will open in your browser at http://localhost:8501

### Navigate Between Tasks

Use the tabs at the top to switch between different tasks:
- **Task 1: Prompts** - View prompt engineering examples
- **Task 2: LLM Chat** - Analyze user activity with structured output
- **Task 3: Data Aug** - Generate synthetic data
- **Task 4: Doc Query** - Query documents with natural language
- **Task 5: NL to SQL** - Convert questions to SQL and execute

## 📁 Project Structure

```
Module_7/
│
├── app.py                      # Unified Streamlit application (NEW)
├── .env                        # Environment variables (API keys)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
│
├── Task1/
│   └── Prompts.txt            # Prompt engineering samples
│
├── Task2/
│   └── llm_chat.py            # Standalone LLM chat script
│
├── Task3/
│   ├── data_augmentation.py   # Standalone data augmentation
│   ├── sample_data.csv        # Sample dataset
│   └── augmented_data.csv     # Generated data
│
├── Task4/
│   ├── interactive_query.py   # Standalone document query
│   ├── document_query.py      # Query script
│   └── sample_document.txt    # Sample document
│
└── Task5/
    ├── db.py                  # Database management
    ├── gemini_client.py       # Gemini API client
    ├── sql_executor.py        # SQL validation & execution
    └── sales.db               # SQLite database (auto-generated)
```

## 🔧 Configuration

### Environment Variables

The `.env` file supports both naming conventions:
- `GEMINI_API_KEY` - Used by Task 5
- `API_Key` - Used by Tasks 2, 3, 4
- `GEMINI_MODEL` - Model selection (default: gemini-1.5-flash)

### Database (Task 5)

The SQLite database is automatically created on first run with:
- **customer** table: Customer information
- **sales** table: Sales transactions
- Sample data with recent dates for time-based queries

## 🌐 Azure Deployment

### Azure App Service Startup Command

```bash
python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0 --server.headless true
```

### Azure Application Settings

Add these environment variables in Azure Portal:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

## 🔒 Security Features

- Environment variables for sensitive data
- SQL injection prevention (only SELECT queries allowed)
- `.env` file excluded from version control
- Database files excluded from git
- Secure API key handling

## 📦 Dependencies

- **streamlit**: Web application framework
- **google-genai**: Google Gemini API SDK
- **python-dotenv**: Environment variable management
- **pandas**: Data manipulation
- **sqlalchemy**: Database toolkit

## ⚠️ Troubleshooting

### API Key Not Found
**Error**: `GEMINI_API_KEY not found`

**Solution**: 
1. Ensure `.env` file exists in the root directory
2. Add your API key: `GEMINI_API_KEY=your_key_here`

### Module Import Error
**Error**: `ModuleNotFoundError`

**Solution**:
```bash
pip install -r requirements.txt
```

### Database Not Created (Task 5)
**Solution**: The database is automatically created on first run. If issues persist, delete `Task5/sales.db` and restart.

### Port Already in Use
**Solution**:
```bash
streamlit run app.py --server.port 8502
```

## 🎨 Customization

### Change Gemini Model

Edit `.env`:
```env
GEMINI_MODEL=gemini-1.5-pro  # or any available model
```

### Add Custom Data Sources

- **Task 3**: Replace `Task3/sample_data.csv`
- **Task 4**: Replace `Task4/sample_document.txt`
- **Task 5**: Modify `Task5/db.py` to add more tables

## 📝 Individual Task Scripts

While the unified app provides all functionality, individual scripts are available:

```bash
# Task 2
python Task2/llm_chat.py

# Task 3
python Task3/data_augmentation.py

# Task 4
python Task4/interactive_query.py
```

## 🔄 Git Best Practices

The `.gitignore` file protects:
- `.env` files (API keys)
- `__pycache__/` (Python cache)
- `venv/` (virtual environments)
- `*.db` files (databases)
- IDE-specific files

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify API key is correctly set
3. Ensure all dependencies are installed
4. Check Python version (3.8+)

## 📄 License

This project is created for educational purposes.

---

**Built with ❤️ using Google Gemini API and Streamlit**
