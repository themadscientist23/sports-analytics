import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getSeasons, getTeam } from '../lib/api.js';
import { LEAGUES } from '../lib/leagues.js';
import TeamHeader from '../components/TeamHeader.jsx';
import CatEloChart from '../components/CatEloChart.jsx';
import RecentGames from '../components/RecentGames.jsx';
import './TeamPage.css';

function TeamPage({ league }) {
  const { abbreviation } = useParams();
  const [teamData, setTeamData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getSeasons(league)
      .then((seasons) =>
        getTeam(league, seasons[seasons.length - 1], abbreviation),
      )
      .then((data) => setTeamData(data))
      .catch((error) => {
        console.error('Error fetching team data:', error);
        setError(true);
      })
      .finally(() => setLoading(false));
  }, [abbreviation, league]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Could not load team</div>;
  }

  const { team, history } = teamData;

  return (
    <div className="team-page">
      <Link to={`/${league}`} className="back-button">
        ← Back to {LEAGUES[league].title}
      </Link>
      <TeamHeader league={league} team={team} />
      {history.length > 0 ? (
        <>
          <CatEloChart history={history} />
          <RecentGames history={history} />
        </>
      ) : (
        <div className="no-data">No game history available</div>
      )}
    </div>
  );
}

export default TeamPage;
