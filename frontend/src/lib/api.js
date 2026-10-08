const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const fetchJson = (path) =>
  fetch(`${API_URL}${path}`).then((response) => {
    if (!response.ok) {
      throw new Error(`${response.status} from ${path}`);
    }
    return response.json();
  });

export const getSeasons = (league) => fetchJson(`/${league}/seasons`);

export const getStandings = (league, season) =>
  fetchJson(`/${league}/seasons/${season}/teams`);

export const getTeam = (league, season, abbreviation) =>
  fetchJson(`/${league}/seasons/${season}/teams/${abbreviation}`);
