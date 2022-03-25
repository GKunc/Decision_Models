import SwitchButton from "../shared/SwitchButton";

export default function ConfigurationScreen(props) {

    return (
        <div className="flex flex-col h-full overflow-hidden">
            <div className="text-xl m-2">Configuration</div>
            <div className={'flex flex-col h-full justify-center m-2 mt-5'}>
                <SwitchButton title="Attributes" isOff={props.hiddenExample} setIsOff={props.setHiddenExample} />
                <SwitchButton title="Nodes" isOff={props.hiddenNodes} setIsOff={props.setHiddenNodes} />
                <SwitchButton title="Process Model" isOff={props.hiddenProcess} setIsOff={props.setHiddenProcess} />
                <SwitchButton title="Decision Model" isOff={props.hiddenDecision} setIsOff={props.setHiddenDecision} />
            </div>
        </div>
    )
}