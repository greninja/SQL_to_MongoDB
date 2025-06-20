from typing import Dict, List, Any, Optional
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import BaseTool
from langchain.chains import LLMChain
from .translator import SQLToMongoDBTranslator
import re
import json
import os

class SQLToMongoDBAgent:
    def __init__(self, llm_type: str = "ollama", model_name: str = "llama2", openai_api_key: str = None):
        self.translator = SQLToMongoDBTranslator()
        self.llm = self._create_llm(llm_type, model_name, openai_api_key)
        self.tools = self._create_tools()
        self.agent_executor = self._create_agent()

    def _create_llm(self, llm_type: str, model_name: str, openai_api_key: str = None):
        """Create LLM based on type."""
        if llm_type == "openai" and openai_api_key:
            return ChatOpenAI(
                temperature=0,
                model="gpt-3.5-turbo",
                openai_api_key=openai_api_key
            )
        elif llm_type == "ollama":
            try:
                return Ollama(
                    model=model_name,
                    temperature=0
                )
            except Exception as e:
                print(f"Warning: Could not connect to Ollama. Error: {e}")
                print("Please install Ollama and pull a model: https://ollama.ai/")
                print("Example: ollama pull llama2")
                return self._create_fallback_llm()
        else:
            return self._create_fallback_llm()

    def _create_fallback_llm(self):
        """Create a simple fallback LLM that provides basic explanations."""
        class FallbackLLM:
            def invoke(self, prompt):
                class MockResponse:
                    def __init__(self, content):
                        self.content = content
                
                # Simple rule-based explanation
                if "SQL" in prompt and "MongoDB" in prompt:
                    explanation = self._generate_simple_explanation(prompt)
                    return MockResponse(explanation)
                else:
                    return MockResponse("I'm a fallback LLM. Please install Ollama for better explanations.")
            
            def _generate_simple_explanation(self, prompt):
                """Generate a simple explanation without using an LLM."""
                if "SELECT" in prompt:
                    return """This SQL SELECT query was converted to a MongoDB find operation. 
                    The table name becomes a MongoDB collection, WHERE conditions become filter criteria, 
                    and SELECT columns become projection fields. ORDER BY becomes sort options, and LIMIT becomes limit options."""
                elif "INSERT" in prompt:
                    return """This SQL INSERT query was converted to a MongoDB insert operation. 
                    The table name becomes a MongoDB collection, and the VALUES become documents to insert."""
                elif "UPDATE" in prompt:
                    return """This SQL UPDATE query was converted to a MongoDB update operation. 
                    The table name becomes a MongoDB collection, WHERE conditions become filter criteria, 
                    and SET values become update operations using $set."""
                elif "DELETE" in prompt:
                    return """This SQL DELETE query was converted to a MongoDB delete operation. 
                    The table name becomes a MongoDB collection, and WHERE conditions become filter criteria."""
                else:
                    return "This SQL query was converted to its MongoDB equivalent using standard transformation rules."
        
        return FallbackLLM()

    def _create_tools(self) -> List[BaseTool]:
        """Create tools for the agent."""
        return [
            Tool(
                name="translate_sql",
                func=self.translator.translate,
                description="Translates a SQL query to MongoDB query format"
            ),
            Tool(
                name="translate_batch",
                func=self.translator.translate_batch,
                description="Translates multiple SQL queries to MongoDB queries"
            ),
            Tool(
                name="explain_translation",
                func=self._explain_translation,
                description="Explains how a SQL query was translated to MongoDB"
            ),
            Tool(
                name="validate_sql",
                func=self._validate_sql,
                description="Validates if a SQL query is valid and can be translated"
            )
        ]

    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor using the newer LangChain API."""
        prompt = PromptTemplate(
            input_variables=["input", "agent_scratchpad"],
            template="""You are an expert SQL to MongoDB translator agent. Your goal is to help users translate SQL queries to MongoDB queries and provide explanations.

Available tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}"""
        )
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True
        )

    def _explain_translation(self, sql_query: str) -> str:
        """Explain how a SQL query was translated to MongoDB."""
        try:
            mongodb_query = self.translator.translate(sql_query)
            explanation = self.llm.invoke(
                f"""Explain how this SQL query:
                {sql_query}
                was translated to this MongoDB query:
                {json.dumps(mongodb_query, indent=2)}
                Focus on the key transformations and MongoDB concepts used."""
            )
            return explanation.content
        except Exception as e:
            return f"Error explaining translation: {str(e)}"

    def _validate_sql(self, sql_query: str) -> Dict[str, Any]:
        """Validate if a SQL query is valid and can be translated."""
        try:
            # Try to translate the query
            self.translator.translate(sql_query)
            return {
                "is_valid": True,
                "message": "SQL query is valid and can be translated"
            }
        except Exception as e:
            return {
                "is_valid": False,
                "message": f"Invalid SQL query: {str(e)}"
            }

    def process_request(self, request: str) -> Dict[str, Any]:
        """
        Process a user request using the agent.
        
        Args:
            request (str): The user's request
            
        Returns:
            Dict[str, Any]: The agent's response
        """
        try:
            response = self.agent_executor.invoke({"input": request})
            return {
                "status": "success",
                "response": response["output"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
