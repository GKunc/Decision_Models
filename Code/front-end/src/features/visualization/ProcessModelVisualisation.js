import { useEffect } from "react";
import BpmnJS from 'bpmn-js';

export default function ProcessModelVisualisation(props) {
    useEffect(() => {
        async function createBPMN() {
            var bpmnViewer = new BpmnJS({
                container: '#bpmn'
            });

            // import diagram
            try {
                await bpmnViewer.importXML(props.bpmn);
                bpmnViewer.get('canvas').zoom('fit-viewport', 'auto');
            } catch (err) {
                alert('could not import BPMN 2.0 XML, see console');
                console.error('could not import BPMN 2.0 diagram', err);
            }
        }
        if (props.bpmn)
            createBPMN();
    }, [props.bpmn]);

    return (
        props.bpmn !== null ?
            <div id='bpmn' className='flex w-[100%] min-h-[100%] items-center justify-center bg-white border rounded-md'></div>
            : <div className="underline">No data</div>
    )
}
