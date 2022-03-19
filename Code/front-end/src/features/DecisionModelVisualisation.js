import { useState } from "react";
import FeatureBox from "./FeatureBox";

export default function DecisionModelVisualisation(props) {
    const [hiddenExample, setHiddenExample] = useState(null);
    const [hiddenNodes, setHiddenNodes] = useState(null);
    const [hiddenProcess, setHiddenProcess] = useState(null);
    const [hiddenDecision, setHiddenDecision] = useState(null);

    return (
        <div className='h-full'>
            <div className='flex flex-row flex-wrap items-stretch h-full'>
                <div className={`grow basis-1/2 ${hiddenExample ? 'hidden' : ''}`}>
                    <FeatureBox content={
                        <div>
                            <div className="text-xl">Add Example</div>
                        </div>
                    } hideDelegate={() => setHiddenExample(true)} />
                </div>
                <div className={`grow basis-1/2 ${hiddenNodes ? 'hidden' : ''}`}>
                    <FeatureBox content={
                        <div>
                            <div className="text-xl">Nodes</div>
                        </div>
                    } hideDelegate={() => setHiddenNodes(true)} />
                </div>
                <div className={`grow basis-1/2 ${hiddenProcess ? 'hidden' : ''}`}>
                    <FeatureBox content={
                        <div className="h-full flex flex-col">
                            <div className="text-xl">Process Model</div>
                            <div className="flex flex-auto items-center justify-center">
                                {props.decision_model !== null ?
                                    props.decision_model.map((element) => <div>{element[0] + ' -> ' + element[1]}</div>)
                                    : <div>No data</div>
                                }
                            </div>
                        </div>
                    }
                        hideDelegate={() => setHiddenProcess(true)} />
                </div>
                <div className={`grow basis-1/2 ${hiddenDecision ? 'hidden' : ''}`}>
                    <FeatureBox content={
                        <div className="h-full flex flex-col">
                            <div className="text-xl">Decision Model</div>
                            <div className="flex flex-auto items-center justify-center">
                                {props.decision_model !== null ?
                                    props.decision_model.map((element) => <div>{element[0] + ' -> ' + element[1]}</div>)
                                    : <div>No data</div>
                                }
                            </div>
                        </div>
                    } hideDelegate={() => setHiddenDecision(true)} />
                </div>
            </div>
        </div>
    )
}
