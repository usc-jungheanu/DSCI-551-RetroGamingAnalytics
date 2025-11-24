# Retro Gaming Market Analytics Application

**DSCI 551 Project - Jason Ungheanu**

A comprehensive analytics application for analyzing retro gaming market trends using custom-built CSV parsing and DataFrame operations with SQL-like functionality.

## Project Overview

This application demonstrates:
- Custom CSV parser supporting multiple delimiters and gaming dataset quirks
- DataFrame class with SQL-like operations (filter, project, group by, join, aggregation)
- Interactive Streamlit web application for retro gaming market analysis
- Real-world gaming dataset integration and analysis

## Quick Start

```bash
# 1. Navigate to project directory
cd retro_gaming_analytics

# 2. Install Streamlit
pip install streamlit

# 3. Run the application
streamlit run streamlit_app.py
```

The app will open automatically at http://localhost:8501

---

## Features

### 🔧 Core Components

- **CSV Parser**: Custom implementation supporting comma, semicolon, and tab delimiters
- **DataFrame Class**: SQL-like operations including:
  - **Filtering**: Find games by rating, era, platform (`df.filter("rating > 8.0")`)
  - **Projection**: Select specific columns (`df.select(["title", "rating"])`)
  - **Group By**: Group by console, genre, publisher (`df.group_by("platform")`)
  - **Aggregation**: Calculate averages, totals, min, max, count
  - **Join**: Combine datasets by common columns (`df.join(other, on="game_id")`)

### 📊 Analytics Features

- **Market Trend Analysis**: Games by decade, platform performance
- **Rating Analysis**: Average ratings by platform and genre
- **Opportunity Finder**: Identify high-rated retro games for potential remasters
- **Performance Comparison**: Original vs remastered game analysis

---

## Datasets

This project uses real gaming datasets from Kaggle:

| Dataset | Size | Description |
|---------|------|-------------|
| appstore_games.csv | 23.4 MB | Apple App Store games with ratings and metadata |
| game_info.csv | 74.2 MB | Comprehensive game information database |
| game_jams_until_feb_2023.csv | 815 KB | Game jam entries and indie game data |
| steam.csv | 5.7 MB | Steam store games with ratings and prices |
| Twitch_game_data.csv | 1.6 MB | Twitch streaming data for popular games |
| video_game_sales_2016_thru_2022.csv | 1.6 MB | Recent video game sales from 2016-2022 |

**Total Coverage:** 100,000+ game records across 6 datasets spanning multiple platforms and eras

**Dataset Sources:**
- Kaggle public datasets
- Apple App Store data
- Steam Store data
- Twitch gaming analytics
- Video game sales archives

---

## Installation & Setup

1. **Clone/Download the project**
   ```bash
   cd retro_gaming_analytics
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit
   ```

3. **Datasets are included**
   - All CSV files are located in the `data/` folder
   - No additional downloads required

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Usage

### Running the Web Application

The Streamlit app provides an interactive interface with multiple sections:

1. **Overview**: Dataset statistics and system information
2. **Data Explorer**: Search and filtering capabilities
3. **Query Builder**: Custom query construction
4. **JOIN Operations**: Multi-dataset combination
5. **Market Analytics**: Interactive dashboard with visualizations
6. **Genre Analysis**: Genre performance metrics
7. **Remaster Opportunities**: Identify remaster candidates

### Using the Core Classes

```python
from src.csv_parser import load_csv
from src.dataframe import DataFrame

# Load CSV data
csv_data = load_csv("data/steam.csv")
df = DataFrame.from_csv_data(csv_data)

# Filter high-rated games
high_rated = df.filter("rating >= 8.5")

# Group by platform and get average ratings
platform_ratings = df.group_by("platform").agg({"rating": "mean"})

# Join with another dataset
combined = df.join(other_df, on="name", how="inner")
```

---

## Project Structure

```
retro_gaming_analytics/
├── src/
│   ├── csv_parser.py      # Custom CSV parsing implementation
│   ├── dataframe.py       # DataFrame class with SQL operations
│   └── data_loader.py     # Dynamic dataset loader
├── data/                  # CSV datasets directory
│   ├── appstore_games.csv
│   ├── game_info.csv
│   ├── game_jams_until_feb_2023.csv
│   ├── steam.csv
│   ├── Twitch_game_data.csv
│   └── video_game_sales_2016_thru_2022.csv
├── streamlit_app.py       # Main application interface
└── README.md              # This file
```

---

## Demo Day Features

The application demonstrates all required DSCI 551 project components:

1. **CSV Parser**: Live demonstration of loading gaming datasets
2. **Filter Operations**: Show games by rating, year, platform
3. **Projection**: Select specific columns for analysis
4. **Group By**: Group games by various attributes
5. **Aggregation**: Calculate statistics (mean, sum, count, etc.)
6. **Join Operations**: Combine datasets from multiple sources
7. **Real-world Application**: Complete retro gaming market analysis

---

## Sample Analyses

- **Market Analysis**: "Show all retro games with rating > 8.0 that got modern remasters"
- **Trend Analysis**: "Group games by decade and show average customer satisfaction"
- **Opportunity Analysis**: "Join sales data with review sentiment to find undervalued classics"
- **Performance Comparison**: "Compare original vs. enhanced versions across different metrics"
- **Streaming Analysis**: "Identify which retro games have strong Twitch viewership"

---

## Technical Implementation

### CSV Parser Features
- Auto-detects delimiters (comma, semicolon, tab)
- Handles special characters in game titles
- Manages missing values and encoding issues
- Automatic type conversion (string, int, float)

### DataFrame Operations
- **Filtering**: Boolean indexing with comparison operators
- **Projection**: Column selection and reordering
- **Grouping**: Multi-column grouping with aggregation functions
- **Joining**: Inner and left joins on single or multiple columns
- **Sorting**: Multi-column sorting with custom ordering

### Dynamic Data Loader
- Automatically scans `data/` directory for CSV files
- Loads all available datasets dynamically
- Column name normalization (e.g., "Platform"/"Platforms" → "platform")
- Enables seamless JOIN operations across different data sources

### Web Application
- Interactive Streamlit interface
- Real-time data visualization
- Responsive design with multiple analysis sections
- Demonstrates all 5 SQL operations

---

## Testing

Test the core components:

```bash
# Test CSV Parser
python src/csv_parser.py

# Test Data Loader
python src/data_loader.py

# Test DataFrame operations
python -c "from src.data_loader import DatasetLoader; loader = DatasetLoader(); datasets = loader.load_all_datasets()"
```

---

## Requirements Met

**DSCI 551 Project Requirements:**

- [x] Custom CSV parser (no `csv` library)
- [x] Custom DataFrame class (no `pandas` for core operations)
- [x] FILTER operation (SQL WHERE)
- [x] PROJECT operation (SQL SELECT)
- [x] GROUP BY operation
- [x] AGGREGATION functions (sum, mean, count, max, min)
- [x] JOIN operation (INNER, LEFT, RIGHT, OUTER)
- [x] Real-world datasets from Kaggle
- [x] Functional application with user interface
- [x] Search and analytics capabilities

---

## Future Enhancements

- Integration with live Kaggle API for real-time data
- Advanced analytics (correlation analysis, predictive modeling)
- Export functionality for analysis results
- Additional visualization types and interactive filters
- Performance optimization for larger datasets

---

## Dependencies

- `streamlit`: Web application framework

Optional for enhanced functionality:
- `plotly`: Interactive visualizations
- `numpy`: Numerical operations support

---

## Author

**Jason Ungheanu** - USC ID: 1652473813  
DSCI 551 - Fall 2024

---

## License

This is an academic project completed for DSCI 551 (Data Management) at USC.

---

**Last Updated:** November 2024
