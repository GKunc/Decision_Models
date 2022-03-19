import { useState } from "react";
import FeatureBox from "./shared/FeatureBox";
import DecisionModelVisualisation from "./visualization/DecisionModelVisualisation";
import NodesModelVisualisation from "./visualization/NodesVisualisation";
import ProcessModelVisualisation from "./visualization/ProcessModelVisualisation";
import SetAttributesVisualisation from "./visualization/SetAttribute";

export default function SummaryScreen(props) {
    const [hiddenExample, setHiddenExample] = useState(null);
    const [hiddenNodes, setHiddenNodes] = useState(null);
    const [hiddenProcess, setHiddenProcess] = useState(null);
    const [hiddenDecision, setHiddenDecision] = useState(null);

    return (
        <div className='flex flex-auto items-center justify-center m-2'>
            <div className='flex flex-auto flex-row flex-wrap items-stretch h-full'>
                <FeatureBox title='Set Attributes' hidden={hiddenExample} content={
                    <SetAttributesVisualisation attributes={props.attributes} />
                } hideDelegate={() => setHiddenExample(true)} />

                <FeatureBox title='Nodes' hidden={hiddenNodes} content={
                    <NodesModelVisualisation nodes={props.nodes} />
                } hideDelegate={() => setHiddenNodes(true)} />

                <FeatureBox title='Process Model' hidden={hiddenProcess} content={
                    <ProcessModelVisualisation processModel={props.processModel} />
                }
                    hideDelegate={() => setHiddenProcess(true)} />

                <FeatureBox title='Decision Model' hidden={hiddenDecision} content={
                    <DecisionModelVisualisation decisionModel={props.decisionModel} />
                } hideDelegate={() => setHiddenDecision(true)} />
            </div>
        </div>
    )
}
