"""
Data Loader for Retro Gaming Analytics
Dynamically loads ALL CSV files from the data folder
Automatically normalizes column names for better JOIN compatibility
"""

import os
import sys
from typing import Dict, Optional

# Add src directory to path
sys.path.append(os.path.dirname(__file__))

from csv_parser import load_csv
from dataframe import DataFrame


def normalize_column_names(columns):
    """
    Normalize column names for better JOIN compatibility
    Converts to lowercase, removes spaces, standardizes common variations
    
    CRITICAL FIX: Ensures "Platform" and "Platforms" both become "platform"
    """
    normalized = []
    for col in columns:
        # Convert to lowercase
        col_lower = str(col).lower().strip()
        
        # Remove extra spaces
        col_clean = ' '.join(col_lower.split())
        
        # Replace spaces with underscores
        col_clean = col_clean.replace(' ', '_')
        
        # Standardize common column name variations
        standardizations = {
            'game_name': 'name',
            'title': 'name',
            'game_title': 'name',
            'release_year': 'year',
            'year_of_release': 'year',
            'meta_score': 'metascore',
            'user_score': 'userscore',
            'critic_score': 'criticscore',
            'platforms': 'platform',      # ← CRITICAL FIX: "platforms" → "platform"
            'platform': 'platform',        # ← "platform" stays "platform"
            'genres': 'genre',             # Also normalize genre variations
            'game_genre': 'genre',
            'category': 'genre',
            'developers': 'developer',
            'publishers': 'publisher',
            'global_sales': 'sales',
            'total_sales': 'sales',
        }
        
        if col_clean in standardizations:
            col_clean = standardizations[col_clean]
        
        normalized.append(col_clean)
    
    return normalized


class DatasetLoader:
    """Loader that dynamically loads ALL CSV files from data folder"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.datasets = {}
    
    def get_csv_files(self):
        """
        Scan data directory and return all CSV files
        Returns list of tuples: (friendly_name, filename)
        """
        if not os.path.exists(self.data_dir):
            print(f"Warning: Directory {self.data_dir} not found")
            return []
        
        csv_files = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.csv'):
                # Create friendly name from filename
                # e.g., "vgsales.csv" -> "vgsales"
                # e.g., "Video_Game_Sales_2016_Thru_2022.csv" -> "vg_sales_2016_2022"
                friendly_name = filename.replace('.csv', '')
                
                # Simplify long names
                if 'Video_Game_Sales' in filename:
                    friendly_name = 'vg_sales_' + filename.split('_')[-1].replace('.csv', '')
                
                csv_files.append((friendly_name.lower(), filename))
        
        return sorted(csv_files)  # Sort alphabetically
    
    def load_csv_file(self, filename: str, friendly_name: str) -> Optional[DataFrame]:
        """Load a single CSV file with normalization"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            csv_data = load_csv(filepath)
            
            # Normalize column names
            csv_data['headers'] = normalize_column_names(csv_data['headers'])
            
            df = DataFrame.from_csv_data(csv_data)
            print(f"✓ Loaded {filename}: {len(df):,} games")
            return df
        except Exception as e:
            print(f"✗ Error loading {filename}: {e}")
            return None
    
    def load_all_datasets(self) -> Dict[str, DataFrame]:
        """
        Dynamically load ALL CSV files from data folder
        No hardcoding - works with any CSV files you add!
        """
        print("🎮 Scanning data folder for CSV files...")
        print("=" * 60)
        
        csv_files = self.get_csv_files()
        
        if not csv_files:
            print("⚠  No CSV files found in data folder!")
            return {}
        
        print(f"Found {len(csv_files)} CSV file(s):")
        for name, filename in csv_files:
            print(f"  • {filename}")
        print()
        
        datasets = {}
        
        # Load each CSV file
        for friendly_name, filename in csv_files:
            df = self.load_csv_file(filename, friendly_name)
            if df is not None:
                datasets[friendly_name] = df
        
        print("=" * 60)
        print(f"✓ Successfully loaded {len(datasets)} dataset(s)")
        
        # Show total records
        if datasets:
            total_records = sum(len(df) for df in datasets.values())
            print(f"📊 Total records across all datasets: {total_records:,}")
            
            # Show which columns are normalized
            print("\n🔧 Column Normalization Active:")
            print("   • 'Platform'/'Platforms' → 'platform' ✓")
            print("   • 'Game_Name'/'Title' → 'name' ✓")
            print("   • 'Genres' → 'genre' ✓")
            print("   • All variations standardized for JOIN operations")
        
        return datasets
    
    def get_retro_games(self, df: DataFrame, year_threshold: int = 2000) -> DataFrame:
        """Filter for retro games (pre-2000 or retro-style modern games)"""
        try:
            # Try to find year column (different names in different datasets)
            year_col = None
            for col in df.columns:
                if col.lower() in ['year', 'release_year', 'release_date', 'year_of_release']:
                    year_col = col
                    break
            
            if year_col:
                return df.filter(f"{year_col} < {year_threshold}")
            else:
                print("Warning: No year column found for retro filtering")
                return df
        except Exception as e:
            print(f"Error filtering retro games: {e}")
            return df
    
    def get_modern_retro_games(self, df: DataFrame, start_year: int = 2014) -> DataFrame:
        """Filter for modern retro-style games (2014+)"""
        try:
            year_col = None
            for col in df.columns:
                if col.lower() in ['year', 'release_year', 'release_date', 'year_of_release']:
                    year_col = col
                    break
            
            if year_col:
                return df.filter(f"{year_col} >= {start_year}")
            else:
                print("Warning: No year column found for modern retro filtering")
                return df
        except Exception as e:
            print(f"Error filtering modern retro games: {e}")
            return df
    
    def get_high_rated_games(self, df: DataFrame, rating_threshold: float = 8.5) -> DataFrame:
        """Filter for high-rated games"""
        try:
            # Try to find rating column
            rating_col = None
            for col in df.columns:
                if any(term in col.lower() for term in ['rating', 'score', 'metascore', 'user_score', 'critic_score']):
                    rating_col = col
                    break
            
            if rating_col:
                return df.filter(f"{rating_col} >= {rating_threshold}")
            else:
                print("Warning: No rating column found")
                return df
        except Exception as e:
            print(f"Error filtering high-rated games: {e}")
            return df


def test_loader():
    """Test the dataset loader"""
    print("🎮 Testing Dynamic Dataset Loader\n")
    
    loader = DatasetLoader()
    datasets = loader.load_all_datasets()
    
    if not datasets:
        print("\n⚠  No datasets loaded. Please add CSV files to the 'data' folder.")
        return
    
    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    
    for name, df in datasets.items():
        print(f"\n{name.upper()}:")
        print(f"  Rows: {len(df):,}")
        print(f"  Columns ({len(df.columns)}): {', '.join(df.columns[:8])}")
        if len(df.columns) > 8:
            print(f"              {', '.join(df.columns[8:])}")
        
        # Check for platform column
        if 'platform' in df.columns:
            print(f"  ✓ Platform column present (normalized)")
        
        # Show sample data
        if len(df) > 0:
            print(f"  Sample (first 2 rows):")
            print(df.head(2))
    
    print("\n" + "=" * 60)
    print("PLATFORM NORMALIZATION TEST")
    print("=" * 60)
    
    # Test platform normalization
    test_columns = ['Platform', 'Platforms', 'platform', 'platforms', 'PLATFORM', 'Game Platform']
    normalized = normalize_column_names(test_columns)
    
    for original, norm in zip(test_columns, normalized):
        status = "✓" if norm == 'platform' else "✗"
        print(f"{status} '{original}' → '{norm}'")


if __name__ == "__main__":
    test_loader()