import sys
import os
import yaml
import importlib
import pickle

# read the command line params
if len(sys.argv) != 3:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write(
        '\tpython3 train.py features-dir-path models-filename\n'
    )
    sys.exit(1)

features_path = sys.argv[1]
model_filename = sys.argv[2]

pipeline_path = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))

# read pipeline params
params = yaml.safe_load(open(os.path.join(pipeline_path, 'params.yaml')))['train']


# load the train features
features_train_pkl = os.path.join(features_path, 'train.pkl')
with open(features_train_pkl, 'rb') as f:
    train_data = pickle.load(f)

X = train_data[:, :-1]
y = train_data[:, -1]

# train the models
model = getattr(
    importlib.import_module(params['import_module']),
    params['name']
)(**params['params'])
model.fit(X, y)

# save the models
with open(model_filename, 'wb') as f:
    pickle.dump(model, f)

# dvc run -n train -p train.import_module,train.name,train.params.n_estimators,train.params.n_jobs,train.params.random_state -d src/train.py -d data/features -o models/model.pkl python3 src/train.py data/features models/model.pkl
# dvc run -n train --force -p train -d src/train.py -d data/features -o models/model.pkl python3 src/train.py data/features models/model.pkl
