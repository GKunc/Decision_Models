from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree

class DecisionTreeUtils:
    def __init__(self):
        self.tree = []

    def classify(self, X, y):
        decision_tree = DecisionTreeClassifier(criterion="entropy", min_samples_split=3, random_state=99)
        decision_tree.fit(X, y)
        return decision_tree

    def get_dependand_features(self, tree, feature_names):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        def __recurse(node, depth, result = []):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                result.append(name)
                result += __recurse(tree_.children_left[node], depth + 1, result)
                result += __recurse(tree_.children_right[node], depth + 1, result)
            return list(set(result))
        return __recurse(0, 1)