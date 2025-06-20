from typing import Dict, List, Any, Optional
from .sql_parser import ParsedSQL, QueryType

class MongoDBQueryBuilder:
    def build(self, parsed_sql: ParsedSQL) -> Dict[str, Any]:
        """
        Build a MongoDB query from parsed SQL.
        
        Args:
            parsed_sql (ParsedSQL): The parsed SQL query
            
        Returns:
            Dict[str, Any]: The MongoDB query
        """
        if parsed_sql.query_type == QueryType.SELECT:
            return self._build_find_query(parsed_sql)
        elif parsed_sql.query_type == QueryType.INSERT:
            return self._build_insert_query(parsed_sql)
        elif parsed_sql.query_type == QueryType.UPDATE:
            return self._build_update_query(parsed_sql)
        elif parsed_sql.query_type == QueryType.DELETE:
            return self._build_delete_query(parsed_sql)
        else:
            raise ValueError(f"Unsupported query type: {parsed_sql.query_type}")

    def _build_find_query(self, parsed_sql: ParsedSQL) -> Dict[str, Any]:
        """Build a MongoDB find query."""
        query = {
            "collection": parsed_sql.table_name,
            "operation": "find",
            "filter": parsed_sql.where_clause or {},
            "projection": self._build_projection(parsed_sql.columns),
            "options": {}
        }
        
        if parsed_sql.order_by:
            query["options"]["sort"] = self._build_sort(parsed_sql.order_by)
            
        if parsed_sql.limit:
            query["options"]["limit"] = parsed_sql.limit
            
        return query

    def _build_insert_query(self, parsed_sql: ParsedSQL) -> Dict[str, Any]:
        """Build a MongoDB insert query."""
        if not parsed_sql.values:
            raise ValueError("No values provided for INSERT query")
            
        return {
            "collection": parsed_sql.table_name,
            "operation": "insert",
            "documents": self._build_documents(parsed_sql.columns, parsed_sql.values)
        }

    def _build_update_query(self, parsed_sql: ParsedSQL) -> Dict[str, Any]:
        """Build a MongoDB update query."""
        return {
            "collection": parsed_sql.table_name,
            "operation": "update",
            "filter": parsed_sql.where_clause or {},
            "update": self._build_update_document(parsed_sql.columns, parsed_sql.values),
            "options": {"multi": True}
        }

    def _build_delete_query(self, parsed_sql: ParsedSQL) -> Dict[str, Any]:
        """Build a MongoDB delete query."""
        return {
            "collection": parsed_sql.table_name,
            "operation": "delete",
            "filter": parsed_sql.where_clause or {}
        }

    def _build_projection(self, columns: List[str]) -> Dict[str, int]:
        """Build MongoDB projection from column list."""
        if not columns or columns[0] == "*":
            return {}
        return {col: 1 for col in columns}

    def _build_sort(self, order_by: List[Dict[str, str]]) -> Dict[str, int]:
        """Build MongoDB sort from ORDER BY clause."""
        return {item["field"]: 1 if item["direction"] == "ASC" else -1 
                for item in order_by}

    def _build_documents(self, columns: List[str], values: List[Any]) -> List[Dict[str, Any]]:
        """Build MongoDB documents from columns and values."""
        if not values:
            return []
            
        if isinstance(values[0], list):
            # Multiple rows
            return [{col: val for col, val in zip(columns, row)} 
                    for row in values]
        else:
            # Single row
            return [{col: val for col, val in zip(columns, values)}]

    def _build_update_document(self, columns: List[str], values: List[Any]) -> Dict[str, Any]:
        """Build MongoDB update document."""
        if not values:
            return {}
            
        return {"$set": {col: val for col, val in zip(columns, values)}} 