import re
from typing import Any, Dict

class Condition:
    """Base class for query conditions."""
    
    def evaluate(self, row_data: Dict[str, Any]) -> bool:
        """Evaluates the condition against a specific row's data."""
        raise NotImplementedError

    def __and__(self, other: 'Condition') -> 'Condition':
        return LogicalCondition(self, "AND", other)

    def __or__(self, other: 'Condition') -> 'Condition':
        return LogicalCondition(self, "OR", other)


class Compare(Condition):
    """Leaf node for comparing a column to a value."""
    
    def __init__(self, column: str, operator: str, value: Any):
        self.column = column
        self.operator = operator.upper()
        self.value = value

    def evaluate(self, row_data: Dict[str, Any]) -> bool:
        val = row_data.get(self.column)
        
        if val is None and self.operator != "LIKE":
            return False 

        if self.operator == "=":
            return val == self.value
        elif self.operator == "!=":
            return val != self.value
        elif self.operator == ">":
            return val > self.value
        elif self.operator == "<":
            return val < self.value
        elif self.operator == ">=":
            return val >= self.value
        elif self.operator == "<=":
            return val <= self.value
        elif self.operator == "LIKE":
            if not isinstance(val, str):
                return False
            
            escaped_val = re.escape(str(self.value))
            pattern = "^" + escaped_val.replace("\\%", ".*").replace("%", ".*").replace("\\_", ".").replace("_", ".") + "$"

            return re.match(pattern, val, re.IGNORECASE) is not None


class LogicalCondition(Condition):
    """Node for combining two conditions with AND / OR."""
    
    def __init__(self, left: Condition, operator: str, right: Condition):
        self.left = left
        self.operator = operator.upper()
        self.right = right

    def evaluate(self, row_data: Dict[str, Any]) -> bool:
        if self.operator == "AND":
            return self.left.evaluate(row_data) and self.right.evaluate(row_data)
        elif self.operator == "OR":
            return self.left.evaluate(row_data) or self.right.evaluate(row_data)
            
        raise ValueError(f"Unknown logical operator: {self.operator}")