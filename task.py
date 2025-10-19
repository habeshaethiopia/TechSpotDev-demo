import streamlit as st
import pandas as pd
import json

# ---------- Page Setup ----------
st.set_page_config(page_title="Snives Dashboard", layout="wide")

# ---------- Load CSS and Font Awesome ----------
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """,
    unsafe_allow_html=True,
)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    # Close button positioned at top right
    st.markdown(
        "<div style='text-align: right; margin-bottom: 0px;'><span class='sidebar-close'><i class='fas fa-times'></i></span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='height: 1px; background-color: #374151; margin: 20px 0;'></div>",
        unsafe_allow_html=True,
    )
    # Menu items with icons
    menu_items = [
        {
            "name": "Overview",
            "icon": "🕐",
            "has_dropdown": True,
            "dropdown_open": False,
        },
        {
            "name": "Input Tables",
            "icon": "📊",
            "has_dropdown": True,
            "dropdown_open": True,
            "active": True,
        },
        {
            "name": "E-commerce",
            "icon": "🛍️",
            "has_dropdown": True,
            "dropdown_open": False,
        },
        {
            "name": "Messages",
            "icon": "💬",
            "has_dropdown": False,
            "dropdown_open": False,
            "badge": "4",
        },
        {"name": "Users", "icon": "👥", "has_dropdown": True, "dropdown_open": False},
        {"name": "Support", "icon": "🎧", "has_dropdown": True, "dropdown_open": False},
    ]

    for item in menu_items:
        if item["name"] == "Input Tables":
            # Active item with dropdown
            st.markdown(
                """
                <div class='menu-item active'>
                    <span class='menu-icon'><i class="fas fa-table" style="color:#0b48d4"></i></span>
                    <span class='menu-text'>Input Tables</span>
                    <span class='dropdown-arrow'><i class="fas fa-chevron-up" style="color:#0b48d4"></i></span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Dropdown items
            dropdown_items = [
                "Aircrew",
                "Aircraft",
                "Range slots",
                "Events",
                "Constraints",
            ]
            for dropdown_item in dropdown_items:
                st.markdown(
                    f"<div class='dropdown-item'>{dropdown_item}</div>",
                    unsafe_allow_html=True,
                )
        else:
            # Regular menu items - using static HTML to avoid f-string issues
            if item["name"] == "Overview":
                st.markdown(
                    """
                    <div class='menu-item'>
                        <span class='menu-icon'><i class="fas fa-clock"></i></span>
                        <span class='menu-text'>Overview</span>
                        <span class='dropdown-arrow'><i class="fas fa-chevron-down"></i></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif item["name"] == "E-commerce":
                st.markdown(
                    """
                    <div class='menu-item'>
                        <span class='menu-icon'><i class="fas fa-shopping-bag"></i></span>
                        <span class='menu-text'>E-commerce</span>
                        <span class='dropdown-arrow'><i class="fas fa-chevron-down"></i></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif item["name"] == "Messages":
                st.markdown(
                    """
                    <div class='menu-item'>
                        <span class='menu-icon'><i class="fas fa-comment"></i></span>
                        <span class='menu-text'>Messages</span>
                        <span class='menu-badge'>4</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif item["name"] == "Users":
                st.markdown(
                    """
                    <div class='menu-item'>
                        <span class='menu-icon'><i class="fas fa-users"></i></span>
                        <span class='menu-text'>Users</span>
                        <span class='dropdown-arrow'><i class="fas fa-chevron-down"></i></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif item["name"] == "Support":
                st.markdown(
                    """
                    <div class='menu-item'>
                        <span class='menu-icon'><i class="fas fa-headset"></i></span>
                        <span class='menu-text'>Support</span>
                        <span class='dropdown-arrow'><i class="fas fa-chevron-down"></i></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# ---------- Header ----------
st.markdown(
    """
    <div class="page-title-container" >
        <h1 class='page-title'">Snives</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------date presentation-------

col1, col3, col2 = st.columns([2, 3, 2])
with col1:
    # Working search functionality with Font Awesome icon

    st.markdown(
        """
        <div class='search-container'>
            <span class='search-icon'><i class="fas fa-search"></i></span>
             <input type='text' class='search-input' placeholder='Search for...' id='searchInput'>
    </div>
        
        """,
        unsafe_allow_html=True,
    )
    search_term = ''
    # search_term = st.text_input(
    #     "Search",
    #     placeholder="Search for...",
    #     label_visibility="collapsed",
    #     key="search_input",
    # )
with col2:
    st.markdown(
        """
        <div class='top-buttons'>
            <button class='add-btn'><i class="fas fa-plus"></i> Add Snivel</button>
            <button class='filter-btn'><i class="fas fa-filter"></i> Filters <i class= "fas fa-chevron-down"></i</button>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Load Data from JSON File ----------
@st.cache_data
def load_data():
    """Load data from JSON file with caching for better performance"""
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        st.error("Data file 'data.json' not found!")
        return pd.DataFrame()
    except json.JSONDecodeError:
        st.error("Invalid JSON format in 'data.json'!")
        return pd.DataFrame()


df = load_data()

# Check if data was loaded successfully
if df.empty:
    st.error("No data available. Please check the data.json file.")
    st.stop()

# ---------- Search Filtering ----------
if search_term:
    # Filter data based on search term
    mask = (
        df["Last Name"].str.contains(search_term, case=False, na=False)
        | df["First Name"].str.contains(search_term, case=False, na=False)
        | df["Start"].str.contains(search_term, case=False, na=False)
        | df["End"].str.contains(search_term, case=False, na=False)
        | df["Recurrence"].str.contains(search_term, case=False, na=False)
        | df["Code"].str.contains(search_term, case=False, na=False)
        | df["Description"].str.contains(search_term, case=False, na=False)
        | df["Remarks"].str.contains(search_term, case=False, na=False)
    )
    filtered_df = df[mask]
else:
    filtered_df = df

# ---------- Table ----------
# Build the COMPLETE table HTML in ONE string
html_table = """
<div class='table-container'>
<table class='data-table'>
    <thead>
        <tr>
            <th>Last Name</th>
            <th class='sortable'>First Name</th>
            <th class='sortable'>Start</th>
            <th>End</th>
            <th>Recurrence</th>
            <th>Code</th>
            <th>Description</th>
            <th>Remarks</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
"""

# Add ALL rows in the same string
for _, row in filtered_df.iterrows():
    html_table += f"""
        <tr>
            <td style='background-color:#1e2937'>{row['Last Name']}</td>
            <td>{row['First Name']}</td>
            <td style='background-color:#1e2937'>{row['Start']}</td>
            <td>{row['End']}</td>
            <td style='background-color:#1e2937'>{row['Recurrence']}</td>
            <td>{row['Code']}</td>
            <td style='background-color:#1e2937'>{row['Description']}</td>
            <td>{row['Remarks']}</td>
            <td style='background-color:#1e2937; ' >
            <div style='display:flex; gap:8px ' >
                <button class='edit-btn'>Edit<i class="fas fa-edit"></i> </button>
                <button class='delete-btn'><i class="fas fa-trash"></i> Delete</button>
                </div>
            </td>
        </tr>
""".strip()

# Close the table
html_table += """
    </tbody>
</table>
</div>
"""


# Render ONCE
st.markdown(html_table, unsafe_allow_html=True)
# ---------- Pagination ----------
# Calculate pagination info based on filtered results
total_results = len(filtered_df)
showing_text = (
    f"Showing 1-{min(10, total_results)} of {total_results}"
    if total_results > 0
    else "Showing 0-0 of 0"
)

st.markdown(
    f"""
<div class='pagination'>
    <span>{showing_text}</span>
    <div class='page-numbers'>
        <button class='page-nav'>&lt;</button>
        <span class='page active'>1</span>
        <span class='page'>2</span>
        <span class='page'>3</span>
        <span class='page'>4</span>
        <span class='page'>5</span>
        <span class='page'>6</span>
        <span class='page'>7</span>
        <span class='page'>8</span>
        <span class='page'>9</span>
        <span class='page'>10</span>
        <button class='page-nav'>&gt;</button>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Close the outer data-presentation container
st.markdown(
    """ 
    </div> 
""",
    unsafe_allow_html=True,
)
