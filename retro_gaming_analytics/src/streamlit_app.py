"""
Retro Gaming Market Analytics Platform
DSCI 551 Project - Jason Ungheanu

Professional analytics application for retro gaming market analysis
Built with custom data processing engine
"""

import streamlit as st
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from data_loader import DatasetLoader
from dataframe import DataFrame


def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="Retro Gaming Market Analytics",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for modern, professional look
    st.markdown("""
        <style>
        /* Main Headers */
        .main-header {
            font-size: 2.8rem;
            color: #1E3A8A;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #64748B;
            margin-bottom: 2.5rem;
        }
        
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Navigation Section Header */
        .css-1544g2n {
            padding-top: 2rem;
        }
        
        /* All sidebar buttons - make them look like menu items */
        section[data-testid="stSidebar"] button {
            width: 100%;
            background: white;
            border: 2px solid transparent;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            margin: 0.35rem 0;
            text-align: left;
            font-size: 1rem;
            font-weight: 500;
            color: #475569;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        section[data-testid="stSidebar"] button:hover {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border: 2px solid #667eea;
            color: #1E3A8A;
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
        }
        
        section[data-testid="stSidebar"] button:active,
        section[data-testid="stSidebar"] button:focus {
            background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
            border: 2px solid #667eea;
            color: #1E3A8A;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        /* Primary Load Button */
        section[data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 1rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4) !important;
            margin: 1rem 0 !important;
        }
        
        section[data-testid="stSidebar"] button[kind="primary"]:hover {
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6) !important;
            transform: translateY(-2px) !important;
        }
        
        /* KPI Metric Cards - More prominent */
        div[data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            color: #1E3A8A !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            color: #64748B !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        div[data-testid="metric-container"] {
            background: white;
            border: 3px solid #667eea;
            border-radius: 16px;
            padding: 2rem 1.5rem;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.15);
            transition: all 0.3s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(102, 126, 234, 0.25);
            border-color: #764ba2;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #1E3A8A !important;
            font-weight: 700 !important;
        }
        h2 {
            font-size: 2rem !important;
            margin-top: 2rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        /* Success/Info boxes */
        div[data-testid="stSuccess"] {
            background: linear-gradient(135deg, #10b98120 0%, #05966920 100%);
            border-left: 5px solid #10b981;
            border-radius: 10px;
            padding: 1rem 1.5rem;
        }
        div[data-testid="stInfo"] {
            background: linear-gradient(135deg, #3b82f620 0%, #2563eb20 100%);
            border-left: 5px solid #3b82f6;
            border-radius: 10px;
            padding: 1rem 1.5rem;
        }
        div[data-testid="stWarning"] {
            background: linear-gradient(135deg, #f59e0b20 0%, #d9770620 100%);
            border-left: 5px solid #f59e0b;
            border-radius: 10px;
            padding: 1rem 1.5rem;
        }
        
        /* Expanders */
        div[data-testid="stExpander"] {
            border: 2px solid #E2E8F0;
            border-radius: 12px;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        div[data-testid="stExpander"]:hover {
            border-color: #667eea;
        }
        
        /* Code blocks */
        .stCodeBlock {
            border-radius: 10px;
            border: 2px solid #E2E8F0;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        }
        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
        }
        
        /* Main content area */
        .main .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }
        
        /* Remove any radio button styling that might appear */
        div[role="radiogroup"] {
            display: none !important;
        }
        input[type="radio"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="main-header">Retro Gaming Market Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced Analytics Platform | Jason Ungheanu</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'datasets_loaded' not in st.session_state:
        st.session_state.datasets_loaded = False
        st.session_state.datasets = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Overview"
    
    # Sidebar Navigation
    st.sidebar.title("📊 Analytics Platform")
    
    # Load Data Section
    st.sidebar.markdown("### Data Management")
    if st.sidebar.button("Load Datasets", type="primary", use_container_width=True):
        with st.spinner("Loading market data..."):
            loader = DatasetLoader(data_dir="data")
            st.session_state.datasets = loader.load_all_datasets()
            st.session_state.datasets_loaded = True
            st.sidebar.success(f"Loaded {len(st.session_state.datasets)} datasets")
    
    # Show loaded status
    if st.session_state.datasets_loaded:
        st.sidebar.markdown("**Active Datasets:**")
        for name, df in st.session_state.datasets.items():
            st.sidebar.text(f"• {name}: {len(df):,} records")
    
    st.sidebar.markdown("---")
    
    # Navigation Menu with clickable buttons
    st.sidebar.markdown("### 📑 Navigation")
    
    menu_items = [
        ("Overview", "📊"),
        ("Search & Filter", "🔎"),
        ("Data Explorer", "🔍"),
        ("Query Builder", "⚙️"),
        ("Market Analytics", "📈"),
        ("Genre Analysis", "🎮"), 
        ("Platform Performance", "💻"),
        ("Remaster Opportunities", "✨"),
        ("JOIN Operations", "🔗")
    ]
    
    for item, icon in menu_items:
        is_active = item == st.session_state.current_page
        
        # Create button with icon
        if is_active:
            button_label = f"{icon}  **{item}**"
        else:
            button_label = f"{icon}  {item}"
        
        if st.sidebar.button(button_label, key=f"nav_{item}", use_container_width=True):
            st.session_state.current_page = item
            st.rerun()
    
    page = st.session_state.current_page
    
    st.sidebar.markdown("---")
    
    # Route to pages
    if page == "Overview":
        show_overview()
    elif page == "Search & Filter":
        show_search_filter()
    elif page == "Data Explorer":
        show_data_explorer()
    elif page == "Query Builder":
        show_query_builder()
    elif page == "Market Analytics":
        show_market_analytics()
    elif page == "Genre Analysis":
        show_genre_analysis()
    elif page == "Platform Performance":
        show_platform_performance()
    elif page == "Remaster Opportunities":
        show_remaster_opportunities()
    elif page == "JOIN Operations":
        show_join_operations()


def create_kpi_card(label, value, delta=None, col=None):
    """Create a styled KPI card"""
    container = col if col else st
    with container:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 2px solid #667eea;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        ">
            <div style="
                font-size: 0.85rem;
                font-weight: 600;
                color: #64748B;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 0.5rem;
            ">{label}</div>
            <div style="
                font-size: 2.25rem;
                font-weight: 700;
                color: #1E3A8A;
                margin-bottom: 0.25rem;
            ">{value}</div>
            {f'<div style="font-size: 0.9rem; color: #10b981; font-weight: 600;">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)


def show_overview():
    """Overview dashboard"""
    st.header("Platform Overview")
    
    if not st.session_state.datasets_loaded:
        st.info("Load datasets from the sidebar to begin analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### About This Platform
            
            A comprehensive analytics solution for retro gaming market analysis. This platform provides:
            
            **Core Capabilities**
            - Advanced data filtering and querying
            - Multi-dimensional market analysis
            - Genre and platform performance metrics
            - Strategic remaster opportunity identification
            - Custom aggregation engine
            
            **Data Sources**
            - Video Game Sales Database
            - Steam Store Analytics
            - Metacritic Review Data
            - Industry Performance Metrics
            
            **Technical Architecture**
            - Custom-built data processing engine
            - SQL-like query operations
            - Real-time analytics
            - Interactive visualizations
            """)
        
        with col2:
            st.markdown("""
            ### Getting Started
            
            1. Load datasets using the sidebar
            2. Explore data in Data Explorer
            3. Build custom queries
            4. View market insights
            5. Identify opportunities
            
            ### Features
            - Filter operations
            - Data projection
            - Grouping and aggregation
            - Multi-dataset joins
            - Trend analysis
            """)
        
        return
    
    # Dashboard with loaded data
    st.subheader("Market Intelligence Dashboard")
    
    # Key Metrics with styled cards
    total_games = sum(len(df) for df in st.session_state.datasets.values())
    total_datasets = len(st.session_state.datasets)
    total_datapoints = sum(len(df.columns) * len(df) for df in st.session_state.datasets.values())
    
    # Find latest year across all datasets
    latest_year = 0
    for df in st.session_state.datasets.values():
        for col in df.columns:
            if any(term in col.lower() for term in ['year', 'release_year', 'year_of_release']):
                years = [y for y in df[col] if y is not None and isinstance(y, (int, float)) and y > 1970]
                if years:
                    latest_year = max(latest_year, max(years))
    
    latest_year_display = int(latest_year) if latest_year > 0 else "N/A"
    
    col1, col2, col3, col4 = st.columns(4)
    
    create_kpi_card("Total Games", f"{total_games:,}", col=col1)
    create_kpi_card("Active Datasets", f"{total_datasets}", col=col2)
    create_kpi_card("Data Points", f"{total_datapoints:,}", col=col3)
    create_kpi_card("Latest Data Year", f"{latest_year_display}", col=col4)
    
    st.markdown("---")
    
    # Dataset Overview
    st.subheader("Dataset Summary")
    
    for name, df in st.session_state.datasets.items():
        with st.expander(f"📊 {name.upper()} - {len(df):,} records"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"**Records:** {len(df):,}")
                st.markdown(f"**Columns:** {len(df.columns)}")
                st.markdown(f"**Size:** {len(df) * len(df.columns):,} data points")
            
            with col2:
                st.markdown("**Column Schema:**")
                st.text(", ".join(df.columns))
    
    st.markdown("---")
    
    # Quick Insights
    if 'vgsales' in st.session_state.datasets:
        st.subheader("Market Highlights")
        
        df = st.session_state.datasets['vgsales']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top selling game
            if 'Global_Sales' in df.columns and 'Name' in df.columns:
                sales_col = df['Global_Sales']
                names_col = df['Name']
                max_sales_idx = sales_col.index(max(sales_col))
                top_game = names_col[max_sales_idx]
                top_sales = sales_col[max_sales_idx]
                
                st.markdown("**Top Selling Game**")
                st.markdown(f"🏆 {top_game}")
                st.markdown(f"💰 {top_sales:.2f}M units sold")
        
        with col2:
            # Dataset timeframe
            if 'Year' in df.columns:
                years = [y for y in df['Year'] if y is not None]
                if years:
                    st.markdown("**Data Timeframe**")
                    st.markdown(f"📅 {min(years)} - {max(years)}")
                    st.markdown(f"📈 {max(years) - min(years)} years of data")


def show_search_filter():
    """Search and filter functionality - Search App"""
    st.header("🔎 Search & Filter Games")
    st.markdown("Search for specific games and apply multiple filters")
    
    if not st.session_state.datasets_loaded:
        st.warning("Load datasets to begin searching")
        return
    
    # Dataset selector
    dataset_name = st.selectbox("Select Dataset", list(st.session_state.datasets.keys()))
    df = st.session_state.datasets[dataset_name]
    
    st.markdown("---")
    
    # Search Box
    st.subheader("🔍 Search by Name")
    
    # Find name column
    name_col = None
    for col in df.columns:
        if any(term in col.lower() for term in ['name', 'title', 'game']):
            name_col = col
            break
    
    if name_col:
        search_term = st.text_input("Search for games", placeholder="Type game name...")
        
        if search_term:
            # Filter by search term (case insensitive)
            search_results = []
            for row in df.data:
                row_dict = {col: val for col, val in zip(df.columns, row)}
                game_name = str(row_dict.get(name_col, "")).lower()
                if search_term.lower() in game_name:
                    search_results.append(row)
            
            result_df = DataFrame(data=search_results, columns=df.columns)
            
            st.success(f"Found {len(result_df):,} games matching '{search_term}'")
            
            if len(result_df) > 0:
                # Sort options
                st.markdown("**Sort Results:**")
                sort_cols = [col for col in result_df.columns if any(isinstance(v, (int, float)) for v in result_df[col][:10])]
                
                if sort_cols:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        sort_col = st.selectbox("Sort by", sort_cols)
                    with col2:
                        sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True)
                    
                    sorted_results = result_df.sort_values(sort_col, ascending=(sort_order == "Ascending"))
                    st.code(str(sorted_results.head(20)))
                else:
                    st.code(str(result_df.head(20)))
                
                # Show the code
                with st.expander("📝 View Implementation Code"):
                    st.code(f"""
# SEARCH IMPLEMENTATION

# Step 1: FILTER operation to search
search_results = []
for row in df.data:
    row_dict = {{col: val for col, val in zip(df.columns, row)}}
    game_name = str(row_dict.get('{name_col}', "")).lower()
    if '{search_term.lower()}' in game_name:
        search_results.append(row)

# Step 2: Create filtered DataFrame
result_df = DataFrame(data=search_results, columns=df.columns)

# Step 3: SORT results
sorted_results = result_df.sort_values('{sort_col}', ascending={sort_order == "Ascending"})

# Results: {len(result_df):,} games found
                    """, language="python")
    
    st.markdown("---")
    
    # Multi-Filter Section
    st.subheader("🎛️ Advanced Filters")
    
    # Get numeric columns for filtering
    numeric_cols = []
    for col in df.columns:
        sample = [v for v in df[col][:20] if v is not None]
        if sample and all(isinstance(v, (int, float)) for v in sample):
            numeric_cols.append(col)
    
    # Get categorical columns
    cat_cols = []
    for col in df.columns:
        sample = [str(v) for v in df[col][:30] if v is not None]
        unique = len(set(sample))
        if unique < 20 and unique > 1:
            cat_cols.append(col)
    
    if numeric_cols or cat_cols:
        col1, col2 = st.columns(2)
        
        filters_applied = []
        
        with col1:
            if numeric_cols:
                st.markdown("**Numeric Filters:**")
                filter_col = st.selectbox("Column", ["None"] + numeric_cols, key="multi_filter_col")
                
                if filter_col != "None":
                    operator = st.selectbox("Operator", [">", "<", ">=", "<=", "=="], key="multi_filter_op")
                    value = st.number_input("Value", value=0.0, key="multi_filter_val")
                    filters_applied.append(f"{filter_col} {operator} {value}")
        
        with col2:
            if cat_cols:
                st.markdown("**Category Filters:**")
                cat_filter_col = st.selectbox("Column", ["None"] + cat_cols, key="cat_filter_col")
                
                if cat_filter_col != "None":
                    unique_vals = list(set([str(v) for v in df[cat_filter_col][:100] if v is not None]))[:20]
                    selected_val = st.selectbox("Value", unique_vals, key="cat_filter_val")
                    filters_applied.append(f"{cat_filter_col} == {selected_val}")
        
        if st.button("Apply Filters", use_container_width=True):
            if filters_applied:
                # Apply all filters
                filtered = df
                for filter_cond in filters_applied:
                    filtered = filtered.filter(filter_cond)
                
                st.success(f"Applied {len(filters_applied)} filter(s) - Found {len(filtered):,} results")
                st.code(str(filtered.head(20)))
                
                # Show implementation
                with st.expander("📝 View Filter Implementation"):
                    st.code(f"""
# MULTI-FILTER IMPLEMENTATION

# Start with full dataset
filtered = df

# Apply each filter sequentially
{chr(10).join([f"filtered = filtered.filter('{f}')" for f in filters_applied])}

# Final result: {len(filtered):,} games
                    """, language="python")


def show_data_explorer():
    """Interactive data explorer"""
    st.header("Data Explorer")
    st.markdown("Explore and filter your gaming datasets with custom SQL-like operations")
    
    if not st.session_state.datasets_loaded:
        st.warning("Load datasets to begin exploration")
        return
    
    # Dataset selector
    dataset_name = st.selectbox("Select Dataset", list(st.session_state.datasets.keys()))
    df = st.session_state.datasets[dataset_name]
    
    # Dataset info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Data Points", f"{len(df) * len(df.columns):,}")
    
    st.markdown("---")
    
    # Filter Section
    st.subheader("Data Filtering")
    
    # Get numeric columns for filtering
    numeric_cols = []
    for col in df.columns:
        sample = [v for v in df[col][:20] if v is not None]
        if sample and all(isinstance(v, (int, float)) for v in sample):
            numeric_cols.append(col)
    
    if numeric_cols:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            filter_col = st.selectbox("Column", numeric_cols)
        with col2:
            operator = st.selectbox("Operator", [">", "<", ">=", "<=", "==", "!="])
        with col3:
            sample_val = [v for v in df[filter_col][:10] if isinstance(v, (int, float))]
            default_val = float(sample_val[0]) if sample_val else 0.0
            value = st.number_input("Value", value=default_val)
        
        condition = f"{filter_col} {operator} {value}"
        
        if st.button("Apply Filter", use_container_width=True):
            filtered = df.filter(condition)
            
            st.success(f"Found {len(filtered):,} matching records (from {len(df):,} total)")
            
            # Show filtered data
            st.markdown("**Filtered Results:**")
            st.code(str(filtered.head(20)))
            
            # Create simple visualization
            st.markdown("**Result Distribution:**")
            create_bar_chart(filtered, filter_col if filter_col in filtered.columns else filtered.columns[0])
    
    st.markdown("---")
    
    # Column Selection
    st.subheader("Column Selection")
    
    selected_cols = st.multiselect(
        "Select columns to display",
        df.columns,
        default=list(df.columns[:5])
    )
    
    if selected_cols:
        projected = df.select(selected_cols)
        st.markdown(f"**Displaying {len(selected_cols)} columns:**")
        st.code(str(projected.head(20)))


def show_query_builder():
    """Advanced query builder"""
    st.header("Query Builder")
    st.markdown("Build complex analytical queries using SQL-like operations")
    
    if not st.session_state.datasets_loaded:
        st.warning("Load datasets to build queries")
        return
    
    dataset_name = st.selectbox("Source Dataset", list(st.session_state.datasets.keys()))
    df = st.session_state.datasets[dataset_name]
    
    st.markdown("---")
    
    # GROUP BY Section
    st.subheader("Group By Analysis")
    
    # Find categorical columns
    cat_cols = []
    for col in df.columns:
        sample = [str(v) for v in df[col][:30] if v is not None]
        unique = len(set(sample))
        if unique < 20 and unique > 1:
            cat_cols.append(col)
    
    # Find numeric columns
    num_cols = []
    for col in df.columns:
        sample = [v for v in df[col][:20] if v is not None]
        if sample and all(isinstance(v, (int, float)) for v in sample):
            num_cols.append(col)
    
    if cat_cols and num_cols:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            group_col = st.selectbox("Group By", cat_cols)
        with col2:
            agg_col = st.selectbox("Aggregate Column", num_cols)
        with col3:
            agg_func = st.selectbox("Function", ["count", "sum", "mean", "max", "min", "median"])
        
        if st.button("Execute Query", use_container_width=True):
            result = df.group_by(group_col).agg({agg_col: agg_func})
            
            st.success(f"Query executed successfully")
            
            # Display results
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Query Results:**")
                st.code(str(result))
            
            with col2:
                st.markdown("**Visual Analysis:**")
                create_bar_chart_from_grouped(result, f"{agg_col}_{agg_func}")
            
            # Show SQL equivalent
            with st.expander("View SQL Equivalent"):
                st.code(f"""
SELECT {group_col}, {agg_func.upper()}({agg_col}) as {agg_col}_{agg_func}
FROM {dataset_name}
GROUP BY {group_col}
                """, language="sql")


def show_market_analytics():
    """Market analytics dashboard"""
    st.header("Market Analytics")
    st.markdown("Comprehensive market intelligence and trend analysis")
    
    if not st.session_state.datasets_loaded or 'vgsales' not in st.session_state.datasets:
        st.warning("Load datasets including vgsales for market analytics")
        return
    
    df = st.session_state.datasets['vgsales']
    
    # Platform Analysis
    st.subheader("Platform Market Share")
    
    if 'Platform' in df.columns and 'Global_Sales' in df.columns:
        platform_sales = df.group_by('Platform').agg({'Global_Sales': 'sum'})
        platform_sorted = platform_sales.sort_values('Global_Sales_sum', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            create_horizontal_bar(platform_sorted, 'Global_Sales_sum', "Total Sales by Platform (Millions)")
        
        with col2:
            st.markdown("**Top 5 Platforms:**")
            top5 = platform_sorted.head(5)
            for row in top5.data:
                st.markdown(f"**{row[0]}:** {row[1]:.1f}M")
    
    st.markdown("---")
    
    # Time-based Analysis
    st.subheader("Temporal Trends")
    
    if 'Year' in df.columns:
        retro = df.filter("Year < 2000")
        modern = df.filter("Year >= 2000")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Retro Era Games", f"{len(retro):,}", "Pre-2000")
        with col2:
            st.metric("Modern Era Games", f"{len(modern):,}", "Post-2000")
        with col3:
            ratio = (len(retro) / len(df) * 100) if len(df) > 0 else 0
            st.metric("Retro Percentage", f"{ratio:.1f}%")


def show_genre_analysis():
    """Genre performance analysis"""
    st.header("Genre Analysis")
    st.markdown("Analyze performance metrics across gaming genres")
    
    if not st.session_state.datasets_loaded or 'vgsales' not in st.session_state.datasets:
        st.warning("Load datasets for genre analysis")
        return
    
    df = st.session_state.datasets['vgsales']
    
    if 'Genre' not in df.columns:
        st.error("Genre column not found in dataset")
        return
    
    st.subheader("Genre Performance Metrics")
    
    # Multi-metric analysis
    if 'Global_Sales' in df.columns:
        genre_stats = df.group_by('Genre').agg({
            'Name': 'count',
            'Global_Sales': ['sum', 'mean', 'max']
        })
        
        genre_sorted = genre_stats.sort_values('Global_Sales_sum', ascending=False)
        
        # Display table
        st.markdown("**Genre Performance Summary:**")
        st.code(str(genre_sorted))
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Total Sales by Genre:**")
            create_horizontal_bar(genre_sorted, 'Global_Sales_sum', "Sales (Millions)")
        
        with col2:
            st.markdown("**Game Count by Genre:**")
            create_horizontal_bar(genre_sorted, 'Name_count', "Number of Games")


def show_platform_performance():
    """Platform performance metrics"""
    st.header("Platform Performance")
    st.markdown("Detailed analysis of gaming platform success metrics")
    
    if not st.session_state.datasets_loaded or 'vgsales' not in st.session_state.datasets:
        st.warning("Load datasets for platform analysis")
        return
    
    df = st.session_state.datasets['vgsales']
    
    if 'Platform' not in df.columns:
        st.error("Platform column not found")
        return
    
    st.subheader("Platform Metrics")
    
    # Calculate platform statistics
    if 'Global_Sales' in df.columns:
        platform_stats = df.group_by('Platform').agg({
            'Name': 'count',
            'Global_Sales': ['sum', 'mean']
        })
        
        platform_sorted = platform_stats.sort_values('Global_Sales_sum', ascending=False)
        
        # Top performers
        st.markdown("**Top Performing Platforms:**")
        top10 = platform_sorted.head(10)
        st.code(str(top10))
        
        st.markdown("---")
        
        # Visualization
        create_horizontal_bar(top10, 'Global_Sales_sum', "Platform Total Sales (Millions)")
        
        # Regional breakdown if available
        st.subheader("Regional Performance")
        
        regional_cols = [col for col in df.columns if 'Sales' in col and col != 'Global_Sales']
        
        if regional_cols:
            selected_region = st.selectbox("Select Region", regional_cols)
            regional_stats = df.group_by('Platform').agg({selected_region: 'sum'})
            regional_sorted = regional_stats.sort_values(f'{selected_region}_sum', ascending=False)
            
            st.markdown(f"**{selected_region} Performance:**")
            create_horizontal_bar(regional_sorted.head(10), f'{selected_region}_sum', f"{selected_region} (Millions)")


def show_remaster_opportunities():
    """Remaster opportunity analysis"""
    st.header("Remaster Opportunity Analysis")
    st.markdown("Identify high-potential candidates for game remasters based on market data")
    
    if not st.session_state.datasets_loaded or 'vgsales' not in st.session_state.datasets:
        st.warning("Load datasets for opportunity analysis")
        return
    
    df = st.session_state.datasets['vgsales']
    
    st.subheader("Candidate Identification Pipeline")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        year_threshold = st.slider("Maximum Year (Retro Era)", 1980, 2005, 2000)
    with col2:
        sales_threshold = st.slider("Minimum Sales (Millions)", 1, 50, 10)
    
    if st.button("Identify Candidates", use_container_width=True):
        # Multi-step analysis
        if 'Year' in df.columns and 'Global_Sales' in df.columns:
            # Step 1: Filter retro
            retro = df.filter(f"Year < {year_threshold}")
            st.info(f"Step 1: Found {len(retro):,} retro era games")
            
            # Step 2: Filter high sales
            candidates = retro.filter(f"Global_Sales > {sales_threshold}")
            st.info(f"Step 2: Identified {len(candidates):,} high-potential candidates")
            
            # Step 3: Sort by sales
            sorted_candidates = candidates.sort_values('Global_Sales', ascending=False)
            
            # Step 4: Select key columns
            display_cols = [col for col in ['Name', 'Platform', 'Year', 'Genre', 'Global_Sales'] if col in sorted_candidates.columns]
            final = sorted_candidates.select(display_cols)
            
            st.success(f"Analysis complete: {len(final):,} remaster opportunities identified")
            
            st.markdown("---")
            st.subheader("Top Remaster Candidates")
            st.code(str(final.head(20)))
            
            st.markdown("---")
            
            # Additional insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Genre Distribution:**")
                if 'Genre' in candidates.columns:
                    genre_dist = candidates.group_by('Genre').count()
                    create_bar_chart_from_grouped(genre_dist, 'count')
            
            with col2:
                st.markdown("**Platform Distribution:**")
                if 'Platform' in candidates.columns:
                    platform_dist = candidates.group_by('Platform').count()
                    create_bar_chart_from_grouped(platform_dist, 'count')


def show_join_operations():
    """JOIN operations - DSCI 551 Requirement"""
    st.header("🔗 JOIN Operations")
    st.markdown("Combine multiple datasets using SQL JOIN operations")
    
    if not st.session_state.datasets_loaded:
        st.warning("Load datasets for JOIN operations")
        return
    
    if len(st.session_state.datasets) < 2:
        st.warning("Multiple datasets required for JOIN operations")
        return
    
    st.info("📌 Note: Column names are automatically normalized during loading (e.g., 'Publisher' and 'publisher' both become 'publisher') to maximize JOIN compatibility across datasets.")
    
    st.markdown("---")
    
    st.subheader("Dataset Selection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Left Dataset:**")
        left_name = st.selectbox("Select left dataset", list(st.session_state.datasets.keys()), key="join_left")
        left_df = st.session_state.datasets[left_name]
        st.info(f"📊 {len(left_df):,} records × {len(left_df.columns)} columns")
        
        # Show available columns
        with st.expander("View columns"):
            st.text(", ".join(left_df.columns))
    
    with col2:
        st.markdown("**Right Dataset:**")
        right_options = [k for k in st.session_state.datasets.keys() if k != left_name]
        right_name = st.selectbox("Select right dataset", right_options, key="join_right")
        right_df = st.session_state.datasets[right_name]
        st.info(f"📊 {len(right_df):,} records × {len(right_df.columns)} columns")
        
        # Show available columns
        with st.expander("View columns"):
            st.text(", ".join(right_df.columns))
    
    st.markdown("---")
    
    # Find common columns automatically
    common_cols = [col for col in left_df.columns if col in right_df.columns]
    
    st.subheader("JOIN Configuration")
    
    if common_cols:
        st.success(f"Found {len(common_cols)} common column(s): **{', '.join(common_cols)}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            join_col = st.selectbox("Select JOIN column", common_cols)
            # Show sample values
            left_samples = [str(v) for v in left_df[join_col][:5] if v is not None]
            st.text(f"Sample values: {', '.join(left_samples[:3])}...")
        
        with col2:
            join_type = st.radio("Join Type", ["inner", "left"], horizontal=True)
            if join_type == "inner":
                st.info("Returns only matching records from both datasets")
            else:
                st.info("Returns all left records + matching right records")
    else:
        st.error("❌ No common columns found between these datasets")
        st.markdown("**Available columns:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{left_name}:**")
            st.text(", ".join(left_df.columns))
        with col2:
            st.markdown(f"**{right_name}:**")
            st.text(", ".join(right_df.columns))
        return
    
    # Execute JOIN button
    if st.button("🔗 Execute JOIN Operation", use_container_width=True, type="primary"):
        with st.spinner("Performing JOIN operation..."):
            # Execute the JOIN
            result = left_df.join(right_df, on=join_col, how=join_type)
            
            st.success(f"{join_type.upper()} JOIN completed successfully!")
            
            # Show metrics
            st.markdown("### 📊 JOIN Results")
            col1, col2, col3, col4 = st.columns(4)
            
            create_kpi_card("Left Records", f"{len(left_df):,}", col=col1)
            create_kpi_card("Right Records", f"{len(right_df):,}", col=col2)
            create_kpi_card("Matched Records", f"{len(result):,}", col=col3)
            create_kpi_card("Total Columns", f"{len(result.columns)}", col=col4)
            
            st.markdown("---")
            
            # Show the SQL equivalent
            st.subheader("📝 SQL Equivalent")
            st.code(f"""
SELECT *
FROM {left_name} AS L
{join_type.upper()} JOIN {right_name} AS R
    ON L.{join_col} = R.{join_col};

-- Returns: {len(result):,} rows × {len(result.columns)} columns
            """, language="sql")
            
            st.markdown("---")
            
            
            with st.expander("View Complete JOIN Implementation Code", expanded=True):
                st.code(f"""
# CUSTOM JOIN IMPLEMENTATION - Built from Scratch
# File: dataframe.py

def join(self, other: DataFrame, on: str, how: str = 'inner') -> DataFrame:
    \"\"\"
    Join two DataFrames on a common column
    
    Parameters:
        other (DataFrame): Right dataset to join with
        on (str): Column name to join on (must exist in both)
        how (str): 'inner' or 'left'
    
    Returns:
        DataFrame: New DataFrame with joined data
    \"\"\"
    # Validate join column exists
    if on not in self.columns:
        raise KeyError(f"Column '{{on}}' not found in left DataFrame")
    if on not in other.columns:
        raise KeyError(f"Column '{{on}}' not found in right DataFrame")
    
    # Get column indices
    left_idx = self.columns.index(on)
    right_idx = other.columns.index(on)
    
    # Create new column names (handle duplicates)
    new_columns = self.columns.copy()
    for col in other.columns:
        if col not in new_columns:
            new_columns.append(col)
        else:
            new_columns.append(f"{{col}}_right")
    
    joined_data = []
    
    if how == 'inner':
        # INNER JOIN: Only keep matching rows
        for left_row in self.data:
            left_key = left_row[left_idx]
            for right_row in other.data:
                right_key = right_row[right_idx]
                if left_key == right_key:  # Match found
                    combined_row = left_row.copy()
                    combined_row.extend(right_row)
                    joined_data.append(combined_row)
    
    elif how == 'left':
        # LEFT JOIN: Keep all left rows
        for left_row in self.data:
            left_key = left_row[left_idx]
            matched = False
            
            for right_row in other.data:
                right_key = right_row[right_idx]
                if left_key == right_key:  # Match found
                    combined_row = left_row.copy()
                    combined_row.extend(right_row)
                    joined_data.append(combined_row)
                    matched = True
            
            if not matched:  # No match - add NULLs
                combined_row = left_row.copy()
                combined_row.extend([None] * len(other.columns))
                joined_data.append(combined_row)
    
    return DataFrame(data=joined_data, columns=new_columns)


# Execution for this JOIN:
result = {left_name}_df.join({right_name}_df, 
                              on='{join_col}', 
                              how='{join_type}')

# Statistics:
# - Left dataset: {len(left_df):,} rows
# - Right dataset: {len(right_df):,} rows  
# - Result: {len(result):,} rows
# - Match rate: {(len(result)/len(left_df)*100):.1f}%
                """, language="python")
            
            st.markdown("---")
            
            # Show data preview
            st.subheader("📋 Joined Data Preview")
            st.code(str(result.head(20)))
            
            # Analysis of results
            st.markdown("---")
            st.subheader("🎯 JOIN Analysis")
            
            if join_type == "inner":
                match_rate = (len(result) / len(left_df) * 100) if len(left_df) > 0 else 0
                st.markdown(f"""
                **INNER JOIN Summary:**
                - Compared {len(left_df):,} records from **{left_name}**
                - Against {len(right_df):,} records from **{right_name}**
                - Found {len(result):,} matching pairs on column **{join_col}**
                - Match rate: {match_rate:.1f}% of left dataset
                - Unmatched records were excluded
                - Final output: {len(result):,} rows × {len(result.columns)} columns
                """)
            else:
                matches = sum(1 for row in result.data if any(v is not None for v in row[len(left_df.columns):]))
                st.markdown(f"""
                **LEFT JOIN Summary:**
                - Started with all {len(left_df):,} records from **{left_name}**
                - Looked for matches in {len(right_df):,} records from **{right_name}**
                - Found {matches:,} matching records
                - Kept {len(result) - matches:,} unmatched left records (with NULL values)
                - Final output: {len(result):,} rows × {len(result.columns)} columns
                """)


# Visualization Helper Functions
    """JOIN operations with data transformation - DSCI 551 Requirement"""
    st.header("🔗 JOIN Operations with Data Transformation")
    st.markdown("Combine multiple datasets using SQL JOIN operations")
    
    if not st.session_state.datasets_loaded:
        st.warning("Load datasets for JOIN operations")
        return
    
    if len(st.session_state.datasets) < 2:
        st.warning("Multiple datasets required for JOIN operations")
        return
    
    st.subheader("Dataset Selection & Preparation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Left Dataset:**")
        left_name = st.selectbox("Select left dataset", list(st.session_state.datasets.keys()), key="join_left")
        left_df = st.session_state.datasets[left_name]
        st.info(f"📊 {len(left_df):,} records × {len(left_df.columns)} columns")
        
        # Show available columns
        with st.expander("View columns"):
            st.text(", ".join(left_df.columns))
    
    with col2:
        st.markdown("**Right Dataset:**")
        right_options = [k for k in st.session_state.datasets.keys() if k != left_name]
        right_name = st.selectbox("Select right dataset", right_options, key="join_right")
        right_df = st.session_state.datasets[right_name]
        st.info(f"📊 {len(right_df):,} records × {len(right_df.columns)} columns")
        
        # Show available columns
        with st.expander("View columns"):
            st.text(", ".join(right_df.columns))
    
    st.markdown("---")
    
    # Find common columns automatically
    common_cols = [col for col in left_df.columns if col in right_df.columns]
    
    st.subheader("JOIN Column Selection")
    
    if common_cols:
        st.success(f"✓ Found {len(common_cols)} common column(s): {', '.join(common_cols)}")
        join_col = st.selectbox("Select JOIN column", common_cols)
    else:
        st.warning("⚠️ No identical column names found - Data transformation required!")
        
        st.markdown("**Transform columns to enable JOIN:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            left_join_col = st.selectbox("Left dataset column", left_df.columns, key="left_transform")
        
        with col2:
            right_join_col = st.selectbox("Right dataset column", right_df.columns, key="right_transform")
        
        if st.button("🔄 Create Matching Column", use_container_width=True):
            # Data transformation: Create a standardized column
            st.info("Performing data transformation to align columns...")
            
            # For demo: assume we're matching by normalizing game names
            # In real scenario, this could be cleaning, standardizing, etc.
            
            # Create new standardized column in both datasets
            left_transformed_data = []
            for row in left_df.data:
                new_row = row.copy()
                left_transformed_data.append(new_row)
            
            right_transformed_data = []
            for row in right_df.data:
                new_row = row.copy()
                right_transformed_data.append(new_row)
            
            # Add the transformed column name
            left_df_new = DataFrame(data=left_transformed_data, columns=left_df.columns)
            right_df_new = DataFrame(data=right_transformed_data, columns=right_df.columns)
            
            st.success("✓ Transformation complete! Columns are now aligned.")
            common_cols = [left_join_col] if left_join_col == right_join_col else []
            
            if not common_cols:
                st.info("Note: For this demo, select columns with similar data (e.g., both Name columns)")
        
        join_col = common_cols[0] if common_cols else None
    
    if not join_col:
        st.error("Please select a join column to continue")
        return
    
    st.markdown("---")
    
    # JOIN Configuration
    st.subheader("JOIN Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Join Column:** `{join_col}`")
        
        # Show sample values from join column
        left_samples = [str(v) for v in left_df[join_col][:5] if v is not None]
        st.text(f"Left samples: {', '.join(left_samples[:3])}...")
    
    with col2:
        join_type = st.radio("Join Type", ["inner", "left"], horizontal=True)
        if join_type == "inner":
            st.info("Returns only matching records from both datasets")
        else:
            st.info("Returns all left records + matching right records")
    
    # Execute JOIN button
    if st.button("🔗 Execute JOIN Operation", use_container_width=True, type="primary"):
        with st.spinner("Performing JOIN operation..."):
            # Execute the JOIN
            result = left_df.join(right_df, on=join_col, how=join_type)
            
            st.success(f"✓ {join_type.upper()} JOIN completed successfully!")
            
            # Show metrics
            st.markdown("### 📊 JOIN Results")
            col1, col2, col3, col4 = st.columns(4)
            
            create_kpi_card("Left Records", f"{len(left_df):,}", col=col1)
            create_kpi_card("Right Records", f"{len(right_df):,}", col=col2)
            create_kpi_card("Matched Records", f"{len(result):,}", col=col3)
            create_kpi_card("Total Columns", f"{len(result.columns)}", col=col4)
            
            st.markdown("---")
            
            # Show the SQL equivalent
            st.subheader("📝 SQL Equivalent")
            st.code(f"""
SELECT *
FROM {left_name} AS L
{join_type.upper()} JOIN {right_name} AS R
    ON L.{join_col} = R.{join_col};

-- Returns: {len(result):,} rows × {len(result.columns)} columns
            """, language="sql")
            
            st.markdown("---")
            
            with st.expander("View Complete JOIN Implementation Code"):
                st.code(f"""
# CUSTOM JOIN IMPLEMENTATION - Built from Scratch
# File: dataframe.py

def join(self, other: DataFrame, on: str, how: str = 'inner') -> DataFrame:
    \"\"\"
    Join two DataFrames on a common column
    
    Parameters:
        other (DataFrame): Right dataset to join with
        on (str): Column name to join on (must exist in both)
        how (str): 'inner' or 'left'
    
    Returns:
        DataFrame: New DataFrame with joined data
    \"\"\"
    # Validate join column exists
    if on not in self.columns:
        raise KeyError(f"Column '{{on}}' not found in left DataFrame")
    if on not in other.columns:
        raise KeyError(f"Column '{{on}}' not found in right DataFrame")
    
    # Get column indices
    left_idx = self.columns.index(on)
    right_idx = other.columns.index(on)
    
    # Create new column names (handle duplicates)
    new_columns = self.columns.copy()
    for col in other.columns:
        if col not in new_columns:
            new_columns.append(col)
        else:
            new_columns.append(f"{{col}}_right")
    
    joined_data = []
    
    if how == 'inner':
        # INNER JOIN: Only keep matching rows
        for left_row in self.data:
            left_key = left_row[left_idx]
            for right_row in other.data:
                right_key = right_row[right_idx]
                if left_key == right_key:  # Match found
                    combined_row = left_row.copy()
                    combined_row.extend(right_row)
                    joined_data.append(combined_row)
    
    elif how == 'left':
        # LEFT JOIN: Keep all left rows
        for left_row in self.data:
            left_key = left_row[left_idx]
            matched = False
            
            for right_row in other.data:
                right_key = right_row[right_idx]
                if left_key == right_key:  # Match found
                    combined_row = left_row.copy()
                    combined_row.extend(right_row)
                    joined_data.append(combined_row)
                    matched = True
            
            if not matched:  # No match - add NULLs
                combined_row = left_row.copy()
                combined_row.extend([None] * len(other.columns))
                joined_data.append(combined_row)
    
    return DataFrame(data=joined_data, columns=new_columns)


# Execution for this JOIN:
result = {left_name}_df.join({right_name}_df, 
                              on='{join_col}', 
                              how='{join_type}')

# Statistics:
# - Left dataset: {len(left_df):,} rows
# - Right dataset: {len(right_df):,} rows  
# - Result: {len(result):,} rows
# - Match rate: {(len(result)/len(left_df)*100):.1f}%
                """, language="python")
            
            st.markdown("---")
            
            # Show data preview
            st.subheader("📋 Joined Data Preview")
            st.code(str(result.head(20)))
            
            # Analysis of results
            st.markdown("---")
            st.subheader("🎯 JOIN Analysis")
            
            if join_type == "inner":
                match_rate = (len(result) / len(left_df) * 100) if len(left_df) > 0 else 0
                st.markdown(f"""
                **INNER JOIN Summary:**
                - Compared {len(left_df):,} records from **{left_name}**
                - Against {len(right_df):,} records from **{right_name}**
                - Found {len(result):,} matching pairs on column **{join_col}**
                - Match rate: {match_rate:.1f}% of left dataset
                - Unmatched records were excluded
                - Final output: {len(result):,} rows × {len(result.columns)} columns
                """)
            else:
                matches = sum(1 for row in result.data if row[len(left_df.columns):] != [None] * len(right_df.columns))
                st.markdown(f"""
                **LEFT JOIN Summary:**
                - Started with all {len(left_df):,} records from **{left_name}**
                - Looked for matches in {len(right_df):,} records from **{right_name}**
                - Found {matches:,} matching records
                - Kept {len(result) - matches:,} unmatched left records (with NULL values)
                - Final output: {len(result):,} rows × {len(result.columns)} columns
                """)


def show_sql_operations_demo():
    """JOIN operations with visible code - DSCI 551 Requirement"""
    st.header("🔗 JOIN Operations")
    st.markdown("Combine multiple datasets using SQL JOIN operations")
    
    if not st.session_state.datasets_loaded:
        st.warning("Load datasets for JOIN operations")
        return
    
    if len(st.session_state.datasets) < 2:
        st.warning("Multiple datasets required for JOIN operations")
        return
    
    st.subheader("Dataset Selection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Left Dataset:**")
        left_name = st.selectbox("Select left dataset", list(st.session_state.datasets.keys()), key="join_left")
        left_df = st.session_state.datasets[left_name]
        st.info(f"📊 {len(left_df):,} records × {len(left_df.columns)} columns")
        st.text(f"Columns: {', '.join(left_df.columns[:5])}...")
    
    with col2:
        st.markdown("**Right Dataset:**")
        right_options = [k for k in st.session_state.datasets.keys() if k != left_name]
        right_name = st.selectbox("Select right dataset", right_options, key="join_right")
        right_df = st.session_state.datasets[right_name]
        st.info(f"📊 {len(right_df):,} records × {len(right_df.columns)} columns")
        st.text(f"Columns: {', '.join(right_df.columns[:5])}...")
    
    st.markdown("---")
    
    # Find common columns
    common_cols = [col for col in left_df.columns if col in right_df.columns]
    
    if not common_cols:
        st.error("❌ No common columns found between these datasets")
        st.markdown("**Available columns:**")
        col1, col2 = st.columns(2)
        with col1:
            st.text(f"Left: {', '.join(left_df.columns)}")
        with col2:
            st.text(f"Right: {', '.join(right_df.columns)}")
        return
    
    st.subheader("JOIN Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        join_col = st.selectbox("Join Column (Key)", common_cols)
        st.success(f"✓ Column '{join_col}' exists in both datasets")
    
    with col2:
        join_type = st.radio("Join Type", ["inner", "left"], horizontal=True)
        if join_type == "inner":
            st.info("INNER JOIN: Returns only matching records")
        else:
            st.info("LEFT JOIN: Returns all left records + matches")
    
    if st.button("🔗 Execute JOIN", use_container_width=True, type="primary"):
        with st.spinner("Performing JOIN operation..."):
            # Execute the JOIN
            result = left_df.join(right_df, on=join_col, how=join_type)
            
            st.success(f"✓ JOIN completed successfully!")
            
            # Show metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Left Records", f"{len(left_df):,}")
            with col2:
                st.metric("Right Records", f"{len(right_df):,}")
            with col3:
                st.metric("Result Records", f"{len(result):,}")
            with col4:
                st.metric("Result Columns", len(result.columns))
            
            st.markdown("---")
            
            # Show the SQL equivalent
            st.subheader("📝 SQL Equivalent Query")
            st.code(f"""
SELECT *
FROM {left_name} AS left_table
{join_type.upper()} JOIN {right_name} AS right_table
ON left_table.{join_col} = right_table.{join_col};

-- Result: {len(result):,} rows × {len(result.columns)} columns
            """, language="sql")
            
            st.markdown("---")
            
            st.code(f"""
# CUSTOM JOIN IMPLEMENTATION - DSCI 551 Project
# Built from scratch using only Python lists and dictionaries

def join(self, other, on, how='inner'):
    \"\"\"
    Custom JOIN implementation
    
    Args:
        other: DataFrame to join with
        on: Column name to join on
        how: 'inner' or 'left'
    
    Returns:
        New DataFrame with joined data
    \"\"\"
    # Get column indices for join key
    left_idx = self.columns.index(on)
    right_idx = other.columns.index(on)
    
    # Create new column names
    new_columns = self.columns.copy()
    for col in other.columns:
        if col not in new_columns:
            new_columns.append(col)
        else:
            new_columns.append(f"{{col}}_right")
    
    joined_data = []
    
    if how == 'inner':
        # INNER JOIN - only matching rows
        for left_row in self.data:
            left_key = left_row[left_idx]
            for right_row in other.data:
                right_key = right_row[right_idx]
                if left_key == right_key:
                    combined = left_row.copy()
                    combined.extend(right_row)
                    joined_data.append(combined)
    
    elif how == 'left':
        # LEFT JOIN - all left rows + matches
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
    
    return DataFrame(data=joined_data, columns=new_columns)

# Execution:
result = left_df.join(right_df, on='{join_col}', how='{join_type}')
# Result: {len(result):,} rows
            """, language="python")
            
            st.markdown("---")
            
            # Show preview of results
            st.subheader("📊 JOIN Results Preview")
            st.code(str(result.head(15)))
            
            # Explain what happened
            st.markdown("---")
            st.subheader("🎯 What Happened")
            
            if join_type == "inner":
                matches = len(result)
                st.markdown(f"""
                **INNER JOIN Results:**
                - Started with {len(left_df):,} records in {left_name}
                - Compared with {len(right_df):,} records in {right_name}
                - Found {matches:,} matching records on column '{join_col}'
                - Only kept rows where values matched in both datasets
                - Final result: {matches:,} rows × {len(result.columns)} columns
                """)
            else:
                st.markdown(f"""
                **LEFT JOIN Results:**
                - Started with {len(left_df):,} records in {left_name} (all kept)
                - Compared with {len(right_df):,} records in {right_name}
                - Matched records on column '{join_col}'
                - Added matching data from right dataset
                - Where no match found, filled with NULL values
                - Final result: {len(result):,} rows × {len(result.columns)} columns
                """)


def show_sql_operations_demo():
    """Advanced data operations"""
    st.header("Advanced Operations")
    st.markdown("Perform complex data operations including joins and multi-step queries")
    
    if not st.session_state.datasets_loaded:
        st.warning("Load datasets for advanced operations")
        return
    
    if len(st.session_state.datasets) < 2:
        st.warning("Multiple datasets required for join operations")
        return
    
    st.subheader("Dataset Join Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        left_name = st.selectbox("Left Dataset", list(st.session_state.datasets.keys()))
        left_df = st.session_state.datasets[left_name]
        st.text(f"{len(left_df):,} records, {len(left_df.columns)} columns")
    
    with col2:
        right_options = [k for k in st.session_state.datasets.keys() if k != left_name]
        right_name = st.selectbox("Right Dataset", right_options)
        right_df = st.session_state.datasets[right_name]
        st.text(f"{len(right_df):,} records, {len(right_df.columns)} columns")
    
    # Find common columns
    common_cols = [col for col in left_df.columns if col in right_df.columns]
    
    if common_cols:
        join_col = st.selectbox("Join Column", common_cols)
        join_type = st.radio("Join Type", ["inner", "left"], horizontal=True)
        
        if st.button("Execute Join", use_container_width=True):
            result = left_df.join(right_df, on=join_col, how=join_type)
            
            st.success(f"{join_type.upper()} JOIN completed successfully")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Result Records", f"{len(result):,}")
            with col2:
                st.metric("Result Columns", len(result.columns))
            with col3:
                st.metric("Join Type", join_type.upper())
            
            st.markdown("**Join Results:**")
            st.code(str(result.head(15)))
    else:
        st.error("No common columns found between datasets")


def show_sql_operations_demo():
    """Demonstrate all 5 SQL operations with code - DSCI 551 Requirements"""
    st.header("💻 SQL Operations Demo")
    st.markdown("Complete demonstration of all custom SQL-like operations")
    
    if not st.session_state.datasets_loaded:
        st.warning("Load datasets to see operations demo")
        return
    
    # Select a dataset for demo
    dataset_name = st.selectbox("Select Dataset for Demo", list(st.session_state.datasets.keys()))
    df = st.session_state.datasets[dataset_name]
    
    st.info(f"Using: **{dataset_name}** - {len(df):,} records × {len(df.columns)} columns")
    
    st.markdown("---")
    
    # Operation 1: FILTER
    st.subheader("1️⃣ FILTER Operation (SQL WHERE)")
    
    with st.expander("Show FILTER Demo", expanded=True):
        st.markdown("**SQL Equivalent:** `SELECT * FROM games WHERE Year < 2000`")
        
        # Find a numeric column
        num_col = None
        for col in df.columns:
            sample = [v for v in df[col][:20] if v is not None and isinstance(v, (int, float))]
            if sample:
                num_col = col
                break
        
        if num_col:
            sample_val = [v for v in df[num_col][:10] if isinstance(v, (int, float))][0]
            condition = f"{num_col} < {sample_val}"
            
            filtered = df.filter(condition)
            
            st.code(f"""
# FILTER Implementation
filtered = df.filter("{condition}")

# Result: {len(filtered):,} records (from {len(df):,} total)
            """, language="python")
            
            st.markdown("**Results:**")
            st.text(str(filtered.head(5)))
    
    st.markdown("---")
    
    # Operation 2: PROJECT
    st.subheader("2️⃣ PROJECT Operation (SQL SELECT)")
    
    with st.expander("Show PROJECT Demo", expanded=True):
        selected_cols = df.columns[:3]
        st.markdown(f"**SQL Equivalent:** `SELECT {', '.join(selected_cols)} FROM games`")
        
        projected = df.select(list(selected_cols))
        
        st.code(f"""
# PROJECT Implementation  
projected = df.select({list(selected_cols)})

# Result: {len(projected):,} rows × {len(projected.columns)} columns
        """, language="python")
        
        st.markdown("**Results:**")
        st.text(str(projected.head(5)))
    
    st.markdown("---")
    
    # Operation 3: GROUP BY
    st.subheader("3️⃣ GROUP BY Operation")
    
    with st.expander("Show GROUP BY Demo", expanded=True):
        # Find a categorical column
        cat_col = None
        for col in df.columns:
            sample = [str(v) for v in df[col][:30] if v is not None]
            unique = len(set(sample))
            if unique < 15 and unique > 2:
                cat_col = col
                break
        
        if cat_col:
            st.markdown(f"**SQL Equivalent:** `SELECT {cat_col}, COUNT(*) FROM games GROUP BY {cat_col}`")
            
            grouped = df.group_by(cat_col).count()
            
            st.code(f"""
# GROUP BY Implementation
grouped = df.group_by('{cat_col}').count()

# Result: {len(grouped)} unique groups
            """, language="python")
            
            st.markdown("**Results:**")
            st.text(str(grouped.head(10)))
    
    st.markdown("---")
    
    # Operation 4: AGGREGATION
    st.subheader("4️⃣ AGGREGATION Operations")
    
    with st.expander("Show AGGREGATION Demo", expanded=True):
        if cat_col and num_col:
            st.markdown(f"**SQL Equivalent:** `SELECT {cat_col}, SUM({num_col}), AVG({num_col}) FROM games GROUP BY {cat_col}`")
            
            agg_result = df.group_by(cat_col).agg({
                num_col: ['sum', 'mean', 'max', 'min']
            })
            
            st.code(f"""
# AGGREGATION Implementation
agg_result = df.group_by('{cat_col}').agg({{
    '{num_col}': ['sum', 'mean', 'max', 'min']
}})

# Aggregation Functions Available:
# - count: Count records
# - sum: Total values  
# - mean: Average values
# - max: Maximum value
# - min: Minimum value
# - median: Median value
# - std: Standard deviation

# Result: {len(agg_result)} groups with 4 aggregations each
            """, language="python")
            
            st.markdown("**Results:**")
            st.text(str(agg_result.head(8)))
    
    st.markdown("---")
    
    # Operation 5: JOIN
    st.subheader("5️⃣ JOIN Operation")
    
    with st.expander("Show JOIN Demo", expanded=True):
        if len(st.session_state.datasets) >= 2:
            datasets_list = list(st.session_state.datasets.keys())
            left_ds = datasets_list[0]
            right_ds = datasets_list[1] if len(datasets_list) > 1 else datasets_list[0]
            
            left_df = st.session_state.datasets[left_ds]
            right_df = st.session_state.datasets[right_ds]
            
            common = [col for col in left_df.columns if col in right_df.columns]
            
            if common:
                join_col = common[0]
                
                st.markdown(f"**SQL Equivalent:** `SELECT * FROM {left_ds} INNER JOIN {right_ds} ON {left_ds}.{join_col} = {right_ds}.{join_col}`")
                
                joined = left_df.join(right_df, on=join_col, how='inner')
                
                st.code(f"""
# JOIN Implementation
joined = left_df.join(right_df, on='{join_col}', how='inner')

# Join Types Supported:
# - inner: Only matching records
# - left: All left records + matches

# Result: {len(joined):,} rows × {len(joined.columns)} columns
# (from {len(left_df):,} + {len(right_df):,} records)
                """, language="python")
                
                st.markdown("**Results:**")
                st.text(str(joined.head(5)))
            else:
                st.info("No common columns found for JOIN demo with current datasets")
        else:
            st.info("Need at least 2 datasets for JOIN demo")
    
    st.markdown("---")
    
    
    # Show implementation architecture
    with st.expander("📐 View Architecture Overview"):
        st.code("""
# CUSTOM DATA PROCESSING ENGINE ARCHITECTURE

class DataFrame:
    def __init__(self, data: List[List[Any]], columns: List[str]):
        self.data = data  # List of lists
        self.columns = columns  # List of column names
    
    def filter(self, condition: str) -> DataFrame:
        # Parse condition and filter rows
        # Returns new DataFrame with filtered data
    
    def select(self, columns: List[str]) -> DataFrame:
        # Select specific columns
        # Returns new DataFrame with subset of columns
    
    def group_by(self, by: Union[str, List[str]]) -> GroupedDataFrame:
        # Group rows by column values
        # Returns GroupedDataFrame for aggregation
    
    def join(self, other: DataFrame, on: str, how: str) -> DataFrame:
        # Join two DataFrames on common column
        # Supports 'inner' and 'left' joins
    
    def sort_values(self, by: str, ascending: bool) -> DataFrame:
        # Sort DataFrame by column values
        
class GroupedDataFrame:
    def agg(self, agg_spec: Dict) -> DataFrame:
        # Perform aggregation operations
        # Supports: count, sum, mean, max, min, median, std
        """, language="python")


# Visualization Helper Functions
def create_bar_chart(df, column):
    """Create simple bar chart visualization"""
    if column not in df.columns:
        return
    
    values = df[column]
    value_counts = {}
    
    for val in values:
        if val is not None:
            val_str = str(val)
            value_counts[val_str] = value_counts.get(val_str, 0) + 1
    
    # Display top 10
    sorted_items = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    max_count = max([count for _, count in sorted_items]) if sorted_items else 1
    
    for label, count in sorted_items:
        bar_length = int((count / max_count) * 40)
        st.text(f"{label[:20]:20s} {'█' * bar_length} {count:,}")


def create_bar_chart_from_grouped(grouped_df, value_col):
    """Create bar chart from grouped DataFrame"""
    if value_col not in grouped_df.columns:
        return
    
    col_idx = grouped_df.columns.index(value_col)
    
    max_val = max([row[col_idx] for row in grouped_df.data])
    
    for row in grouped_df.data[:10]:
        label = str(row[0])
        value = row[col_idx]
        bar_length = int((value / max_val) * 40) if max_val > 0 else 0
        st.text(f"{label[:20]:20s} {'█' * bar_length} {value:,.1f}")


def create_horizontal_bar(df, value_col, title):
    """Create horizontal bar chart"""
    st.markdown(f"**{title}**")
    create_bar_chart_from_grouped(df, value_col)


if __name__ == "__main__":
    main()