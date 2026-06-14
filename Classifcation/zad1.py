import os
import warnings

from sklearn.naive_bayes import GaussianNB

os.environ['OPENBLAS_NUM_THREADS'] = '1'
warnings.filterwarnings("ignore")

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

dataset = [
    [3000, 0.001, 0.1, 15, 'Dwarf'],
    [3200, 0.002, 0.12, 14, 'Dwarf'],
    [3500, 0.003, 0.15, 13, 'Dwarf'],
    [2900, 0.001, 0.09, 16, 'Dwarf'],
    [5000, 0.5, 0.8, 5, 'Dwarf'],
    [5500, 0.8, 0.9, 4, 'Dwarf'],
    [10000, 100, 15, -2, 'Giant'],
    [12000, 150, 20, -3, 'Giant'],
    [9000, 90, 12, -1, 'Giant'],
    [15000, 300, 30, -4, 'Giant'],
    [8000, 80, 10, 0, 'Giant'],
    [11000, 120, 18, -2.5, 'Giant'],
    [20000, 10000, 500, -8, 'Supergiant'],
    [25000, 20000, 800, -9, 'Supergiant'],
    [18000, 8000, 400, -7, 'Supergiant'],
    [30000, 50000, 1200, -10, 'Supergiant'],
    [22000, 15000, 600, -8.5, 'Supergiant'],
    [28000, 40000, 1000, -9.5, 'Supergiant']
]

if __name__ == '__main__':
    N = int(input().strip())
    P = float(input().strip())

    # PRO MODDIFICIRIMAE
    modify_dataset = []
    for row in dataset:
        temp = row[0]
        lum = row[1]
        radius = row[2]
        magnitude = row[3]
        lable = row[4]

        sum = lum * radius

        new_row = [temp, sum, magnitude, lable]
        modify_dataset.append(new_row)

    # POSLED SPLIT ZA SEKOJA OD 3 KLASI
    class_dwarf = [row for row in modify_dataset if row[-1] == 'Dwarf']
    class_giant = [row for row in modify_dataset if row[-1] == 'Giant']
    class_sgiant = [row for row in modify_dataset if row[-1] == 'Supergiant']

    def split_dataset(data, p):
        split_idx = int(len(data) * (p / 100))
        train_data = data[:split_idx]
        test_data = data[split_idx:]
        return train_data, test_data

    train_D, test_D = split_dataset(class_dwarf, P)
    train_G, test_G = split_dataset(class_giant, P)
    train_SG, test_SG = split_dataset(class_sgiant, P)

    final_training_data = train_D + train_G + train_SG
    final_test_data = test_D + test_G + test_SG

    train_X = [row[:-1] for row in final_training_data]
    train_Y = [row[-1] for row in final_training_data]

    test_X = [row[:-1] for row in final_test_data]
    test_Y = [row[-1] for row in final_test_data]

    # GI SKALIRAME
    scaler = StandardScaler()
    train_X_s = scaler.fit_transform(train_X)
    test_X_s = scaler.transform(test_X)

    # PRVBIOT MODEL
    model_rf = RandomForestClassifier(n_estimators=N,criterion='entropy', random_state=0)
    model_rf.fit(train_X_s, train_Y)

    pred_rf = model_rf.predict(test_X_s)
    proba_rf = model_rf.predict_proba(test_X_s)

    # VTORTIO MODEL
    model_nb = GaussianNB()
    model_nb.fit(train_X_s, train_Y)

    pred_nb = model_nb.predict(test_X_s)
    proba_nb = model_nb.predict_proba(test_X_s) #- vrfakja sa mo niza od brojk[0.10, 0.85, 0.05]

    # ANAMBL - AKO DVATA KLASIFIKATORA POTRVRDUVAAT ISTA KLASA

    # 1. ENSEMBLE - BITKA NA VEROJATNOSTI
    # classes_rf = list(model_rf.classes_)
    # classes_nb = list(model_nb.classes_)
    # correct_predictions = 0
    # for i in range(len(test_Y)):
    #     true_label = test_Y[i]
    #     guess_rf = pred_rf[i]
    #     guess_nb = pred_nb[i]
    #
    #     if guess_rf == guess_nb:
    #         correct_predictions += 1
    #     else:
    #         # Trebna da vdime confdicence score
    #         # Za toa go zemame indeksot an klasata so toj prediction
    #         idx_rf = classes_rf.index(guess_rf)
    #         confidence_rf = proba_rf[i][idx_rf]
    #
    #         idx_nb = classes_nb.index(guess_nb)
    #         confidence_nb = proba_nb[i][idx_nb]
    #
    #         if confidence_rf > confidence_nb:
    #             final_guess = guess_nb
    #         else:
    #             final_guess = guess_rf
    #
    #         if final_guess == true_label:
    #             correct_predictions += 1

    # 2.  ENSEMBLE - LOGICAL OR/ AT LEAST ONME
    # correct_predictions = 0
    # for i in range(len(test_Y)):
    #     true_label = test_Y[i]
    #     guess_rf = pred_rf[i]
    #     guess_nb = pred_nb[i]
    #
    #     if guess_nb == true_label or guess_rf == true_label:
    #         correct_predictions += 1
    # acc = correct_predictions / len(test_Y)

    # 3. ENSEMBLE - STRICT AGREEMENT - AKO BAREM EDEN ZGRESHI NE E TOCNO
    # correct_predictions = 0
    # for i in range(len(test_Y)):
    #     true_label = test_Y[i]
    #     guess_rf = pred_rf[i]
    #     guess_nb = pred_nb[i]
    #
    #     if guess_nb == true_label and guess_rf == true_label:
    #         correct_predictions += 1

    # 4. ENSEMBLE - 3 MODEL VOTING SYSTEM
    # correct_predictions = 0
    # for i in range(len(test_Y)):
    #     true_label = test_Y[i]
    #
    #     guesses = [pred_rf[i], pred_nb[i], pred_mlp[i]]
    #     correct_guiesses = guesses.count(true_label)
    #
    #     if correct_guiesses >= 2:
    #         correct_predictions += 1;


    acc_rf = accuracy_score(test_Y, pred_rf)
    acc_nb = accuracy_score(test_Y, pred_nb)
    acc_vote = correct_predictions / len(test_Y)

    print(f"Accuracy with Random Forest: {acc_rf}")
    print(f"Accuracy with Naive Bayes: {acc_nb}")
    print(f"Accuracy with Ensemble: {acc_vote}")
