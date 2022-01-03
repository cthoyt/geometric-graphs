# -*- coding: utf-8 -*-

"""Benchmark CLI."""

import json
from hashlib import md5

import click
import matplotlib.pyplot as plt
import pandas as pd
import pystow
import seaborn as sns
from pykeen.models import model_resolver
from pykeen.pipeline import pipeline
from tqdm import tqdm, trange
from tqdm.contrib.logging import tqdm_logging_redirect

from .api import generator_resolver

__all__ = [
    "benchmark",
]

DEFAULT_METRIC = "adjusted_arithmetic_mean_rank_index"
DEFAULT_TRIALS = 13
MODULE = pystow.module("pykeen", "geobenchmark")
experiments = [
    {
        "generator": "SquareGrid2D",
        "generator_kwargs": {"rows": 5, "columns": 5},
        "inverse": False,
    },
    {
        "generator": "SquareGrid2D",
        "generator_kwargs": {"rows": 30, "columns": 30},
        "inverse": True,
    },
    {
        "generator": "SquareGrid2D",
        "generator_kwargs": {"rows": 30, "columns": 30},
        "inverse": False,
    },
    {
        "generator": "SquareGrid2D",
        "generator_kwargs": {"rows": 45, "columns": 45},
        "inverse": True,
    },
]
models = [
    "TransE",
    "TransD",
    "PairRE",
    "FixedModel",
]


def get_digest(experiment, length: int = 8) -> str:
    """Get a hexdigest for a dictionary of a given length."""
    return md5(json.dumps(experiment, sort_keys=True).encode()).hexdigest()[:length]  # noqa:S303


def run(
    experiment,
    *,
    trials: int = DEFAULT_TRIALS,
    device: str = "cpu",
    force: bool = False,
    model: str = "PairRE",
    metric: str = DEFAULT_METRIC,
):
    """Run a single benchmark experiment."""
    digest = get_digest(experiment)
    model = model_resolver.normalize(model)
    submodule = MODULE.submodule(digest, model)

    generator = generator_resolver.make_from_kwargs(experiment, "generator")
    factory = generator.to_pykeen(create_inverse_triples=experiment["inverse"])
    rv = []
    for trial in trange(trials, desc="Trials"):
        trial_directory = submodule.join("trials", f"{trial:03}")
        results_path = trial_directory.joinpath("results.json")
        if results_path.is_file() and not force:
            rv.append((digest, json.loads(results_path.read_text())))
            continue
        train, test, valid = factory.split([0.90, 0.05, 0.05], random_state=trial)
        res = pipeline(
            training=train,
            testing=test,
            validation=valid,
            model=model,
            stopper="early",
            stopper_kwargs=dict(metric=metric),
            epochs=200,
            random_seed=trial,
            device=device,
            training_loop_kwargs=dict(automatic_memory_optimization=False),
            training_kwargs=dict(batch_size=2048, checkpoint_name=None),
            evaluator_kwargs=dict(automatic_memory_optimization=False, batch_size=2048),
            evaluation_kwargs=dict(batch_size=2048),
        )
        res.save_to_directory(
            trial_directory,
            save_metadata=False,
        )
        rv.append((digest, res._get_results()))
    return rv


def run_many(x, trials, device, force, metric):
    """Run a group of benchmark experiments."""
    rows = []
    experiment_it = tqdm(x, desc="Experiments")
    for experiment in experiment_it:
        experiment_it.set_postfix(type=experiment["generator"])
        model_it = tqdm(models, desc="Models")
        for model in model_it:
            model_it.set_postfix(model=model)
            results = run(
                experiment=experiment,
                model=model,
                trials=trials,
                device=device,
                force=force,
                metric=metric,
            )
            for digest, result in results:
                rows.append(
                    (
                        digest,
                        model_resolver.normalize(model),
                        round(result["metrics"][metric]["both"]["realistic"], 3),
                    )
                )

    df = pd.DataFrame(rows, columns=["digest", "model", metric])
    df.to_csv(MODULE.join(name="results.tsv"), sep="\t", index=False)

    fig, ax = plt.subplots(figsize=(9, 4))
    sns.boxplot(data=df, x="digest", hue="model", y=metric, ax=ax)
    fig.savefig(MODULE.join(name="chart.svg"))

    return rows


@click.command()
@click.option("--trials", type=int, default=DEFAULT_TRIALS, show_default=True)
@click.option("--device", default="cpu", show_default=True)
@click.option("--metric", default=DEFAULT_METRIC, show_default=True)
@click.option("-f", "--force", is_flag=True)
def benchmark(trials: int, device: str, force: bool, metric: str):
    """Run PyKEEN benchmark."""
    with tqdm_logging_redirect():
        run_many(experiments, trials=trials, device=device, force=force, metric=metric)


if __name__ == "__main__":
    benchmark()
