# Bachelorarbeit

To start the setup process, follow the instructions below based on your operating system:

## Windows

1. Open a command prompt in the project directory.
2. Run the following command to execute the setup script:
`setup.bat`
3. Enter Your Api-Key
4. Select app to run

## Unix/Linux/Mac

1. Open a terminal in the project directory.
2. Run the following command to make the shell script executable:
`source setup.sh`
3. Enter Your Api-Key
4. Select app to run
### How to install manually

pip install -r requirements.txt

## Setup API key

Create file .env and add your OpenAI API key to it.

`OPENAI_API_KEY='YOUR_OPENAI_API_KEY_HERE'`

## Start Application

`streamlit run app_doc.py` -> to check documents
`streamlit run app_gbt.py` -> to get regular gpt response

## Example

![alt text](img/image.png)

## Thank you
