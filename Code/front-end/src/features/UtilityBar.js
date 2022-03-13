import React from 'react';
import UtilityButton from './UtilityButton';

export default function UtilityBar(props) {
  return (
    <div className="flex justify-between items-center p-1 bg-gray-900 w-full border-b-0 border-white-100/0.1 text-white text-lg" >
      <div className='flex flex-row gap-x-4 p-2'>
        <UtilityButton text={"Upload File"} />
        <UtilityButton text={"Process Model"} />
        <UtilityButton text={"Decision Model"} />
      </div>
      <h1 className="text-3xl font-bold underline mr-2">Decision Model Miner</h1>
    </div>
  );
}