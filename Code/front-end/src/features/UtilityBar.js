import React from 'react';
import UtilityButton from './shared/UtilityButton';

export default function UtilityBar(props) {

  return (
    <div className="h-full flex flex-col justify-between items-center p-1 bg-gray-900 h-full border-b-0 border-white-100/0.1 text-white text-lg" >
      {/* <h1 className="text-3xl font-bold underline mr-2">Decision Model Miner</h1> */}
      <div className='flex flex-col gap-y-4 p-2'>
        <UtilityButton text={"Configuration"} clickDelegate={props.openConfigurationModalClick} />
        <UtilityButton text={"Upload File"} clickDelegate={props.openUploadFileModalClick} />
        <UtilityButton text={"Save to file"} clickDelegate={props.openSaveToFileModalClick} disabled={props.disableButtons} />
        <UtilityButton text={"Print BPMN"} clickDelegate={props.printBPMNModalClick} disabled={props.disableButtons} />
        <UtilityButton text={"Print DMN"} clickDelegate={props.printDMNModalClick} disabled={props.disableButtons} />
      </div>
    </div>
  );
}