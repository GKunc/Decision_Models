import xml.etree.cElementTree as ET
import uuid

# add guid to req


class DMNCreator:
    def apply(self, decisions, cfds, attributes, decision_model):
        print("++++++++++++")
        print(decisions)
        print(cfds)
        print(attributes)
        print(decision_model)
        print("++++++++++++")

        connected_elements = {}
        width = 100
        height = 40
        root = ET.Element(
            "definitions", xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/")
        root.attrib["xmlns:dmndi"] = "https://www.omg.org/spec/DMN/20191111/DMNDI/"
        root.attrib["xmlns:di"] = "http://www.omg.org/spec/DMN/20180521/DI/"

        # add all decisions
        # create decision
        # add dependend features
        for decision, _ in decisions:
            decision_element = ET.SubElement(
                root, "decision", id=f"{decision}", name=f"{decision}")
            for el1, el2 in decision_model:
                if el2 == decision:
                    el_id = f"{el1}_req_{uuid.uuid4()}"
                    if el2 not in connected_elements:
                        connected_elements[el2] = []
                    connected_elements[el2].append(el_id)

                    req_element = ET.SubElement(
                        decision_element, "informationRequirement", id=el_id)
                    ET.SubElement(req_element, "requiredInput", href=f"#{el1}")

        for cfd, _ in cfds:
            decision_element = ET.SubElement(
                root, "decision", id=f"{cfd}", name=f"{cfd}")
            for el1, el2 in decision_model:
                if el2 == cfd:
                    el_id = f"{el1}_req_{uuid.uuid4()}"
                    if el2 not in connected_elements:
                        connected_elements[el2] = []
                    connected_elements[el2].append(el_id)

                    req_element = ET.SubElement(
                        decision_element, "informationRequirement", id=el_id)
                    ET.SubElement(req_element, "requiredInput", href=f"#{el1}")

        # add all attributes
        for attribute in attributes:
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
        for decision, _ in decisions:
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

            new_id = el1
            for id in connected_elements[el2]:
                if f"{el1}" in id:
                    new_id = id

            edge = ET.SubElement(diagram, "dmndi:DMNEdge",
                                 dmnElementRef=f"{new_id}")
            ET.SubElement(edge, "di:waypoint",
                          x=f"{x1 + width/2}", y=f"{y1 + height}")
            ET.SubElement(edge, "di:waypoint",
                          x=f"{x2 + width/2}", y=f"{y2}")

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write("./uploads/result.dmn", encoding="utf-8")
        return
