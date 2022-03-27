import { useEffect } from "react";
import FeatureBox from "../shared/FeatureBox";
import DecisionModelVisualisation from "../Visualization/DecisionModelVisualisation";
import NodesModelVisualisation from "../Visualization/NodesVisualisation";
import ProcessModelVisualisation from "../Visualization/ProcessModelVisualisation";
import SetAttributesVisualisation from "../Visualization/SetAttribute";

export default function SummaryScreen(props) {
    const calculateNumberOfBoxes = () => {
        let numberOfBoxes = 4
        if (props.hiddenExample) numberOfBoxes -= 1
        if (props.hiddenNodes) numberOfBoxes -= 1
        if (props.hiddenProcess) numberOfBoxes -= 1
        if (props.hiddenDecision) numberOfBoxes -= 1
        return numberOfBoxes
    }

    let numberOfBoxes = calculateNumberOfBoxes()

    return (
        <div className='flex flex-row flex-wrap items-stretch items-center justify-center max-h-screen w-full overflow-hidden content-containter'>
            <FeatureBox
                numberOfBoxes={numberOfBoxes}
                title='Set Attributes'
                hidden={props.hiddenExample}
                content={
                    < SetAttributesVisualisation attributes={props.attributes} />
                }
                hideDelegate={() => props.setHiddenExample(true)} />

            < FeatureBox
                numberOfBoxes={numberOfBoxes}
                title='Nodes'
                hidden={props.hiddenNodes}
                content={
                    < NodesModelVisualisation decisionNodes={props.decisionNodes} dataDecisions={props.dataDecisions} attributes={props.attributes} />
                }
                hideDelegate={() => props.setHiddenNodes(true)} />

            < FeatureBox
                numberOfBoxes={numberOfBoxes}
                title='Process Model'
                hidden={props.hiddenProcess}
                content={
                    < ProcessModelVisualisation processModel={props.processModel} />
                }
                hideDelegate={() => props.setHiddenProcess(true)} />

            < FeatureBox
                numberOfBoxes={numberOfBoxes}
                title='Decision Model'
                hidden={props.hiddenDecision}
                content={
                    < DecisionModelVisualisation decisionModel={props.decisionModel} />
                }
                hideDelegate={() => props.setHiddenDecision(true)} />
        </div >
    )
}
