from numpy import NaN
import pandas as pd
from sklearn.metrics import accuracy_score
import itertools
import random
from utils.log_utils import LogUtils
from utils.decision_tree_utils import DecisionTreeUtils
from utils.dataframe_utils import DataframeUtils
from sklearn import preprocessing


class DataDecisionMiner:
    def __init__(self):
        self.log_utils = LogUtils()
        self.decision_tree_utils = DecisionTreeUtils()
        self.dataframe_utils = DataframeUtils()

    def apply(self, net, log):
        self.net = net
        self.log = log
        self.attributes = self.log_utils.get_all_attributes_from_log(self.log)
        rule_base_data_decisions, functional_data_decisions, decision_rules = self.find_data_decisions()
        data_nodes = self.find_data_nodes(
            rule_base_data_decisions, functional_data_decisions)

        return (
            rule_base_data_decisions,
            functional_data_decisions,
            data_nodes,
            decision_rules
        )

    def find_data_nodes(self, rule_base_data_decisions, functional_data_decisions):
        result = self.attributes
        for (decision, _) in rule_base_data_decisions:
            if decision in self.attributes:
                result.remove(decision)
        for (decision, _) in functional_data_decisions:
            if decision in self.attributes:
                result.remove(decision)
        return result

    def find_data_decisions(self):
        rule_base_data_decisions = []
        functional_data_decisions = []
        decision_rules = []
        for attribute in self.attributes:
            possible_attributes = self.possible_influencing_attributes(
                attribute)
            X, y = self.dataframe_utils.create_decision_table_for_attribute(
                self.log, attribute, possible_attributes)

            model = self.decision_tree_utils.classify(X, y)

            columns = list(X.columns)

            if self.is_rule_base_data_decision(model, X, y):
                decision_list = self.decision_tree_utils.get_decision_rules(
                    model, columns, attribute)
                if decision_list != None:
                    for decision_rule in decision_list:
                        rule = ''
                        for str_d in decision_rule:
                            rule += str(str_d)
                        decision_rules.append((attribute, rule))

                rule_base_data_decisions.append((attribute, columns))

            (attribute, possible_attributes, decision_rule) = self.check_if_functional_data_decision(
                attribute)

            if attribute != None:
                functional_data_decisions.append(
                    (attribute, possible_attributes))
                decision_rules.append((attribute, decision_rule))

        return self.filter_duplicated_decisions(rule_base_data_decisions), self.filter_duplicated_decisions(functional_data_decisions), decision_rules

    def filter_duplicated_decisions(self, data_decisions):
        result = []
        result_set = []

        random.shuffle(data_decisions)
        for (decision, attributes) in data_decisions:
            element_to_check = []
            element_to_check.append(decision)
            element_to_check.extend(attributes)
            element_to_check.sort()

            if element_to_check not in result_set:
                result.append((decision, attributes))
                result_set.append(element_to_check)

        return result

    def check_if_functional_data_decision(self, attribute):
        possible_attributes = self.possible_influencing_attributes(attribute)
        X, y = self.dataframe_utils.create_decision_table_for_attribute(
            self.log, attribute, possible_attributes)
        X = self.dataframe_utils.get_only_numeric_columns(
            X)

        (value_1, value_2, func) = self.check_all_functions(X, y)
        if value_1 != None:
            return (attribute, [value_1, value_2], f'{attribute} = {value_1} {func} {value_2}')

        return (None, None, None)

    def check_all_functions(self, decision_table, expected_results):
        columns = list(decision_table.columns)
        expected_results = expected_results['label'].values.tolist()
        combinations = itertools.combinations(columns, 2)
        for combination in combinations:
            is_function = [True, True, True, True]
            for index in range(decision_table.shape[1]):
                value_1 = decision_table.iloc[index][combination[0]]
                value_2 = decision_table.iloc[index][combination[1]]
                try:
                    expected_result = float(expected_results[index])
                except:
                    return (None, None, None)

                if value_1 + value_2 != expected_result:
                    is_function[0] = False
                if value_1 - value_2 != expected_result:
                    is_function[1] = False
                if value_1 * value_2 != expected_result:
                    is_function[2] = False
                if value_2 != 0 and value_1 / value_2 != expected_result:
                    is_function[3] = False

            # there can be multiple
            if is_function[0]:
                return (combination[0], combination[1], '+')
            elif is_function[1]:
                return (combination[0], combination[1], '-')
            elif is_function[2]:
                return (combination[0], combination[1], '*')
            elif is_function[0]:
                return (combination[0], combination[1], '/')

        return (None, None, None)

    def is_rule_base_data_decision(self, model, data, real_labels):
        lab = preprocessing.LabelEncoder()
        data = data.to_numpy()

        for i in range(data.shape[1]):
            if (isinstance(data[:, i][0], str)):
                data[:, i] = lab.fit_transform(data[:, i])
        predicted_labels = model.predict(data)
        predicted_labels = lab.fit_transform(predicted_labels)
        real_labels = lab.fit_transform(real_labels)
        acc = accuracy_score(real_labels, predicted_labels)
        if (acc == 1.0):
            return True
        return False

    def possible_influencing_attributes(self, attribute):
        transition = self.log_utils.find_transition_in_log(self.log, attribute)

        return self.log_utils.get_all_previous_transitions(self.net, transition)
