from numpy import NaN
import pandas as pd

class DecisionDependencies:
    def __init__(self):
        self.dependencies = []
    
    def apply(self, log, net, decisions, data_nodes):
        self.log = log
        self.net = net
        self.decisions = decisions
        self.data_nodes = data_nodes
        return self.find_dependencies()
        
    def find_dependencies(self):
        for (decision, relations) in self.decisions:
            # self.find_trivial_dependencies(decision, relations)
            # self.find_non_trivial_dependencies(decision)
            self.find_dependencies_between_attributes(decision, relations)
        return self.dependencies

    def find_dependencies_between_attributes(self, decision, relations): # verify this
    
        for node in self.data_nodes:
            if node in relations:
                self.dependencies.append((node, decision))

    def find_trivial_dependencies(self, decision, relations): # wrong here probably
        for relation in relations:
            for (decision_node, _) in self.decisions:
                if decision_node == relation:
                    self.dependencies.append((relation, decision))

    def find_non_trivial_dependencies(self, decision):
        control_flow_decisions = self.find_control_flow_decisions()
        for cfd in control_flow_decisions:
            if self.is_influencing_decision(cfd, decision) and self.attributes_are_subset(cfd, decision):
                features = self.attributes_set_differance(cfd, decision)
                if features:
                    self.dependencies.append((cfd, decision))       

    def find_control_flow_decisions(self):
        control_flow_decisions = []
        for (decision, _) in self.decisions:
            if type(decision) != str and 'p' in decision.name:
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
        if hasattr(decision, 'name') and decision.name == cfd.name:
            return False
        if self.is_before_start_transition(end_transition, cfd.name):        
            return True
        return False

    def find_starting_transition(self, decision):
        if type(decision) == str and 'p' not in decision:
            return self.find_transition_in_log(decision)
        for arc in self.net.arcs:
            if arc.source == decision and hasattr(arc.source, 'label'):
                return arc.target.label
            elif arc.target == decision and hasattr(arc.source, 'label'):
                return arc.source.label
        raise Exception('Transition not found in log')

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

