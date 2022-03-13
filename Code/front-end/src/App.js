import React from 'react';
import ContentContainer from './features/ContentContainer';
import UtilityBar from './features/UtilityBar';

class App extends React.Component {

  render() {
    return (
      <div className="bg-gray-800 flex flex-col h-full">
        <UtilityBar className="flex-initial" />
        <ContentContainer className="flex-auto" />
      </div>
    );
  }
}

export default App;
