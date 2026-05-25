from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator
from datetime import datetime, date

class DataType(ABC):
    """Base class for all database data types."""

    @abstractmethod
    def validate(self, value: Any) -> bool:
        """Validates if the provided value matches the expected type."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Returns the string representation of the data type."""
        pass

    @classmethod
    def from_string(cls, type_str: str) -> "DataType":
        """Creates an instance of a DataType based on a string description."""
        type_str = type_str.strip().upper()
        mapping = {
            "INTEGER": IntegerType,
            "STRING": StringType,
            "BOOLEAN": BooleanType,
            "DATE": DateType,
            "FLOAT": FloatType
        }
        
        target_class = mapping.get(type_str)
        if not target_class:
            raise ValueError(f"Unknown data type string: {type_str}")
        return target_class()


class IntegerType(DataType):
    def validate(self, value: Any) -> bool:
        return isinstance(value, int) and not isinstance(value, bool)

    def __str__(self) -> str:
        return "INTEGER"


class StringType(DataType):
    def validate(self, value: Any) -> bool:
        return isinstance(value, str)

    def __str__(self) -> str:
        return "STRING"


class BooleanType(DataType):
    def validate(self, value: Any) -> bool:
        return isinstance(value, bool)

    def __str__(self) -> str:
        return "BOOLEAN"


class DateType(DataType):
    def validate(self, value: Any) -> bool:
        if isinstance(value, (date, datetime)):
            return True
        if isinstance(value, str):
            try:
                date.fromisoformat(value)
                return True
            except ValueError:
                return False
        return False

    def __str__(self) -> str:
        return "DATE"


class FloatType(DataType):
    def validate(self, value: Any) -> bool:
        return isinstance(value, float) or isinstance(value, int)

    def __str__(self) -> str:
        return "FLOAT"