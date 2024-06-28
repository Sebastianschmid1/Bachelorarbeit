from openai.types import CreateEmbeddingResponse
from openai import OpenAI
import matplotlib.pyplot as plt
import numpy as np


def get_embedding(
    input_text: str, client: OpenAI, model: str = "text-embedding-3-small"
) -> CreateEmbeddingResponse:
    return client.embeddings.create(
        model=model,
        input=input_text,
        encoding_format="float",
    )


def plot_results(results, line_names, xlim=(0, 20), ylim=(1, 1.7), titel=""):
    colors = plt.cm.viridis(np.linspace(0, 1, 20))
    line_styles = ["-", "--", "-.", ":", "-", "--", "-.", ":", "-", "--"]

    # Plotten der Daten
    plt.figure(figsize=(12, 8), dpi=150)
    for i in range(results.shape[0]):
        plt.plot(
            results[i],
            label=line_names[i],
            color=colors[i],
            linestyle=line_styles[i],
            linewidth=2,
        )
    plt.plot(
        [results[:, index].mean() for index in range(results.shape[1])],
        label="Durchschnitt",
        color="red",
        linestyle="-",
        linewidth=3,
    )
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.legend(loc="lower right")
    plt.xlabel("k", fontsize=12)
    plt.ylabel("Score", fontsize=12)
    plt.title(
        titel,
        fontsize=14,
    )
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
