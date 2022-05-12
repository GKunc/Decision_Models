export default function ErrorBox(props) {
    return (
        // <div className={`flex justify-between items-center rounded-md bg-red-600 mt-1 mb-1 p-1 ${props.errorMessage ? '' : 'hidden'}`}>
        <div className={`flex justify-between items-center rounded-md bg-red-600 mt-1 mb-1 p-1 hidden`}>
            <div>{props.errorMessage}</div>
            <div onClick={props.resetError} className='flex justify-center items-center rounded-md cursor-pointer hover:bg-red-700 w-[32px] h-[32px]'>X</div>
        </div>
    );
}