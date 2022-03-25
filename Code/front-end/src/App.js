import React, { useState } from 'react';
import UtilityBar from './features/UtilityBar';
import ReactModal from 'react-modal';
import SummaryScreen from './features/screens/SummaryScreen';
import FileUploadScreen from './features/screens/FileUploadScreen';
import ConfigurationScreen from './features/screens/ConfigurationScreen';
import SaveToFileScreen from './features/screens/SaveToFileScreen';

export default function App(props) {
  const [modalWidth, setModalWidth] = useState(null)
  const [modalHeight, setModalHeight] = useState(null)
  const [openModal, setOpenModal] = useState(false)

  const [openUpload, setOpenUpload] = useState(false)
  const [openConfig, setOpenConfig] = useState(false)
  const [openSaveToFile, setOpenSaveToFile] = useState(false)

  const [attributes, setAttributes] = useState(null)
  const [decisionNodes, setDecisionNodes] = useState(null)
  const [dataDecisions, setDataDecisions] = useState(null)
  const [processModel, setProcessModel] = useState(null)
  const [decisionModel, setDecisionModel] = useState(null)

  const [hiddenExample, setHiddenExample] = useState(null);
  const [hiddenNodes, setHiddenNodes] = useState(null);
  const [hiddenProcess, setHiddenProcess] = useState(null);
  const [hiddenDecision, setHiddenDecision] = useState(null);

  function closeModal() {
    setOpenModal(false)
  }

  function openUploadFileModal() {
    setModalWidth('50%')
    setModalHeight('400px')
    setOpenUpload(true)
    setOpenConfig(false)
    setOpenSaveToFile(false)

    setOpenModal(true)
  }

  function openConfigModal() {
    setModalWidth('20%')
    setModalHeight('250px')
    setOpenUpload(false)
    setOpenConfig(true)
    setOpenSaveToFile(false)

    setOpenModal(true)
  }

  function openSaveToFileModal() {
    setModalWidth('360px')
    setModalHeight('200px')
    setOpenUpload(false)
    setOpenConfig(false)
    setOpenSaveToFile(true)

    setOpenModal(true)
  }

  function openPrintModelModal() {
    window.print()
  }

  function modalContent() {
    if (openUpload) {
      return <FileUploadScreen
        closeDelegate={closeModal}

        setAttributes={setAttributes}
        setDecisionNodes={setDecisionNodes}
        setDataDecisions={setDataDecisions}
        setProcessModel={setProcessModel}
        setDecisionModel={setDecisionModel}
        decisionModel={decisionModel}
        closeModal={closeModal} />
    }
    if (openConfig) {
      return <ConfigurationScreen
        closeDelegate={closeModal}

        hiddenExample={hiddenExample}
        setHiddenExample={setHiddenExample}

        hiddenNodes={hiddenNodes}
        setHiddenNodes={setHiddenNodes}

        hiddenProcess={hiddenProcess}
        setHiddenProcess={setHiddenProcess}

        hiddenDecision={hiddenDecision}
        setHiddenDecision={setHiddenDecision} />
    }
    if (openSaveToFile) {
      return <SaveToFileScreen
        closeDelegate={closeModal}
        decisionModel={decisionModel} />
    }
  }

  return (
    <div id='app' className="bg-gray-800 flex-col flex items-stretch h-full overflow-auto text-white">
      <UtilityBar
        openUploadFileModalClick={openUploadFileModal}
        openConfigurationModalClick={openConfigModal}
        openSaveToFileModalClick={openSaveToFileModal}
        printModelModalClick={openPrintModelModal}
        disableButtons={!decisionModel} />

      <SummaryScreen
        attributes={attributes}
        hiddenExample={hiddenExample}
        setHiddenExample={setHiddenExample}

        decisionNodes={decisionNodes}
        hiddenNodes={hiddenNodes}
        dataDecisions={dataDecisions}
        setHiddenNodes={setHiddenNodes}

        processModel={processModel}
        hiddenProcess={hiddenProcess}
        setHiddenProcess={setHiddenProcess}

        decisionModel={decisionModel}
        hiddenDecision={hiddenDecision}
        setHiddenDecision={setHiddenDecision}
      />

      <ReactModal
        appElement={document.getElementById('app')}
        isOpen={openModal}
        contentLabel="Example Modal"
        style={{ overlay: {}, content: { background: 'rgb(31 41 55 / 1', color: 'white', width: modalWidth, height: modalHeight, top: '0', left: '0', margin: 'auto' } }}
        centered
      >

        {modalContent()}
      </ReactModal>
    </div >
  );
}