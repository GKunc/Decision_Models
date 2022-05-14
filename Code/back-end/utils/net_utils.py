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
                if arc.source.label != None:
                    return arc.source.label

        return

    def get_output_transitions_for_place(self, net, place):
        outputs = []
        for arc in net.arcs:
            if arc.source.name == place:
                if arc.target.label != None:
                    outputs.append(arc.target.label)

        return outputs

    def find_arc_in_net(self, net, source):
        result = []
        for arc in net.arcs:
            if hasattr(arc.source, 'name') and arc.source.name == source:
                result.append(arc.target.label)
            elif hasattr(arc.source, 'label') and arc.source.label == source:
                result.append(arc.target.name)
        if len(result) > 0:
            return result
        return []
