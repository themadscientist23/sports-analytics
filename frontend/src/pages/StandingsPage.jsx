import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getSeasons, getStandings } from '../lib/api.js';
import { LEAGUES, logoUrl } from '../lib/leagues.js';
import { formatCatelo } from '../lib/format.js';
import './StandingsPage.css';

const withStats = (team, hasTies) => {
  const games = team.wins + team.losses + (hasTies ? team.ties : 0);
  return {
    ...team,
    winPercentage: games > 0 ? (team.wins / games) * 100 : 0,
    pointsForPerGame: games > 0 ? team.points_for / games : 0,
    pointsAgainstPerGame: games > 0 ? team.points_against / games : 0,
    pointsDifferential:
      games > 0 ? (team.points_for - team.points_against) / games : 0,
  };
};

function StandingsPage({ league }) {
  const { title, hasTies } = LEAGUES[league];
  const [searchParams, setSearchParams] = useSearchParams();
  const [seasons, setSeasons] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [sortConfig, setSortConfig] = useState({
    key: 'catelo',
    direction: 'descending',
  });

  const season = searchParams.get('season') ?? seasons[seasons.length - 1];

  useEffect(() => {
    getSeasons(league)
      .then(setSeasons)
      .catch((error) => {
        console.error('Error fetching seasons:', error);
        setError(true);
        setLoading(false);
      });
  }, [league]);

  useEffect(() => {
    if (season === undefined) {
      return;
    }
    getStandings(league, season)
      .then((data) => setTeams(data.map((team) => withStats(team, hasTies))))
      .catch((error) => {
        console.error('Error fetching standings:', error);
        setError(true);
      })
      .finally(() => setLoading(false));
  }, [league, season, hasTies]);

  const sortBy = (key) => {
    const direction =
      sortConfig.key === key && sortConfig.direction === 'descending'
        ? 'ascending'
        : 'descending';
    setSortConfig({ key, direction });
  };

  const sortedTeams = [...teams].sort((a, b) => {
    const { key, direction } = sortConfig;
    const difference = (a[key] ?? 0) - (b[key] ?? 0);
    return direction === 'ascending' ? difference : -difference;
  });

  const sortableHeader = (key, label) => (
    <th
      aria-sort={sortConfig.key === key ? sortConfig.direction : undefined}
      className={`sortable ${sortConfig.key === key ? (sortConfig.direction === 'ascending' ? 'sort-asc' : 'sort-desc') : ''}`}>
      <button onClick={() => sortBy(key)}>{label}</button>
    </th>
  );

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Could not load standings</div>;
  }

  return (
    <>
      <h1>{title}</h1>
      <div className="season-picker">
        <label>
          Season{' '}
          <select
            value={season}
            onChange={(event) =>
              setSearchParams({ season: event.target.value })
            }>
            {seasons.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="standings">
        <div className="table-wrapper">
          <table>
            <colgroup>
              <col className="team-column" />
            </colgroup>
            <thead>
              <tr>
                <th>Team</th>
                {sortableHeader('catelo', 'CatElo')}
                {sortableHeader('wins', 'Wins')}
                {sortableHeader('losses', 'Losses')}
                {hasTies && sortableHeader('ties', 'Ties')}
                {sortableHeader('winPercentage', 'Win %')}
                {sortableHeader('pointsForPerGame', 'PPG')}
                {sortableHeader('pointsAgainstPerGame', 'Opp PPG')}
                {sortableHeader('pointsDifferential', 'Diff')}
              </tr>
            </thead>
            <tbody>
              {sortedTeams.map((team) => (
                <tr key={team.id}>
                  <td className="team-name">
                    <Link to={`/${league}/team/${team.abbreviation}`}>
                      <img
                        src={logoUrl(league, team.abbreviation)}
                        alt={`${team.name} logo`}
                      />
                      {team.name}
                    </Link>
                  </td>
                  <td className="catelo">{formatCatelo(team.catelo)}</td>
                  <td>{team.wins}</td>
                  <td>{team.losses}</td>
                  {hasTies && <td>{team.ties}</td>}
                  <td>{team.winPercentage.toFixed(1)}</td>
                  <td>{team.pointsForPerGame.toFixed(1)}</td>
                  <td>{team.pointsAgainstPerGame.toFixed(1)}</td>
                  <td>{team.pointsDifferential.toFixed(1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default StandingsPage;
