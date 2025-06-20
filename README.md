# SQL to MongoDB Translator

A Python package that translates SQL queries to MongoDB queries using an intelligent agent powered by LangChain. This tool helps in migrating from SQL databases to MongoDB by providing an automated way to convert SQL queries to their MongoDB equivalents.

## Features

- **Intelligent Translation**: Uses LangChain agents for smart SQL to MongoDB translation
- **Web Interface**: Modern web UI with syntax highlighting and real-time translation
- **Query Validation**: Validates SQL queries before translation
- **Translation Explanations**: Provides detailed explanations of how queries are translated
- **Batch Processing**: Translate multiple queries at once
- **API Endpoints**: RESTful API for programmatic access

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for agent features)

### Installation

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd sql_to_mongodb
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file in the root directory:
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### Running the Application

#### Option 1: Web Application (Recommended)

Run the web interface:
```bash
python run_webapp.py
```

Then open your browser and navigate to: `http://localhost:8000`

#### Option 2: Command Line

Use the translator directly in Python:
```python
from sql_to_mongodb import SQLToMongoDBTranslator

translator = SQLToMongoDBTranslator()
sql_query = "SELECT name, age FROM users WHERE age > 18 ORDER BY name ASC LIMIT 10"
mongodb_query = translator.translate(sql_query)
print(mongodb_query)
```

#### Option 3: Using the Agent

```python
from sql_to_mongodb.agent import SQLToMongoDBAgent
import os

agent = SQLToMongoDBAgent(openai_api_key=os.getenv("OPENAI_API_KEY"))
response = agent.process_request("Translate this SQL query: SELECT * FROM users WHERE age > 18")
print(response)
```

## Web Interface Features

The web interface provides:

- **Split-screen layout**: SQL input on the left, MongoDB output on the right
- **Syntax highlighting**: Using CodeMirror for better readability
- **Query validation**: Validate SQL queries before translation
- **Translation explanations**: Get detailed explanations of translations
- **Copy to clipboard**: Easy copying of MongoDB queries
- **Example queries**: Pre-loaded examples for reference

## API Endpoints

### Basic Translation
- `POST /translate` - Translate a single SQL query
- `POST /translate/batch` - Translate multiple SQL queries

### Agent Features
- `POST /agent/process` - Process requests using the intelligent agent
- `POST /agent/explain` - Get explanation of translation
- `POST /agent/validate` - Validate SQL query

### Example API Usage

```bash
# Translate a query
curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "sql_query=SELECT name, age FROM users WHERE age > 18"

# Validate a query
curl -X POST "http://localhost:8000/agent/validate" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "sql_query=SELECT * FROM users"
```

## Example Queries

### SELECT Queries
```sql
SELECT name, age FROM users WHERE age > 18 ORDER BY name ASC LIMIT 10
```

Translates to:
```json
{
  "collection": "users",
  "operation": "find",
  "filter": {"age": {"$gt": 18}},
  "projection": {"name": 1, "age": 1},
  "options": {
    "sort": {"name": 1},
    "limit": 10
  }
}
```

### INSERT Queries
```sql
INSERT INTO users (name, age) VALUES ('John', 25)
```

### UPDATE Queries
```sql
UPDATE users SET age = 26 WHERE name = 'John'
```

### DELETE Queries
```sql
DELETE FROM users WHERE age < 18
```

## Supported SQL Features

- Basic SELECT, INSERT, UPDATE, DELETE operations
- WHERE clauses with common operators (=, !=, >, >=, <, <=, IN, NOT IN, LIKE)
- ORDER BY clauses
- LIMIT clauses
- Column projections
- Basic JOIN operations (coming soon)

## Development

### Project Structure
```
sql_to_mongodb/
├── sql_to_mongodb/
│   ├── __init__.py
│   ├── translator.py      # Main translator
│   ├── sql_parser.py      # SQL parsing logic
│   ├── mongodb_builder.py # MongoDB query building
│   └── agent.py          # LangChain agent
├── web/
│   ├── main.py           # FastAPI application
│   └── templates/
│       └── index.html    # Web interface
├── requirements.txt      # Dependencies
├── run_webapp.py        # Web app runner
└── README.md
```

### Running Tests
```bash
python test_translator.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **OpenAI API errors**: Check your API key in the `.env` file
   ```bash
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

3. **Port already in use**: Change the port in `run_webapp.py`
   ```python
   uvicorn.run("web.main:app", host="0.0.0.0", port=8001, reload=True)
   ```

### Getting Help

- Check the API documentation at `http://localhost:8000/docs`
- Review the example queries in the web interface
- Check the console output for error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.





