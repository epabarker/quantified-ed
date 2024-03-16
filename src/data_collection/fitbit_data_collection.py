import os
import pandas as pd
import json

df_dict = {}
path_dict = {
    'profile': '../data/raw/Profile.csv',
    'respiratory_rate': '../data/raw/breath/rr/rr_summary/',
    'vo2_max': '../data/raw/breath/demographic_vo2max/',
    'oxygen_variation': '../data/raw/breath/oxygen_variation/',
    'spo2_daily': '../data/raw/breath/spo2/daily_spo2/',
    'spo2_intraday': '../data/raw/breath/spo2/minute_spo2/',
    'afib_ecg': '../data/raw/heart/afib_ecg/',
    'heart_rate': '../data/raw/heart/hr/',
    'hrv_summary': '../data/raw/heart/hrv/hrv_summary/',
    'hrv_histogram': '../data/raw/heart/hrv/hrv_histogram/',
    'hrv_details': '../data/raw/heart/hrv/hrv_details/',
    'time_in_hr_zones': '../data/raw/heart/time_in_hr_zones/',
    'sleep_profile': '../data/raw/sleep/Sleep Profile.csv',
    'sleep_score': '../data/raw/sleep/sleep_score.csv',
    'sleep_json': '../data/raw/sleep/json/',
    'stress': '../data/raw/stress/Stress Score.csv',
    'weight': '../data/raw/weight/'
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
    df_dict[name] = fitbit_data_handler(path)

# ================================ SAVE FILES ===============================
output_directory = '../data/processed/'
for name, df in df_dict.items():
    df.to_csv(f'{output_directory}{name}.csv', index=False)
