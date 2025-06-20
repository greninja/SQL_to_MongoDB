from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sql_to_mongodb import SQLToMongoDBTranslator
from sql_to_mongodb.agent import SQLToMongoDBAgent
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="SQL to MongoDB Translator")
templates = Jinja2Templates(directory="web/templates")

# Mount static files if directory exists
static_dir = "web/static"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize the translator and agent
translator = SQLToMongoDBTranslator()

# Try to use OpenAI if API key is available, otherwise use Ollama
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    agent = SQLToMongoDBAgent(llm_type="openai", openai_api_key=openai_api_key)
else:
    # Use Ollama (free local LLM)
    agent = SQLToMongoDBAgent(llm_type="ollama", model_name="llama2")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/translate")
async def translate_sql(sql_query: str = Form(...)):
    try:
        mongodb_query = translator.translate(sql_query)
        return {
            "status": "success",
            "mongodb_query": mongodb_query
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/translate/batch")
async def translate_batch(sql_queries: str = Form(...)):
    try:
        queries = json.loads(sql_queries)
        mongodb_queries = translator.translate_batch(queries)
        return {
            "status": "success",
            "mongodb_queries": mongodb_queries
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/agent/process")
async def process_agent_request(request: str = Form(...)):
    """Process a request using the agent."""
    try:
        response = agent.process_request(request)
        return response
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/agent/explain")
async def explain_translation(sql_query: str = Form(...)):
    """Get an explanation of how a SQL query was translated to MongoDB."""
    try:
        explanation = agent._explain_translation(sql_query)
        return {
            "status": "success",
            "explanation": explanation
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/agent/validate")
async def validate_sql(sql_query: str = Form(...)):
    """Validate if a SQL query is valid and can be translated."""
    try:
        validation = agent._validate_sql(sql_query)
        return validation
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        } 