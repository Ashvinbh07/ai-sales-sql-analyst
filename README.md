# AI Sales SQL Analyst

An AI-powered sales analytics application that converts natural-language business questions into PostgreSQL queries, executes them against a sales database, analyzes the results, and generates business insights with automatic visualizations.

## 🚀 Overview

The AI Sales SQL Analyst allows users to ask questions such as:

- Which customer segment generated the highest revenue?
- Which product categories generated the highest revenue?
- Which customer segments had the largest revenue decline in Q2 compared with Q1?
- What was the monthly revenue trend in 2024?
- Which cities generated the highest profit?

Instead of writing SQL manually, the system uses a local LLM to understand the question and generate the required PostgreSQL query.

## 🏗️ Architecture

```text
User Question
      ↓
SQL Generator
      ↓
SQL Rules + Database Schema
      ↓
Generated SQL
      ↓
SQL Validator
      ↓
SQL Executor
      ↓
 ┌────┴─────┐
 ↓          ↓
Success    SQL Error
 ↓          ↓
Result   SQL Corrector
             ↓
        Corrected SQL
             ↓
          Execute
      ↓
Result Analyzer
      ↓
Business Insight
      ↓
Automatic Visualization
      ↓
Streamlit Dashboard
```

## ✨ Features

- Natural-language sales analytics
- AI-generated PostgreSQL SQL
- Dynamic database schema discovery
- Sales-specific SQL rules
- SQL validation before execution
- Automatic SQL error correction
- PostgreSQL query execution
- Pandas-based result processing
- AI-generated business insights
- Automatic chart selection
- Monthly and yearly trend visualizations
- Category, segment, city, and product comparisons
- Empty-result handling
- Interactive Streamlit interface

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| PostgreSQL | Sales database |
| SQLAlchemy | Database connection |
| Psycopg2 | PostgreSQL driver |
| Pandas | Result processing and analysis |
| Ollama | Local LLM runtime |
| Qwen2.5-Coder 7B | SQL generation and analysis |
| Requests | Ollama API communication |
| Streamlit | Web interface |
| python-dotenv | Environment variable management |
| Git | Version control |
| GitHub | Source code hosting |

## 🗄️ Database

The project uses a PostgreSQL sales database with three main tables.

### Customers

```text
customer_id
customer_name
segment
city
signup_date
```

### Products

```text
product_id
product_name
category
price
```

### Orders

```text
order_id
customer_id
product_id
order_date
quantity
revenue
profit
```

### Relationships

```text
customers.customer_id
        │
        ▼
orders.customer_id


products.product_id
        │
        ▼
orders.product_id
```

The sample database contains:

- 1,000 customers
- 50 products
- 20,000 orders
- Sales data from 2024-01-01 to 2025-12-31

## 🔄 How It Works

### 1. User asks a question

Example:

```text
Which customer segment generated the highest revenue?
```

### 2. Schema Discovery

The application dynamically reads the available tables and columns from PostgreSQL.

### 3. SQL Generation

The local Qwen2.5-Coder model generates PostgreSQL SQL using the database schema and predefined sales analytics rules.

### 4. SQL Validation

The generated SQL is checked before execution.

Only read-only queries are allowed.

### 5. SQL Execution

The validated query is executed against PostgreSQL and returned as a Pandas DataFrame.

### 6. Automatic SQL Correction

If the generated SQL fails because of a database error, the SQL corrector receives the original question, generated SQL, database error, database schema, and SQL rules and attempts to generate a corrected query.

### 7. Result Analysis

The query result is analyzed by the local LLM to produce a concise business insight based on the returned data.

### 8. Visualization

The application automatically selects a suitable chart based on the structure of the query result.

Examples:

- Category comparison → Bar chart
- Monthly trend → Line chart
- Yearly trend → Line chart
- Q1 vs Q2 comparison → Grouped bar chart

## 📊 Example Questions

```text
Which product categories generated the highest revenue?

Which customer segment generated the highest revenue?

Which cities generated the highest profit?

What was the monthly revenue trend in 2024?

Which customer segments had the largest revenue decline in Q2 compared with Q1?
```

## 📁 Project Structure

```text
ai-sales-sql-analyst/
│
├── app.py
├── workflow.py
│
├── database.py
├── schema.sql
├── schema_loader.py
├── seed.py
│
├── sql_rules.py
├── sql_generator.py
├── sql_validator.py
├── sql_executor.py
├── sql_corrector.py
│
├── result_analyzer.py
│
├── requirements.txt
├── .gitignore
├── README.md
└── report/
    └── AI_Sales_SQL_Analyst_Testing_Report.pdf
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ashvinbh07/ai-sales-sql-analyst.git
cd ai-sales-sql-analyst
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
ai_sql_analyst
```

Then run:

```bash
psql -U postgres -d ai_sql_analyst -f schema.sql
```

### 5. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ai_sql_analyst
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

### 6. Generate sample data

```bash
python seed.py
```

### 7. Install and run Ollama

Download the Qwen2.5-Coder model:

```bash
ollama pull qwen2.5-coder:7b
```

Make sure Ollama is running locally.

### 8. Start the application

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

## 🧪 Command-Line Usage

The complete workflow can also be tested without Streamlit:

```bash
python workflow.py
```

Enter a sales-related business question when prompted.

## 🔐 Security

The application includes a SQL validation layer that restricts generated queries to read-only operations.

The following operations are blocked:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE
```

The `.env` file and virtual environment are excluded from Git using `.gitignore`.

## 📌 Project Scope

This project is designed specifically for sales and e-commerce analytics using the provided PostgreSQL schema.

It is a portfolio project and should not be connected directly to a production database without additional security, authentication, access control, query limits, monitoring, and logging.

## 🔮 Future Improvements

- Query history
- User authentication
- Advanced SQL validation
- Query performance monitoring
- Additional visualization types
- Cloud deployment
- Automated SQL evaluation
- Production database access controls

## 👨‍💻 Project Goal

The goal of this project is to demonstrate how Large Language Models can be integrated with traditional data analytics workflows to create an AI-assisted interface for querying and understanding structured sales data.
