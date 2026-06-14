import os
import warnings
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

from dataset_script_anomaly import dataset


if __name__ == '__main__':
    C = int(input().strip())
    N = int(input().strip())
    S = int(input().strip())


    #Vadime nivo na PM 10, ako e pogolem od 50 dodavame y kolona so viosko, spotroivon nisko
    modified_dataset = []
    for row in dataset:
        features = [float(val) for val in row[:-1]]

        pm10 = float(row[-1])

        if pm10 > 50:
            label = 'visoko'
        elif pm10 <= 50:
            label = 'nisko'

        new_row = features + [label]
        modified_dataset.append(new_row)

    # Gradime finalen dateset
    def split_dataset(dataset):
        idx = int(len(dataset) * 0.70)

        # 1. Прво ги делиме редовите на тренинг и тест
        train_data = dataset[:idx]
        test_data = dataset[idx:]

        train_X = [row[:-1] for row in train_data]
        train_Y = [row[-1] for row in train_data]

        test_X = [row[:-1] for row in test_data]
        test_Y = [row[-1] for row in test_data]

        return train_X, train_Y, test_X, test_Y

    # Delime na treniranje i test
    train_X, train_Y, test_X, test_Y = split_dataset(modified_dataset)
    # Treniranje originalen dataset

    model = MLPClassifier(hidden_layer_sizes=(50,), activation='relu', learning_rate_init=0.001,max_iter=25, random_state=0)
    model.fit(train_X, train_Y)

    pred_org = model.predict(test_X)
    acc_org = accuracy_score(test_Y, pred_org)

    dataset_no_anomalies = []
    for row in modified_dataset:
        features = row[:-1]
        label = row[-1]

        co2 = features[3]
        no2 = features[4]
        so2 = features[5]

        if co2 > C:
            co2 = C
        if no2 > N:
            no2 = N
        if so2 > S:
            so2 = S

        new_row = features[:3] + [co2, no2, so2, features[6], [label]]
        dataset_no_anomalies.append(new_row)

    # Ucenje na nov model so izramneni vrednosti, akmo C02, N02, S02 za
    train_X_a, train_Y_a, test_X_a, test_Y_a = split_dataset(dataset_no_anomalies)
    model.fit(train_X_a, train_Y_a)
    pred_anomalies = model.predict(test_X_a)
    acc_anomalies = accuracy_score(test_Y_a, pred_anomalies)

    # Ucenje na uste eden model so skalirani podatoci.
    scaler = StandardScaler()
    train_X_s = scaler.fit_transform(train_X)
    test_X_s = scaler.transform(test_X)

    model.fit(train_X_s, train_Y)
    pred_org_scaled = model.predict(test_X_s)
    acc_org_scaled = accuracy_score(test_Y, pred_org_scaled)

    # UCenje uste eden model so filtriran i skaliran
    train_X_a_s = scaler.fit_transform(train_X_a)
    test_X_a_s = scaler.transform(test_X_a)

    model.fit(train_X_a_s, train_Y_a)
    pred_anom_scaled = model.predict(test_X_a_s)
    acc_anom_scaled = accuracy_score(test_Y_a, pred_anom_scaled)

    print(f"Accuracy with:")
    print(f"The original dataset: {acc_org}")
    print(f"Removed anomalies: {acc_anomalies}")
    print(f"Scaled attributes: {acc_org_scaled}")
    print(f"Removed anomalies and scaled attributes: {acc_anom_scaled}")


