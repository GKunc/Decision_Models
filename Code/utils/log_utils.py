from cmath import nan
from utils.net_utils import NetUtils

class LogUtils:
    def __init__(self):
        self.net_utils = NetUtils()

    def filter_log_for_place(self, log, net, place):
        transitions_names = self.net_utils.get_output_transitions_for_place(net, place)
        transitions_names.append(self.net_utils.get_input_transition_for_place(net, place))
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
