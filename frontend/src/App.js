import React, { useRef, useEffect, useState } from 'react'

import {
  BrowserRouter as Router,
  Redirect,
  Switch,
  Route,
  NavLink,
  useParams,
  useHistory,
  useLocation,
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
            <Route path="/brackets/:bracketId">
              <Bracket />
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
    <div className="page-content bracket-list">
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
  const { bracketId } = useParams()

  const [bracketInfo, setBracketInfo] = useState(null)
  const [bracketLoading, setBracketLoading] = useState(true)
  const [bracketRefreshing, setBracketRefreshing] = useState(false)
  const [pickedInfoString, setPickedInfoString] = useState('')

  const fetchBrackets = () => {
    return fetch(`/brackets/${bracketId}`)
      .then((resp) => resp.json())
      .then((bracketInfo) => {
        console.log('bracketInfo', bracketInfo)
        setBracketInfo(bracketInfo)
        setBracketLoading(false)
      })
  }

  const location = useLocation()
  const { search } = location
  const history = useHistory()

  const prevBracketInfoRef = useRef()
  useEffect(() => {
    prevBracketInfoRef.current = bracketInfo
  })
  const prevBracketInfo = prevBracketInfoRef.current

  useEffect(() => {
    fetchBrackets()
  }, [bracketLoading])

  useEffect(() => {
    if (search.includes('refresh=true')) {
      fetchBrackets()
    }
  })

  useEffect(() => {
    if (!bracketInfo) {
      return
    }
    const {
      available_matchups,
      unavailable_matchups,
      picked_matchups,
    } = bracketInfo

    const totalMatchups =
      available_matchups.length +
      unavailable_matchups.length +
      picked_matchups.length
    const pickedInfoString = `Picked ${picked_matchups.length} out of ${totalMatchups} games`
    setPickedInfoString(pickedInfoString)
  }, [bracketInfo])

  if (bracketLoading) {
    return <div className="loading-container"></div>
  }

  return (
    <div className="page">
      <div className="bracket-info-bar">
        <div className="bracket-name">{bracketInfo.name}</div>
        <div>{pickedInfoString}</div>
      </div>

      <div className="page-content">
        <Switch>
          <Route exact path="/brackets/:bracketId/">
            {(!prevBracketInfo ||
              prevBracketInfo.picked_matchups.length !==
                bracketInfo.picked_matchups.length) && (
              <MatchupRedirect bracketInfo={bracketInfo} />
            )}
          </Route>
          <Route path="/brackets/:bracketId/finished-bracket">
            <FinishedBracket bracketInfo={bracketInfo} />
          </Route>
          <Route path="/brackets/:bracketId/matchups/:matchupId">
            <Matchup />
          </Route>
        </Switch>
      </div>
    </div>
  )
}

const MatchupRedirect = (props) => {
  const { bracketInfo } = props
  const history = useHistory()
  useEffect(() => {
    if (!bracketInfo) {
      return
    }
    const { id, available_matchups } = bracketInfo

    if (available_matchups.length) {
      const nextMatchupIdx = Math.floor(
        Math.random() * available_matchups.length
      )
      const nextMatchup = available_matchups[nextMatchupIdx]
      history.push(`/brackets/${id}/matchups/${nextMatchup.id}`)
    } else {
      history.push(`/brackets/${id}/finished-bracket`)
    }
  })
  return <div></div>
}

const Matchup = () => {
  const { bracketId, matchupId } = useParams()

  const [matchup1Left, setMatchup1Left] = useState(true)
  const [matchupInfo, setMatchupInfo] = useState(null)
  const [matchupLoading, setMatchupLoading] = useState(true)
  const [pickedInfoString, setPickedInfoString] = useState('')

  useEffect(() => {
    fetch(`/bracket-matchups/${matchupId}`)
      .then((resp) => resp.json())
      .then((matchupInfo) => {
        setMatchupInfo(matchupInfo)
        setMatchupLoading(false)
      })
  }, [matchupLoading])

  useEffect(() => {
    const shouldSetMatchupLeft = Math.floor(Math.random() * 2) == 0
    setMatchup1Left(shouldSetMatchupLeft)
  }, [true])

  const history = useHistory()
  const handleTeamSelect = (teamInfo) => {
    fetch(`/bracket-matchups/${matchupId}`, {
      method: 'PATCH',
      body: JSON.stringify({
        winner_id: teamInfo.id,
        notes: 'fooo',
        confidence: 2,
      }),
      headers: { 'Content-Type': 'application/json' },
    }).then(() => {
      history.push(`/brackets/${bracketId}?refresh=true`)
    })
  }

  if (!matchupInfo) {
    return null
  }

  const { team1, team2 } = matchupInfo
  const team1Info = (
    <TeamInfo teamInfo={team1} num="team1" onTeamSelect={handleTeamSelect} />
  )
  const team2Info = (
    <TeamInfo teamInfo={team2} num="team2" onTeamSelect={handleTeamSelect} />
  )

  return (
    <div className="page-content matchup-container">
      {matchup1Left && team1Info}
      {!matchup1Left && team2Info}
      {!matchup1Left && team1Info}
      {matchup1Left && team2Info}
    </div>
  )
}

const TeamInfo = (props) => {
  const { teamInfo, num } = props
  const handleTeamSelect = (e) => {
    props.onTeamSelect(teamInfo)
  }

  return (
    <div className="team-info">
      <div>Team Info</div>
      <div>{num}</div>
      <div>{teamInfo.name}</div>
      <button onClick={handleTeamSelect}>Select Team</button>
    </div>
  )
}

const FinishedBracket = () => {
  return <div>FinishedBracket</div>
}

export default App
