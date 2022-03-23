import React, { useState } from 'react';
import UtilityBar from './features/UtilityBar';
import ReactModal from 'react-modal';
import SummaryScreen from './features/sreens/SummaryScreen';
import FileUploadScreen from './features/sreens/FileUploadScreen';
import ConfigurationScreen from './features/sreens/ConfigurationScreen';

export default function App(props) {
  const [attributes, setAttributes] = useState(null)
  const [nodes, setNodes] = useState(null)
  const [processModel, setProcessModel] = useState(null)
  const [decisionModel, setDecisionModel] = useState([])

  const [openModal, setOpenModal] = React.useState(false)
  const [openUpload, setOpenUpload] = React.useState(false)
  const [openConfig, setOpenConfig] = React.useState(false)

  function setDecisionModelFun(dec) {
    console.log("DECISION")
    setDecisionModel(dec)
  }

  function closeModal() {
    console.log(decisionModel)
    setOpenModal(false)
  }

  function openUploadFileModal() {
    setOpenUpload(true)
    setOpenConfig(false)

    setOpenModal(true)
  }

  function openConfigModal() {
    setOpenUpload(false)
    setOpenConfig(true)
    console.log(decisionModel)
    setOpenModal(true)
  }

  function modalContent() {
    if (openUpload) {
      return <FileUploadScreen
        setAttributes={setAttributes}
        setNodes={setNodes}
        setProcessModel={setProcessModel}
        setDecisionModel={setDecisionModelFun}
        closeModal={closeModal} />
    }
    if (openConfig) {
      return <ConfigurationScreen />
    }
  }

  return (
    <div id='app' className="bg-gray-800 flex flex-col h-full overflow-hidden text-white">
      <UtilityBar openUploadFileModalClick={openUploadFileModal} openConfigurationModalClick={openConfigModal} />
      <SummaryScreen attributes={attributes} nodes={nodes} processModel={processModel} decisionModel={decisionModel} />

      <ReactModal
        appElement={document.getElementById('app')}
        isOpen={openModal}
        contentLabel="Example Modal"
        style={{ overlay: {}, content: { background: 'rgb(31 41 55 / 1', color: 'white', width: '50%', height: '50%', top: '25%', left: '25%', } }}
        centered
      >

        <div onClick={closeModal} className="absolute z-100 top-2 left-2 p-1 z-2 bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
        {modalContent()}
      </ReactModal>
    </div >
  );
}