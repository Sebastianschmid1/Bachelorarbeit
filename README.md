# Bachelorarbeit

To start the setup process, follow the instructions below based on your operating system:
### How to install automatically
## Windows

1. Open a command prompt in the project directory.
2. Run the following command to execute the setup script:
`setup.bat`
3. Enter Your Api-Key
4. Select app to run
5. Open in your browser `http://localhost:8501/` for gpt or `http://localhost:8500/` for embeddings

## Unix/Linux/Mac

1. Open a terminal in the project directory.
2. Run the following command to execute the shell script:
`source setup.sh`
3. Enter Your Api-Key
4. Select app to run
5. Open in your browser `http://localhost:8501/` for gpt or `http://localhost:8500/` for embeddings

## Unix/Linux/Mac with SSH if you want to run it permanent

1. Open a terminal in the project directory.
2. Run the following command to give permission to run nohup:
`chmod +x setup.sh`
4. Run the following command to execute the shell script:
`nohup ./setup.sh`
5. Enter Your Api-Key
6. Select app to run
5. Open in your browser `http://HOSTENAME:8501/` for gpt or `http://HOSTENAME:8500/` for embeddings


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
