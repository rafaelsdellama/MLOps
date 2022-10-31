import sys
import os
import pandas as pd
import pickle

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


def encode_targets(df_1, df_2):
    targets_train = list(df_1["target"].unique())
    targets_test = list(df_2["target"].unique())

    unique_targets = list(sorted(set(targets_train + targets_test)))
    class_to_id = {
        l: i for i, l in enumerate(unique_targets)
    }

    df_1["target"] = [class_to_id[l] for l in df_1["target"]]
    df_2["target"] = [class_to_id[l] for l in df_2["target"]]


def save_pkl(df, filename):
    output_file = os.path.join(features_path, filename)
    output = df.values

    with open(output_file, 'wb') as f:
        pickle.dump(output, f)


# we need to encode both train and test target
encode_targets(df_train, df_test)

# save data to pickle (appending the labels column)
save_pkl(df_train, 'train.pkl')
save_pkl(df_test, 'test.pkl')

# dvc run -n featurize -d src/featurize.py -d data/prepared -o data/features python3 src/featurize.py data/prepared data/features