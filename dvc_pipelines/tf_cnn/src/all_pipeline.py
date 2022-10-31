import os
import yaml
import pickle
import numpy as np
import json
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    adjusted_rand_score
)
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization

pipeline_path = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))

# ################################### Prepare ###################################
# read params
params = yaml.safe_load(open(os.path.join(pipeline_path, 'params.yaml')))

# fetch data
(X_treinamento, y_treinamento), (X_test, y_test) = mnist.load_data()

# ################################### Feturize ###################################
previsores_treinamento = X_treinamento.reshape(X_treinamento.shape[0], 28, 28, 1)
previsores_teste = X_test.reshape(X_test.shape[0], 28, 28, 1)
previsores_treinamento = previsores_treinamento.astype('float32')
previsores_teste = previsores_teste.astype('float32')

previsores_treinamento /= 255
previsores_teste /= 255

NRO_LABELS = len(set(y_treinamento))
classe_treinamento = to_categorical(y_treinamento, NRO_LABELS)  # Converter para dammy, nro de elementos
classe_teste = to_categorical(y_test, NRO_LABELS)

# ################################### Train ###################################
classificador = Sequential()
classificador.add(Conv2D(32, (3, 3),
                         input_shape=(28, 28, 1),
                         activation='relu'))
classificador.add(BatchNormalization())
classificador.add(MaxPooling2D(pool_size=(2, 2)))

classificador.add(Conv2D(32, (3, 3), activation='relu'))
classificador.add(BatchNormalization())
classificador.add(MaxPooling2D(pool_size=(2, 2)))

classificador.add(Flatten())

classificador.add(Dense(units=128, activation='relu'))
classificador.add(Dropout(0.2))
classificador.add(Dense(units=128, activation='relu'))
classificador.add(Dropout(0.2))
classificador.add(Dense(units=NRO_LABELS,
                        activation='softmax'))
classificador.compile(loss='categorical_crossentropy',
                      optimizer='adam', metrics=['accuracy'])

classificador.fit(previsores_treinamento, classe_treinamento,
                  batch_size=params['train']['params']['batch_size'],
                  epochs=params['train']['params']['epochs'],
                  validation_data=(previsores_teste, classe_teste))


# save the models
model_filename = params['train']['model_filename']
with open(model_filename, 'wb') as f:
    pickle.dump(classificador, f)

# ################################### Evaluate ###################################
# make predictions
predictions_by_class = classificador.predict(X_test)
predictions = np.argmax(predictions_by_class, axis=1)

# generate scores
metrics = {
    'accuracy': accuracy_score(y_test, predictions),
    'balanced_accuracy': balanced_accuracy_score(y_test, predictions),
    'adjusted_rand_score': adjusted_rand_score(y_test, predictions),
}

# save scores
scores_file = params['evaluate']['scores_file']
with open(scores_file, 'w') as f:
    json.dump(metrics, f)

pd.DataFrame({'predicted': list(predictions), 'real': list(y_test)}).to_csv(params['evaluate']['plots_file'], index=False)

# dvc run -n all_pipeline -p prepare.test_size,prepare.random_state,train.params.random_state,train.params.batch_size,train.params.epochs,train.model_filename,evaluate.scores_file,evaluate.plots_file -d src/all_pipeline.py -o models/model.pkl --metrics-no-cache metrics/scores.json python3 src/all_pipeline.py
# dvc plots show metrics/cm_classes.csv --template confusion -x real -y predicted


