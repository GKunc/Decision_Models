import React from 'react';

export default function DecisionRulesVisualisation(props) {
    return (
        <div className='flex flex-col w-[100%]'>
            {
                props.decisionRules !== null ?
                    React.Children.toArray(props.decisionRules.map((element) => <div className="flex items-center p-2 font-bold border border-white h-10 w-full">{element}</div>))
                    : <div className="underline">No data</div>
            }
        </div>
    )
}
