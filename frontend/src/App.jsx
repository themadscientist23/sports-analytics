import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Nav from './components/Nav.jsx';
import Homepage from './pages/Homepage.jsx';
import StandingsPage from './pages/StandingsPage.jsx';
import TeamPage from './pages/TeamPage.jsx';
import NotFound from './pages/NotFound.jsx';
import { LEAGUES } from './lib/leagues.js';

function App() {
  return (
    <Router>
      <Nav />
      <Routes>
        <Route path="/" element={<Homepage />} />
        {Object.keys(LEAGUES).map((league) => (
          <Route key={league} path={league}>
            <Route
              index
              element={<StandingsPage key={league} league={league} />}
            />
            <Route
              path="team/:abbreviation"
              element={<TeamPage league={league} />}
            />
          </Route>
        ))}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
