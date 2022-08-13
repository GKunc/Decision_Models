import { useEffect } from "react";
import BpmnJS from 'bpmn-js/lib/Modeler';

import "bpmn-js/dist/assets/diagram-js.css";
import "bpmn-js/dist/assets/bpmn-js.css";
import "bpmn-js/dist/assets/bpmn-font/css/bpmn-embedded.css";

export default function ProcessModelVisualisation(props) {
    useEffect(async () => {
        function clearContainer() {
            document.getElementById('bpmn').innerHTML = "";
        }

        async function createBPMN() {
            var bpmnViewer = new BpmnJS({
                container: '#bpmn',
                keyboard: {
                    bindTo: window
                }
            });

            try {
                await bpmnViewer.importXML(props.bpmn);
                bpmnViewer.get('canvas').zoom('fit-viewport', 'auto');
            } catch (err) {
                console.error('could not import BPMN 2.0 diagram', err);
            }
        }
        if (props.bpmn)
            clearContainer()
        await createBPMN();
    }, [props.bpmn]);

    return (
        props.bpmn !== null ?
            <div id="bpmn-container" className='flex w-[100%] min-h-[100%] items-center justify-center bg-white border rounded-md'>
                <div id='bpmn' className='flex w-[100%] min-h-[100%] items-center justify-center bg-white border rounded-md'></div>
            </div>
            : <div className="underline">No data</div>
    )
}
