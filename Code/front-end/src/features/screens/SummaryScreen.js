import FeatureBox from "../shared/FeatureBox";
import DecisionModelVisualisation from "../Visualization/DecisionModelVisualisation";
import DecisionRulesVisualisation from "../Visualization/DecisionRulesVisualisation";
import NodesModelVisualisation from "../Visualization/NodesVisualisation";
import ProcessModelVisualisation from "../Visualization/ProcessModelVisualisation";

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
                title='Decision Rules'
                hidden={props.hiddenExample}
                content={
                    < DecisionRulesVisualisation decisionRules={props.decisionRules} />
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
                    < ProcessModelVisualisation bpmn={props.bpmn} />
                }
                hideDelegate={() => props.setHiddenProcess(true)} />

            < FeatureBox

                numberOfBoxes={numberOfBoxes}
                title='Decision Model'
                hidden={props.hiddenDecision}
                content={
                    <div id="decision-model" className="flex w-[100%] min-h-[100%] justify-center">
                        < DecisionModelVisualisation decisionModel={props.decisionModel} />
                    </div>
                }
                hideDelegate={() => props.setHiddenDecision(true)} />
        </div >
    )
}
