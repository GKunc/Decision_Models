import logo from './logo.svg';
import './App.css';
import React from 'react';

class App extends React.Component {
  
  render() {
    return (
      <div className="App">
        <form action="http://127.0.0.1:5000/decision_model" enctype="multipart/form-data" target="dummyframe" method="POST">
          <input type="file" name="file" />
          <input type="submit"/>
        </form>   
        <iframe style={{display: "none"}} name="dummyframe" id="dummyframe"></iframe>
      </div>
    );
  }
}

export default App;