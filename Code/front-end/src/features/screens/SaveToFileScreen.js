import { useState } from "react";
import UtilityButton from "../shared/UtilityButton";
import { saveAs } from 'file-saver';

export default function SaveToFileScreen(props) {
    const [bpmnFileName, setBpmnFileName] = useState('bpmn')
    const [dmnFileName, setDmnFileName] = useState('dmn')

    const saveBpmnToFile = () => {
        var bpmnModel = new Blob([props.bpmn], { type: "text/xml" });
        saveAs(bpmnModel, `${bpmnFileName}.bpmn`);
    }

    const saveDmnToFile = () => {
        var dmnModel = new Blob([props.dmn], { type: "text/xml" });
        saveAs(dmnModel, `${dmnFileName}.dmn`);
    }

    return (
        <div className="flex flex-col h-full overflow-hidden">
            <div className="flex items-center justify-between">
                <div className="text-xl m-2">Save To File</div>
                <div onClick={props.closeDelegate} className="bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
            </div>
            <div className={'flex flex-col h-full justify-center m-2 mt-5'}>
                <div className="flex w-full mb-2 items-center">
                    <div className="w-[150px]">BPMN file name:</div>
                    <div className="m-2">
                        <input
                            className="w-[200px] h-full rounded-md text-black p-1"
                            type="text"
                            value={bpmnFileName}
                            onChange={(e) => setBpmnFileName(e.target.value)} />
                    </div>
                    <UtilityButton text="Save" clickDelegate={saveBpmnToFile} />
                </div>
                <div className="flex w-full mb-2 items-center">
                    <div className="w-[150px]">DMN file name:</div>
                    <div className="m-2">
                        <input
                            className="w-[200px] h-full rounded-md text-black p-1"
                            type="text"
                            value={dmnFileName}
                            onChange={(e) => setDmnFileName(e.target.value)} />
                    </div>
                    <UtilityButton text="Save" clickDelegate={saveDmnToFile} />
                </div>
                <a href="none" id="fileHook" className="hidden">x</a>
            </div>
        </div>
    )
}