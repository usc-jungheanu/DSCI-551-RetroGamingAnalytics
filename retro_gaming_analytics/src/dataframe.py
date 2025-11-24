"""
Custom DataFrame Implementation for DSCI 551 Project
Implements SQL-like operations: FILTER, PROJECT, GROUP BY, AGGREGATE, JOIN
NO pandas or csv library used - built from scratch
"""

import re
from typing import List, Dict, Any, Union, Optional, Callable


class DataFrame:
    """Custom DataFrame class with SQL-like operations"""
    
    def __init__(self, data: List[List[Any]] = None, columns: List[str] = None):
        """
        Initialize DataFrame
        
        Args:
            data: List of lists representing rows
            columns: List of column names
        """
        self.data = data if data is not None else []
        self.columns = columns if columns is not None else []
        self._validate_structure()
    
    def _validate_structure(self):
        """Ensure data structure is valid"""
        if self.data and self.columns:
            expected_cols = len(self.columns)
            for i, row in enumerate(self.data):
                if len(row) != expected_cols:
                    raise ValueError(f"Row {i} has {len(row)} values but {expected_cols} columns expected")
    
    @classmethod
    def from_csv_data(cls, csv_data: Dict[str, Any]) -> 'DataFrame':
        """
        Create DataFrame from CSV parser output
        
        Args:
            csv_data: Dictionary with 'headers' and 'data' keys
            
        Returns:
            DataFrame instance
        """
        headers = csv_data.get('headers', [])
        data = csv_data.get('data', [])
        return cls(data=data, columns=headers)
    
    def __len__(self) -> int:
        """Return number of rows"""
        return len(self.data)
    
    def __repr__(self) -> str:
        """String representation of DataFrame"""
        if not self.data:
            return f"DataFrame(empty, columns={self.columns})"
        
        # Create string representation
        lines = []
        
        # Header
        header_line = " | ".join(str(col) for col in self.columns)
        lines.append(header_line)
        lines.append("-" * len(header_line))
        
        # Data rows (show first 10)
        for i, row in enumerate(self.data[:10]):
            row_line = " | ".join(str(val) if val is not None else "None" for val in row)
            lines.append(row_line)
        
        if len(self.data) > 10:
            lines.append(f"... ({len(self.data) - 10} more rows)")
        
        return "\n".join(lines)
    
    def __getitem__(self, key: Union[str, List[str]]) -> Union[List[Any], 'DataFrame']:
        """
        Enable bracket notation: df['column'] or df[['col1', 'col2']]
        
        Args:
            key: Column name or list of column names
            
        Returns:
            List of values for single column, or DataFrame for multiple columns
        """
        if isinstance(key, str):
            # Single column selection - return list of values
            if key not in self.columns:
                raise KeyError(f"Column '{key}' not found")
            col_idx = self.columns.index(key)
            return [row[col_idx] for row in self.data]
        
        elif isinstance(key, list):
            # Multiple columns - return new DataFrame
            return self.select(key)
        
        else:
            raise TypeError("Key must be string or list of strings")
    
    # ==================== CORE SQL OPERATIONS ====================
    
    def filter(self, condition: Union[str, Callable]) -> 'DataFrame':
        """
        Filter rows based on condition (SQL WHERE equivalent)
        
        Args:
            condition: String expression (e.g., "Rating >= 8.5") or callable
            
        Returns:
            Filtered DataFrame
        """
        if isinstance(condition, str):
            # Parse string condition
            filtered_data = []
            for row in self.data:
                row_dict = {col: val for col, val in zip(self.columns, row)}
                if self._evaluate_condition(condition, row_dict):
                    filtered_data.append(row)
            return DataFrame(data=filtered_data, columns=self.columns)
        
        elif callable(condition):
            # Use callable condition
            filtered_data = []
            for row in self.data:
                row_dict = {col: val for col, val in zip(self.columns, row)}
                if condition(row_dict):
                    filtered_data.append(row)
            return DataFrame(data=filtered_data, columns=self.columns)
        
        else:
            raise TypeError("Condition must be string or callable")
    
    def _evaluate_condition(self, condition: str, row_dict: Dict[str, Any]) -> bool:
        """
        Evaluate a condition string against a row
        
        Args:
            condition: String like "Rating >= 8.5" or "Year < 2000"
            row_dict: Dictionary of column values
            
        Returns:
            True if condition is met
        """
        # Handle AND/OR operators
        if ' and ' in condition.lower():
            parts = re.split(r'\s+and\s+', condition, flags=re.IGNORECASE)
            return all(self._evaluate_condition(part.strip(), row_dict) for part in parts)
        
        if ' or ' in condition.lower():
            parts = re.split(r'\s+or\s+', condition, flags=re.IGNORECASE)
            return any(self._evaluate_condition(part.strip(), row_dict) for part in parts)
        
        # Parse single condition
        operators = ['>=', '<=', '!=', '==', '>', '<', '=']
        
        for op in operators:
            if op in condition:
                parts = condition.split(op)
                if len(parts) != 2:
                    continue
                
                left = parts[0].strip()
                right = parts[1].strip()
                
                # Get left value (column name)
                if left not in row_dict:
                    return False
                left_val = row_dict[left]
                
                # Get right value (literal or column)
                if right in row_dict:
                    right_val = row_dict[right]
                else:
                    # Parse literal value
                    right_val = self._parse_literal(right)
                
                # Handle None values
                if left_val is None or right_val is None:
                    if op in ['!=', '==', '=']:
                        return (left_val is None) == (right_val is None) if op in ['==', '='] else (left_val is None) != (right_val is None)
                    return False
                
                # Perform comparison
                try:
                    if op == '>':
                        return left_val > right_val
                    elif op == '<':
                        return left_val < right_val
                    elif op == '>=':
                        return left_val >= right_val
                    elif op == '<=':
                        return left_val <= right_val
                    elif op in ['==', '=']:
                        return left_val == right_val
                    elif op == '!=':
                        return left_val != right_val
                except TypeError:
                    # Type mismatch - convert to strings and compare
                    return str(left_val) == str(right_val) if op in ['==', '='] else str(left_val) != str(right_val)
        
        return False
    
    def _parse_literal(self, value: str) -> Any:
        """Parse a literal value from string"""
        value = value.strip().strip('"').strip("'")
        
        # Try integer
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def select(self, columns: List[str]) -> 'DataFrame':
        """
        Select specific columns (SQL SELECT equivalent / PROJECTION)
        
        Args:
            columns: List of column names to select
            
        Returns:
            DataFrame with selected columns
        """
        # Validate columns exist
        for col in columns:
            if col not in self.columns:
                raise KeyError(f"Column '{col}' not found")
        
        # Get column indices
        col_indices = [self.columns.index(col) for col in columns]
        
        # Extract data for selected columns
        selected_data = []
        for row in self.data:
            selected_data.append([row[i] for i in col_indices])
        
        return DataFrame(data=selected_data, columns=columns)
    
    def group_by(self, by: Union[str, List[str]]) -> 'GroupedDataFrame':
        """
        Group DataFrame by column(s) (SQL GROUP BY equivalent)
        
        Args:
            by: Column name or list of column names
            
        Returns:
            GroupedDataFrame object for aggregation
        """
        if isinstance(by, str):
            by = [by]
        
        return GroupedDataFrame(self, by)
    
    def join(self, other: 'DataFrame', on: str, how: str = 'inner') -> 'DataFrame':
        """
        Join two DataFrames (SQL JOIN equivalent)
        
        Args:
            other: DataFrame to join with
            on: Column name to join on (must exist in both DataFrames)
            how: Join type ('inner' or 'left')
            
        Returns:
            Joined DataFrame
        """
        if on not in self.columns:
            raise KeyError(f"Column '{on}' not found in left DataFrame")
        if on not in other.columns:
            raise KeyError(f"Column '{on}' not found in right DataFrame")
        
        left_idx = self.columns.index(on)
        right_idx = other.columns.index(on)
        
        # Create new column names (avoid duplicates)
        new_columns = self.columns.copy()
        for col in other.columns:
            if col not in new_columns:
                new_columns.append(col)
            else:
                new_columns.append(f"{col}_right")
        
        joined_data = []
        
        if how == 'inner':
            # Inner join - only matching rows
            for left_row in self.data:
                left_key = left_row[left_idx]
                for right_row in other.data:
                    right_key = right_row[right_idx]
                    if left_key == right_key:
                        combined = left_row.copy()
                        combined.extend(right_row)
                        joined_data.append(combined)
        
        elif how == 'left':
            # Left join - all left rows, matching right rows
            for left_row in self.data:
                left_key = left_row[left_idx]
                matched = False
                
                for right_row in other.data:
                    right_key = right_row[right_idx]
                    if left_key == right_key:
                        combined = left_row.copy()
                        combined.extend(right_row)
                        joined_data.append(combined)
                        matched = True
                
                if not matched:
                    # Add left row with None for right columns
                    combined = left_row.copy()
                    combined.extend([None] * len(other.columns))
                    joined_data.append(combined)
        
        else:
            raise ValueError(f"Join type '{how}' not supported. Use 'inner' or 'left'.")
        
        return DataFrame(data=joined_data, columns=new_columns)
    
    # ==================== UTILITY METHODS ====================
    
    def head(self, n: int = 5) -> 'DataFrame':
        """Return first n rows"""
        return DataFrame(data=self.data[:n], columns=self.columns)
    
    def tail(self, n: int = 5) -> 'DataFrame':
        """Return last n rows"""
        return DataFrame(data=self.data[-n:], columns=self.columns)
    
    def shape(self) -> tuple:
        """Return (rows, columns) tuple"""
        return (len(self.data), len(self.columns))
    
    def sort_values(self, by: str, ascending: bool = True) -> 'DataFrame':
        """
        Sort DataFrame by column (SQL ORDER BY equivalent)
        
        Args:
            by: Column name to sort by
            ascending: Sort order
            
        Returns:
            Sorted DataFrame
        """
        if by not in self.columns:
            raise KeyError(f"Column '{by}' not found")
        
        col_idx = self.columns.index(by)
        
        # Sort data, handling None values
        sorted_data = sorted(
            self.data,
            key=lambda row: (row[col_idx] is None, row[col_idx]),
            reverse=not ascending
        )
        
        return DataFrame(data=sorted_data, columns=self.columns)
    
    def to_dict(self, orient: str = 'records') -> Union[List[Dict], Dict[str, List]]:
        """
        Convert DataFrame to dictionary
        
        Args:
            orient: 'records' (list of dicts) or 'columns' (dict of lists)
            
        Returns:
            Dictionary representation
        """
        if orient == 'records':
            return [
                {col: val for col, val in zip(self.columns, row)}
                for row in self.data
            ]
        elif orient == 'columns':
            return {
                col: [row[i] for row in self.data]
                for i, col in enumerate(self.columns)
            }
        else:
            raise ValueError("orient must be 'records' or 'columns'")


class GroupedDataFrame:
    """Helper class for grouped DataFrame operations"""
    
    def __init__(self, dataframe: DataFrame, by_columns: List[str]):
        """
        Initialize grouped DataFrame
        
        Args:
            dataframe: Source DataFrame
            by_columns: Columns to group by
        """
        self.df = dataframe
        self.by_columns = by_columns
        self._groups = self._create_groups()
    
    def _create_groups(self) -> Dict[tuple, List[List[Any]]]:
        """Create dictionary of groups"""
        groups = {}
        
        by_indices = [self.df.columns.index(col) for col in self.by_columns]
        
        for row in self.df.data:
            # Create group key
            key = tuple(row[i] for i in by_indices)
            
            if key not in groups:
                groups[key] = []
            groups[key].append(row)
        
        return groups
    
    def agg(self, agg_spec: Dict[str, Union[str, List[str]]]) -> DataFrame:
        """
        Perform aggregation (SQL aggregate functions)
        
        Args:
            agg_spec: Dictionary mapping column names to aggregation functions
                     e.g., {'Sales': 'sum', 'Rating': ['mean', 'max']}
            
        Returns:
            Aggregated DataFrame
        """
        result_data = []
        result_columns = self.by_columns.copy()
        
        # Build result column names
        for col, funcs in agg_spec.items():
            if isinstance(funcs, str):
                funcs = [funcs]
            for func in funcs:
                result_columns.append(f"{col}_{func}")
        
        # Perform aggregation for each group
        for group_key, rows in self._groups.items():
            result_row = list(group_key)
            
            for col, funcs in agg_spec.items():
                if col not in self.df.columns:
                    raise KeyError(f"Column '{col}' not found")
                
                col_idx = self.df.columns.index(col)
                
                if isinstance(funcs, str):
                    funcs = [funcs]
                
                for func in funcs:
                    # Extract values (filter out None)
                    values = [row[col_idx] for row in rows if row[col_idx] is not None]
                    
                    # Calculate aggregation
                    result_row.append(self._calculate_agg(values, func))
            
            result_data.append(result_row)
        
        return DataFrame(data=result_data, columns=result_columns)
    
    def _calculate_agg(self, values: List[Any], func: str) -> Any:
        """Calculate aggregation function"""
        if not values:
            return None
        
        if func == 'count':
            return len(values)
        elif func == 'sum':
            return sum(values)
        elif func == 'mean':
            return sum(values) / len(values)
        elif func == 'avg':
            return sum(values) / len(values)
        elif func == 'max':
            return max(values)
        elif func == 'min':
            return min(values)
        elif func == 'median':
            sorted_vals = sorted(values)
            n = len(sorted_vals)
            if n % 2 == 0:
                return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
            else:
                return sorted_vals[n//2]
        elif func == 'std':
            # Standard deviation
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            return variance ** 0.5
        else:
            raise ValueError(f"Unknown aggregation function: {func}")
    
    def count(self) -> DataFrame:
        """Count records in each group"""
        result_data = []
        result_columns = self.by_columns + ['count']
        
        for group_key, rows in self._groups.items():
            result_row = list(group_key) + [len(rows)]
            result_data.append(result_row)
        
        return DataFrame(data=result_data, columns=result_columns)
    
    def sum(self, columns: List[str] = None) -> DataFrame:
        """Sum numeric columns in each group"""
        if columns is None:
            # Sum all numeric columns
            columns = []
            for col in self.df.columns:
                if col not in self.by_columns:
                    # Check if column is numeric
                    col_idx = self.df.columns.index(col)
                    if any(isinstance(row[col_idx], (int, float)) for row in self.df.data):
                        columns.append(col)
        
        return self.agg({col: 'sum' for col in columns})
    
    def mean(self, columns: List[str] = None) -> DataFrame:
        """Calculate mean of numeric columns in each group"""
        if columns is None:
            columns = []
            for col in self.df.columns:
                if col not in self.by_columns:
                    col_idx = self.df.columns.index(col)
                    if any(isinstance(row[col_idx], (int, float)) for row in self.df.data):
                        columns.append(col)
        
        return self.agg({col: 'mean' for col in columns})