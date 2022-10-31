import sys
import os

import pandas as pd
from sklearn.metrics import (
    get_scorer,
    SCORERS,
)
import pickle
import json
import yaml
import numpy as np
from datetime import date

# read command line parameters
if len(sys.argv) != 5:
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write(
        '\tpython3 evaluate.py models-filename features-dir-path scores-filename\
                plots-filename\n'
    )
    sys.exit(1)

model_filename = sys.argv[1]
features_path = sys.argv[2]
test_features_file = os.path.join(os.path.join(features_path, 'test.pkl'))
scores_file = sys.argv[3]
plots_file = sys.argv[4]

pipeline_path = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))

# read pipeline params
params = yaml.safe_load(open(os.path.join(pipeline_path, 'params.yaml')))['evaluate']

# load features
with open(test_features_file, 'rb') as f:
    test_features = pickle.load(f)

X_test = test_features[:, :-1]
y_test = test_features[:, -1]

# load models
with open(model_filename, 'rb') as f:
    model = pickle.load(f)

# make predictions
predictions_by_class = model.predict_proba(X_test)
predictions = np.argmax(predictions_by_class, axis=1)

# generate scores
metrics = {
    'ref_date': date.today().strftime('%Y-%m-%d')
}
params['metrics'] = [f for f in params['metrics'] if f in list(SCORERS.keys())]
for m in params['metrics']:
    m_result = get_scorer(m)(model, X_test, y_test)
    metrics[m] = float(m_result)

# save scores
with open(scores_file, 'w') as f:
    json.dump(metrics, f)

pd.DataFrame({'predicted': list(predictions), 'real': list(y_test)}).to_csv(plots_file, index=False)

# dvc run -n evaluate -p evaluate.metrics -d src/evaluate.py -d models/model.pkl -d data/features --metrics-no-cache metrics/scores.json python3 src/evaluate.py models/model.pkl data/features metrics/scores.json metrics/cm_classes.csv
# dvc plots show cm_classes.csv --template confusion -x real -y predicted