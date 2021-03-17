import React from 'react'
import {
  BrowserRouter as Router,
  Redirect,
  Switch,
  Route,
  NavLink,
} from 'react-router-dom'

import BracketList from './components/BracketList.js'
import Bracket from './components/Bracket.js'

import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <header className="header">
          <NavLink to="/" className="menu-link">
            <div>Bracket Picker</div>
          </NavLink>
        </header>

        <div role="main">
          <Switch>
            <Route exact path="/">
              <Redirect to="/brackets" />
            </Route>
            <Route exact path="/brackets">
              <BracketList />
            </Route>
            <Route path="/brackets/:bracketId">
              <Bracket />
            </Route>
          </Switch>
        </div>
      </div>
    </Router>
  )
}

export default App
