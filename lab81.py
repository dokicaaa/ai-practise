import os
import numpy as np
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from submission_script import *
from dataset_script import dataset
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


# Ova e primerok od podatochnoto mnozestvo, za treniranje/evaluacija koristete ja
# importiranata promenliva dataset
dataset_sample = [[180.0, 23.6, 25.2, 27.9, 25.4, 14.0, 'Roach'],
                  [12.2, 11.5, 12.2, 13.4, 15.6, 10.4, 'Smelt'],
                  [135.0, 20.0, 22.0, 23.5, 25.0, 15.0, 'Perch'],
                  [1600.0, 56.0, 60.0, 64.0, 15.0, 9.6, 'Pike'],
                  [120.0, 20.0, 22.0, 23.5, 26.0, 14.5, 'Perch']]

if __name__ == '__main__':
    col_index = int(input())
    num_neurons = int(input())
    new_sample = list(map(float, input().split()))

    data = np.array(dataset, dtype=object)

    X = np.delete(data[:, :-1].astype(float), col_index, axis=1)
    Y = data[:, -1]

    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, train_size=0.8, shuffle=False)

    classifier = MLPClassifier(hidden_layer_sizes=(num_neurons,), max_iter=500, random_state=0)
    classifier.fit(train_X, train_Y)

    predictions = classifier.predict(test_X)
    accuracy = accuracy_score(test_Y, predictions)

    new_sample_arr = np.array([new_sample])
    new_sample_final = np.delete(new_sample_arr, col_index, axis=1)

    predicted_class = classifier.predict(new_sample_final)[0]
    probabilities = classifier.predict_proba(new_sample_final)[0]

    print(f"Tochnost: {accuracy}")
    print(f"Predvidena klasa: {predicted_class}")
    print(f"Verojatnosti: {list(probabilities)}")
