import FeatureBox from "../shared/FeatureBox";
import DecisionModelVisualisation from "../Visualization/DecisionModelVisualisation";
import NodesModelVisualisation from "../Visualization/NodesVisualisation";
import ProcessModelVisualisation from "../Visualization/ProcessModelVisualisation";
import SetAttributesVisualisation from "../Visualization/SetAttribute";

export default function SummaryScreen(props) {

    return (
        <div className='flex-1 flex flex-row flex-wrap items-stretch items-center justify-center m-2 '>
            <FeatureBox title='Set Attributes' hidden={props.hiddenExample} content={
                < SetAttributesVisualisation attributes={props.attributes} />
            } hideDelegate={() => props.setHiddenExample(true)} />

            < FeatureBox title='Nodes' hidden={props.hiddenNodes} content={
                < NodesModelVisualisation decisionNodes={props.decisionNodes} dataDecisions={props.dataDecisions} attributes={props.attributes} />
            } hideDelegate={() => props.setHiddenNodes(true)} />

            < FeatureBox title='Process Model' hidden={props.hiddenProcess} content={
                < ProcessModelVisualisation processModel={props.processModel} />
            }
                hideDelegate={() => props.setHiddenProcess(true)} />

            < FeatureBox title='Decision Model' hidden={props.hiddenDecision} content={
                < DecisionModelVisualisation decisionModel={props.decisionModel} />
            } hideDelegate={() => props.setHiddenDecision(true)} />
        </div >
    )
}
