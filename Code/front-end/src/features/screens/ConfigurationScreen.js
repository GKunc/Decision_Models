import SwitchButton from "../shared/SwitchButton";

export default function ConfigurationScreen(props) {

    return (
        <div className="flex flex-col h-full overflow-hidden">
            <div className="flex items-center justify-between">
                <div className="text-xl m-2">Configuration</div>
                <div onClick={props.closeDelegate} className="bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
            </div>
            <div className={'flex flex-col h-full justify-center mt-5'}>
                <SwitchButton title="Attributes" isOff={props.hiddenExample} setIsOff={props.setHiddenExample} />
                <SwitchButton title="Nodes" isOff={props.hiddenNodes} setIsOff={props.setHiddenNodes} />
                <SwitchButton title="Process Model" isOff={props.hiddenProcess} setIsOff={props.setHiddenProcess} />
                <SwitchButton title="Decision Model" isOff={props.hiddenDecision} setIsOff={props.setHiddenDecision} />
            </div>
        </div>
    )
}