
export default function FeatureBox(props) {
    return (
        <div className="relative flex flex-auto m-2 h-full">
            <div onClick={props.hideDelegate} className="absolute top-0 left-0 p-1 z-10 bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
            <div className="rounded-md m-1 p-4 border border-white bg-gray-900 min-w-[100%]">
                {props.content}
            </div>
        </div>
    );
}