from utils.net_utils import NetUtils

class LogUtils:
    def __init__(self):
        self.net_utils = NetUtils()

    def filter_log_for_place(self, log, net, place):
        transitions_names = self.net_utils.get_output_transitions_for_place(net, place)
        transitions_names.append(self.net_utils.get_input_transition_for_place(net, place))
        return self.log.loc[self.log['concept:name'].isin(transitions_names)]