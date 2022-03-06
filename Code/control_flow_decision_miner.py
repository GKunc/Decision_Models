from utils.log_utils import LogUtils
from utils.decision_tree_utils import DecisionTreeUtils
from utils.dataframe_utils import DataframeUtils
from utils.net_utils import NetUtils

class ControlFlowDecisionMiner():
  def __init__(self):
    self.attributes = []
    self.net_utils = NetUtils()
    self.dataframe_utils = DataframeUtils()
    self.decision_tree_utils = DecisionTreeUtils()
    self.log_utils = LogUtils()

  def apply(self, log, net):
    self.log = log
    self.net = net
    return self.find_places_with_relations()

  def find_places_with_relations(self):
    control_flow_decisions = self.net_utils.find_decision_places(self.net)
    places_with_relations = []
    for place in control_flow_decisions:
      dataframe_for_place = self.log_utils.filter_log_for_place(self.log, self.net, place)
      (X, y) = self.dataframe_utils.create_decision_table(dataframe_for_place)
      decision_tree = self.decision_tree_utils.classify(X, y)
      places_with_relations.append((place, self.decision_tree_utils.get_dependand_features(decision_tree, X.columns)))
    return places_with_relations