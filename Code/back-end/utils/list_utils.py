class ListUtils:
    def attributes_set_differance(self, decisions, cfd, decision):
        attributes_cfd, attributes_decision = self.__get_attributes_for_decision(
            decisions, cfd, decision)

        return set(attributes_decision).difference(set(attributes_cfd))

    def attributes_are_subset(self, decisions, cfd, decision):
        attributes_cfd, attributes_decision = self.__get_attributes_for_decision(
            decisions, cfd, decision)

        if set(attributes_cfd).issubset(set(attributes_decision)):
            return True
        return False

    def __get_attributes_for_decision(self, decisions, cfd, decision):
        for (found_decision, relations) in decisions:
            if found_decision == cfd:
                attributes_cfd = relations
            elif found_decision == decision:
                attributes_decision = relations
        return attributes_cfd, attributes_decision
