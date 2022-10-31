import sys
import os
import pandas as pd
import pickle


def save_pkl(df, filename):
    output_file = os.path.join(features_path, filename)
    output = df.values

    with open(output_file, 'wb') as f:
        pickle.dump(output, f)


# read command line params
if len(sys.argv) != 3:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write(
        '\tpython featurize.py data-dir-path features-dir-path\n'
    )
    sys.exit(1)

data_path = sys.argv[1]
features_path = sys.argv[2]

os.makedirs(features_path, exist_ok=True)

# read the data from file
df_train = pd.read_csv(os.path.join(data_path, 'train.csv'))
df_test = pd.read_csv(os.path.join(data_path, 'test.csv'))

# save data to pickle (appending the labels column)
save_pkl(df_train, 'train.pkl')
save_pkl(df_test, 'test.pkl')

# dvc run -n featurize -d src/featurize.py -d data/prepared -o data/features python3 src/featurize.py data/prepared data/features