import React, { useState } from 'react';
import SummaryScreen from './features/SummaryScreen';
import UtilityBar from './features/UtilityBar';

export default function App(props) {
  const [file, setFile] = useState(null);
  const [attributes, setAttributes] = useState(null);
  const [nodes, setNodes] = useState(null);
  const [processModel, setProcessModel] = useState(null);
  const [decisionModel, setDecisionModel] = useState(null);

  return (
    <div className="bg-gray-800 flex flex-col h-full overflow-hidden text-white">
      <UtilityBar />
      <SummaryScreen attributes={attributes} nodes={nodes} processModel={processModel} decisionModel={decisionModel} />
    </div>
  );
}