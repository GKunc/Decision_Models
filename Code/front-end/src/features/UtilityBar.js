import React from 'react';
import UtilityButton from './shared/UtilityButton';

export default function UtilityBar(props) {

  return (
    <div className="h-[60px] flex justify-between items-center p-1 bg-gray-900 w-full border-b-0 border-white-100/0.1 text-white text-lg" >
      <div className='flex flex-row gap-x-4 p-2'>
        <UtilityButton text={"Configuration"} clickDelegate={props.openConfigurationModalClick} />
        <UtilityButton text={"Upload File"} clickDelegate={props.openUploadFileModalClick} />
        <UtilityButton text={"Save to file"} clickDelegate={props.openSaveToFileModalClick} disabled={props.disableButtons} />
        <UtilityButton text={"Print Model"} clickDelegate={props.printModelModalClick} disabled={props.disableButtons} />
      </div>
      <h1 className="text-3xl font-bold underline mr-2">Decision Model Miner</h1>
    </div>
  );
}