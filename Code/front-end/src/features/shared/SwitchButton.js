
export default function SwitchButton(props) {
    const change = () => {
        props.setIsOff(!props.isOff)
    }

    return (
        props.isOff ?
            <div className="flex flex-row items-center justify-between m-1">
                {props.title}
                <div onClick={change} className="cursor-pointer flex items-center w-[40px] h-[20px] rounded-full ml-2 h-[18px] bg-slate-400">
                    <div className="bg-white w-[18px] h-[18px] rounded-full ml-[1px]"></div>
                </div>
            </div>
            : <div className="flex flex-row items-center justify-between m-1">
                {props.title}
                <div onClick={change} className="cursor-pointer flex items-center justify-end w-[40px] h-[20px] rounded-full ml-2 h-[18px] bg-green-500">
                    <div className="bg-white w-[18px] h-[18px] rounded-full ml-[1px]"></div>
                </div>
            </div>
    );
}