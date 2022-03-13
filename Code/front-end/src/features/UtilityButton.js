import React from 'react';

export default function UtilityButton(props) {
    return <div className="bg-green-500 hover:bg-green-600 rounded-md p-2 cursor-pointer" onClick={props.clickDelegate}>{props.text}</div>
}

