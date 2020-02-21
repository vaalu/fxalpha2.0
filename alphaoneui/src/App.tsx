import React from 'react';
import './App.css';
import { BrowserRouter, Route, Link } from 'react-router-dom'
import Secured from './components/Secured';

const App: React.FC = () => {

  return (

      <BrowserRouter>
        <div className="container">
          <ul>
            <li><Link to="/">public component</Link></li>
            <li><Link to="/secured">secured component</Link></li>
          </ul>
          <Route path="/secured" component={Secured} />
        </div>
      </BrowserRouter>
    )

  /* return (
      <BrowserRouter>
        <Secured />
      </BrowserRouter>
  ); */
}

export default App;
