export default function ProcessModelVisualisation(props) {
    return (
        props.processModel !== null ?
            props.processModel.map((element) => <div>{element[0] + ' -> ' + element[1]}</div>)
            : <div className="underline">No data</div>
    )
}
