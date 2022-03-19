export default function DecisionModelVisualisation(props) {
    return (
        props.decisionModel !== null ?
            props.decisionModel.map((element) => <div>{element[0] + ' -> ' + element[1]}</div>)
            : <div>No data</div>
    )
}
