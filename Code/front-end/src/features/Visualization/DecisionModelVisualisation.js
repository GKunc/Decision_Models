import { useEffect } from "react";
import DmnJS from 'dmn-js/lib/Modeler';

import "dmn-js/dist/assets/diagram-js.css";
import "dmn-js/dist/assets/dmn-font/css/dmn-embedded.css";
import "dmn-js/dist/assets/dmn-js-decision-table.css";
import "dmn-js/dist/assets/dmn-js-literal-expression.css";
import "dmn-js/dist/assets/dmn-js-shared.css";

export default function DecisionModelVisualisation(props) {
    useEffect(async () => {
        function clearContainer() {
            document.getElementById('dmn').innerHTML = "";
        }

        async function createDMN() {
            const dmnModeler = new DmnJS({
                container: '#dmn',
                keyboard: {
                    bindTo: window
                }
            });

            try {
                await dmnModeler.importXML(props.dmn);
                const activeEditor = dmnModeler.getActiveViewer();
                const canvas = activeEditor.get('canvas');
                canvas.zoom('fit-viewport', 'auto');

            } catch (err) {
                console.error('could not import DMN 1.3 diagram', err);
            }
        }

        if (props.dmn)
            clearContainer();
        await createDMN();

    }, [props.dmn]);

    return (
        props.dmn !== null ?
            <div id="dmn-container" className='flex w-[100%] min-h-[100%] items-center justify-center bg-white border rounded-md'>
                <div id='dmn' className='flex w-[100%] min-h-[100%] items-center justify-center bg-white border rounded-md'></div>
            </div>
            : <div className="underline">No data</div>
    )
}
