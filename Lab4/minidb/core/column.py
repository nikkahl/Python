from typing import Any, Tuple, Optional, Iterable, TYPE_CHECKING
from .datatypes import DataType

if TYPE_CHECKING:
    from ..database import Database

class Column:
    """Represents a column schema in a database table."""

    def __init__(
        self,
        name: str,
        data_type: DataType,
        nullable: bool = True,
        unique: bool = False,
        references: Optional[Tuple[str, str]] = None
    ):
        """
        Initializes a new Column.
        
        :param name: The name of the column.
        :param data_type: An instance of a DataType subclass.
        :param nullable: Whether the column can contain None.
        :param unique: Whether the column values must be unique.
        :param references: Tuple of (table_name, column_name) for foreign keys.
        """
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.unique = unique
        self.references = references

    def validate(self, value: Any) -> None:
        """
        Validates a value against the column's data type and nullability rules.
        Raises ValueError if validation fails.
        """
        if value is None:
            if not self.nullable:
                raise ValueError(f"Column '{self.name}' cannot be null.")
            return

        if not self.data_type.validate(value):
            raise TypeError(f"Invalid type for column '{self.name}'. Expected {self.data_type}, got {type(value).__name__}.")

    def check_unique(self, value: Any, table_rows: Iterable[Any]) -> None:
        """
        Checks if the value is unique among the existing rows.
        Assumes table_rows yields objects that can be accessed via dictionary keys.
        """
        if not self.unique or value is None:
            return
            
        for row in table_rows:
            if row[self.name] == value:
                raise ValueError(f"Unique constraint failed: '{value}' already exists in column '{self.name}'.")

    def check_foreign_key(self, value: Any, database: 'Database') -> None:
        """
        Validates the foreign key constraint against the target table.
        """
        if not self.references or value is None:
            return

        ref_table_name, ref_col_name = self.references
        ref_table = database.get_table(ref_table_name)
        
        found = False
        for row in ref_table:
            if row[ref_col_name] == value:
                found = True
                break
                
        if not found:
            raise ValueError(
                f"Foreign key constraint failed: Value '{value}' not found in "
                f"{ref_table_name}.{ref_col_name}."
            )

    def __repr__(self) -> str:
        constraints = []
        if not self.nullable:
            constraints.append("NOT NULL")
        if self.unique:
            constraints.append("UNIQUE")
        if self.references:
            constraints.append(f"REFERENCES {self.references[0]}({self.references[1]})")
            
        constraint_str = f" ({', '.join(constraints)})" if constraints else ""
        return f"<Column: {self.name} {self.data_type}{constraint_str}>"