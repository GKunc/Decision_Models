from this import d
from numpy import NaN
import pandas as pd
import subprocess
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from pandas.api.types import is_numeric_dtype
import itertools
import random
from sklearn.tree import _tree
from utils.log_utils import LogUtils


class DataDecisionMiner:
    # ADD RULES TO RESULT
    def apply(self, net, log):
        self.net = net
        self.log = log
        self.log_utils = LogUtils()
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
            decision_table = self.create_decision_table_for_attribute(
                attribute, possible_attributes)

            model = self.create_decision_tree(decision_table)
            real_labels = decision_table["label"]
            data = decision_table.drop(['label'], axis=1)
            columns = list(decision_table.columns)
            columns.remove('label')

            if self.is_rule_base_data_decision(model, data, real_labels):
                self.tree_to_code(model, columns, attribute)
                print(decision_table)
                rule_base_data_decisions.append((attribute, columns))
                decision_rules.append('X = Y > 2 and Z = 3')

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
        decision_table = self.create_decision_table_for_attribute(
            attribute, possible_attributes)
        decision_table = self.get_only_numeric_columns(decision_table)
        columns = list(decision_table.columns)
        columns.remove('label')

        (value_1, value_2, func) = self.check_all_functions(decision_table)
        if value_1 != None:
            return (attribute, [value_1, value_2], f'{attribute} = {value_1} {func} {value_2}')

        return (None, None, None)

    def check_all_functions(self, decision_table):
        columns = list(decision_table.columns)
        columns.remove('label')
        combinations = itertools.combinations(columns, 2)
        for combination in combinations:
            is_function = [True, True, True, True]
            for index in range(decision_table.shape[1]):
                value_1 = decision_table.iloc[index][combination[0]]
                value_2 = decision_table.iloc[index][combination[1]]
                expected_result = decision_table.iloc[index]['label']

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

    def get_only_numeric_columns(self, decision_table):
        decision_table = decision_table.apply(pd.to_numeric, errors='ignore')
        columns = decision_table.columns
        numeric_columns = []
        for column in columns:
            if is_numeric_dtype(decision_table[column]):
                numeric_columns.append(column)
        return decision_table[numeric_columns]

    def is_rule_base_data_decision(self, model, data, real_labels):
        predicted_labels = model.predict(data)
        acc = accuracy_score(real_labels, predicted_labels)
        if (acc == 1.0):
            return True
        return False

    def create_decision_tree(self, decision_table):
        y = decision_table["label"]
        X = decision_table.drop(['label'], axis=1)
        decision_tree = DecisionTreeClassifier(
            criterion="entropy", min_samples_split=3, random_state=99)
        model = decision_tree.fit(X, y)
        # self.visualize_tree(decision_tree, X.columns) # not really necassary
        return model

    def visualize_tree(self, tree, feature_names):
        with open("dt.dot", 'w') as f:
            export_graphviz(tree, out_file=f,
                            feature_names=feature_names)

        command = ["dot", "-Tpng", "dt.dot", "-o", "dt.png"]
        try:
            subprocess.check_call(command)
        except:
            exit("Could not run dot, ie graphviz, to "
                 "produce visualization")

    def find_transition_in_log(self, attribute):
        index = 0
        while index < self.log.shape[0]:
            if self.log.iloc[index]['data'] != NaN and self.log.iloc[index]['data'] != '':
                row_data = self.log.iloc[index]['data'].split(';')
                for single_var in row_data:
                    split_value = single_var.split('=')
                    name = split_value[0].strip()
                    if (name == attribute):
                        return self.log.iloc[index]['activity']
            index += 1
        raise Exception('Attribute not found in log')

    def get_all_previous_transitions(self, last_transition):
        objects_to_check = [last_transition]
        result = []
        while len(objects_to_check) > 0:
            to_delete = []
            for arc in self.net.arcs:
                # it is transition
                if (hasattr(arc.target, 'label') and arc.target.label in objects_to_check):
                    if(arc.source.name != 'source'):
                        # can be multiple objs
                        objects_to_check.append(arc.source)
                    result.append(arc.target.label)
                    to_delete.append(arc.target.label)
                elif (arc.target and arc.target in objects_to_check):
                    # can be multiple objs
                    objects_to_check.append(arc.source.label)
                    to_delete.append(arc.target)

            for object in set(to_delete):
                objects_to_check.remove(object)

        return list(set(result))

    def possible_influencing_attributes(self, attribute):
        transition = self.find_transition_in_log(attribute)
        return self.get_all_previous_transitions(transition)

    def create_decision_table_for_attribute(self, attribute, possible_attributes):
        filtered_log = self.log.loc[self.log['activity'].isin(
            possible_attributes)]
        data = []
        labels = self.get_column_names(filtered_log, attribute)
        traces_id = list(set(filtered_log['case']))
        for trace_id in traces_id:
            single_trace_log = filtered_log.loc[filtered_log['case'] == trace_id]
            index = 0
            label = None
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
                            label = value
                index += 1
            row.append(label)
            data.append(row)
        table = pd.DataFrame(data, columns=labels)
        table = table.replace({'True': '1', 'False': '0'})
        return table

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

    def tree_to_code(self, tree, feature_names, attribute):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        pathto = dict()

        global k
        k = 0

        def recurse(node, depth, parent):
            global k

            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                s = "{} <= {} ".format(name, threshold, node)
                if node == 0:
                    pathto[node] = s
                else:
                    pathto[node] = pathto[parent] + ' and ' + s

                recurse(tree_.children_left[node], depth + 1, node)
                s = "{} > {}".format(name, threshold)
                if node == 0:
                    pathto[node] = s
                else:
                    pathto[node] = pathto[parent] + ' and ' + s
                recurse(tree_.children_right[node], depth + 1, node)
            else:
                k = k+1
                value = [i for i, e in enumerate(
                    tree_.value[node][0]) if e != 0]
                print(k, ')', pathto[parent], attribute, '=', value[0] + 1)
        recurse(0, 1, 0)
