import React, { useEffect, useState } from 'react';

export default function DecisionRulesVisualisation(props) {
    const [decisionAttributes, setDecisionAttributes] = useState(null)
    const [decisionRules, setDecisionRules] = useState([])
    const [expandedRow, setExpandedRow] = useState(null)

    useEffect(() => {
        const attributes = []
        const rules = []
        if (props.decisionRules) {
            props.decisionRules.forEach(rule => {
                attributes.push(rule[0])
                rules.push(rule)
            });
            const uniqueAttributes = [...new Set(attributes)];
            setDecisionAttributes(uniqueAttributes)
        }
    }, [props.decisionRules]);

    function clickedExpand(element) {
        const expandedElements = []
        if (element === expandedRow && decisionRules.length !== 0) {
            setDecisionRules([])
        } else {
            setExpandedRow(element)
            props.decisionRules.forEach(rule => {
                if (rule[0] === element) {
                    expandedElements.push(rule[1])
                }
            })
            setDecisionRules(expandedElements)
        }
    }

    return (
        <div className='flex flex-col w-[100%] items-center pt-8 pb-8'>
            {
                decisionAttributes !== null && decisionRules ?
                    React.Children.toArray(decisionAttributes.map((element) =>
                        <table className='"border-collapse w-[100%]"'>
                            <tr className='w-[100%] border border-slate-500 bg-white text-black'>
                                <td className='flex w-[100%] p-2 cursor-pointer border border-white' onClick={() => clickedExpand(element)}>
                                    {element}
                                    {
                                        decisionRules.length > 0 && expandedRow === element ?
                                            <span class="material-symbols-outlined">
                                                expand_more
                                            </span>
                                            :
                                            <span class="material-symbols-outlined">
                                                chevron_right
                                            </span>
                                    }
                                </td>
                                {
                                    decisionRules !== null && expandedRow === element ?
                                        React.Children.toArray(decisionRules.map((rule) =>
                                            <td className='flex w-[100%] p-2 cursor-pointer border border-white bg-black text-white'>
                                                {rule}
                                            </td>
                                        ))
                                        : ''
                                }
                            </tr>
                        </table>))
                    : <div className="underline">No data</div>
            }
        </div>
    )
}
