import UtilityButton from "./UtilityButton";

export default function Error(props) {
    return (
        <div className='h-full flex flex-col items-center justify-center font-sans'>
            <div className='flex flex-col items-center justify-center h-full'>
                <div className="error">X</div>
            </div>
            <div className="text-2xl">Error Occourd!</div>
            <UtilityButton text={'Try again'} clickDelegate={props.resetScreen} />
        </div>
    );
}