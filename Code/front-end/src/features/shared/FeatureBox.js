
export default function FeatureBox(props) {
    return (
        <div className={`relative box-border flex flex-row flex-auto m-2 basis-1/3 min-w-[40%] ${props.hidden ? 'hidden' : ''} ${props.numberOfBoxes <= 2 ? 'h-[96%]' : 'h-[45%]'}`}>
            <div onClick={props.hideDelegate} className="absolute -top-[4px] -right-[5px] z-2 bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
            <div className="flex flex-col box-border rounded-md m-1 p-4 border border-white bg-gray-900 h-full w-full overflow-scroll box-border">
                <div className="text-xl mb-2">{props.title}</div>
                {
                    <div className="flex flex-col items-center justify-center h-full mt-3 box-border">
                        {props.content}
                    </div>
                }
            </div>
        </div>
    );
}