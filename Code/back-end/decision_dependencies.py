from numpy import NaN
import pandas as pd
from utils.log_utils import LogUtils
from utils.net_utils import NetUtils


class DecisionDependencies:
    def __init__(self):
        self.dependencies = []
        self.log_utils = LogUtils()
        self.net_utils = NetUtils()

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

        for (decision, relations) in self.decisions:
            self.find_dependencies_between_attributes(decision, relations)

        return list(set(self.dependencies))

    def find_dependencies_between_attributes(self, decision, relations):
        attribute_connections = []
        for node in self.data_nodes:
            if node in relations and not self.decision_has_input_dependencies(decision):
                attribute_connections.append((node, decision))
        self.dependencies += attribute_connections

    def decision_has_input_dependencies(self, decision):
        for _, target in self.dependencies:
            if decision == target:
                return True
        return False

    def find_trivial_dependencies(self, decision, relations):
        for relation in relations:
            for (decision_node, _) in self.decisions:
                if decision_node == relation:
                    self.dependencies.append((relation, decision))
                    return True
        return False

    def find_non_trivial_dependencies(self, decision):
        control_flow_decisions = self.find_control_flow_decisions()
        for cfd in control_flow_decisions:
            if self.is_influencing_decision(cfd, decision) and self.attributes_are_subset(cfd, decision):
                features = self.attributes_set_differance(
                    cfd, decision)
                if features:
                    self.dependencies.append((cfd, decision))

    def find_control_flow_decisions(self):
        control_flow_decisions = []
        for (decision, _) in self.decisions:
            if 'p' in decision:
                control_flow_decisions.append(decision)
        return control_flow_decisions

    def attributes_set_differance(self, cfd, decision):
        for (found_decision, relations) in self.decisions:
            if found_decision == cfd:
                attributes_cfd = relations
            elif found_decision == decision:
                attributes_decision = relations

        return set(attributes_decision).difference(set(attributes_cfd))

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
            return self.log_utils.find_transition_in_log(self.log, decision)
        for arc in self.net.arcs:
            if arc.source == decision and hasattr(arc.source, 'label'):
                return arc.target.label
            elif arc.target == decision and hasattr(arc.source, 'label'):
                return arc.source.label
        # raise Exception('Transition not found in log')

    def is_before_start_transition(self, end_transition, decision):
        to_check = ['source']
        while len(to_check) > 0:
            for check in to_check:
                targets = self.net_utils.find_arc_in_net(self.net, check)
                if end_transition in to_check:
                    return False
                elif decision in targets:
                    return True
                else:
                    to_check.extend(targets)
                to_check.remove(check)
        return False
