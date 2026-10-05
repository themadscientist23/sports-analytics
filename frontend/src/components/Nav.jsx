import { Link } from 'react-router-dom';
import { LEAGUES } from '../lib/leagues.js';
import './Nav.css';

function Nav() {
  return (
    <header>
      <nav className="main-nav">
        <Link to="/" className="logo">
          <img src="/simplelogo.png" alt="Sports Analytics Platform home" />
        </Link>
        <div className="nav-links">
          {Object.keys(LEAGUES).map((league) => (
            <Link key={league} to={`/${league}`}>
              {league.toUpperCase()}
            </Link>
          ))}
        </div>
      </nav>
    </header>
  );
}

export default Nav;
