import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

def encrypt_rail_fence(text, k):
    rail = [['\n' for i in range(len(text))] for j in range(k)]
    dir_down = True
    row, col = k - 1, 0

    for i in range(len(text)):
        if (row == 0) or (row == k - 1):
            dir_down = not dir_down
        rail[row][col] = text[i]
        col += 1
        row += 1 if dir_down else -1

    encrypted_text = []
    for i in range(k-1, -1, -1):  # Start from the bottom line and go up
        for j in range(len(text)):
            if rail[i][j] != '\n':
                encrypted_text.append(rail[i][j])
    return "".join(encrypted_text)

def decrypt_rail_fence(text, k):
    rail = [['\n' for i in range(len(text))] for j in range(k)]
    dir_down = None
    row, col = 0, 0

    for i in range(len(text)):
        if row == 0:
            dir_down = True
        if row == k - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    index = 0
    for i in range(k):
        for j in range(len(text)):
            if (rail[i][j] == '*') and (index < len(text)):
                rail[i][j] = text[index]
                index += 1

    decrypted_text = []
    row, col = 0, 0
    for i in range(len(text)):
        if row == 0:
            dir_down = True
        if row == k - 1:
            dir_down = False
        if rail[row][col] != '\n':
            decrypted_text.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1

    return "".join(decrypted_text)

def preprocess_text(text):
    return text.replace(" ", "")

def format_output(text):
    return ' '.join([text[i:i+5] for i in range(0, len(text), 5)])

def render_rail_fence_as_table(text, k):
    rail = [[' ' for i in range(len(text))] for j in range(k)]
    dir_down = False
    row, col = 0, 0

    for i in range(len(text)):
        if (row == 0) or (row == k - 1):
            dir_down = not dir_down
        rail[row][col] = text[i]
        col += 1
        row += 1 if dir_down else -1

    table_html = "<table>"
    for row in reversed(rail):  # Reverse the order of rows
        table_html += "<tr>"
        for char in row:
            if char != ' ':
                table_html += f"<td style='background-color: #FFD700; color: black;'>{char}</td>"
            else:
                table_html += f"<td>{char}</td>"
        table_html += "</tr>"
    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)

st.title("Text Encryption and Decryption")

# Text input for the text to be encrypted
text = st.text_area("Enter text to be encrypted")
text = preprocess_text(text)

# Number input for the number of levels (k)
k = st.number_input("Enter the number of levels (k)", min_value=2, step=1)

# Encrypt button
if st.button("Encrypt"):
    encrypted_text = encrypt_rail_fence(text, k)
    formatted_encrypted_text = format_output(encrypted_text)
    st.text_area("Encrypted Text", value=formatted_encrypted_text, height=200)
    render_rail_fence_as_table(text, k)

# Decrypt button
if st.button("Decrypt"):
    decrypted_text = decrypt_rail_fence(text, k)
    formatted_decrypted_text = format_output(decrypted_text)
    st.text_area("Decrypted Text", value=formatted_decrypted_text, height=200)
    render_rail_fence_as_table(text, k)