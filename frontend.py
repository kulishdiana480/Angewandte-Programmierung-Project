import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
NAAS_URL = "https://naas.isalman.dev/no"

############################################
### Say No App
############################################

st.title("🙅 Say No App")

def request_no():
    response = requests.get(NAAS_URL)
    response_json = response.json()
    return response_json["reason"]

if 'text1' not in st.session_state:
    st.session_state['text1'] = request_no()

if 'text' not in st.session_state:
    st.session_state['text'] = request_no()

name = st.text_input('Name', placeholder="Hier Name eingeben...")
st.write(name)

if st.button("Neuer Text1"):
    st.session_state['text1'] = request_no()
st.write(st.session_state["text1"])

if st.button("Neuer Text"):
    st.session_state['text'] = request_no()
st.write(st.session_state["text"])

with st.expander('session state'):
    st.write(st.session_state)

st.divider()

############################################
### Notes App
############################################

st.title("📝 Notes App")

############################################
### Function 1: Show all notes
############################################

st.header("📋 All Notes")

def get_notes():
    response = requests.get(f"{API_URL}/notes")
    if response.status_code == 200:
        return response.json()
    return []

notes = get_notes()

if not notes:
    st.info("No notes found. Create one below!")
else:
    note_titles = [f"{note['id']}: {note['title']}" for note in notes]
    selected_title = st.selectbox("Select a note to view:", note_titles)

    selected_id = int(selected_title.split(":")[0])
    selected_note = next((n for n in notes if n["id"] == selected_id), None)

    if selected_note:
        st.subheader(selected_note["title"])
        st.write(f"**Category:** {selected_note['category']}")
        st.write(f"**Tags:** {', '.join(selected_note['tags']) if selected_note['tags'] else 'No tags'}")
        st.write(f"**Created:** {selected_note['created_at']}")
        st.write(f"**Content:**")
        st.write(selected_note["content"])

############################################
### Function 2: Create a new note
############################################

st.header("➕ Create New Note")

with st.form("create_note_form"):
    title = st.text_input("Title", placeholder="Enter note title...")
    content = st.text_area("Content", placeholder="Enter note content...")
    category = st.selectbox(
        "Category",
        ["general", "work", "personal", "school", "ideas"]
    )
    tags_input = st.text_input(
        "Tags",
        placeholder="Enter tags separated by commas (e.g. urgent, work)"
    )

    submitted = st.form_submit_button("Create Note")

    if submitted:
        if not title or not content:
            st.error("Title and content are required!")
        else:
            tags = []
            if tags_input:
                tags = [t.strip() for t in tags_input.split(",") if t.strip()]

            payload = {
                "title": title,
                "content": content,
                "category": category,
                "tags": tags
            }

            response = requests.post(f"{API_URL}/notes", json=payload)

            if response.status_code == 201:
                st.success(f"Note '{title}' created successfully!")
                st.rerun()
            else:
                st.error(f"Error: {response.text}")