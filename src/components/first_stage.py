import argparse
import json
import os
import time

from components.datasets import datasets_cls
from components.eval import accumulate_results, eval_bm25
from components.index import Index
from components.settings import dataset_settings_cls
from tqdm.auto import tqdm


def first_stage(dataset_name):
    index = Index()
    args = dataset_settings_cls[dataset_name]()

    dataset = datasets_cls[args.name](
        corpus_path=args.corpus_path,
        topics_path=args.topics_path,
        qrels_path=args.qrels_path,
        load_corpus=not index.index_exists(index=args.name),
        remove_topics_with_few_annotations=False,
    )

    if not index.index_exists(index=args.name):
        index.index_corpus(
            index=args.name, corpus=dataset.corpus, corpus_size=dataset.corpus_size
        )

    bm25_results, bm25_docs, _ = index.bm25_query(
        index=args.name, topics=dataset.topics, size=args.bm25_size
    )
    bm25_eval = eval_bm25(dataset.qrels, bm25_results)
    bm25_eval_acc = accumulate_results(bm25_eval)

    dataset_path = os.path.join(args.data_path, str(args.bm25_size))
    os.makedirs(dataset_path, exist_ok=True)
    for obj, name in zip(
        [
            bm25_results,
            bm25_docs,
            bm25_eval,
            bm25_eval_acc,
        ],
        [
            "full_bm25_results",
            "full_bm25_docs",
            "full_bm25_eval",
            "full_bm25_eval_acc",
        ],
    ):
        with open(os.path.join(dataset_path, f"{name}.json"), "w") as fh:
            json.dump(obj, fh, indent=4)
