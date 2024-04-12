
import re
from pathlib import Path

import pandas as pd


# PARSE LOG FILES FROM KAGGLE
def parse_log(log_file_path):
    # Define a pattern to find trial_id and values, and a pattern for parameters.
    trial_pattern = re.compile(r"Trial (\d+) finished with value: ([\d.]+)")
    params_pattern = re.compile(r"'(\w+)': (\d+)")
    
    # Prepare storage for the extracted data
    data = {
        'trial_id': [],
        'value': [],
        'n_pivots': [],
        'n_clusters': [],
        'n_lookback': [],
        'hold_period': []
    }
    
    # Open and read the log file
    with open(log_file_path, 'r') as file:
        for line in file:
            # Find trial data
            trial_match = trial_pattern.search(line)
            if trial_match:
                trial_id, value = trial_match.groups()
                data['trial_id'].append(int(trial_id))
                data['value'].append(float(value))
                
                # Find and store parameters
                params = params_pattern.findall(line)
                for param, val in params:
                    if param in data:
                        data[param].append(int(val))

                # Ensure all parameters have values
                for key in ['n_pivots', 'n_clusters', 'n_lookback', 'hold_period']:
                    if len(data[key]) < len(data['trial_id']):
                        data[key].append(None)  # Append None for missing parameters
            
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    # Usage
    log_file_path = Path.cwd() / 'log_params_bayesian.txt'
    df = parse_log(log_file_path)
    print(df)