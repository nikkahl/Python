import copy
from typing import TYPE_CHECKING, Optional, Type
from types import TracebackType

if TYPE_CHECKING:
    from .database import Database

class TransactionError(Exception):
    """Custom exception raised when a transaction fails and rolls back."""
    pass

class Transaction:
    """Context manager for ensuring atomic database operations."""
    
    def __init__(self, db: 'Database'):
        self.db = db
        self._backup_state = {}

    def __enter__(self) -> 'Transaction':
        self._backup_state = {}
        for name, table in self.db.tables.items():
            self._backup_state[name] = {
                '_rows': copy.deepcopy(table._rows),
                '_indexes': copy.deepcopy(table._indexes),
                '_next_id': table._next_id
            }
        return self

    def __exit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_val: Optional[BaseException], 
        exc_tb: Optional[TracebackType]
    ) -> bool:
        if exc_type is not None:
            for name, state in self._backup_state.items():
                table = self.db.tables[name]
                table._rows = state['_rows']
                table._indexes = state['_indexes']
                table._next_id = state['_next_id']
            
            if issubclass(exc_type, TransactionError):
                return False
                
            raise TransactionError(f"Transaction rolled back. Caused by: {exc_val}") from exc_val
        
        self._backup_state.clear()
        return False