from typing import Any, Dict, List, Optional, Iterator, TYPE_CHECKING
from .row import Row
from .column import Column
from ..query.engine import Query

if TYPE_CHECKING:
    from ..database import Database

class Table:
    """Coordinator for data structure, constraints, and CRUD operations."""

    def __init__(self, name: str, columns: List[Column], database: 'Database'):
        self.name = name
                           #DICTIONARY COMPREHENSION
        self.columns = {col.name: col for col in columns}
        self.database = database
        
        self._rows: Dict[int, Row] = {}
        self._next_id = 1

        self._indexes: Dict[str, Dict[Any, int]] = {
            col.name: {} for col in columns if col.unique
        }

    def _validate_row_data(self, data: Dict[str, Any], exclude_row_id: Optional[int] = None) -> None:
        """Validates data against column constraints before insert/update."""
        for col_name, col in self.columns.items():
            value = data.get(col_name)
            
            col.validate(value)
            
            rows_to_check = [r for r in self._rows.values() if r.id != exclude_row_id]
            col.check_unique(value, rows_to_check)
            
            col.check_foreign_key(value, self.database)

    def insert(self, data: Dict[str, Any]) -> Row:
        """Inserts a new row into the table."""
        row_id = data.get("id", self._next_id)
        if row_id in self._rows:
            raise ValueError(f"Primary key error: row with id {row_id} already exists in {self.name}.")

        for col_name in self.columns:
            if col_name not in data and col_name != "id":
                data[col_name] = None

        self._validate_row_data(data)

        row = Row(row_id, data)
        self._rows[row_id] = row
        
        if row_id >= self._next_id:
            self._next_id = row_id + 1

        self._add_to_index(row)
        return row

    def get_by_id(self, row_id: int) -> Optional[Row]:
        """Retrieves a row by its exact ID."""
        return self._rows.get(row_id)

    def get_row(self, column_name: str, value: Any) -> List[Row]:
        """
        Retrieves rows matching a specific column value.
        Utilizes the O(1) index dictionary if the column is marked as unique.
        """
        if column_name not in self.columns and column_name != "id":
            raise ValueError(f"Column '{column_name}' does not exist in table '{self.name}'.")

        if column_name in self._indexes:
            row_id = self._indexes[column_name].get(value)
            if row_id is not None:
                return [self._rows[row_id]]
            return []

        return [row for row in self._rows.values() if row.to_dict().get(column_name) == value]

    def update(self, row_id: int, data: Dict[str, Any]) -> None:
        """Updates an existing row."""
        row = self.get_by_id(row_id)
        if not row:
            raise ValueError(f"Row with id {row_id} does not exist.")

        new_data = row.to_dict()
        new_data.update(data)

        self._validate_row_data(new_data, exclude_row_id=row_id)

        self._remove_from_index(row)

        for key, val in data.items():
            if key in self.columns:
                row[key] = val

        self._add_to_index(row)

    def delete(self, row_id: int, policy: str = "RESTRICT") -> None:
        """
        Deletes a row from the table. 
        Enforces RESTRICT or CASCADE policies for foreign keys.
        """
        if row_id not in self._rows:
            return

        for target_table_name, target_table in self.database.tables.items():
            if target_table_name == self.name:
                continue
                
            for col_name, col in target_table.columns.items():
                if col.references == (self.name, "id"):
                    dependent_rows = target_table.get_row(col_name, row_id)
                    
                    if dependent_rows:
                        if policy == "RESTRICT":
                            raise ValueError(
                                f"RESTRICT POLICY: Cannot delete row {row_id} from '{self.name}'. "
                                f"It is referenced by '{target_table_name}.{col_name}'."
                            )
                        elif policy == "CASCADE":
                            
                            for dep_row in dependent_rows:
                                target_table.delete(dep_row.id, policy="CASCADE")

        row = self._rows.pop(row_id)
        self._remove_from_index(row)

    def _add_to_index(self, row: Row) -> None:
        for col_name, index_dict in self._indexes.items():
            val = row[col_name]
            if val is not None:
                index_dict[val] = row.id

    def _remove_from_index(self, row: Row) -> None:
        for col_name, index_dict in self._indexes.items():
            val = row[col_name]
            if val is not None and val in index_dict:
                del index_dict[val]

    def __iter__(self) -> Iterator[Row]:
        return iter(self._rows.values())

    def __len__(self) -> int:
        return len(self._rows)
    
    def query(self) -> 'Query':
        """Returns a Query object initialized with this table's rows."""
        from ..query.engine import Query
        return Query(self)