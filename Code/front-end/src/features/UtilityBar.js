import React from 'react';
import UtilityButton from './shared/UtilityButton';

export default function UtilityBar(props) {
  return (
    <div className="flex justify-between items-center p-1 bg-gray-900 w-full border-b-0 border-white-100/0.1 text-white text-lg" >
      <div className='flex flex-row gap-x-4 p-2'>
        <UtilityButton text={"Upload File"} clickDelegate={() => alert('upload')} />
        <UtilityButton text={"Configuration"} clickDelegate={() => alert('configure')} />
        <UtilityButton text={"Save to file"} clickDelegate={() => alert('save')} />
        <UtilityButton text={"Read from file"} clickDelegate={() => alert('read')} />
        <UtilityButton text={"Print"} clickDelegate={() => alert('print')} />
      </div>
      <h1 className="text-3xl font-bold underline mr-2">Decision Model Miner</h1>
    </div>
  );
}