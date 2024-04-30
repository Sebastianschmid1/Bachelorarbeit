#!/bin/bash

if [ -f ".env" ]; then
    echo "The .env file does not exist. It is created..."
    read -p "Please enter your OPENAI_API_KEY: " OPENAI_API_KEY
    echo "You entered: $OPENAI_API_KEY"
    echo "OPENAI_API_KEY='$OPENAI_API_KEY'" > .env
    echo ".env file was created successfully!"
else
    echo "The .env file already exists."
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
echo "2. gbt"
read -p "Gib deine Wahl ein: " choice

if [ $choice = 1 ]
then
    echo "Starte embeddings app..."
    streamlit run app_doc.py
else
    echo "Starte gpt app..."
    streamlit run app_gpt.py
fi