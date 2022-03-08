class NetUtils():
    def find_decision_places(self, net):
        control_flow_decisions = []
        for place in net.places:
            count = 0
            for arc in net.arcs:
                if arc.source == place:
                    count += 1
                if count == 2:
                    control_flow_decisions.append(place.name)
                    break
        return control_flow_decisions

    def get_input_transition_for_place(self, net, place):
        for arc in net.arcs:
            if arc.target.name == place:
                return arc.source.label
        return

    def get_output_transitions_for_place(self, net, place):
        outputs = []
        for arc in net.arcs:
            if arc.source.name == place:
                outputs.append(arc.target.label)
        return outputs