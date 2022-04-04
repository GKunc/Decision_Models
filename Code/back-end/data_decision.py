from numpy import NaN
import pandas as pd
from sklearn.metrics import accuracy_score
import itertools
import random
from utils.log_utils import LogUtils
from utils.decision_tree_utils import DecisionTreeUtils
from utils.dataframe_utils import DataframeUtils


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
            X, y = self.create_decision_table_for_attribute(
                attribute, possible_attributes)

            model = self.decision_tree_utils.classify(X, y)

            columns = list(X.columns)

            if self.is_rule_base_data_decision(model, X, y):
                decision_list = self.decision_tree_utils.get_decision_rules(
                    model, columns, attribute)
                for decision_rule in decision_list:
                    rule = ''
                    for str_d in decision_rule:
                        rule += str(str_d)
                    decision_rules.append(rule)

                rule_base_data_decisions.append((attribute, columns))

            (attribute, possible_attributes, decision_rule) = self.check_if_functional_data_decision(
                attribute)

            if attribute != None:
                functional_data_decisions.append(
                    (attribute, possible_attributes))
                decision_rules.append(decision_rule)

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
        X, y = self.create_decision_table_for_attribute(
            attribute, possible_attributes)
        X = self.dataframe_utils.get_only_numeric_columns(
            X)
        columns = list(X.columns)

        (value_1, value_2, func) = self.check_all_functions(X, y)
        if value_1 != None:
            return (attribute, [value_1, value_2], f'{attribute} = {value_1} {func} {value_2}')

        return (None, None, None)

    def check_all_functions(self, decision_table, expected_results):
        columns = list(decision_table.columns)

        combinations = itertools.combinations(columns, 2)
        for combination in combinations:
            is_function = [True, True, True, True]
            for index in range(decision_table.shape[1]):
                value_1 = decision_table.iloc[index][combination[0]]
                value_2 = decision_table.iloc[index][combination[1]]
                expected_result = float(expected_results[index])

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
        predicted_labels = model.predict(data)
        acc = accuracy_score(real_labels, predicted_labels)
        if (acc == 1.0):
            return True
        return False

    def possible_influencing_attributes(self, attribute):
        transition = self.log_utils.find_transition_in_log(self.log, attribute)
        return self.log_utils.get_all_previous_transitions(self.net, transition)

    def create_decision_table_for_attribute(self, attribute, possible_attributes):
        data = []
        filtered_log = self.log.loc[self.log['activity'].isin(
            possible_attributes)]
        labels = self.get_column_names(filtered_log, attribute)
        traces_id = list(set(filtered_log['case']))
        for trace_id in traces_id:
            single_trace_log = filtered_log.loc[filtered_log['case'] == trace_id]
            index = 0
            expected_result = None
            row = []
            while index < single_trace_log.shape[0]:
                if single_trace_log.iloc[index]['data'] != NaN and single_trace_log.iloc[index]['data'] != '':
                    row_data = single_trace_log.iloc[index]['data'].split(';')
                    for single_var in row_data:
                        name = single_var.split('=')[0].strip()
                        value = single_var.split('=')[1].strip()
                        if(name != attribute):
                            row.append(value)
                        else:
                            expected_result = value
                index += 1
            row.append(expected_result)
            data.append(row)

        return self.dataframe_utils.get_traning_data(self.dataframe_utils.convert_to_dataframe(data, labels))

    def get_column_names(self, log, attribute):
        columns = []
        first_index = log['case'].iloc[0]
        single_trace_log = log.loc[log['case'] == first_index]
        index = 0
        while index < single_trace_log.shape[0]:
            if single_trace_log.iloc[index]['data'] != NaN and single_trace_log.iloc[index]['data'] != '':
                row_data = single_trace_log.iloc[index]['data'].split(';')
                for single_var in row_data:
                    name = single_var.split('=')[0].strip()
                    if(name != attribute):
                        columns.append(name)
            index += 1
        columns.append('label')
        return columns
