import { useEffect } from "react";
import cytoscape from 'cytoscape'

export default function ProcessModelVisualisation(props) {
    useEffect(() => {
        if (props.processModel) {
            const cy = cytoscape({
                container: document.getElementById('cy-process-model'),
                elements: [
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
                    name: 'breadthfirst',
                }

            })

            addAllNodes(cy)
            addAllConnections(cy)
            cy.layout({ name: 'cose' }).run();
        }
    }, [props.processModel]);

    const addAllNodes = (cy) => {
        let allNodes = []
        props.processModel.forEach(elements => {
            elements.forEach(element => {
                allNodes.push(element)
            })
        });

        allNodes = [...new Set(allNodes)]

        allNodes.forEach(element => {
            cy.add({
                group: 'nodes',
                data: { id: element }
            })
        });
    }

    const addAllConnections = (cy) => {
        props.processModel.forEach((element, id) => {
            cy.add({ group: 'edges', data: { id: 'e' + id, source: element[0], target: element[1] } })
        });
    }

    return (
        props.processModel !== null ?
            <div id='cy-process-model' className='flex w-[100%] min-h-[80%]'></div>
            : <div className="underline">No data</div>
    )
}
//     return (
//         props.processModel !== null ?
//             props.processModel.map((element) => <div>{element[0] + ' -> ' + element[1]}</div>)
//             : <div className="underline">No data</div>
//     )
// }
