import React, { useEffect, useState } from 'react'

import { useHistory } from 'react-router-dom'

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

export default BracketList
