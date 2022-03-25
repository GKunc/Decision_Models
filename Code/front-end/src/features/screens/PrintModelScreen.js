export default function PrintModelScreen(props) {

    return (
        <div className="flex flex-col h-full overflow-hidden">
            <div className="flex items-center justify-between">
                <div className="text-xl m-2">Print Model</div>
                <div onClick={props.closeDelegate} className="bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
            </div>
            <div className={'flex flex-col h-full justify-center m-2 mt-5'}>

            </div>
        </div>
    )
}