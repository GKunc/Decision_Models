import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree
from sklearn import preprocessing


class DecisionTreeUtils:
    def __init__(self):
        self.tree = []

    def classify(self, X, y):
        decision_tree = DecisionTreeClassifier(
            criterion="entropy", min_samples_split=3, random_state=99)

        lab = preprocessing.LabelEncoder()
        X = X.to_numpy()
        print('DecisionTreeUtils - before transform XXXXX')
        print(X)
        for i in range(X.shape[1]):
            print(type(X[:, i]))
            if (isinstance(X[:, i][0], str)):
                X[:, i] = lab.fit_transform(X[:, i])

        print('DecisionTreeUtils - after transform XXXXX')
        print(X)
        y_transformed = lab.fit_transform(y)

        print('DecisionTreeUtils - after transform YYYYYY')
        print(y_transformed)
        decision_tree.fit(X, y_transformed)
        return decision_tree

    def get_dependand_features(self, tree, feature_names):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        def __recurse(node, depth, result=[]):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                result.append(name)
                result += __recurse(tree_.children_left[node],
                                    depth + 1, result)
                result += __recurse(tree_.children_right[node],
                                    depth + 1, result)
            return list(set(result))
        return __recurse(0, 1)

    def get_decision_rules(self, tree, feature_names, attribute):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        pathto = dict()

        global k
        k = 0
        return self.__search_for_decision_rules(tree_, feature_name, pathto, attribute, 0, 1, 0, [])

    def __search_for_decision_rules(self, tree_, feature_name, pathto, attribute, node, depth, parent, result):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            s = "{} <= {} ".format(name, threshold, node)
            if node == 0:
                pathto[node] = s
            else:
                pathto[node] = pathto[parent] + ' and ' + s
            self.__search_for_decision_rules(tree_, feature_name, pathto, attribute,
                                             tree_.children_left[node], depth + 1, node, result)
            s = "{} > {}".format(name, threshold)
            if node == 0:
                pathto[node] = s
            else:
                pathto[node] = pathto[parent] + ' and ' + s
            self.__search_for_decision_rules(tree_, feature_name, pathto, attribute,
                                             tree_.children_right[node], depth + 1, node, result)
            return result
        else:
            value = [i for i, e in enumerate(
                tree_.value[node][0]) if e != 0]
            try:
                result.append((pathto[parent], ' then ',
                               attribute, '=', value[0] + 1))
            except KeyError:
                return
