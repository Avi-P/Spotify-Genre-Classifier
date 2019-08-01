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


# Finds the best classifier out of all the classifiers with the best parameters
def find_best_method(log_reg_bp, svm_bp, tree_bp, forest_bp, knn_bp, nn_bp, x, y):
    print("Performing Cross Validation")

    # Splits data in training and testing dataset
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)

    std_sc = StandardScaler()

    # Finds std and mean about the data and transforms it
    x_train_std = std_sc.fit_transform(x_train)

    # Creates classifiers with the best parameters found
    log_reg = LogisticRegression(C=log_reg_bp["C"])
    svm = SVC(kernel=svm_bp["kernel"], probability=True)
    tree = DecisionTreeClassifier(max_depth=tree_bp["max_depth"])
    forest = RandomForestClassifier(n_estimators=forest_bp["n_estimators"], random_state=0)
    knn = KNeighborsClassifier(n_neighbors=knn_bp["n_neighbors"], weights=knn_bp["weights"])
    nn = MLPClassifier(activation=nn_bp["activation"], hidden_layer_sizes=nn_bp["hidden_layer_sizes"])

    classifiers = [log_reg, knn, tree, svm, forest, nn]
    index = ["LR", "KNN", "Tree", "SVM", "Forest", "NN"]

    model_scores = []

    # Performs cross validation on all the classifiers
    for clf in classifiers:
        model_scores.append(cross_val_score(clf, x_train_std, y_train, scoring='accuracy', cv=10))

    models_df = pd.DataFrame(model_scores, columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             index=index)

    # Finds the means classification rate for all the classifier
    models_df["Mean"] = models_df.mean(axis=1)

    # Finds the best classifier and best index
    best_method = models_df["Mean"].idxmax()
    best_index = index.index(best_method)

    print("\nBest Method Determined: " + best_method + "\n")

    # Returns best classifier
    return classifiers[best_index]


# Finds the best parameters for all the classifiers
def best_parameters(classifier_list, classifiers, param_ranges, x, y):
    # Splits the data in to training and testing
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)

    std_sc = StandardScaler()

    # fit_transform calculates standard deviation and mean and then transforms the data into z-values
    x_train_std = std_sc.fit_transform(x_train)
    # transform only transforms the data into z-values using the std and mean from training data
    x_test_std = std_sc.transform(x_test)

    obj = []

    # Loops through the classifiers
    for i in range(0, len(classifier_list)):

        print(classifier_list[i] + "\n")

        # Performs grid search on all combinations of parameter ranges to find the best params
        gs = GridSearchCV(estimator=classifiers[i], param_grid=param_ranges[i], scoring='accuracy', cv=10)

        # Trains the classifier on the training data
        gs.fit(x_train_std, y_train)

        # Gets score for training and testing dataset
        train_score = gs.score(x_train_std, y_train)
        test_score = gs.score(x_test_std, y_test)

        print(gs.best_params_)

        print("Train score: {} \nTest score: {}\n".format(train_score, test_score))

        print("----------------------------------------------------------------------")

        # Adds it to list of classifiers
        obj.append(gs.best_params_)

    return obj


# Entry method
def build_classifier():
    # Reads the data from the CSV
    sp_data = pd.read_csv("data.csv")

    # Gets the values of the features we want to classify
    x = sp_data[
        ["Danceability", "Energy", "Loudness", "Speechiness", "Acousticness", "Instrumentalness", "Liveness",
         "Valence"]].values
    y = sp_data['Target'].values

    # Calls wrapper method
    find_best(x, y)


# Wrapper method to other methods
def find_best(x, y):
    # List of classifiers we will be testing
    classifier_list = ["Logistic Regression", "Support Vector Machine", "Decision Tree",
                       "Forest", "K Nearest Neighbor", "Neural Network"]

    # Creates the classifiers
    log_reg = LogisticRegression()
    svm = SVC()
    tree = DecisionTreeClassifier()
    forest = RandomForestClassifier(random_state=0)
    knn = KNeighborsClassifier()
    nn = MLPClassifier()

    # Stores them into an list
    classifiers = [log_reg, svm, tree, forest, knn, nn]

    # List of list with all the parameters we want to test for the classifiers
    param_ranges = [
        [{'C': [0.0001, 0.001, .005, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]}],                         # Logistic Regression
        [{'kernel': ['rbf', 'linear']}],                                                             # Support Vector Machine
        [{'max_depth': [3, 5, 7]}],                                                                  # Decision Tree
        [{'n_estimators': [10, 100, 1000]}],                                                         # Forest
        [{'weights': ['distance', 'uniform'], 'n_neighbors': [3, 5, 7]}],                            # K Nearest Neighbors
        [{'hidden_layer_sizes': [100, 250, 500, 1000], 'activation': ['relu', 'tanh', 'logistic']}]  # Neural Network
    ]

    print("----------------------------------------------------------------------")

    # Returns an list with all the classifiers instantiated with the best parameters found
    parameter_tuned = best_parameters(classifier_list, classifiers, param_ranges, x, y)

    # Finds the best classifier out of all the classifiers
    classifier = find_best_method(parameter_tuned[0], parameter_tuned[1], parameter_tuned[2],
                                  parameter_tuned[3], parameter_tuned[4], parameter_tuned[5],
                                  x, y)

    # Trains the best classifier on all the data
    classifier.fit(x, y)

    print("Saving model to disk\n")

    # Save the model to disk
    joblib.dump(classifier, 'classifier.sav')
