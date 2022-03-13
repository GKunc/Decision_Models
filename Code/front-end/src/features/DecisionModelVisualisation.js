export default function DecisionModelVisualisation(props) {

    return (
        <div className='h-full'>
            <div className='flex flex-col items-center justify-center h-full'>
                {
                    props.decision_model.map((element) => <div>{element[0] + ' -> ' + element[1]}</div>)
                }
            </div>
        </div>
    )
}
