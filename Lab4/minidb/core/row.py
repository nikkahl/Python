from typing import Any, Dict, Iterator

class Row:
    """Represents a single record in a database table."""
    
    def __init__(self, row_id: int, data: Dict[str, Any]):
        self.id = row_id
        self._data = data
        
    def __getitem__(self, key: str) -> Any:
        return self._data[key]
        
    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value
        
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Row):
            return False
        return self.id == other.id and self._data == other._data
        
    def __iter__(self) -> Iterator[str]:
        return iter(self._data)
        
    def to_dict(self) -> Dict[str, Any]:
        """Returns the row data as a dictionary, including the id."""
        result = self._data.copy()
        result['id'] = self.id
        return result
        
    def __repr__(self) -> str:
        return f"<Row id={self.id} data={self._data}>"