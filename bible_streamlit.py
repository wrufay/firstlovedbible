import streamlit as st
import requests


st.set_page_config(page_title="Fay's Bible", page_icon="☻", layout="centered")

st.header("Search a Bible Verse in KJV")


with st.sidebar:
    st.header("Search Instructions")
    st.markdown("""
    - Search an entire chapter :red['Philippians 4']
    
    - Search a single verse :red['Jeremiah 29:11']
    
    - Search for a range of verses :red['Matthew 6:25-34']
    
    - Search for multiple chapters :red['Genesis 1-2'] or :red['John 3:16-4:10']
    
    
    """)
    st.markdown("""
                <div style='text-align: center; color: gray;'>
                <small>Made with ❤️ by Fay</small>
                </div>
                """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 0.5, 0.5])

with col1:
    book = st.text_input("Book Name", placeholder="Genesis")

with col2:
    verse = st.text_input("Chapter + Verse", placeholder="1:1")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("Search", type="primary")


def get_verse(book, verse):
    url = f'https://bible-api.com/{book}+{verse}?translation=kjv'
    try:
        response = requests.get(url)
        if response.status_code == 404:
            st.error("Error! Please enter a valid book and verse.")
            return
        elif response.status_code == 200: # if successful
            bible_content = response.json()
            st.markdown("---")
            st.badge(f"{bible_content['reference']}", color="blue")
            verses = bible_content["verses"]
            
            for v in verses:
                with st.container():
                    st.write(f'`{v['verse']}` {v['text']}')
        
        else:
            # catch errors
            st.warning(f"Unexpected error. (Status code: {response.status_code})")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


if search_button:
    if book and verse:
        with st.spinner("..."):
            get_verse(book, verse)
    elif book and not verse:
        st.warning("Please enter a chapter and verse.")
    else:
        st.warning("Please enter both a book name and verse.")
