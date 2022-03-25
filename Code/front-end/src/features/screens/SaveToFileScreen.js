import { useState } from "react";
import UtilityButton from "../shared/UtilityButton";

export default function SaveToFileScreen(props) {
    const [fileName, setFileName] = useState('decision_model')

    const saveToFile = () => {
        let a = document.getElementById("fileHook");
        const text = JSON.stringify(
            {
                "decision model": props.decisionModel
            })
        const file = new Blob([text], { type: 'application/json' });
        a.href = URL.createObjectURL(file);
        a.download = fileName + '.json';
        a.click()
    }

    return (
        <div className="flex flex-col h-full overflow-hidden">
            <div className="flex items-center justify-between">
                <div className="text-xl m-2">Save To File</div>
                <div onClick={props.closeDelegate} className="bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
            </div>
            <div className={'flex flex-col h-full justify-center m-2 mt-5'}>
                <div className="flex w-full mb-2 items-center">
                    <div className="w-[100px]">File name:</div>
                    <div>
                        <input
                            className="w-[200px] h-full rounded-md text-black p-1"
                            type="text"
                            value={fileName}
                            onChange={(e) => setFileName(e.target.value)} />
                    </div>
                </div>
                <a href="" id="fileHook"></a>
                <UtilityButton text="Save" clickDelegate={saveToFile} />
            </div>
        </div>
    )
}