import cytoscape from 'cytoscape'
import { useEffect } from 'react';

export default function DecisionModelVisualisation(props) {
    useEffect(() => {
        var cy = cytoscape({
            container: document.getElementById('cy'), // container to render in
            elements: [
                {
                    data: { id: 'a' }
                },
                {
                    data: { id: 'b' }
                },
                {
                    data: { id: 'ab', source: 'a', target: 'b' }
                }
            ],
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#666',
                        'label': 'data(id)',
                        'color': 'white'
                    }
                },

                {
                    selector: 'edge',
                    style: {
                        'width': 3,
                        'line-color': '#ccc',
                        'target-arrow-color': '#ccc',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier'
                    }
                }
            ],

            layout: {
                name: 'grid',
                rows: 1
            }

        });
    }, []);

    return (
        <div id='cy' className='flex w-[100%] min-h-[80%]'></div>
        // props.decisionModel !== null ?
        // props.decisionModel.map((element) => <div>{element[0] + ' -> ' + element[1]}</div>)
        // : <div className="underline">No data</div>
    )
}
