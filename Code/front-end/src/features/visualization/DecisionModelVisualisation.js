import cytoscape from 'cytoscape'
import { useEffect } from 'react';

export default function DecisionModelVisualisation(props) {
    useEffect(() => {
        const addAllNodes = (cy) => {
            let allNodes = []
            props.decisionModel.forEach(elements => {
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
            props.decisionModel.forEach((element, id) => {
                cy.add({ group: 'edges', data: { id: 'e' + id, source: element[0], target: element[1] } })
            });
        }

        if (props.decisionModel) {
            var cy = cytoscape({
                container: document.getElementById('cy'),
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
                ]
            })

            addAllNodes(cy)
            addAllConnections(cy)
            cy.layout({ name: 'cose' }).run();
        }
    }, [props.decisionModel]);


    return (
        props.decisionModel !== null ?
            <div id='cy' className='flex w-[100%] min-h-[80%]'></div>
            : <div className="underline">No data</div>
    )
}
