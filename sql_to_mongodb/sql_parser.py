import sqlparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class QueryType(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

@dataclass
class ParsedSQL:
    query_type: QueryType
    table_name: str
    columns: List[str]
    where_clause: Optional[Dict[str, Any]]
    order_by: Optional[List[Dict[str, str]]]
    limit: Optional[int]
    values: Optional[List[Any]]

class SQLParser:
    def __init__(self):
        # Supported operators for SQL to MongoDB translation
        self.supported_operators = {
            '=': '$eq',
            '!=': '$ne',
            '>': '$gt',
            '>=': '$gte',
            '<': '$lt',
            '<=': '$lte',
            'IN': '$in',
            'NOT IN': '$nin',
            'LIKE': '$regex',
            'AND': '$and',
            'OR': '$or'
        }

    def parse(self, sql_query: str) -> ParsedSQL:
        """
        Parse a SQL query into a structured format.
        
        Args:
            sql_query (str): The SQL query to parse
            
        Returns:
            ParsedSQL: Structured representation of the SQL query
        """
        # Parse the SQL query using sqlparse
        parsed = sqlparse.parse(sql_query)[0]
        
        # Determine query type
        query_type = self._get_query_type(parsed)
        
        # Extract basic components
        table_name = self._extract_table_name(parsed)
        columns = self._extract_columns(parsed)
        where_clause = self._extract_where_clause(parsed)
        order_by = self._extract_order_by(parsed)
        limit = self._extract_limit(parsed)
        values = self._extract_values(parsed) if query_type == QueryType.INSERT else None
        
        return ParsedSQL(
            query_type=query_type,
            table_name=table_name,
            columns=columns,
            where_clause=where_clause,
            order_by=order_by,
            limit=limit,
            values=values
        )

    def _get_query_type(self, parsed: sqlparse.sql.Statement) -> QueryType:
        """Extract the type of SQL query."""
        first_token = parsed.tokens[0].value.upper()
        return QueryType(first_token)

    def _extract_table_name(self, parsed: sqlparse.sql.Statement) -> str:
        """Extract the table name from the parsed SQL."""
        # Implementation depends on query type
        # This is a simplified version
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.Identifier):
                return token.get_real_name()
        return ""

    def _extract_columns(self, parsed: sqlparse.sql.Statement) -> List[str]:
        """Extract column names from the parsed SQL."""
        columns = []
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.IdentifierList):
                for identifier in token.get_identifiers():
                    columns.append(identifier.get_real_name())
        return columns

    def _extract_where_clause(self, parsed: sqlparse.sql.Statement) -> Optional[Dict[str, Any]]:
        """Extract and parse the WHERE clause."""
        where_token = None
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.Where):
                where_token = token
                break
        
        if not where_token:
            return None
            
        # Convert WHERE clause to MongoDB format
        return self._parse_where_clause(where_token)

    def _parse_where_clause(self, where_token: sqlparse.sql.Where) -> Dict[str, Any]:
        """Parse WHERE clause into MongoDB format."""
        # This is a simplified version - would need more complex parsing
        # for nested conditions, operators, etc.
        conditions = {}
        for token in where_token.tokens:
            if isinstance(token, sqlparse.sql.Comparison):
                field = token.left.get_real_name()
                operator = token.token_next(0)[1].value
                value = token.right.value
                
                if operator in self.supported_operators:
                    conditions[field] = {
                        self.supported_operators[operator]: value
                    }
        
        return conditions

    def _extract_order_by(self, parsed: sqlparse.sql.Statement) -> Optional[List[Dict[str, str]]]:
        """Extract ORDER BY clause."""
        # Implementation for ORDER BY parsing
        return None

    def _extract_limit(self, parsed: sqlparse.sql.Statement) -> Optional[int]:
        """Extract LIMIT clause."""
        # Implementation for LIMIT parsing
        return None

    def _extract_values(self, parsed: sqlparse.sql.Statement) -> Optional[List[Any]]:
        """Extract VALUES for INSERT statements."""
        # Implementation for VALUES parsing
        return None 