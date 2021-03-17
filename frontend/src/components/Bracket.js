import React, { useEffect, useState } from 'react'

import { Switch, Route, useParams, useHistory } from 'react-router-dom'

const Bracket = (props) => {
  const { bracketId } = useParams()

  const [bracketInfo, setBracketInfo] = useState(null)
  const [bracketLoading, setBracketLoading] = useState(true)
  const [pickedInfoString, setPickedInfoString] = useState('')
  let history = useHistory()

  const handleMatchupTeamSelect = (matchupId, winnerId, notes, confidence) => {
    if (!winnerId) {
      return
    }
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
  return null
}

const Matchup = (props) => {
  const { matchupId } = useParams()

  const [team1Left, setTeam1Left] = useState(true)
  const [matchupInfo, setMatchupInfo] = useState(null)
  const [selectedTeamId, setSelectedTeamId] = useState('')
  const [matchupLoading, setMatchupLoading] = useState(true)
  const [matchupConfidence, setMatchupConfidence] = useState(null)
  const [matchupNotes, setMatchupNotes] = useState('')

  const handleTeamSelect = (teamId) => {
    setSelectedTeamId(teamId)
  }

  const handleConfidenceChange = (confidence) => {
    setMatchupConfidence(confidence)
  }

  const handleNotesChange = (e) => {
    const { value } = e.currentTarget
    setMatchupNotes(value)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!selectedTeamId) {
      return
    }
    props.onMatchupTeamSelect(
      matchupId,
      selectedTeamId,
      matchupNotes,
      matchupConfidence
    )
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
    setTeam1Left(shouldSetMatchupLeft)
  }, [matchupId])

  if (!matchupInfo) {
    return null
  }

  const { team1, team2 } = matchupInfo
  const team1Info = (
    <TeamInfo
      teamInfo={team1}
      positionNumber={team1Left ? 'Team1' : 'Team2'}
      isSelected={selectedTeamId === team1.id}
      onTeamSelect={handleTeamSelect}
    />
  )
  const team2Info = (
    <TeamInfo
      teamInfo={team2}
      positionNumber={team1Left ? 'Team2' : 'Team1'}
      onTeamSelect={handleTeamSelect}
      isSelected={selectedTeamId === team2.id}
    />
  )

  return (
    <div className="page-content">
      <form className="matchup-select-form" onSubmit={handleSubmit}>
        <div className="matchup-select-form-item team-matchup-container">
          {team1Left && team1Info}
          {!team1Left && team2Info}
          {!team1Left && team1Info}
          {team1Left && team2Info}
        </div>
        <div className="matchup-select-form-item">
          <label>Matchup Confidence:</label>
          <ConfidencePicker
            onConfidenceChange={handleConfidenceChange}
            confidence={matchupConfidence}
          />
        </div>
        <div className="matchup-select-form-item">
          <label>Notes:</label>
          <textarea
            className="matchup-notes"
            value={matchupNotes}
            onChange={handleNotesChange}
          />
        </div>
        <div className="matchup-select-form-item">
          <input
            className="btn"
            type="submit"
            value="Submit"
            disabled={!selectedTeamId}
          />
        </div>
      </form>
    </div>
  )
}

const ConfidencePicker = (props) => {
  const { confidence } = props

  const handleConfidenceSelect = (e) => {
    const { value } = e.currentTarget
    props.onConfidenceChange(Number(value))
  }

  return (
    <div className="confidence-picker-container">
      <input
        type="radio"
        value={1}
        onChange={handleConfidenceSelect}
        checked={confidence === 1}
      />
      1
      <input
        type="radio"
        value={2}
        onChange={handleConfidenceSelect}
        checked={confidence === 2}
      />
      2
      <input
        type="radio"
        value={3}
        onChange={handleConfidenceSelect}
        checked={confidence === 3}
      />
      3
      <input
        type="radio"
        value={4}
        onChange={handleConfidenceSelect}
        checked={confidence === 4}
      />
      4
      <input
        type="radio"
        value={5}
        onChange={handleConfidenceSelect}
        checked={confidence === 5}
      />
      5
      <input
        type="radio"
        value={6}
        onChange={handleConfidenceSelect}
        checked={confidence === 6}
      />
      6
      <input
        type="radio"
        value={7}
        onChange={handleConfidenceSelect}
        checked={confidence === 7}
      />
      7
      <input
        type="radio"
        value={8}
        onChange={handleConfidenceSelect}
        checked={confidence === 8}
      />
      8
      <input
        type="radio"
        value={9}
        onChange={handleConfidenceSelect}
        checked={confidence === 9}
      />
      9
      <input
        type="radio"
        value={10}
        onChange={handleConfidenceSelect}
        checked={confidence === 10}
      />
      10
    </div>
  )
}

const STAT_LABEL_MAP = {
  off_2_point_dist: '2-Pointers',
  off_3_point_dist: '3-Pointers',
  off_3pa_per_fga: '3PA/FGA',
  off_assist_rate: 'A/FGM',
  off_block_pct: 'Block%',
  off_eff: 'Adj. Eff',
  off_efg: 'EFG%',
  off_ft_pct: 'FT%',
  off_ft_point_dist: 'Free Throws',
  off_fta_rate: 'FTA/FGA',
  off_reb: 'Off Reb%',
  off_steal_pct: 'Steal%',
  off_three_point_pct: '3P%',
  off_turnover: 'Turnover%',
  off_two_point_pct: '2P%',
  sos: 'SOS',
  tempo: 'Tempo',
}

const OFF_DEF_MAP = {
  off_2_point_dist: 'def_2_point_dist',
  off_3_point_dist: 'def_3_point_dist',
  off_3pa_per_fga: 'def_3pa_per_fga',
  off_assist_rate: 'def_assist_rate',
  off_block_pct: 'def_block_pct',
  off_eff: 'def_eff',
  off_efg: 'def_efg',
  off_ft_pct: 'def_ft_pct',
  off_ft_point_dist: 'def_ft_point_dist',
  off_fta_rate: 'def_fta_rate',
  off_reb: 'def_reb',
  off_steal_pct: 'def_steal_pct',
  off_three_point_pct: 'def_three_point_pct',
  off_turnover: 'def_turnover',
  off_two_point_pct: 'def_two_point_pct',
}

const STAT_RANK_MAP = {
  bench_minutes: 'bench_minutes_rank',
  def_2_point_dist: 'def_2_point_dist_rank',
  def_3_point_dist: 'def_3_point_dist_rank',
  def_3pa_per_fga: 'def_3pa_per_fga_rank',
  def_assist_rate: 'def_assist_rate_rank',
  def_block_pct: 'def_block_pct_rank',
  def_eff: 'def_eff_rank',
  def_efg: 'def_efg_rank',
  def_ft_pct: 'def_ft_pct_rank',
  def_ft_point_dist: 'def_ft_point_dist_rank',
  def_fta_rate: 'def_fta_rate_rank',
  def_reb: 'def_reb_rank',
  def_steal_pct: 'def_steal_pct_rank',
  def_three_point_pct: 'def_three_point_pct_rank',
  def_turnover: 'def_turnover_rank',
  def_two_point_pct: 'def_two_point_pct_rank',
  experience: 'experience_rank',
  off_2_point_dist: 'off_2_point_dist_rank',
  off_3_point_dist: 'off_3_point_dist_rank',
  off_3pa_per_fga: 'off_3pa_per_fga_rank',
  off_assist_rate: 'off_assist_rate_rank',
  off_block_pct: 'off_block_pct_rank',
  off_eff: 'off_eff_rank',
  off_efg: 'off_efg_rank',
  off_ft_pct: 'off_ft_pct_rank',
  off_ft_point_dist: 'off_ft_point_dist_rank',
  off_fta_rate: 'off_fta_rate_rank',
  off_reb: 'off_reb_rank',
  off_steal_pct: 'off_steal_pct_rank',
  off_three_point_pct: 'off_three_point_pct_rank',
  off_turnover: 'off_turnover_rank',
  off_two_point_pct: 'off_two_point_pct_rank',
  sos: 'sos_rank',
  tempo: null,
}

const teamInfoLayout = [
  {
    sectionLabel: 'Effeciency',
    stats: ['off_eff', 'tempo'],
  },
  {
    sectionLabel: 'Four Factors',
    stats: ['off_efg', 'off_turnover', 'off_reb', 'off_fta_rate'],
  },
  {
    sectionLabel: 'Miscellaneous Components',
    stats: [
      'off_three_point_pct',
      'off_two_point_pct',
      'off_ft_pct',
      'off_block_pct',
      'off_steal_pct',
    ],
  },
  {
    sectionLabel: 'Style Components',
    stats: ['off_3pa_per_fga', 'off_assist_rate'],
  },
  {
    sectionLabel: 'Points Distribution',
    stats: ['off_3_point_dist', 'off_2_point_dist', 'off_ft_point_dist'],
  },
  {
    sectionLabel: 'Strength of Schedule',
    stats: ['sos'],
  },
]

const TeamInfo = (props) => {
  const { teamInfo, positionNumber, isSelected } = props

  const handleTeamSelect = (e) => {
    props.onTeamSelect(teamInfo.id)
  }

  return (
    <div className="team-info-container" onClick={handleTeamSelect}>
      <div className="team-info-card-label">{positionNumber} Info</div>
      {teamInfoLayout.map((layoutObj) => {
        return (
          <div className="layout-section" key={layoutObj.sectionLabel}>
            <div className="layout-section-label">{layoutObj.sectionLabel}</div>
            <div className="layout-stats">
              {layoutObj.stats.map((stat) => {
                const statLabel = STAT_LABEL_MAP[stat]
                const offStatValue = teamInfo.stats[stat]
                const offStatRankStat = STAT_RANK_MAP[stat]
                const offStatRank =
                  offStatRankStat && teamInfo.stats[offStatRankStat]

                const defStat = OFF_DEF_MAP[stat]
                const defStatValue = defStat && teamInfo.stats[defStat]
                const defStatRankStat = STAT_RANK_MAP[defStat]
                const defStatRank =
                  defStatRankStat && teamInfo.stats[defStatRankStat]
                return (
                  <div key={stat} className="stat-row">
                    <div>{statLabel}</div>
                    <div className="layout-stat-value">
                      {offStatValue}{' '}
                      {offStatRank && <span>({offStatRank})</span>}
                    </div>
                    {defStat && (
                      <div className="layout-stat-value">
                        {defStatValue}{' '}
                        {defStatRank && <span>({defStatRank})</span>}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )
      })}

      <input
        type="radio"
        value={teamInfo.id}
        onChange={handleTeamSelect}
        checked={isSelected}
      />
    </div>
  )
}

const FinishedBracket = (props) => {
  const { bracketInfo } = props
  const { picked_matchups } = bracketInfo
  const matchups = picked_matchups.sort((a, b) => {
    if (a.round_number !== b.round_number) {
      if (a.round_number > b.round_number) {
        return 1
      } else {
        return -1
      }
    }
    if (a.game_number > b.game_number) {
      return 1
    }
    return -1
  })
  return (
    <div>
      {matchups.map((matchup, idx) => {
        const prevMatchup = matchups[idx - 1]
        let roundInfo = null
        if (!prevMatchup || matchup.round_number !== prevMatchup.round_number) {
          roundInfo = (
            <div className="round-info">Round {matchup.round_number}</div>
          )
        }

        return (
          <div key={matchup.id}>
            {roundInfo}
            <div className="matchup-card-container">
              <MatchupCard matchupId={matchup.id} />
            </div>
          </div>
        )
      })}
    </div>
  )
}

const MatchupCard = (props) => {
  const { matchupId } = props

  const [matchupInfo, setMatchupInfo] = useState(null)
  const [matchupLoading, setMatchupLoading] = useState(true)

  useEffect(() => {
    fetch(`/bracket-matchups/${matchupId}`)
      .then((resp) => resp.json())
      .then((matchupInfo) => {
        setMatchupInfo(matchupInfo)
        setMatchupLoading(false)
      })
  }, [matchupId, matchupLoading])

  if (matchupLoading) {
    return null
  }

  const { team1, team2, winner_id } = matchupInfo
  return (
    <div className="matchup-card">
      <div
        className={`matchup-card-team-info ${
          winner_id === team1.id ? 'winner' : ''
        }`}
      >
        <div>{team1.seed}</div>
        <div>{team1.name}</div>
        <div>
          {team1.stats.off_eff}({team1.stats.off_eff_rank})
        </div>
        <div>
          {team1.stats.def_eff}({team1.stats.def_eff_rank})
        </div>
      </div>
      <div
        className={`matchup-card-team-info ${
          winner_id === team2.id ? 'winner' : ''
        }`}
      >
        <div>{team2.seed}</div>
        <div>{team2.name}</div>
        <div>
          {team2.stats.off_eff}({team2.stats.off_eff_rank})
        </div>
        <div>
          {team2.stats.def_eff}({team2.stats.def_eff_rank})
        </div>
      </div>
      {matchupInfo.confidence && (
        <div className="matchup-card-info matchup-card-confidence">
          Confidence: {matchupInfo.confidence}
        </div>
      )}
      {matchupInfo.notes && (
        <div className="matchup-card-info matchup-card-notes">
          Notes: {matchupInfo.notes}
        </div>
      )}
    </div>
  )
}

export default Bracket
