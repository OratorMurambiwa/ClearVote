"""CPU embedding smoke checks with public synthetic text, not quality benchmarks."""

import json
import platform
import resource
import time
from importlib.metadata import version

import numpy as np
import torch
from huggingface_hub import model_info
from sentence_transformers import SentenceTransformer


def run_checks():
    """Resolve exact revisions, load shortlisted embeddings and check output shapes."""
    torch.set_num_threads(2)
    results = {"python": platform.python_version(), "threads": 2,
               "packages": {name: version(name) for name in
                            ("torch", "transformers", "sentence-transformers")},
               "models": []}
    candidates = [
        ("sentence-transformers/all-MiniLM-L6-v2", "", ""),
        ("intfloat/e5-small-v2", "query: ", "passage: "),
        ("BAAI/bge-small-en-v1.5",
         "Represent this sentence for searching relevant passages: ", ""),
    ]
    for model_id, query_prefix, passage_prefix in candidates:
        row = {"model": model_id}
        started = time.perf_counter()
        try:
            revision = model_info(model_id).sha
            row["revision"] = revision
            model = SentenceTransformer(model_id, revision=revision, device="cpu")
            row["load_seconds_including_download"] = round(time.perf_counter() - started, 3)
            texts = [query_prefix + "The council approved a budget.",
                     passage_prefix + "The council voted to approve its budget."]
            started = time.perf_counter()
            vectors = model.encode(texts, normalize_embeddings=True)
            assert vectors.shape[0] == 2 and vectors.shape[1] > 0
            assert np.isfinite(vectors).all()
            assert np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=0.001)
            row.update({"status": "passed", "shape": list(vectors.shape),
                        "encode_seconds": round(time.perf_counter() - started, 3),
                        "max_seq_length": model.max_seq_length})
            del model
        except Exception as error:
            # Avoid raw errors that can include request URLs, tokens or response bodies.
            row.update({"status": "failed", "error_type": type(error).__name__})
        row["process_peak_rss_kib_cumulative"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        results["models"].append(row)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    run_checks()
