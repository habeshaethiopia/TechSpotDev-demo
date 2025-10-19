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
    # Build the sidebar menu as one HTML block so we can attach JS handlers to toggle dropdown groups
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

        menu_items = [
            {
                "name": "Overview",
                "icon": "fas fa-clock",
                "has_dropdown": True,
                "dropdown_open": False,
            },
            {
                "name": "Input Tables",
                "icon": "fas fa-table",
                "has_dropdown": True,
                "dropdown_open": True,
                "active": True,
                "id": "input-tables",
            },
            {
                "name": "E-commerce",
                "icon": "fas fa-shopping-bag",
                "has_dropdown": True,
                "dropdown_open": False,
            },
            {
                "name": "Messages",
                "icon": "fas fa-comment",
                "has_dropdown": False,
                "badge": "4",
            },
            {
                "name": "Users",
                "icon": "fas fa-users",
                "has_dropdown": True,
                "dropdown_open": False,
            },
            {
                "name": "Support",
                "icon": "fas fa-headset",
                "has_dropdown": True,
                "dropdown_open": False,
            },
        ]

        html = """
        <style>
        .dropdown-group{display:none}
        .dropdown-group.open{display:block}
        </style>
        <div class='sidebar-menu'>
        """

        for item in menu_items:
            # Input Tables gets a specific id so its dropdown can be targeted
            if item.get("name") == "Input Tables":
                active_class = "active" if item.get("active") else ""
                arrow_icon = (
                    "fa-chevron-up" if item.get("dropdown_open") else "fa-chevron-down"
                )
                arrow_color = (
                    'style="color:#0b48d4"' if item.get("dropdown_open") else ""
                )
                html += f"<div class='menu-item {active_class}' data-target='{item.get('id')}'>"
                html += f"<span class='menu-icon'><i class='{item.get('icon')}' {arrow_color}></i></span>"
                html += f"<span class='menu-text'>{item.get('name')}</span>"
                html += f"<span class='dropdown-arrow'><i class='fas {arrow_icon}' {arrow_color}></i></span>"
                html += "</div>"

                # Dropdown items wrapped in a group so we can toggle show/hide
                dropdown_items = [
                    "Aircrew",
                    "Aircraft",
                    "Range slots",
                    "Events",
                    "Constraints",
                ]
                display_style = (
                    'style="display:block"' if item.get("dropdown_open") else ""
                )
                html += f"<div class='dropdown-group' data-parent='{item.get('id')}' {display_style}>"
                for di in dropdown_items:
                    html += f"<div class='dropdown-item'>{di}</div>"
                html += "</div>"
            else:
                # Regular menu items
                badge_html = (
                    f"<span class='menu-badge'>{item.get('badge')}</span>"
                    if item.get("badge")
                    else "<span class='dropdown-arrow'><i class='fas fa-chevron-down'></i></span>"
                )
                html += "<div class='menu-item'>"
                html += (
                    f"<span class='menu-icon'><i class='{item.get('icon')}'></i></span>"
                )
                html += f"<span class='menu-text'>{item.get('name')}</span>"
                html += badge_html
                html += "</div>"

        html += "</div>"

        # Inline JS to handle toggling dropdown groups when clicking corresponding menu-item
        html += """
        <script>
        document.addEventListener('click', function(e){
            const menuItem = e.target.closest('.menu-item');
            if(!menuItem) return;
            const target = menuItem.dataset.target;
            if(!target) return;
            const group = document.querySelector(`[data-parent="${target}"]`);
            if(!group) return;
            const isOpen = group.classList.toggle('open');
            if(isOpen) {
                group.style.display = 'block';
                const icon = menuItem.querySelector('.dropdown-arrow i');
                if(icon){ icon.classList.remove('fa-chevron-down'); icon.classList.add('fa-chevron-up'); icon.style.color = '#0b48d4'; }
            } else {
                group.style.display = 'none';
                const icon = menuItem.querySelector('.dropdown-arrow i');
                if(icon){ icon.classList.remove('fa-chevron-up'); icon.classList.add('fa-chevron-down'); icon.style.color = ''; }
            }
        });
        </script>
        """

        st.markdown(html, unsafe_allow_html=True)

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

    # st.markdown(
    #     """
    #     <div class='search-container'>
    #         <span class='search-icon'><i class="fas fa-search"></i></span>
    #          <input type='text' class='search-input' placeholder='Search for...' id='searchInput'>
    # </div>

    #     """,
    #     unsafe_allow_html=True,
    # )
    search_term = st.text_input(
        "Search",
        placeholder="Search for...",
        label_visibility="collapsed",
        key="search_input",
    )
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

# ---------- Table + Pagination ----------
# Pagination settings
per_page = 4
total_results = len(filtered_df)
import math

total_pages = max(1, math.ceil(total_results / per_page))

# Read page from query params so clicks on links update the URL and Streamlit will rerun
params = st.query_params
try:
    current_page = int(params.get("page", [1])[0])
except Exception:
    current_page = 1
current_page = max(1, min(total_pages, current_page))

# Slice the DataFrame for the current page
start = (current_page - 1) * per_page
end = start + per_page
page_df = filtered_df.iloc[start:end]

# Showing text
if total_results > 0:
    showing_text = f"Showing {start+1}-{min(end, total_results)} of {total_results}"
else:
    showing_text = "Showing 0-0 of 0"

# Build the COMPLETE table HTML in ONE string using only the page rows
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

for _, row in page_df.iterrows():
    html_table += f"""
        <tr>
            <td style='background-color:#1e2937'>{row.get('Last Name','')}</td>
            <td>{row.get('First Name','')}</td>
            <td style='background-color:#1e2937'>{row.get('Start','')}</td>
            <td>{row.get('End','')}</td>
            <td style='background-color:#1e2937'>{row.get('Recurrence','')}</td>
            <td>{row.get('Code','')}</td>
            <td style='background-color:#1e2937'>{row.get('Description','')}</td>
            <td>{row.get('Remarks','')}</td>
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

"""

# Render table
# st.markdown(html_table, unsafe_allow_html=True)


# Build pagination links (using query params so clicks trigger a full rerun)
def page_link(p):
    return f"?page={p}"


# Build a compact set of page numbers to show (windowed)
max_display = 10
page_items = []
if total_pages <= max_display:
    page_items = list(range(1, total_pages + 1))
else:
    # always show first and last, and a window around current_page
    left = max(2, current_page - 2)
    right = min(total_pages - 1, current_page + 2)
    page_items = [1]
    if left > 2:
        page_items.append("...")
    page_items.extend(range(left, right + 1))
    if right < total_pages - 1:
        page_items.append("...")
    page_items.append(total_pages)

pagination_html = """
<div class='pagination'>
    <span>{showing_text}</span>
    <div class='page-numbers'>
""".format(
    showing_text=showing_text
)

# Prev button
prev_page = max(1, current_page - 1)
pagination_html += f"<a class='page-nav' href='{page_link(prev_page)}'>&lt;</a>"

for p in page_items:
    if p == "...":
        pagination_html += "<span class='ellipsis'>...</span>"
        continue
    cls = "page active" if p == current_page else "page"
    pagination_html += f"<a class='{cls}' href='{page_link(p)}'>{p}</a>"

# Next button
next_page = min(total_pages, current_page + 1)
pagination_html += f"<a class='page-nav' href='{page_link(next_page)}'>&gt;</a>"

pagination_html += "</div></div></div>"
# st.markdown(html_table, unsafe_allow_html=True)
st.markdown(html_table+pagination_html, unsafe_allow_html=True)
