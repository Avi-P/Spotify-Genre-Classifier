import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

from sklearn.externals import joblib

import warnings
warnings.filterwarnings('ignore')


class ClassifierBuilder:

    @staticmethod
    def build_classifier():
        sp_data = pd.read_csv("test.csv")

        x = sp_data[
            ["Danceability", "Energy", "Loudness", "Speechiness", "Acousticness", "Instrumentalness", "Liveness",
             "Valence"]].values
        y = sp_data['Target'].values

        ClassifierBuilder.find_best(x, y)

        X_std = stdsc.fit_transform(X)

        forest.fit(X_std, y)

    @staticmethod
    def find_best(x, y):
        classifier_list = ["Logistic Regression", "Support Vector Machine", "Decision Tree",
                           "Forest", "K Nearest Neighbor", "Neural Network"]

        log_reg = LogisticRegression()
        svm = SVC()
        tree = DecisionTreeClassifier()
        forest = RandomForestClassifier(random_state=0)
        knn = KNeighborsClassifier()
        nn = MLPClassifier()

        classifiers = [log_reg, svm, tree, forest, knn, nn]

        param_ranges = [
            [{'C': [0.0001, 0.001, .005, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]}],  # Logistic Regression
            [{'kernel': ['rbf', 'linear']}],  # Support Vector Machine
            [{'max_depth': [3, 5, 7]}],  # Decision Tree
            [{'n_estimators': [10, 100, 1000]}],  # Forest
            [{'weights': ['distance', 'uniform'], 'n_neighbors': [3, 5, 7]}],  # K Nearest Neighbors
            [{'weights': ['distance', 'uniform'], 'n_neighbors': [3, 5, 7]}]  # Neural Network
        ]

        parameter_tuned = ClassifierBuilder.best_parameters(classifier_list, classifiers, param_ranges, x, y)

        classifier = ClassifierBuilder.find_best_method(parameter_tuned[0], parameter_tuned[1], parameter_tuned[2],
                                                        parameter_tuned[3], parameter_tuned[4], parameter_tuned[5],
                                                        x, y)

        std_sc = StandardScaler()

        x_std = std_sc.fit_transform(x)

        classifier.fit(x_std, y)

        # save the model to disk
        joblib.dump(forest, 'final_forest_model.sav')


    @staticmethod
    def best_parameters(classifier_list, classifiers, param_ranges, x, y):
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)

        std_sc = StandardScaler()

        x_train_std = std_sc.fit_transform(x_train)
        x_test_std = std_sc.transform(x_test)

        obj = []

        for i in range(0, len(classifier_list)):
            print(classifier_list[i] + "\n")

            gs = GridSearchCV(estimator=classifiers[i], param_grid=param_ranges[i], scoring='accuracy', cv=10)

            gs.fit(x_train_std, y_train)
            train_score = gs.score(x_train_std, y_train)
            test_score = gs.score(x_test_std, y_test)
            print(gs.best_params_ + "\n")

            print("Train score: {} \nTest score: {}\n".format(train_score, test_score))

            obj.append(gs.best_params_)

        return obj

    @staticmethod
    def find_best_method(log_reg_bp, svm_bp, tree_bp, forest_bp, knn_bp, nn_bp, x, y):
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)

        std_sc = StandardScaler()

        x_train_std = std_sc.fit_transform(x_train)
        x_test_std = std_sc.transform(x_test)

        log_reg = LogisticRegression(C=log_reg_bp["C"])
        svm = SVC(kernel=svm_bp["kernel"])
        tree = DecisionTreeClassifier(max_depth=tree_bp["max_depth"])
        forest = RandomForestClassifier(n_estimators=forest_bp["n_estimators"], random_state=0)
        knn = KNeighborsClassifier(n_neighbors=knn_bp["n_neighbors"], weights=knn_bp["weights"])
        nn = MLPClassifier(activation=nn_bp["activation"], hidden_layer_sizes=nn_bp["hidden_layer_sizes"])

        classifiers = [log_reg, knn, tree, svm, forest, nn]
        index = ["LR", "KNN", "Tree", "SVM", "Forest", "NN"]

        model_scores = []
        for clf in classifiers:
            model_scores.append(cross_val_score(clf, x_train_std, y_train, scoring='accuracy', cv=10))

        models_df = pd.DataFrame(model_scores, columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                 index=index)

        models_df["Mean"] = models_df.mean(axis=1)

        best_method = models_df["Mean"].idxmax()
        best_index = index.index(best_method)

        return classifiers[best_index]
