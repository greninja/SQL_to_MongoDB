from typing import Dict, List, Union, Any
from .sql_parser import SQLParser
from .mongodb_builder import MongoDBQueryBuilder

class SQLToMongoDBTranslator:
    def __init__(self):
        self.sql_parser = SQLParser()
        self.mongodb_builder = MongoDBQueryBuilder()

    def translate(self, sql_query: str) -> Dict[str, Any]:
        """
        Translate a SQL query to MongoDB query format.
        
        Args:
            sql_query (str): The SQL query to translate
            
        Returns:
            Dict[str, Any]: The equivalent MongoDB query
        """
        # Parse the SQL query
        parsed_sql = self.sql_parser.parse(sql_query)
        
        # Build MongoDB query
        mongodb_query = self.mongodb_builder.build(parsed_sql)
        
        return mongodb_query

    def translate_batch(self, sql_queries: List[str]) -> List[Dict[str, Any]]:
        """
        Translate multiple SQL queries to MongoDB queries.
        
        Args:
            sql_queries (List[str]): List of SQL queries to translate
            
        Returns:
            List[Dict[str, Any]]: List of equivalent MongoDB queries
        """
        return [self.translate(query) for query in sql_queries] 