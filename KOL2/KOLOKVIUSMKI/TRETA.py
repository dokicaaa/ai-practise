import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

from dataset_script import dataset


if __name__ == '__main__':
    N = int(input().strip())
    M = int(input().strip())

    split = int(len(dataset) // 3)
    P1 = dataset[:split]
    P2 = dataset[split:2*split]
    P3 = dataset[2*split:]

    steps = [
        (P2 + P3, P1),
        (P1 + P3, P2),
        (P1 + P2, P3)
    ]

    def split_dataset(dataset):
        X = [row[:-1] for row in dataset]
        Y = [row[-1] for row in dataset]
        return X, Y

    # Dve listi za eden i za drugiot klasifiaktor
    acc_rf_list = []
    acc_ensemble_list = []

    for train_data, test_data in steps:
        train_X, train_Y = split_dataset(train_data)
        test_X, test_Y = split_dataset(test_data)

        # Prv random forest klassifkator
        rf = RandomForestClassifier(n_estimators=N, criterion='gini', random_state=0)
        rf.fit(train_X, train_Y)
        pred_rf = rf.predict(test_X)
        acc_rf = accuracy_score(test_Y, pred_rf)
        acc_rf_list.append(acc_rf)

        # Kolkecija od klasifikatori
        nb = GaussianNB()
        dt = DecisionTreeClassifier(criterion='gini', max_depth=M, random_state=0)

        nb.fit(train_X, train_Y)
        dt.fit(train_X, train_Y)

        pred_nb = nb.predict(test_X)
        pred_dt = dt.predict(test_X)

        proba_nb = nb.predict_proba(test_X)
        proba_dt = dt.predict_proba(test_X)

        classes = list(nb.classes_)

        correct_ensemble = 0
        for i in range(len(test_Y)):
            true_label = test_Y[i]  # fix: was train_Y[i]
            guess_nb = pred_nb[i]
            guess_dt = pred_dt[i]

            if guess_nb == guess_dt:
                final_pred = guess_nb
            else:
                # each classifier's confidence in its own prediction
                prob_nb = proba_nb[i][classes.index(guess_nb)]
                prob_dt = proba_dt[i][classes.index(guess_dt)]
                if prob_nb >= prob_dt:
                    final_pred = guess_nb
                else:
                    final_pred = guess_dt

            if final_pred == true_label:
                correct_ensemble += 1

        acc_ensemble_list.append(correct_ensemble / len(test_Y))

        final_rf_acc = sum(acc_rf_list) / 3.0
        final_acc_ensamble = sum(acc_ensemble_list) / 3.0

    print(f"Accuracy with random forest: {final_rf_acc}")
    print(f"Accuracy with naive bayes and decision tree: {final_acc_ensamble}")

