@echo off
setlocal EnableDelayedExpansion
if NOT exist ".env" (
    echo The .env file does not exist. It is created...
    set /p "OPENAI_API_KEY=Please enter your OPENAI_API_KEY:"
    echo You entered: !OPENAI_API_KEY!
    echo OPENAI_API_KEY="!OPENAI_API_KEY!">.env
    echo .env file was created successfully!
) else (
    echo The .env file already exists.
)

IF NOT EXIST venv (
    echo Python venv does not exist. Creating one...
    py -m venv venv
    echo Activating venv...
    call venv\Scripts\activate

    echo Installing requirements...
    pip install -r requirements.txt
)
IF  EXIST venv (
    echo Activating venv...
    call venv\Scripts\activate
)

echo Choose a script to run:
echo 1. embeddings 1
echo 2. gbt 2
set /p choice="Enter your choice: "
if %choice%==1 (
    echo Starting embeddings app...
    streamlit run app_doc.py
) else (
    
    echo Starting gpt app...
    streamlit run app_gpt.py
)
