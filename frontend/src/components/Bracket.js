import React, { useEffect, useState } from 'react'

import { Switch, Route, useParams, useHistory } from 'react-router-dom'

const Bracket = (props) => {
  const { bracketId } = useParams()

  const [bracketInfo, setBracketInfo] = useState(null)
  const [bracketLoading, setBracketLoading] = useState(true)
  const [pickedInfoString, setPickedInfoString] = useState('')
  let history = useHistory()

  const handleMatchupTeamSelect = (matchupId, winnerId, notes, confidence) => {
    fetch(`/bracket-matchups/${matchupId}`, {
      method: 'PATCH',
      body: JSON.stringify({
        winner_id: winnerId,
        notes,
        confidence,
      }),
      headers: { 'Content-Type': 'application/json' },
    })
      .then(() => {
        setBracketLoading(true)
        fetchBracketInfo(bracketId)
      })
      .then(() => {
        history.push(`/brackets/${bracketId}`)
      })
  }

  const fetchBracketInfo = (bracketId) => {
    return fetch(`/brackets/${bracketId}`)
      .then((resp) => resp.json())
      .then((bracketInfo) => {
        setBracketInfo(bracketInfo)
        setBracketLoading(false)
      })
  }

  useEffect(() => {
    fetchBracketInfo(bracketId)
  }, [bracketId, bracketLoading])

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
            <MatchupRedirect bracketInfo={bracketInfo} />
          </Route>
          <Route path="/brackets/:bracketId/finished-bracket">
            <FinishedBracket bracketInfo={bracketInfo} />
          </Route>
          <Route path="/brackets/:bracketId/matchups/:matchupId">
            <Matchup onMatchupTeamSelect={handleMatchupTeamSelect} />
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

const Matchup = (props) => {
  const { matchupId } = useParams()

  const [matchup1Left, setMatchup1Left] = useState(true)
  const [matchupInfo, setMatchupInfo] = useState(null)
  const [matchupLoading, setMatchupLoading] = useState(true)

  const handleTeamSelect = (teamInfo) => {
    props.onMatchupTeamSelect(matchupId, teamInfo.id)
  }

  useEffect(() => {
    fetch(`/bracket-matchups/${matchupId}`)
      .then((resp) => resp.json())
      .then((matchupInfo) => {
        setMatchupInfo(matchupInfo)
        setMatchupLoading(false)
      })
  }, [matchupId, matchupLoading])

  useEffect(() => {
    const shouldSetMatchupLeft = Math.floor(Math.random() * 2) === 0
    setMatchup1Left(shouldSetMatchupLeft)
  }, [matchupId])

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
      <div>{teamInfo.seed}</div>
      <button onClick={handleTeamSelect}>Select Team</button>
    </div>
  )
}

const FinishedBracket = () => {
  return <div>FinishedBracket</div>
}

export default Bracket
