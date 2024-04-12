# Import Necessary Libraries, Define the parameters
from pathlib import Path

import numpy as np
import optuna
import pandas as pd
from quantminer import Miner

data_dir = Path.cwd()

# Read Price Data
data_path = data_dir / 'eur_h1.parquet'
raw_data = pd.read_parquet(data_path)

# Clean the data
data = raw_data.copy()
data = data.dropna()

# Feature Engineering
data['returns'] = data['close'].diff().fillna(0)
data['returns+1'] = data['returns'].shift(-1)

# Prepare the training data
train_daterange_start = 2010
train_daterange_end = 2021

train_data = data[(data.index.year >= train_daterange_start) & (data.index.year <= train_daterange_end)]['close']
train_data = np.array(train_data)



# Functions for Optuna Parameter Sensitivity test
def run_strategy(n_pivots, n_clusters, n_lookback, hold_period):

    data = np.array(train_data)

    # Initialize the model
    miner = Miner(
        n_lookback=n_lookback,
        n_pivots=n_pivots,
        hold_period=hold_period,
        n_clusters = n_clusters,
    )
    
    # Fit the model
    return miner.fit(data)


def objective(trial):
    n_pivots = trial.suggest_int('n_pivots', 3, 8)
    n_clusters = trial.suggest_int('n_clusters', 3, 16)
    n_lookback = trial.suggest_int('n_lookback', 8, 120)
    hold_period = trial.suggest_int('hold_period', 1, 24)
    
    UPI = run_strategy(n_pivots, n_clusters, n_lookback, hold_period) # Ulcer Performance Index
    return UPI 


def optimize_trading_params():
    search_space = {
        'n_pivots': [int(x) for x in np.arange(3, 6)],
        'n_clusters': [int(x) for x in np.arange(16, 24)],
        'n_lookback': [int(x) for x in np.arange(8, 26)],
        'hold_period': [int(x) for x in np.arange(1, 12)]
    }
    sampler = optuna.samplers.GridSampler(search_space)
    study = optuna.create_study(direction='maximize', sampler=sampler)
    study.optimize(objective)  # Total combinations of parameters

    print("Best parameters: ", study.best_params)
    print("Best value (metric): ", study.best_value)
    return study


def compile_results(study):
    results = []
    for trial in study.trials:
        params:dict = trial.params
        params.update(
            martin=trial.value,
            state=trial.state
        )
        results.append(params)

    results_df = pd.DataFrame(results)
    results_df.to_parquet(Path.cwd() / 'results.parquet')
    return results_df

# Execute the optimization
compile_results(optimize_trading_params())

# [1] 6669