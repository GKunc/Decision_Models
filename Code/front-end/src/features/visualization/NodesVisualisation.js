export default function NodesModelVisualisation(props) {

    return (
        props.decisionNodes !== null && props.dataDecisions !== null && props.attributes !== null ?
            <div>
                <div className="border border-white">
                    {
                        props.decisionNodes.map((element) => <div>{element}</div>)
                    }
                </div>
                <div className="border border-white">
                    {
                        props.dataDecisions.map((element) => <div>{element}</div>)
                    }
                </div>
                <div className="border border-white">
                    {
                        props.attributes.map((element) => <div>{element}</div>)
                    }
                </div>

            </div> : <div>No data</div>
    )
}
