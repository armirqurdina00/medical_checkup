import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Doctor checkup", layout="wide")

try:
    conn = sqlite3.connect('patients.db')
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE Patient(
            fullname TEXT,
            email TEXT,
            birthdate TEXT,
            typeofvisit TEXT
        );
    """)

except sqlite3.OperationalError:
    pass

def add_patient(fullname, email, birthdate, typeofvisit):
    return cur.execute("INSERT INTO Patient VALUES(?, ?, ?, ?)", (fullname, email, birthdate, typeofvisit))

def delete_patient(fullname):
    return cur.execute("DELETE FROM Patient WHERE fullname=?", (fullname,))

def modify_patient(email, new_fullname):
    return cur.execute("UPDATE Patient SET fullname=? WHERE email=?", (new_fullname, email))

def search(field, text):
    if field == 'Full name':
        return cur.execute("SELECT * FROM Patient WHERE fullname=?", (text,))
    elif field == 'Email':
        return cur.execute("SELECT * FROM Patient WHERE email=?", (text,))
    elif field == 'Type of visit':
        return cur.execute("SELECT * FROM Patient WHERE typeofvisit=?", (text,))

def get_data(file_name):
    file = open(file_name)
    data = file.readlines()
    return data


st.header("Doctor checkup")
st.markdown("***")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.subheader("Add patient")

    with st.form("add_patient"):

        fullname = st.text_input("Full name:")
        email = st.text_input("Email:")
        birthdate = st.date_input("Date of birth:")
        typeofvisit = st.selectbox(
            'Type of visit:',
            ('Sore throat', 'Headache', 'Stomach'))
        
        st.text("")

        submit_btn = st.form_submit_button("Add")

        if submit_btn:
            if fullname and email:
                add_patient(fullname, email, birthdate, typeofvisit)
                st.success("Patient added to database.")
            else:
                st.warning("Please fill out all the fields.")

with col2:

    st.subheader("Delete patient")

    with st.form("delete_patient"):
        fullname_to_delete = st.text_input("Full name: ")
        delete_btn = st.form_submit_button("Delete")

        if delete_btn:
            if fullname_to_delete:
                delete_patient(fullname_to_delete)
                st.success("Patient deleted from database.")
            else:
                st.warning("Please fill out the field")

with col3:
    st.subheader("Modify patient")

    with st.form("modify_patient"):
        current_email = st.text_input("Email: ")

        new_fullname = st.text_input("New full name: ")
        
        modify_btn = st.form_submit_button("Modify")

        if modify_btn:
            if new_fullname:
                modify_patient(current_email, new_fullname)
                st.success("Patient modified in the database.")
            else:
                st.warning("Please fill out the field")

with col4:
    st.subheader("Import data")

    with st.form("import_data"):
        file = st.file_uploader("Upload file")

        import_btn = st.form_submit_button("Import")

        if import_btn:
            if file:
                file_data = get_data(file.name)
                for row in file_data:
                    add_patient(row.split()[0], row.split()[1], row.split()[2], row.split()[3])
                st.success("Data imported successfully from file.")
            else:
                st.warning("Please upload a file")

data = cur.execute("SELECT * FROM Patient")

with st.form("search_patient"):
    st.subheader("Search patient")

    fields = st.radio("Search by:", ('Full name', 'Email', 'Type of visit'))
    text_to_search = st.text_input("Search")

    search_btn = st.form_submit_button("Search")
    if search_btn:
        if text_to_search:
            data = search(fields, text_to_search)
            data = cur.fetchall()

conn.commit()

fullnames = []
emails = []
birthdates = []
typeofvisits = []

for row in data:
    fullnames.append(row[0])
    emails.append(row[1])
    birthdates.append(row[2])
    typeofvisits.append(row[3])

table_data = pd.DataFrame(
    {
        "Full name": fullnames,
        "Email": emails,
        "Date of birth": birthdates,
        "Type of visit": typeofvisits
    }
)

st.header("Patients")

st.table(table_data)