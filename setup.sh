#!/bin/bash

if [ -f ".env" ]; then
    echo "The .env file already exists."
else
    echo "The .env file does not exist. It is created..."
    read -p "Please enter your OPENAI_API_KEY: " OPENAI_API_KEY
    echo "You entered: $OPENAI_API_KEY"
    echo "OPENAI_API_KEY='$OPENAI_API_KEY'" > .env
    echo ".env file was created successfully!"
fi

if [ ! -d "venv" ]; then
    echo "Python venv does not exist. Creating one..."
    python3 -m venv venv
    echo "Activating venv..."
    source venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

if [ -d "venv" ]; then
    echo "Activating venv..."
    source venv/bin/activate
fi

echo "Wähle ein Script zum Ausführen:"
echo "1. embeddings"
echo "2. gpt"
read -p "Gib deine Wahl ein: " choice

if [ $choice = 1 ]
then
    echo "Starte embeddings app..."
    streamlit run apps/app_doc.py --server.port 8500
elif [ $choice = 2 ]
then
    echo "Starte gpt app..."
    streamlit run apps/app_gpt.py --server.port 8501
elif [ $choice = 3 ]
then
    echo "Starte PDF summery app..."
    streamlit run apps/app_doc_summery.py --server.port 8500
else
    echo "wrong input"
fi