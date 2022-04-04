from cmath import nan
from utils.net_utils import NetUtils
import pandas as pd


class LogUtils:
    def __init__(self):
        self.net_utils = NetUtils()

    def filter_log_for_place(self, log, net, place):
        transitions_names = self.net_utils.get_output_transitions_for_place(
            net, place)
        transitions_names.append(
            self.net_utils.get_input_transition_for_place(net, place))
        return log.loc[log['concept:name'].isin(transitions_names)]

    def get_all_attributes_from_log(self, log):
        attributes = []
        index = 0
        while index < log.shape[0]:
            if log.iloc[index]['data'] != nan and log.iloc[index]['data'] != '':
                row_data = log.iloc[index]['data'].split(';')
                for single_var in row_data:
                    attributes.append(single_var.split('=')[0].strip())
            index += 1
        return list(set(attributes))

    def get_all_previous_transitions(self, net, last_transition):
        objects_to_check = [last_transition]
        result = []
        while len(objects_to_check) > 0:
            to_delete = []
            for arc in net.arcs:
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

    def find_transition_in_log(self, log, attribute):
        index = 0
        while index < log.shape[0]:
            if log.iloc[index]['data'] != nan and not pd.isnull(log.iloc[index]['data']) and log.iloc[index]['data'] != '':
                row_data = log.iloc[index]['data'].split(';')
                for single_var in row_data:
                    split_value = single_var.split('=')
                    name = split_value[0].strip()
                    if name == attribute:
                        return log.iloc[index]['activity']
            index += 1
        raise Exception('Attribute not found in log')

    def find_starting_transition(self, log, net, decision):
        if 'p' not in decision:
            return self.find_transition_in_log(log, decision)
        for arc in net.arcs:
            if arc.source == decision and hasattr(arc.source, 'label'):
                return arc.target.label
            elif arc.target == decision and hasattr(arc.source, 'label'):
                return arc.source.label
        # raise Exception('Transition not found in log')

    def is_before_start_transition(self, net, end_transition, decision):
        to_check = ['source']
        while len(to_check) > 0:
            for check in to_check:
                targets = self.net_utils.find_arc_in_net(net, check)
                if end_transition in to_check:
                    return False
                elif decision in targets:
                    return True
                else:
                    to_check.extend(targets)
                to_check.remove(check)
        return False
