# Classification Problems — Pattern Repository

## Quick Reference

| Problem | Models | Split Strategy | Ensemble | Key Technique |
|---------|--------|---------------|----------|---------------|
| Star Type (zad1) | RandomForest + GaussianNB | Per-class P% | Probability tiebreak | Feature product, StandardScaler |
| Car Evaluation (za3pre) | DecisionTree | OrdinalEncoder | — | Categorical → numeric encoding |
| Zadata 8Pre | RandomForest | Simple split | — | Feature importance |
| Zadata 10Pre | MLP | Simple split | — | Neural network |
| Zadata 13Pre | GaussianNB, SVM, Tree | Per-class P% | Majority voting | Model comparison |
| Zadata 15Pre | Various | Simple split | — | Cross-validation |
| Zadata 16Pre | Multiple | Per-class P% | Voting | Model comparison |
| ParamOptimisation | DecisionTree (GA-optimized) | 75/25 split | — | GA hyperparameter search |

---

## 0. Environment Setup

```python
import os
import warnings
os.environ['OPENBLAS_NUM_THREADS'] = '1'      # suppress BLAS threading
warnings.filterwarnings("ignore")               # suppress sklearn warnings
```

---

## 1. Dataset Splitting Patterns

### 1A. Percentage Split Per-Class (most common)
Split each class separately by P%, then concatenate:

```python
# Group by class
class_dwarf = [row for row in dataset if row[-1] == 'Dwarf']
class_giant = [row for row in dataset if row[-1] == 'Giant']

def split_by_percent(data, p):
    split_idx = int(len(data) * (p / 100))
    return data[:split_idx], data[split_idx:]

train_D, test_D = split_by_percent(class_dwarf, P)
train_G, test_G = split_by_percent(class_giant, P)

final_train = train_D + train_G
final_test = test_D + test_G

train_X = [row[:-1] for row in final_train]
train_Y = [row[-1] for row in final_train]
test_X  = [row[:-1] for row in final_test]
test_Y  = [row[-1] for row in final_test]
```

### 1B. Simple Index Split
```python
split = int(len(dataset) * 0.75)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
```

### 1C. k-Fold Cross-Validation
```python
from sklearn.model_selection import cross_val_score, KFold

kf = KFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')
print(f"CV scores: {scores}")
print(f"Mean: {scores.mean():.4f}")
```

---

## 2. Feature Engineering

### Replace features with their product
```python
# Replace 2nd and 3rd features with their product
modified_dataset = []
for row in dataset:
    temp = row[0]
    lum = row[1]
    radius = row[2]
    magnitude = row[3]
    label = row[4]

    product = lum * radius                      # new combined feature
    new_row = [temp, product, magnitude, label]  # 3 features instead of 4
    modified_dataset.append(new_row)
```

---

## 3. Scaling

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
train_X_scaled = scaler.fit_transform(train_X)    # fit on TRAIN only
test_X_scaled = scaler.transform(test_X)          # transform test with TRAIN's scaler
```

---

## 4. Classification Models

### Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=N,          # number of trees
    criterion='entropy',     # or 'gini'
    random_state=0
)
model.fit(train_X, train_Y)
preds = model.predict(test_X)
probas = model.predict_proba(test_X)   # probabilities for each class
```

### Gaussian Naive Bayes
```python
from sklearn.naive_bayes import GaussianNB

model = GaussianNB()
model.fit(train_X, train_Y)
preds = model.predict(test_X)
probas = model.predict_proba(test_X)
```

### Decision Tree
```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    criterion='entropy',     # or 'gini'
    max_depth=5,
    min_samples_split=2,
    max_leaf_nodes=10,
    random_state=0
)
model.fit(train_X, train_Y)
```

### SVM
```python
from sklearn.svm import SVC

model = SVC(kernel='rbf', probability=True, random_state=0)
model.fit(train_X, train_Y)
```

### MLP (Neural Network)
```python
from sklearn.neural_network import MLPClassifier

model = MLPClassifier(
    hidden_layer_sizes=(10, 5),
    activation='relu',
    max_iter=500,
    random_state=0
)
model.fit(train_X, train_Y)
```

---

## 5. Ensemble Strategies

### 5A. Probability-Based Tiebreak (most used)
When two classifiers disagree, the one with higher confidence (`predict_proba`) wins:
```python
classes_rf = list(model_rf.classes_)
classes_nb = list(model_nb.classes_)

correct = 0
for i in range(len(test_Y)):
    true = test_Y[i]
    guess_rf = pred_rf[i]
    guess_nb = pred_nb[i]

    if guess_rf == guess_nb:
        if guess_rf == true:
            correct += 1
    else:
        # Higher confidence wins
        idx_rf = classes_rf.index(guess_rf)
        conf_rf = proba_rf[i][idx_rf]

        idx_nb = classes_nb.index(guess_nb)
        conf_nb = proba_nb[i][idx_nb]

        final = guess_rf if conf_rf > conf_nb else guess_nb
        if final == true:
            correct += 1
```

### 5B. Strict Agreement (AND)
Both classifiers must predict correctly:
```python
correct = sum(1 for i in range(len(test_Y))
              if pred_rf[i] == test_Y[i] and pred_nb[i] == test_Y[i])
```

### 5C. At Least One (OR)
Either classifier predicts correctly:
```python
correct = sum(1 for i in range(len(test_Y))
              if pred_rf[i] == test_Y[i] or pred_nb[i] == test_Y[i])
```

### 5D. Majority Voting (3+ models)
```python
correct = 0
for i in range(len(test_Y)):
    true = test_Y[i]
    guesses = [pred_rf[i], pred_nb[i], pred_mlp[i]]
    if guesses.count(true) >= 2:          # majority (≥2 of 3)
        correct += 1
```

---

## 6. Feature Importance

```python
import numpy as np

model.fit(X_train, y_train)
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

print("Feature ranking:")
for i in indices:
    print(f"{i}: {importances[i]:.4f}")
```

---

## 7. Ordinal Encoding (Categorical Data)

```python
from sklearn.preprocessing import OrdinalEncoder

dataset = [['C', 'S', 'O', '1', '2', '1', '1', '2', '1', '2', '0'], ...]

encoder = OrdinalEncoder()
X = [row[:-1] for row in dataset]        # features (all categorical)
y = [row[-1] for row in dataset]          # labels

X_encoded = encoder.fit_transform(X)      # convert letters → numbers
```

---

## 8. GA Hyperparameter Optimization (ParamOptimisation)

```python
import pygad
from sklearn.tree import DecisionTreeClassifier

# Hyperparameter choices as gene spaces
criterion_choices   = ['gini', 'entropy']
max_depth_choices   = [5, 10, 15, 20, 25]
min_samples_choices = [2, 3, 4, 5, 10]
max_leaf_choices    = [5, 10, 15, 20, 25]

gene_space = [criterion_choices, max_depth_choices,
              min_samples_choices, max_leaf_choices]

def fitness_func(ga, solution, idx):
    criterion   = criterion_choices[int(solution[0])]
    max_depth   = max_depth_choices[int(solution[1])]
    min_samples = min_samples_choices[int(solution[2])]
    max_leaf    = max_leaf_choices[int(solution[3])]

    model = DecisionTreeClassifier(
        criterion=criterion, max_depth=max_depth,
        min_samples_split=min_samples, max_leaf_nodes=max_leaf
    )
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    # Tie-breaker: prefer smaller trees
    size_penalty = (max_depth + max_leaf) * 0.001
    return accuracy - size_penalty
```

---

## 9. Anomaly Detection

```python
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest

# Isolation Forest
model = IsolationForest(contamination=0.1, random_state=0)
preds = model.fit_predict(X)        # 1 = normal, -1 = anomaly

# OneClassSVM
model = OneClassSVM(nu=0.1, kernel='rbf')
preds = model.fit_predict(X)

# LocalOutlierFactor
model = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
preds = model.fit_predict(X)

# EllipticEnvelope
model = EllipticEnvelope(contamination=0.1, random_state=0)
preds = model.fit_predict(X)
```

---

## 10. Common Traps

1. **Split per class, not globally**: Always split each class separately to maintain class balance in train/test

2. **Scaler on train only**: `fit_transform` on train, `transform` on test — never fit scaler on test data

3. **predict_proba order**: The order of classes in `predict_proba` matches `model.classes_`, NOT the order in the test data

4. **OPENBLAS_NUM_THREADS=1**: Required before importing sklearn to prevent threading issues on some systems

5. **random_state=0**: Set everywhere for reproducibility (models, splits, GA)
