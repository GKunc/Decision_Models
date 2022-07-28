import { useEffect } from "react";
import DmnJS from 'dmn-js';

export default function DecisionModelVisualisation(props) {
    useEffect(() => {
        function clearContainer() {
            document.getElementById('dmn').innerHTML = "";
        }

        async function createDMN() {
            console.log(props.dmn)

            const dmnViewer = new DmnJS({
                container: '#dmn'
            });

            try {
                await dmnViewer.importXML(props.dmn);
                const activeEditor = dmnViewer.getActiveViewer();
                const canvas = activeEditor.get('canvas');
                canvas.zoom('fit-viewport');
            } catch (err) {
                console.error('could not import DMN 1.3 diagram', err);
            }

        }

        if (props.dmn)
            clearContainer();
        createDMN();

    }, [props.dmn]);

    return (
        props.dmn !== null ?
            <div id="dmn-container" className='flex w-[100%] min-h-[100%] items-center justify-center bg-white border rounded-md'>
                <div id='dmn' className='flex w-[100%] min-h-[100%] items-center justify-center bg-white border rounded-md'></div>
            </div>
            : <div className="underline">No data</div>
    )
}
