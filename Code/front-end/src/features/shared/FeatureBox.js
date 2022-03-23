import Spinner from "./Spinner";

export default function FeatureBox(props) {
    return (
        <div className={`relative flex flex-row flex-auto m-2 basis-1/3 ${props.hidden ? 'hidden' : ''}`}>
            <div onClick={props.hideDelegate} className="absolute top-0 left-0 p-1 z-2 bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
            <div className="rounded-md m-1 p-4 border border-white bg-gray-900 h-full min-w-[100%]">
                <div className="text-xl">{props.title}</div>
                {
                    <div className="flex flex-col items-center justify-center h-full">
                        {props.content}
                    </div>
                }
            </div>
        </div>
    );
}