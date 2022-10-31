import os
import yaml
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

pipeline_path = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))

# read params
params = yaml.safe_load(open(os.path.join(pipeline_path, 'params.yaml')))['prepare']

# create folder to save file
data_path = os.path.join(pipeline_path, 'data', 'prepared')
os.makedirs(data_path, exist_ok=True)

# fetch data
data = load_diabetes()

# split
X_train, X_test, y_train, y_test = train_test_split(
    data.data,
    data.target,
    test_size=params['test_size'],
    random_state=params['random_state']
)

# save
df_train = pd.DataFrame(np.concatenate((X_train,  np.expand_dims(y_train, 1)), axis=1), columns=data.feature_names + ['target'])
df_test = pd.DataFrame(np.concatenate((X_test,  np.expand_dims(y_test, 1)), axis=1), columns=data.feature_names + ['target'])

df_train.to_csv(os.path.join(data_path, 'train.csv'))
df_test.to_csv(os.path.join(data_path, 'test.csv'))

# dvc run -n prepare -p prepare.test_size,prepare.random_state -d src/prepare.py -o data/prepared python3 src/prepare.py

