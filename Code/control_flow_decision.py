import subprocess
import pandas
from math import nan
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from sklearn.tree import _tree
from sklearn.tree import DecisionTreeClassifier, export_graphviz

class ControlFlowDecisionMiner():
  def __init__(self, event_log):
    self.attributes = []
    self.event_log = event_log
    self.net, self.im, self.fm = inductive_miner.apply(event_log)
    self.relations = self.find_relationships()

  def find_decision_places(self):
    control_flow_decisions = []
    for place in self.net.places:
      count = 0
      for arc in self.net.arcs:
        if arc.source == place:
          count += 1
        if count == 2:
          control_flow_decisions.append(place)
          break
    return control_flow_decisions

  def get_input_transition(self, cfd):
    for arc in self.net.arcs:
      if arc.target == cfd:
        return arc.source.label
    return

  def get_output_transitions(self, cfd):
    outputs = []
    for arc in self.net.arcs:
      if arc.source == cfd:
        outputs.append(arc.target.label)
    return outputs

  def get_event_log_for_place(self, place):
    input_transitions = self.get_input_transition(place)
    output_transitions = self.get_output_transitions(place)
    output_transitions.append(input_transitions)

    return self.event_log.loc[self.event_log['concept:name'].isin(output_transitions)]

  # is number of params always the same ?
  def get_column_names(self, params):
    columns = []
    for param in params:
      columns.append(param.split('=')[0].strip())
    columns.append('label')
    return columns

  # make sure that I can just take 2 values next to each other (SORT BY CASE ID)
  # get event log where all data are in one column (easier to parse)
  def create_decision_table(self, log):
    log = log.fillna('')
    data = []
    labels = []
    index = 0
    while index < log.shape[0]:
      row = []
      if log.iloc[index]['data'] != nan:
        row_data = log.iloc[index]['data'].split(';')
        for single_var in row_data:
          row.append(single_var.split('=')[1].strip())
        labels = self.get_column_names(row_data)
      label = log.iloc[index + 1]['concept:name']
      row.append(label)
      data.append(row)
      index += 2
      table = pandas.DataFrame(data, columns = labels)
      table = table.replace({'True': 1, 'False': 0})

    return table
  
  def find_relationships(self):
    control_flow_decisions = self.find_decision_places()
    places_with_relations = []
    for place in control_flow_decisions:
      log = self.get_event_log_for_place(place)
      decision_table = self.create_decision_table(log)
      y = decision_table["label"]
      X = decision_table.drop(['label'], axis=1) # tu jest problem
      self.attributes.extend(X.columns)
      decision_tree = DecisionTreeClassifier(criterion="entropy", min_samples_split=3, random_state=99)
      decision_tree.fit(X, y)
      # self.visualize_tree(decision_tree, X.columns) # not really necassary
      places_with_relations.append((place, self.get_dependand_features(decision_tree, X.columns)))
    return places_with_relations

  # refactor to use self
  def get_dependand_features(self, tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    def recurse(node, depth, result = []):
      if tree_.feature[node] != _tree.TREE_UNDEFINED:
        name = feature_name[node]
        result.append(name)
        result += recurse(tree_.children_left[node], depth + 1, result)
        result += recurse(tree_.children_right[node], depth + 1, result)
      return list(set(result))
    return recurse(0, 1)

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