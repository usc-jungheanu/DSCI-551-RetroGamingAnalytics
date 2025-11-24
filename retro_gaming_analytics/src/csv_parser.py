"""
Custom CSV Parser for Gaming Datasets
Handles different delimiters and gaming dataset quirks
"""

import re
from typing import List, Dict, Any, Optional, Union


class CSVParser:
    """Custom CSV parser supporting multiple delimiters and gaming dataset quirks"""
    
    def __init__(self, delimiter: str = ',', quote_char: str = '"', escape_char: str = '\\'):
        self.delimiter = delimiter
        self.quote_char = quote_char
        self.escape_char = escape_char
    
    def detect_delimiter(self, sample_line: str) -> str:
        """Auto-detect delimiter from sample line"""
        delimiters = [',', ';', '\t', '|']
        delimiter_counts = {}
        
        for delimiter in delimiters:
            # Count occurrences outside of quotes
            count = 0
            in_quotes = False
            for i, char in enumerate(sample_line):
                if char == self.quote_char and (i == 0 or sample_line[i-1] != self.escape_char):
                    in_quotes = not in_quotes
                elif char == delimiter and not in_quotes:
                    count += 1
            delimiter_counts[delimiter] = count
        
        # Return delimiter with highest count
        return max(delimiter_counts, key=delimiter_counts.get)
    
    def parse_line(self, line: str) -> List[str]:
        """Parse a single CSV line handling quotes and escapes"""
        if not line.strip():
            return []
        
        fields = []
        current_field = ""
        in_quotes = False
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if char == self.quote_char:
                if in_quotes and i + 1 < len(line) and line[i + 1] == self.quote_char:
                    # Handle escaped quotes
                    current_field += self.quote_char
                    i += 1  # Skip next quote
                else:
                    in_quotes = not in_quotes
            elif char == self.delimiter and not in_quotes:
                fields.append(self.clean_field(current_field))
                current_field = ""
            else:
                current_field += char
            
            i += 1
        
        # Add the last field
        fields.append(self.clean_field(current_field))
        return fields
    
    def clean_field(self, field: str) -> str:
        """Clean field data for gaming datasets"""
        field = field.strip()
        
        # Handle special gaming characters and encoding issues
        field = field.replace('â€™', "'")  # Common encoding issue
        field = field.replace('â€œ', '"')
        field = field.replace('â€', '"')
        
        # Handle missing values
        if field.lower() in ['', 'n/a', 'na', 'null', 'none', 'unknown', 'tbd']:
            return None
        
        # Try to convert to appropriate type
        return self.convert_type(field)
    
    def convert_type(self, value: str) -> Union[str, int, float, None]:
        """Convert string to appropriate type"""
        if value is None:
            return None
        
        # Try integer
        try:
            if '.' not in value and value.isdigit():
                return int(value)
        except (ValueError, AttributeError):
            pass
        
        # Try float
        try:
            if '.' in value or 'e' in value.lower():
                return float(value)
        except (ValueError, AttributeError):
            pass
        
        # Return as string
        return value
    
    def parse_file(self, filepath: str, has_header: bool = True, auto_detect_delimiter: bool = True) -> Dict[str, Any]:
        """Parse entire CSV file and return structured data"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            # Try different encodings for gaming datasets
            encodings = ['latin1', 'cp1252', 'iso-8859-1']
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as file:
                        lines = file.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError(f"Could not decode file {filepath} with any supported encoding")
        
        if not lines:
            return {'headers': [], 'data': []}
        
        # Auto-detect delimiter if requested
        if auto_detect_delimiter:
            self.delimiter = self.detect_delimiter(lines[0])
        
        # Parse header
        headers = []
        data_start_idx = 0
        
        if has_header:
            headers = self.parse_line(lines[0])
            data_start_idx = 1
        else:
            # Generate default headers
            first_row = self.parse_line(lines[0])
            headers = [f'column_{i}' for i in range(len(first_row))]
        
        # Parse data rows
        data = []
        for line_num, line in enumerate(lines[data_start_idx:], start=data_start_idx + 1):
            try:
                row = self.parse_line(line)
                if row:  # Skip empty rows
                    # Ensure row has same length as headers
                    while len(row) < len(headers):
                        row.append(None)
                    if len(row) > len(headers):
                        row = row[:len(headers)]
                    data.append(row)
            except Exception as e:
                print(f"Warning: Error parsing line {line_num}: {e}")
                continue
        
        return {
            'headers': headers,
            'data': data,
            'delimiter': self.delimiter,
            'rows_parsed': len(data)
        }


def load_csv(filepath: str, delimiter: str = None, has_header: bool = True) -> Dict[str, Any]:
    """Convenience function to load CSV file"""
    parser = CSVParser(delimiter=delimiter if delimiter else ',')
    return parser.parse_file(filepath, has_header=has_header, auto_detect_delimiter=delimiter is None)
