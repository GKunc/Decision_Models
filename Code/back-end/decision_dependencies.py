from numpy import NaN
import pandas as pd
from utils.log_utils import LogUtils
from utils.net_utils import NetUtils
from utils.list_utils import ListUtils


class DecisionDependencies:
    def __init__(self):
        self.dependencies = []
        self.log_utils = LogUtils()
        self.net_utils = NetUtils()
        self.list_utils = ListUtils()

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
        control_flow_decisions = self.net_utils.find_decision_places(self.net)
        for cfd in control_flow_decisions:
            if self.is_influencing_decision(cfd, decision):
                features = self.list_utils.attributes_set_differance(
                    self.decisions, cfd, decision)
                if features:
                    self.dependencies.append((cfd, decision))

    def is_influencing_decision(self, cfd, decision):
        end_transition = self.log_utils.find_starting_transition(
            self.log, self.net, decision)
        if decision == cfd:
            return False
        if self.log_utils.is_before_start_transition(self.net, end_transition, cfd) and self.list_utils.attributes_are_subset(self.decisions, cfd, decision):
            return True
        return False
