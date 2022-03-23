import React, { useState } from 'react';
import UtilityBar from './features/UtilityBar';
import ReactModal from 'react-modal';
import SummaryScreen from './features/sreens/SummaryScreen';
import FileUploadScreen from './features/sreens/FileUploadScreen';
import ConfigurationScreen from './features/sreens/ConfigurationScreen';

export default function App(props) {
  const [attributes, setAttributes] = useState(null)
  const [decisionNodes, setDecisionNodes] = useState(null)
  const [dataDecisions, setDataDecisions] = useState(null)
  const [processModel, setProcessModel] = useState(null)
  const [decisionModel, setDecisionModel] = useState(null)

  const [openModal, setOpenModal] = React.useState(false)
  const [openUpload, setOpenUpload] = React.useState(false)
  const [openConfig, setOpenConfig] = React.useState(false)

  function closeModal() {
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
        setDecisionNodes={setDecisionNodes}
        setDataDecisions={setDataDecisions}
        setProcessModel={setProcessModel}
        setDecisionModel={setDecisionModel}
        decisionModel={decisionModel}
        closeModal={closeModal} />
    }
    if (openConfig) {
      return <ConfigurationScreen />
    }
  }

  function saveToFile() {
    alert("saveToFile")
  }

  function readFromFile() {
    alert("readFromFile")
  }

  function printModel() {
    alert("printModel")
  }

  return (
    <div id='app' className="bg-gray-800 flex flex-col h-full overflow-auto text-white">
      <UtilityBar
        openUploadFileModalClick={openUploadFileModal}
        openConfigurationModalClick={openConfigModal}
        saveToFile={saveToFile}
        readFromFile={readFromFile}
        printModel={printModel} />
      <SummaryScreen attributes={attributes} decisionNodes={decisionNodes} dataDecisions={dataDecisions} processModel={processModel} decisionModel={decisionModel} />

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