import React, { useRef, useState } from 'react';
import DecisionModelVisualisation from './DecisionModelVisualisation';
import Spinner from './Spinner';

export default function FileUpload(props) {
  const inputFileRef = useRef()
  const submitButton = useRef()
  const [file, setFile] = useState(null);
  const [decisionModel, setDecisionModel] = useState(null);

  const browseForFile = () => {
    inputFileRef.current.click()
  }

  const handleFileSelected = () => {
    setFile(inputFileRef.current.files[0])
    submitButton.current.click()
  }

  const getModel = () => {
    var url = "http://127.0.0.1:5000/decision_model"
    var formElement = document.querySelector("form");
    fetch(url, { method: 'post', body: new FormData(formElement), mode: 'cors' })
      .then(r => r.json()
        .then(data => {
          setDecisionModel(data)
        }))
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

  console.log(file)
  console.log(decisionModel)
  if (file && !decisionModel) {
    return (
      <Spinner />
    );
  } else if (file === null && decisionModel === null) {
    return (
      <DecisionModelVisualisation decision_model={decisionModel} />
    );
  } else {
    return (
      <div id="drop-zone" className={'border border-dashed h-full'}
        onDrop={e => handleDrop(e)}
        onDragOver={e => handleDragOver(e)}
        onDragEnter={e => handleDragEnter(e)}
        onDragLeave={e => handleDragLeave(e)} >
        <form id="myForm" className='flex flex-col items-center justify-center h-full' enctype="multipart/form-data" target="dummyframe" method="POST">
          <input className='hidden' ref={inputFileRef} onChange={handleFileSelected} type="file" name="file" />
          <div>
            Drop your <span className='font-bold'>.csv</span> or <span className='font-bold'>.xes</span> log here
          </div>
          <div>
            or <span className='underline font-bold text-green-500 hover:text-green-600 cursor-pointer' onClick={browseForFile}>select from your PC</span>
          </div>
          <button className='hidden' type='' ref={submitButton} onClick={getModel}></button>
        </form>

        <iframe className='hidden' title="dummyframe" name="dummyframe" id="dummyframe"></iframe>
      </ div >
    );
  }
}