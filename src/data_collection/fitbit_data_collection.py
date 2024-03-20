import os
import pandas as pd
import json

df_dict = {}
data_directory = '../../data/raw/'
path_dict = {
    'profile': 'Profile.csv',
    'rr': 'breath/rr/rr_summary/',
    'vo2_max': 'breath/demographic_vo2max/',
    'ox_var': 'breath/oxygen_variation/',
    'spo2_daily': 'breath/spo2/daily_spo2/',
    'spo2_intraday': 'breath/spo2/minute_spo2/',
    'afib_ecg': 'heart/afib_ecg/',
    'hr': 'heart/hr/',
    'hrv_summary': 'heart/hrv/hrv_summary/',
    'hrv_histogram': 'heart/hrv/hrv_histogram/',
    'hrv_details': 'heart/hrv/hrv_details/',
    'time_in_hr_zones': 'heart/time_in_hr_zones/',
    'sleep_profile': 'sleep/Sleep Profile.csv',
    'sleep_score': 'sleep/sleep_score.csv',
    'sleep_json': 'sleep/json/',
    'stress': 'stress/Stress Score.csv',
    'weight': 'weight/'
}


# ================================ FUNCTIONS ================================
# noinspection PyTypeChecker
def read_file(filename, directory=None):
    filepath = os.path.join(directory, filename) if directory else filename
    if filename.endswith('.csv'):
        temp = pd.read_csv(filepath)
    elif filename.endswith('.json'):
        with open(filepath, 'r') as file:
            data = json.load(file)
            temp = pd.json_normalize(data)
    else:
        temp = None
    return temp


def fitbit_data_handler(path_string):
    # If path is a directory, read all files in the directory
    if os.path.isdir(path_string):
        directory = path_string
        dfs = []
        for filename in os.listdir(directory):
            temp = read_file(filename, directory)
            dfs.append(temp)
        dfs = pd.concat(dfs, ignore_index=True)
        return dfs
    else:  # Otherwise, just operate on one file
        return read_file(filename=path_string)


# ============================== PROCESS FILES ==============================
for name, path in path_dict.items():
    whole_path = os.path.join(data_directory, path)
    df_dict[name] = fitbit_data_handler(whole_path)

# ================================ SAVE FILES ===============================
output_directory = '../../data/processed/csv/'
for name, df in df_dict.items():
    df.to_csv(f'{output_directory}{name}.csv', index=False)

pd.to_pickle(df_dict, '../../data/processed/pickle/fitbit_data.pkl')
