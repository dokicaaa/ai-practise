import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

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
    split_index = int(len(data) * (P / 100))

    X = data[:, :-1]
    Y = data[:, -1]
    
    train_X = X[:split_index]
    train_Y = Y[:split_index]
    
    test_X = X[split_index:]
    test_Y = Y[split_index:]
    
    model_org = DecisionTreeClassifier(criterion=C, max_leaf_nodes=L, random_state=0)
    model_org.fit(train_X,train_Y)
    pred_org = model_org.predict(test_X)
    acc_org = accuracy_score(test_Y, pred_org)
    
    print(f"Tochnost so originalniot klasifikator: {acc_org}")
    
    # Kolekcija od 3 drva kade sekoe drvo za sekoja kolona gleda dali e 1 tip riba 
    classes = ['Perch', 'Roach', 'Bream']
    models = {}
    
    # Translation treba da se napravi Od string vo binaren za modelot da razbere
    # [Pearch, Bream .... ] vo [1, 0 ,0 ...] za sekoj od modelite
    
    for cls in classes:
        # Ako momentalnata clasa na modelot ednakvo so klasata na reddicata stavi ja
        # kako 1
        train_Y_bin = [1 if y == cls else 0 for y in train_Y]
    
        # ustvari se gradi niza on binarni vrednost za koe treba sekoj model da gi uchi
        dt_bin =  DecisionTreeClassifier(criterion=C, max_leaf_nodes=L, random_state=0)
        dt_bin.fit(train_X, train_Y_bin)
        # Dictinary za cauvanje na list od predictions za sekoja 3 od clasite
        models[cls] = dt_bin
        
    correct_predictions = 0
    
    for i in range(len(test_X)):
        # zemam samples od sekoja redica
        # Mora da e 2d niza
        # test_X = [[23 23 23 23 ], [42 32 32 32 32]]
        test_sample = [test_X[i]]
        true_class = test_Y[i]
        
        # Lista za site predictions vo sekoja redica
        predictions = []
        for cls in classes:
            # Ako tocno go predicnatlo za sekoj od modelite togash go stava vo nizata
            prediction_bin = models[cls].predict(test_sample)[0]
            if prediction_bin == 1:
                predictions.append(cls)
        
        # Ako nizata ni e so golemina 1 i tocno e pridcatnoto toash e vazecko
        if len(predictions) == 1 and predictions[0] == true_class:
            correct_predictions += 1
                
    
    acc_class = correct_predictions / float(len(test_X))
    print(f"Tochnost so kolekcija od klasifikatori: {acc_class}")
    