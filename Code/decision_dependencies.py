class DecisionDependencies:
    def __init__(self, event_log, decisions):
        self.log = event_log
        self.decisions = decisions

    def find_dependencies(self):
        for (decision, relations) in self.decisions:
            self.find_trivial_dependencies(decision, relations)
        return "TEST FIND"

    def find_trivial_dependencies(self, decision, relations):
        for relation in relations:
            # if this relation is one of data decisions
            # then its a trivial dependency
            for (decision_node, _) in self.decisions:
                if decision_node == relation:
                    print(f"Decision: {decision} -> {relation}")

        return None

    def find_non_trivial_dependencies(self):
        return "non-trivial"