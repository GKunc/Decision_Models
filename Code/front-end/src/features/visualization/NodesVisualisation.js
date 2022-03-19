export default function NodesModelVisualisation(props) {
    return (
        props.nodes !== null ?
            props.nodes.map((element) => <div>{element}</div>)
            : <div>No data</div>
    )
}
