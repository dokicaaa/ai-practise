import os

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

os.environ['OPENBLAS_NUM_THREADS'] = '1'

from dataset_script import dataset

if __name__ == '__main__':
    P = int(input().strip())
    C = input().strip()
    L = int(input().strip())

    data = np.array(dataset)
    X = data[:, :-1]
    Y = data[:, -1]

    split_idx = int(len(data) * (P / 100))
    X_train = X[:split_idx]
    Y_train = Y[:split_idx]

    X_test = X[split_idx:]
    Y_test = Y[split_idx:]

    dt = DecisionTreeClassifier(criterion=C, max_leaf_nodes=L, random_state=0)
    dt.fit(X_train, Y_train)
    predOrg = dt.predict(X_test)
    accOrg = accuracy_score(Y_test, predOrg)

    # ONE VS REST ENSSALBMLE
    classes = ['Perch', 'Roach', 'Bream']
    models = {}

    for cls in classes:
        # Za sekoja clasa, ako posledna kolona e ednakva so klasata togash e tocno
        Y_train_bin = [1 if y == cls else 0 for y in Y_train]

        dt_bin = DecisionTreeClassifier(criterion=C, max_leaf_nodes=L, random_state=0)
        dt_bin.fit(X_train, Y_train_bin)
        models[cls] = dt_bin

    correct_votes = 0

    for i in range(len(X_test)):
        sample_x = [X_test[i]]
        true_y = Y_test[i]

        predicted_classes = []
        for cls in classes:
            pred_bin = models[cls].predict(sample_x)[0]
            if pred_bin == 1:
                predicted_classes.append(cls)

        if len(predicted_classes) == 1 and predicted_classes[0] == true_y:
            correct_votes += 1

    acc_vote = correct_votes / float(len(X_test))

    print(f"Tochnost so originalniot klasifikator: {accOrg}")
    print(f"Tochnost so kolekcija od klasifikatori: {acc_vote}")


