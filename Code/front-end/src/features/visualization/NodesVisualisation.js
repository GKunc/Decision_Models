export default function NodesModelVisualisation(props) {

    return (
        props.decisionNodes !== null && props.dataDecisions !== null && props.attributes !== null ?
            <div>
                <div className="p-2 flex items-center border border-dashed border-white">
                    <div className="w-[200px]">Attributes</div>
                    {
                        props.decisionNodes.map((element) => <div className="m-1 p-1 border border-white">{element}</div>)
                    }
                </div>
                <div className="p-2 flex items-center border border-dashed border-white">
                    <div className="w-[200px]">Control flow decisions</div>
                    {
                        props.dataDecisions.map((element) => <div className="m-1 p-1 border border-white">{element}</div>)
                    }
                </div>
                <div className="p-2 flex items-center border border-dashed border-white">
                    <div className="w-[200px]">Data Decisions</div>

                    {
                        props.attributes.map((element) => <div className="m-1 p-1 border border-white">{element}</div>)
                    }
                </div>

            </div>
            : <div className="underline">No data</div>

    )
}
