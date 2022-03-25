export default function SetAttributesVisualisation(props) {
    return (
        <div>
            <div>Let user set attributes of model and show found decisions</div>
            {
                props.attributes !== null ?
                    props.attributes.map((element) => <div className="font-bold">{element}</div>)
                    : <div className="underline">No data</div>
            }
        </div>
    )
}
