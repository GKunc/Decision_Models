import { useState } from "react";
import FeatureBox from "../shared/FeatureBox";
import DecisionModelVisualisation from "../Visualization/DecisionModelVisualisation";
import NodesModelVisualisation from "../Visualization/NodesVisualisation";
import ProcessModelVisualisation from "../Visualization/ProcessModelVisualisation";
import SetAttributesVisualisation from "../Visualization/SetAttribute";

export default function SummaryScreen(props) {
    const [hiddenExample, setHiddenExample] = useState(null);
    const [hiddenNodes, setHiddenNodes] = useState(null);
    const [hiddenProcess, setHiddenProcess] = useState(null);
    const [hiddenDecision, setHiddenDecision] = useState(null);


    return (
        <div className='flex flex-auto flex-row flex-wrap items-stretch items-center justify-center m-2 h-full'>
            <FeatureBox title='Set Attributes' hidden={hiddenExample} content={
                <SetAttributesVisualisation attributes={props.attributes} />
            } hideDelegate={() => setHiddenExample(true)} />

            <FeatureBox title='Nodes' hidden={hiddenNodes} content={
                <NodesModelVisualisation decisionNodes={props.decisionNodes} dataDecisions={props.dataDecisions} attributes={props.attributes} />
            } hideDelegate={() => setHiddenNodes(true)} />

            <FeatureBox title='Process Model' hidden={hiddenProcess} content={
                <ProcessModelVisualisation processModel={props.processModel} />
            }
                hideDelegate={() => setHiddenProcess(true)} />

            <FeatureBox title='Decision Model' hidden={hiddenDecision} content={
                <DecisionModelVisualisation decisionModel={props.decisionModel} />
            } hideDelegate={() => setHiddenDecision(true)} />
        </div>
    )
}
