import json
from typing import Dict, List
from datetime import date, datetime

from .core.table import Table
from .core.column import Column
from .core.datatypes import DataType, DateType
from .core.row import Row
from .transaction import Transaction


class Database:
    """Central access point for the database."""

    def __init__(self, name: str):
        self.name = name
        self.tables: Dict[str, Table] = {}

    def create_table(self, name: str, columns: List[Column]) -> Table:
        """Creates a new table and adds it to the database."""
        if name in self.tables:
            raise ValueError(f"Table '{name}' already exists.")
        
        new_table = Table(name, columns, self)
        self.tables[name] = new_table
        return new_table

    def get_table(self, name: str) -> Table:
        """Retrieves a table by name."""
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist.")
        return self.tables[name]

    def transaction(self) -> Transaction:
        """Returns a transaction context manager for atomic operations."""
        return Transaction(self)

    def save_to_json(self, filename: str) -> None:
        """Serializes the database schema and data to a JSON file."""
        db_dump = {"name": self.name, "tables": {}}

        for table_name, table in self.tables.items():
            cols_dump = []
            for col in table.columns.values():
                cols_dump.append({
                    "name": col.name,
                    "data_type": str(col.data_type),
                    "nullable": col.nullable,
                    "unique": col.unique,
                    "references": col.references
                })

            rows_dump = []
            for row in table:
                row_data = row.to_dict()
                for key, val in row_data.items():
                    if isinstance(val, (date, datetime)):
                        row_data[key] = val.isoformat()
                rows_dump.append(row_data)

            db_dump["tables"][table_name] = {
                "columns": cols_dump,
                "rows": rows_dump,
                "next_id": table._next_id
            }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(db_dump, f, indent=4)

    def load_from_json(self, filename: str) -> None:
        """Loads database schema and data from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            db_dump = json.load(f)

        self.name = db_dump.get("name", self.name)
        self.tables.clear()

        for table_name, table_data in db_dump["tables"].items():
            columns = []
            for col_data in table_data["columns"]:
                ref = col_data.get("references")
                if ref:
                    ref = tuple(ref)

                columns.append(Column(
                    name=col_data["name"],
                    data_type=DataType.from_string(col_data["data_type"]),
                    nullable=col_data["nullable"],
                    unique=col_data["unique"],
                    references=ref
                ))
            
            table = self.create_table(table_name, columns)
            table._next_id = table_data.get("next_id", 1)

        for table_name, table_data in db_dump["tables"].items():
            table = self.get_table(table_name)
            
            for row_data in table_data["rows"]:
                for col_name, col in table.columns.items():
                    if isinstance(col.data_type, DateType) and row_data.get(col_name):
                        row_data[col_name] = date.fromisoformat(row_data[col_name])
                    
                row_id = row_data["id"] 
                row = Row(row_id, row_data)
                
                table._rows[row_id] = row
                table._add_to_index(row)