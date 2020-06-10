import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def svm_classifier(point1, point2):

    bankdata = pd.read_csv("Book4.csv")
    X = bankdata.drop('thin=0/normal=1/flat=2', axis=1)
    X = X.drop('lewa=0/prawa=1', axis=1)
    X = X.drop('Clarke', axis=1)
    y = bankdata['thin=0/normal=1/flat=2']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
    svclassifier = SVC(kernel='poly', gamma=10, C=4, degree=3)
    svclassifier.fit(X_train, y_train)
    y_pred = svclassifier.predict([[point1, point2]])

    return y_pred
