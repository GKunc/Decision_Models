import xml.etree.cElementTree as ET


class DMNCreator:
    def apply(self, decisions, cfds, attributes, decision_model):
        print("++++++++++++")
        print(decisions)
        print(cfds)
        print(attributes)
        print(decision_model)
        print("++++++++++++")

        root = ET.Element(
            "definitions", xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/")
        root.attrib["xmlns:dmndi"] = "https://www.omg.org/spec/DMN/20191111/DMNDI/"
        root.attrib["xmlns:di"] = "http://www.omg.org/spec/DMN/20180521/DI/"

        # add all decisions
        # create decision
        # add dependend features
        for decision, reqs in decisions:
            decision_element = ET.SubElement(
                root, "decision", id=f"{decision}", name=f"{decision}")
            for req in reqs:
                req_element = ET.SubElement(
                    decision_element, "informationRequirement", id=f"{req}_req")
                ET.SubElement(req_element, "requiredInput", href=f"{req}")

        for cfd, reqs in cfds:
            decision_element = ET.SubElement(
                root, "decision", id=f"{cfd}", name=f"{cfd}")
            for req in reqs:
                req_element_cfd = ET.SubElement(
                    decision_element, "informationRequirement", id=f"{req}_req")
                ET.SubElement(req_element_cfd, "requiredInput", href=f"{req}")

        decision = ET.SubElement(
            root, "decision", id="Decision", name="Decision")
        req = ET.SubElement(decision, "informationRequirement", id="Info1")
        ET.SubElement(req, "requiredInput", href="Input1")

        req2 = ET.SubElement(decision, "informationRequirement", id="Info2")
        ET.SubElement(req2, "requiredInput", href="Input2")

        # add all attributes
        for attribute in attributes:
            ET.SubElement(root, "inputData",
                          id=f'{attribute.replace(" ", "")}', name=f'{attribute}')

        ET.SubElement(root, "inputData", id="Input1", name="Input 1 XD")
        ET.SubElement(root, "inputData", id="Input2", name="Input 2")

        dmnDI = ET.SubElement(root, "dmndi:DMNDI")
        diagram = ET.SubElement(dmnDI, "dmndi:DMNDiagram", id="Diagram")
        shape1 = ET.SubElement(diagram, "dmndi:DMNShape",
                               dmnElementRef="Decision")
        ET.SubElement(shape1, "dc:Bounds", height="80",
                      width="180", x="270", y="260")

        shape2 = ET.SubElement(diagram, "dmndi:DMNShape",
                               dmnElementRef="Input1")
        ET.SubElement(shape2, "dc:Bounds", height="45",
                      width="125", x="407", y="118")

        shape3 = ET.SubElement(diagram, "dmndi:DMNShape",
                               dmnElementRef="Input2")
        ET.SubElement(shape3, "dc:Bounds", height="45",
                      width="125", x="158", y="119")

        edge1 = ET.SubElement(diagram, "dmndi:DMNEdge",
                              dmnElementRef="Info1")
        ET.SubElement(edge1, "di:waypoint", x="221", y="164")
        ET.SubElement(edge1, "di:waypoint", x="330", y="240")
        ET.SubElement(edge1, "di:waypoint", x="330", y="260")

        edge2 = ET.SubElement(diagram, "dmndi:DMNEdge",
                              dmnElementRef="Info2")
        ET.SubElement(edge2, "di:waypoint", x="470", y="163")
        ET.SubElement(edge2, "di:waypoint", x="390", y="240")
        ET.SubElement(edge2, "di:waypoint", x="390", y="260")

        tree = ET.ElementTree(root)
        tree.write("./uploads/result.dmn")
        return
