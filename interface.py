import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess

st.title("VerstkAi")
st.subheader("A simple Website generator")

# Create an input field for the company name
company_name = st.text_input("Enter the company name")

# Create an input field for the company description
company_description = st.text_area("Enter the company description")

# Create a button
if st.button('Generate'):
    # When pressed, the field content will be written to the variables
    st.write(f'Company Name: {company_name}')
    st.write(f'Company Description: {company_description}')

    if (company_name and company_description):

        # Prepare the inputs
        input_data = f'{company_name}\n{company_description}\n'
        
        # Start the script with command-line arguments
        process = subprocess.Popen(['python3', 'streamlit', 'run', 'run.py', company_name, company_description], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Provide the input and wait for the process to complete
        stdout, stderr = process.communicate(input=input_data)

        # Open and read the HTML file
        with open('output.html', 'r') as f:
            html_string = f.read()

        # Display the HTML file
        components.html(html_string, height=900)

        # Create a button for exporting the HTML file
        # Check if the file exists
        if os.path.exists("output.html"):
            # Read the file
            with open("output.html", "r") as file:
                file_content = file.read()

            # Create a button for downloading the file
            st.download_button(
                label="Export",
                data=file_content,
                file_name="output.html",
                mime="text/html",
            )
        else:
            st.write("The file output.html does not exist in the current directory.")

    else:
        # Open error, cause input's empty
        with open('error.html', 'r') as f:
            html_string = f.read()

        # Display the HTML file
        components.html(html_string, height=900)