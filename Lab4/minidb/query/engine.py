from typing import Any, List, Dict, Optional, Union, Iterable
from collections import defaultdict
from .conditions import Condition, Compare

#Agg Wrapper Cls

class AggFunc:
    def __init__(self, column: str):
        self.column = column
    def __repr__(self):
        return f"{self.__class__.__name__}({self.column})"

class COUNT(AggFunc): pass
class SUM(AggFunc): pass
class AVG(AggFunc): pass
class MAX(AggFunc): pass
class MIN(AggFunc): pass

#Join Logic

class JoinedTable:
    """Represents an INNER JOIN between two tables."""
    
    def __init__(self, table1: Any, table2: Any, on_col1: str, on_col2: str):
        self.table1 = table1
        self.table2 = table2
        self.on_col1 = on_col1
        self.on_col2 = on_col2

    def __iter__(self):
        """Yields merged dictionary rows with prefixed column names."""
        for r1 in self.table1:
            for r2 in self.table2:
                if r1[self.on_col1] == r2[self.on_col2]:
                    merged = {}
                    for k, v in r1.to_dict().items():
                        merged[f"{self.table1.name}.{k}"] = v
                    for k, v in r2.to_dict().items():
                        merged[f"{self.table2.name}.{k}"] = v
                    yield merged

#Query Engine

class Query:
    """Handles chaining, filtering, and executing queries."""

    def __init__(self, source: Iterable[Any]):
        self.source = source
        self._select_cols: Optional[List[Union[str, AggFunc]]] = None
        self._where_cond: Optional[Condition] = None
        self._order_by_col: Optional[str] = None
        self._order_asc: bool = True
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._group_by_col: Optional[str] = None

    def select(self, columns: List[Union[str, AggFunc]]) -> 'Query':
        self._select_cols = columns
        return self

    def where(self, column_or_cond: Union[str, Condition], operator: Optional[str] = None, value: Any = None) -> 'Query':
        """Allows either passing a full Condition object OR a simple col, op, val setup."""
        if isinstance(column_or_cond, Condition):
            new_cond = column_or_cond
        else:
            if operator is None:
                raise ValueError("Operator required if passing column string.")
            new_cond = Compare(column_or_cond, operator, value)

        if self._where_cond:
            self._where_cond = self._where_cond & new_cond
        else:
            self._where_cond = new_cond
            
        return self

    def group_by(self, column: str) -> 'Query':
        self._group_by_col = column
        return self

    def order_by(self, column: str, ascending: bool = True) -> 'Query':
        self._order_by_col = column
        self._order_asc = ascending
        return self

    def limit(self, count: int) -> 'Query':
        self._limit = count
        return self

    def offset(self, count: int) -> 'Query':
        self._offset = count
        return self

    def _apply_aggregation(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handles grouping and aggregation functions."""
        groups = defaultdict(list)
        
        if self._group_by_col:
            for row in data:
                groups[row.get(self._group_by_col)].append(row)
        else:
            groups[None] = data 
            
        result = []
        for group_key, rows in groups.items():
            res_row = {}
            if self._group_by_col:
                res_row[self._group_by_col] = group_key
                
            for col in (self._select_cols or []):
                if isinstance(col, AggFunc):
                    vals = [r.get(col.column) for r in rows if r.get(col.column) is not None]
                    col_name = str(col)
                    if isinstance(col, COUNT):
                        res_row[col_name] = len(vals)
                    elif isinstance(col, SUM):
                        res_row[col_name] = sum(vals)
                    elif isinstance(col, AVG):
                        res_row[col_name] = sum(vals) / len(vals) if vals else 0
                    elif isinstance(col, MAX):
                        res_row[col_name] = max(vals) if vals else None
                    elif isinstance(col, MIN):
                        res_row[col_name] = min(vals) if vals else None
                elif isinstance(col, str) and col != self._group_by_col:
                    res_row[col] = rows[0].get(col) if rows else None
                    
            result.append(res_row)
        return result

    def execute(self) -> List[Dict[str, Any]]:
        """Compiles the query chain and executes it against the data source."""
        data = []
        for item in self.source:
            data.append(item.to_dict() if hasattr(item, 'to_dict') else item)

        # WHERE
        if self._where_cond:
            data = [row for row in data if self._where_cond.evaluate(row)]

        #SELECT
        has_aggregations = any(isinstance(c, AggFunc) for c in (self._select_cols or []))
        if self._group_by_col or has_aggregations:
            data = self._apply_aggregation(data)
        elif self._select_cols:
            data = [{col: row.get(col) for col in self._select_cols if isinstance(col, str)} for row in data]

        #ORDER BY
        if self._order_by_col:
            data.sort(
                key=lambda x: (x.get(self._order_by_col) is None, x.get(self._order_by_col)), 
                reverse=not self._order_asc
            )

        if self._offset is not None:
            data = data[self._offset:]
        if self._limit is not None:
            data = data[:self._limit]

        return data