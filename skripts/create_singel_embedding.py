from openai import OpenAI

client = OpenAI()

input_text = "Bachelorsarbeit"
client.embeddings.create(
    model="text-embedding-ada-002",
    input=input_text,
    encoding_format="float",
)
print(
    "Text:",
    input_text,
    ",Embedding:",
    client.embeddings.create(
        model="text-embedding-ada-002",
        input="Bachelorsarbeit",
        encoding_format="float",
    ),
)
