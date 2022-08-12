import xml.etree.cElementTree as ET


# add only 1 element!!
class DMNCreator:
    def apply(self, decisions, cfds, attributes, decision_model):
        print("++++++++++++")
        print(decisions)
        print(cfds)
        print(attributes)
        print(decision_model)
        print("++++++++++++")

        width = 100
        height = 40
        added_elements = []
        root = ET.Element(
            "definitions", xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/")
        root.attrib["xmlns:dmndi"] = "https://www.omg.org/spec/DMN/20191111/DMNDI/"
        root.attrib["xmlns:di"] = "http://www.omg.org/spec/DMN/20180521/DI/"

        # add all decisions
        # create decision
        # add dependend features
        for decision, reqs in decisions:
            added_elements.append(decision)
            decision_element = ET.SubElement(
                root, "decision", id=f"{decision}", name=f"{decision}")
            for req in reqs:
                req_element = ET.SubElement(
                    decision_element, "informationRequirement", id=f"{req}_req")
                ET.SubElement(req_element, "requiredInput", href=f"#{req}")

        for cfd, reqs in cfds:
            added_elements.append(cfd)
            decision_element = ET.SubElement(
                root, "decision", id=f"{cfd}", name=f"{cfd}")
            for req in reqs:
                req_element_cfd = ET.SubElement(
                    decision_element, "informationRequirement", id=f"{req}_req")
                ET.SubElement(req_element_cfd, "requiredInput", href=f"#{req}")

        # add all attributes
        for attribute in attributes:
            added_elements.append(attribute)
            ET.SubElement(root, "inputData",
                          id=f'{attribute.replace(" ", "")}', name=f'{attribute}')

        dmnDI = ET.SubElement(root, "dmndi:DMNDI")
        diagram = ET.SubElement(dmnDI, "dmndi:DMNDiagram", id="Diagram")

        elements_with_coords = {}

        x = 170
        y = 60
        for attribute in attributes:
            x += 150
            shape = ET.SubElement(diagram, "dmndi:DMNShape",
                                  dmnElementRef=f"{attribute}")

            ET.SubElement(shape, "dc:Bounds", height=f"{height}",
                          width=f"{width}", x=f"{x}", y=f"{y}")
            elements_with_coords[f"{attribute}"] = [x, y]
        x = 170
        y = 260
        for decision, reqs in decisions:
            x += 150
            shape = ET.SubElement(diagram, "dmndi:DMNShape",
                                  dmnElementRef=f"{decision}")

            ET.SubElement(shape, "dc:Bounds", height=f"{height}",
                          width=f"{width}", x=f"{x}", y=f"{y}")
            elements_with_coords[f"{decision}"] = [x, y]

        x = 170
        y = 460
        for cfd, reqs in cfds:
            x += 150
            shape = ET.SubElement(diagram, "dmndi:DMNShape",
                                  dmnElementRef=f"{cfd}")

            ET.SubElement(shape, "dc:Bounds", height=f"{height}",
                          width=f"{width}", x=f"{x}", y=f"{y}")
            elements_with_coords[f"{cfd}"] = [x, y]

        # place reslationships here
        for el1, el2 in decision_model:
            x1, y1 = elements_with_coords[el1]
            x2, y2 = elements_with_coords[el2]
            if "p_" in el1:
                edge = ET.SubElement(diagram, "dmndi:DMNEdge",
                                     dmnElementRef=f"{el1}")
            else:
                edge = ET.SubElement(diagram, "dmndi:DMNEdge",
                                     dmnElementRef=f"{el1}_req")
            ET.SubElement(edge, "di:waypoint",
                          x=f"{x1 + width/2}", y=f"{y1 + height}")
            ET.SubElement(edge, "di:waypoint",
                          x=f"{x2 + width/2}", y=f"{y2}")

        print(elements_with_coords)
        tree = ET.ElementTree(root)
        tree.write("./uploads/result.dmn")
        return
