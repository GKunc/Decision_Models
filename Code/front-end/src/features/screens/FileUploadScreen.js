import React, { useRef, useState } from 'react';
import ErrorBox from '../shared/ErrorBox';
import Spinner from '../shared/Spinner';

export default function FileUploadScreen(props) {
  const inputFileRef = useRef()
  const submitButton = useRef()

  const [file, setFile] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)
  const setAttributes = props.setAttributes
  const setDecisionNodes = props.setDecisionNodes
  const setDataDecisions = props.setDataDecisions
  const setProcessModel = props.setProcessModel
  const setDecisionModel = props.setDecisionModel
  const decisionModel = props.decisionModel
  const closeModal = props.closeModal

  const browseForFile = () => {
    inputFileRef.current.click()
  }

  const handleFileSelected = () => {
    setFile(inputFileRef.current.files[0])
    submitButton.current.click()
  }

  const getAttributes = () => {
    var url = "http://127.0.0.1:5000/attributes"
    var formElement = document.querySelector("form");
    fetch(url, { method: 'post', body: new FormData(formElement), mode: 'cors' })
      .then(r => r.json()
        .then(data => {
          setAttributes(data)
          closeModal()
        })).catch((error) => {
          console.log(error.message)
          setErrorMessage(error.message)
        })
  }

  const getNodes = () => {
    var url = "http://127.0.0.1:5000/nodes"
    var formElement = document.querySelector("form");
    fetch(url, { method: 'post', body: new FormData(formElement), mode: 'cors' })
      .then(r => r.json()
        .then(data => {
          setDataDecisions(data[0])
          setDecisionNodes(data[1])
          closeModal()
        })).catch((error) => {
          setErrorMessage(error.message)
        })
  }

  const getProcessModel = () => {
    var url = "http://127.0.0.1:5000/process_model"
    var formElement = document.querySelector("form");
    fetch(url, { method: 'post', body: new FormData(formElement), mode: 'cors' })
      .then(r => r.json()
        .then(data => {
          setProcessModel(data)
          closeModal()
        })).catch((error) => {
          setErrorMessage(error.message)
        })
  }

  const getDecisionModel = () => {
    var url = "http://127.0.0.1:5000/decision_model"
    var formElement = document.querySelector("form");
    fetch(url, { method: 'post', body: new FormData(formElement), mode: 'cors' })
      .then(r => r.json()
        .then(data => {
          setDecisionModel(data)
          closeModal()
        })).catch((error) => {
          setErrorMessage(error.message)
        })
  }

  const getDataFromServer = () => {
    setErrorMessage(null)
    setDecisionModel(null)

    getAttributes()
    getNodes()
    getProcessModel()
    getDecisionModel()
  }

  const handleDragEnter = e => {
    e.preventDefault();
    e.stopPropagation();
    const dropZone = document.getElementById('drop-zone')
    dropZone.classList.add('active-dropzone')
    dropZone.classList.remove('inactive-dropzone')
  };

  const handleDragLeave = e => {
    e.preventDefault();
    e.stopPropagation();
    const dropZone = document.getElementById('drop-zone')
    dropZone.classList.remove('active-dropzone')
    dropZone.classList.add('inactive-dropzone')
  };

  const handleDragOver = e => {
    e.preventDefault();
    e.stopPropagation();
    const dropZone = document.getElementById('drop-zone')
    dropZone.classList.add('active-dropzone')
    dropZone.classList.remove('inactive-dropzone')
  };

  const handleDrop = e => {
    e.preventDefault();
    e.stopPropagation();
    const dropZone = document.getElementById('drop-zone')
    dropZone.classList.remove('active-dropzone')
    dropZone.classList.add('inactive-dropzone')
    console.log(e.dataTransfer.files[0])
    inputFileRef.current.files = e.dataTransfer.files
    handleFileSelected()
  };

  const resetError = () => {
    setErrorMessage(null)
  }

  if (file && !decisionModel && !errorMessage) {
    return (
      <Spinner />
    );
  } else {
    return (
      <div className='h-full flex flex-col'>
        <div className="flex items-center justify-between">
          <div className="text-xl m-2">Upload file</div>
          <div onClick={props.closeDelegate} className="bg-green-500 hover:bg-green-600 text-white rounded-full w-[24px] h-[24px] flex items-center justify-center cursor-pointer">X</div>
        </div>

        <ErrorBox resetError={resetError} errorMessage={errorMessage} />

        <div id="drop-zone" className={'bg-gray-800 border border-dashed grow'}
          onDrop={e => handleDrop(e)}
          onDragOver={e => handleDragOver(e)}
          onDragEnter={e => handleDragEnter(e)}
          onDragLeave={e => handleDragLeave(e)} >
          <form id="myForm" className='flex flex-col items-center justify-center h-full' encType="multipart/form-data" target="dummyframe" method="POST">
            <input className='hidden' ref={inputFileRef} onChange={handleFileSelected} type="file" name="file" />
            <div>
              Drop your <span className='font-bold'>.csv</span> or <span className='font-bold'>.xes</span> log here
            </div>
            <div>
              or <span className='underline font-bold text-green-500 hover:text-green-600 cursor-pointer' onClick={browseForFile}>select from your PC</span>
            </div>
            <button className='hidden' type='' ref={submitButton} onClick={getDataFromServer}></button>
          </form>

          <iframe className='hidden' title="dummyframe" name="dummyframe" id="dummyframe"></iframe>
        </div>
      </div>
    );
  }
}