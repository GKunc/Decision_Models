import React from 'react';

export default function UtilityButton(props) {
    return <button
        className={`flex justify-center rounded-md p-2 ${props.disabled ? 'bg-slate-400' : 'bg-green-500 hover:bg-green-600 cursor-pointer'}`}
        onClick={props.clickDelegate}
        disabled={props.disabled}>
        {props.text}
    </button>
}

