from operator import not_
from numpy import NaN
import pandas as pd


class DecisionDependencies:
    def __init__(self):
        self.dependencies = []
        self.not_to_connect = []

    def apply(self, log, net, decisions, data_nodes):
        self.log = log
        self.net = net
        self.decisions = decisions
        self.data_nodes = data_nodes
        return self.find_dependencies()

    def find_dependencies(self):
        for (decision, relations) in self.decisions:
            self.find_trivial_dependencies(decision, relations)
            self.find_non_trivial_dependencies(decision)
            self.find_dependencies_between_attributes(decision, relations)
        return self.dependencies

    def find_dependencies_between_attributes(self, decision, relations):
        for node in self.data_nodes:
            if node in relations:
                for not_connect_list, not_connected in self.not_to_connect:
                    if not_connected != decision or not node in not_connect_list:
                        self.dependencies.append((node, decision))

    def add_to_not_connect(self, relationships, decision):
        add_new = True
        for not_connect_list, not_to_connect in self.not_to_connect:
            if decision == not_to_connect:
                not_connect_list.extend(relationships)
                add_new = False

        if add_new:
            self.not_to_connect.append((relationships, decision))

    def find_trivial_dependencies(self, decision, relations):
        for relation in relations:
            for (decision_node, relationships) in self.decisions:
                if decision_node == relation:
                    self.add_to_not_connect(
                        self.get_not_to_connect(relationships), decision)
                    self.dependencies.append((relation, decision))
                    return True
        return False

    def find_non_trivial_dependencies(self, decision):
        control_flow_decisions = self.find_control_flow_decisions()
        for cfd in control_flow_decisions:
            if self.is_influencing_decision(cfd, decision) and self.attributes_are_subset(cfd, decision):
                features, not_connect = self.attributes_set_differance_and_intersection(
                    cfd, decision)
                if features:
                    self.add_to_not_connect(
                        self.get_not_to_connect(list(not_connect)), decision)
                    self.dependencies.append((cfd, decision))

    def get_not_to_connect(self, not_connect):
        all_elements = not_connect
        all_decisions = []
        for decision, _ in self.decisions:
            all_decisions.append(decision)

        result = []
        for element in all_elements:
            if not element in all_decisions:
                result.append(element)
        return result

    def find_control_flow_decisions(self):
        control_flow_decisions = []
        for (decision, _) in self.decisions:
            if 'p' in decision:
                control_flow_decisions.append(decision)
        return control_flow_decisions

    def attributes_set_differance_and_intersection(self, cfd, decision):
        for (found_decision, relations) in self.decisions:
            if found_decision == cfd:
                attributes_cfd = relations
            elif found_decision == decision:
                attributes_decision = relations

        return set(attributes_decision).difference(set(attributes_cfd)), set(attributes_decision).intersection(set(attributes_cfd))

    def attributes_are_subset(self, cfd, decision):
        attributes_cfd = []
        attributes_decision = []
        for (found_decision, relations) in self.decisions:
            if found_decision == cfd:
                attributes_cfd = relations

            elif found_decision == decision:
                attributes_decision = relations

        if set(attributes_cfd).issubset(set(attributes_decision)):
            return True
        return False

    def is_influencing_decision(self, cfd, decision):
        end_transition = self.find_starting_transition(decision)
        if decision == cfd:
            return False
        if self.is_before_start_transition(end_transition, cfd):
            return True
        return False

    def find_starting_transition(self, decision):
        if 'p' not in decision:
            return self.find_transition_in_log(decision)
        for arc in self.net.arcs:
            if arc.source == decision and hasattr(arc.source, 'label'):
                return arc.target.label
            elif arc.target == decision and hasattr(arc.source, 'label'):
                return arc.source.label
        # raise Exception('Transition not found in log')

    def find_transition_in_log(self, attribute):
        index = 0
        while index < self.log.shape[0]:
            if self.log.iloc[index]['data'] != NaN and not pd.isnull(self.log.iloc[index]['data']) and self.log.iloc[index]['data'] != '':
                row_data = self.log.iloc[index]['data'].split(';')
                for single_var in row_data:
                    split_value = single_var.split('=')
                    name = split_value[0].strip()
                    if name == attribute:
                        return self.log.iloc[index]['activity']
            index += 1
        raise Exception('Attribute not found in log')

    def is_before_start_transition(self, end_transition, decision):
        to_check = ['source']
        while len(to_check) > 0:
            for check in to_check:
                targets = self.find_arc_in_net(check)
                if end_transition in to_check:
                    return False
                elif decision in targets:
                    return True
                else:
                    to_check.extend(targets)
                to_check.remove(check)
        return False

    def find_arc_in_net(self, source):
        result = []
        for arc in self.net.arcs:
            if hasattr(arc.source, 'name') and arc.source.name == source:
                result.append(arc.target.label)
            elif hasattr(arc.source, 'label') and arc.source.label == source:
                result.append(arc.target.name)
        if len(result) > 0:
            return result
        return []
