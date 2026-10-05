export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const fetchJson = (url) =>
  fetch(url).then((response) => {
    if (!response.ok) {
      throw new Error(`${response.status} from ${url}`);
    }
    return response.json();
  });
