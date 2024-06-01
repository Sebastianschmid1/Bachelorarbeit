from openai.types import CreateEmbeddingResponse
from openai import OpenAI


def get_embedding(
    input_text: str, client: OpenAI, model: str = "text-embedding-3-small"
) -> CreateEmbeddingResponse:
    return client.embeddings.create(
        model=model,
        input=input_text,
        encoding_format="float",
    )
