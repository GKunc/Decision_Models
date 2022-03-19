export default function SetAttributesVisualisation(props) {
    return (
        props.attributes !== null ?
            props.attributes.map((element) => <div>{element}</div>)
            : <div>No data</div>
    )
}
