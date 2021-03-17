import React, { useEffect, useState } from 'react'

import {
  BrowserRouter as Router,
  Redirect,
  Switch,
  Route,
  NavLink,
  useParams,
  useHistory,
} from 'react-router-dom'

import logo from './logo.svg'
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
            <Route path="/brackets/:bracket_id">
              <Bracket foo="foo" />
            </Route>
            <Route path="/brackets/:bracket_id/matchups/:matchup_id">
              <Matchup />
            </Route>
          </Switch>
        </div>
      </div>
    </Router>
  )
}

function BracketCard(props) {
  const { bracket } = props

  const history = useHistory()
  const handleClick = (e) => {
    console.log('here', e)
    history.push(`/brackets/${bracket.id}`)
  }

  return (
    <div className="bracket-card" onClick={handleClick}>
      {bracket.name}
    </div>
  )
}

function BracketList() {
  const [brackets, setBrackets] = useState([])
  const [bracketsLoading, setBracketsLoading] = useState(true)
  const [bracketName, setBracketName] = useState('')

  useEffect(() => {
    fetch('/brackets')
      .then((resp) => resp.json())
      .then((brackets) => {
        setBrackets(brackets)
        setBracketsLoading(false)
      })
  }, [bracketsLoading])

  const handleCreateBracket = (e) => {
    e.preventDefault()
    fetch('/brackets', {
      method: 'POST',
      body: JSON.stringify({ name: bracketName }),
      headers: { 'Content-Type': 'application/json' },
    }).then((resp) => {
      setBracketName('')
      setBracketsLoading(true)
    })
  }

  return (
    <div className="bracket-list">
      <h2>Available Brackets</h2>

      {bracketsLoading && <div className="loading-container"></div>}
      {!bracketsLoading && (
        <div className="bracket-list-container">
          {brackets.map((bracket) => {
            return (
              <BracketCard key={bracket.id} bracket={bracket}></BracketCard>
            )
          })}
        </div>
      )}

      <form onSubmit={handleCreateBracket}>
        <label>
          Create New Bracket:
          <input
            type="text"
            value={bracketName}
            onChange={(e) => setBracketName(e.target.value)}
          />
        </label>
        <input type="submit" value="Submit" />
      </form>
    </div>
  )
}

const Bracket = (props) => {
  const params = useParams()
  console.log('params', params)
  return (
    <div>
      <h2>Bracket</h2>
      <span>{props.foo}</span>
    </div>
  )
}

const Matchup = () => {
  const params = useParams()
  console.log('params', params)
  return <div>Matchup</div>
}

/*
function App() {
  const [getMessage, setGetMessage] = useState({})

  useEffect(async ()=>{
    console.log('here!!!')
    // fetch('/brackets', { method: 'POST', body: JSON.stringify({ name: 'testbraacket' }), headers: { 'Content-Type': 'application/json' }})
    const response = await fetch('/brackets')
    console.log('response', response)
    const body = await response.json()
    console.log('body', body)
    const individualBracketResponse = await fetch(`/brackets/${body[0].id}`)
    const individualBracket = await individualBracketResponse.json()
    console.log('individualBracket', individualBracket)
    const bracketMatchup = individualBracket.available_matchups[0]
    const matchupResponse = await fetch(`/bracket-matchups/${bracketMatchup.id}`)
    const matchup = await matchupResponse.json()
    console.log('matchup', matchup)
    const updatedMatchupResponse = await fetch(`/bracket-matchups/${bracketMatchup.id}`, { method: 'PATCH', body: JSON.stringify({ winner_id: matchup.team1_id, notes: "fooo", confidence: 2 }), headers: { 'Content-Type': 'application/json' }})
    const updatedMatchup = await updatedMatchupResponse.json()
    console.log('updatedMatchup', updatedMatchup)




   */

export default App
