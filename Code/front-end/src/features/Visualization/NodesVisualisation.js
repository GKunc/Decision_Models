import React, { useEffect } from 'react';

export default function NodesModelVisualisation(props) {
    useEffect(() => {
        console.log(props.decisionNodes)
        console.log(props.dataDecisions)
        console.log(props.attributes)
    })

    return (

        props.decisionNodes !== null && props.dataDecisions !== null && props.attributes !== null ?
            <div className='w-[100%] flex-wrap'>
                <div className="p-2 flex items-center border border-dashed border-white">
                    <div className="w-[200px]">Attributes</div>

                    {
                        React.Children.toArray(props.attributes.map((element) => <div className="m-1 p-1 border border-white">{element}</div>))
                    }
                </div>
                <div className="p-2 flex items-center border border-dashed border-white">
                    <div className="w-[200px]">Data Decisions</div>
                    {
                        React.Children.toArray(props.decisionNodes.map((element) => <div className="m-1 p-1 border border-white">{element}</div>))
                    }
                </div>
                <div className="p-2 flex items-center border border-dashed border-white">
                    <div className="w-[200px]">Control flow decisions</div>
                    {
                        React.Children.toArray(props.dataDecisions.map((element) => <div className="m-1 p-1 border border-white">{element}</div>))
                    }
                </div>

            </div>
            : <div className="underline">No data</div>

    )
}
