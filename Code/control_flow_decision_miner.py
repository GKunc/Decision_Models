from utils.decision_tree_utils import DecisionTreeUtils
from utils.dataframe_utils import DataframeUtils
from utils.net_utils import NetUtils

class ControlFlowDecisionMiner():
  def __init__(self):
    self.attributes = []
    self.relations = []
    self.net_utils = NetUtils()
    self.dataframe_utils = DataframeUtils()
    self.decision_tree_utils = DecisionTreeUtils()

  def apply(self, log, net):
    self.log = log
    self.net = net
    return (self.find_places_with_relations(), self.attributes)

  def find_places_with_relations(self):
    control_flow_decisions = self.net_utils.find_decision_places(self.net)
    places_with_relations = []
    for place in control_flow_decisions:
      dataframe_for_place = self.get_dataframe_for_place(place)
      (X, y) = self.dataframe_utils.create_decision_table(dataframe_for_place)
      self.attributes.extend(X.columns)
      decision_tree = self.decision_tree_utils.classify(X, y)
      places_with_relations.append((place, self.decision_tree_utils.get_dependand_features(decision_tree, X.columns)))
    return places_with_relations

  def get_dataframe_for_place(self, place):
    transitions_names = self.net_utils.get_output_transitions_for_place(self.net, place)
    transitions_names.append(self.net_utils.get_input_transition_for_place(self.net, place))
    return self.log.loc[self.log['concept:name'].isin(transitions_names)]