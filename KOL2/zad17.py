import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import MinMaxScaler
from dataset_script import dataset


if __name__ == '__main__':
    C = int(input().strip())
    P = int(input().strip())

    modified_dataset = []

    for row in dataset:
        features = [float(v) for v in row[:-1]]
        label = row[-1]

        sum = features[0] + features[-1]

        new_row = [sum] + features[1:-1] + [label]
        modified_dataset.append(new_row)

    class_good = [row for row in modified_dataset if row[-1] == "good"]
    class_bad = [row for row in modified_dataset if row[-1] == 'bad']

    idx_good = int(len(class_good) * (P / 100))
    idx_bad = int(len(class_bad) * (P / 100))



    if C == 0:
        train_good = class_good[:idx_good]
        test_good = class_good[idx_good:]

        train_bad = class_bad[:idx_bad]
        test_bad = class_bad[idx_bad:]
    elif C == 1:
        split_good = int(len(class_good) * ((100 - P) / 100))
        split_bad = int(len(class_bad) * ((100 - P) / 100))

        test_good = class_good[:split_good]
        train_good = class_good[split_good:]

        test_bad = class_bad[:split_bad]
        train_bad = class_bad[split_bad:]

    train_data = train_good + train_bad
    test_data = test_good + test_bad

    def split_data(data):
        X = [[float(v) for v in row[:-1]] for row in data]
        Y = [row[-1] for row in data]
        return X, Y

    train_X, train_Y = split_data(train_data)
    test_X, test_Y = split_data(test_data)

    # Klasifikacija bez skaliranje
    model1 = GaussianNB()
    model1.fit(train_X, train_Y)
    pred1 = model1.predict(test_X)
    acc1 = accuracy_score(test_Y, pred1)

    # Klasifikacija so skaliranje
    scaler = MinMaxScaler(feature_range=(-1, 1))
    train_X_s = scaler.fit_transform(train_X)
    test_X_s = scaler.transform(test_X)

    model2 = GaussianNB()
    model2.fit(train_X_s, train_Y)
    pred2 = model2.predict(test_X_s)
    acc2 = accuracy_score(test_Y, pred2)

    print(f"Tochnost so zbir na koloni: {acc1}")
    print(f"Tochnost so zbir na koloni i skaliranje: {acc2}")
