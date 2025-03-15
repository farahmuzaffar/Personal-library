import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import os

# File to store library data
LIBRARY_FILE = "library.txt"

# Initialize session state to store the library data
if 'library' not in st.session_state:
    if os.path.exists(LIBRARY_FILE):
        st.session_state.library = pd.read_csv(LIBRARY_FILE)
    else:
        st.session_state.library = pd.DataFrame(columns=['Title', 'Author', 'Year', 'Genre', 'Read Status'])

# Function to save the library to a file
def save_library():
    st.session_state.library.to_csv(LIBRARY_FILE, index=False)

# Function to add a book
def add_book(title, author, year, genre, read_status):
    new_book = pd.DataFrame([[title, author, year, genre, read_status]], 
                            columns=['Title', 'Author', 'Year', 'Genre', 'Read Status'])
    st.session_state.library = pd.concat([st.session_state.library, new_book], ignore_index=True)
    save_library()

# Function to remove a book
def remove_book(title):
    st.session_state.library = st.session_state.library[st.session_state.library['Title'] != title]
    save_library()

# Function to search for books
def search_books(search_term, search_by):
    if search_by == "Title":
        return st.session_state.library[st.session_state.library['Title'].str.contains(search_term, case=False)]
    elif search_by == "Author":
        return st.session_state.library[st.session_state.library['Author'].str.contains(search_term, case=False)]
    return pd.DataFrame()

# Function to display statistics
def display_statistics():
    total_books = len(st.session_state.library)
    if total_books == 0:
        return 0, 0.0
    read_books = st.session_state.library['Read Status'].sum()
    percentage_read = (read_books / total_books) * 100
    return total_books, percentage_read

# Streamlit app layout
st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")
st.sidebar.title("📖 Library Manager")

# Sidebar for menu options
menu_option = st.sidebar.radio(
    "Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"],
    index=0,
)

# Add a Book
if menu_option == "Add a Book":
    st.header("📚 Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1800, max_value=2100)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    if st.button("➕ Add Book", use_container_width=True):
        if title and author and year and genre:
            add_book(title, author, year, genre, read_status)
            st.success("✅ Book added successfully!")
        else:
            st.error("⚠️ Please fill in all fields.")

# Remove a Book
elif menu_option == "Remove a Book":
    st.header("❌ Remove a Book")
    title_to_remove = st.text_input("Enter the title of the book to remove")
    if st.button("🗑 Remove Book", use_container_width=True):
        if title_to_remove:
            remove_book(title_to_remove)
            st.success("✅ Book removed successfully!")
        else:
            st.error("⚠️ Please enter a title.")

# Search for a Book
elif menu_option == "Search for a Book":
    st.header("🔍 Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"], horizontal=True)
    search_term = st.text_input(f"Enter the {search_by.lower()}")
    if st.button("🔎 Search", use_container_width=True):
        if search_term:
            results = search_books(search_term, search_by)
            if not results.empty:
                st.write("📋 Matching Books:")
                st.dataframe(results)
            else:
                st.info("❌ No matching books found.")
        else:
            st.error("⚠️ Please enter a search term.")

# Display All Books
elif menu_option == "Display All Books":
    st.header("📖 Your Library")
    if not st.session_state.library.empty:
        st.dataframe(st.session_state.library)
    else:
        st.info("📭 No books in the library yet.")

# Display Statistics
elif menu_option == "Display Statistics":
    st.header("📊 Library Statistics")
    total_books, percentage_read = display_statistics()
    st.metric(label="Total Books", value=total_books)
    st.metric(label="Percentage Read", value=f"{percentage_read:.1f}%")

# Save library on exit
st.sidebar.write("---")
if st.sidebar.button("💾 Save & Exit", use_container_width=True):
    save_library()
    st.sidebar.success("✅ Library saved to file.")
    st.stop()





