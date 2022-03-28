import React from 'react';

export default function DecisionRulesVisualisation(props) {
    return (
        <div>
            {
                props.decisionRules !== null ?
                    React.Children.toArray(props.decisionRules.map((element,) => <div key="${}" className="font-bold">{element}</div>))
                    : <div className="underline">No data</div>
            }
        </div>
    )
}
