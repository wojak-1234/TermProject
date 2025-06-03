const clientId = "7eee20d5ef9d400998fd8a8ee3bfe5c9";
const redirectUri = "http://127.0.0.1:8000/callback"; 
const scopes = [
  "user-read-recently-played",
  "user-top-read",
  "user-read-email"
];

function redirectToSpotifyLogin() {
  const authUrl = "https://accounts.spotify.com/authorize" +
    "?response_type=token" +
    `&client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&scope=${encodeURIComponent(scopes.join(" "))}`;
  window.location.href = authUrl;
}

function getAccessTokenFromUrl() {
  const hash = window.location.hash;
  if (!hash) return null;
  const tokenMatch = hash.match(/access_token=([^&]*)/);
  return tokenMatch ? tokenMatch[1] : null;
}

function saveAccessToken() {
  const token = getAccessTokenFromUrl();
  if (token) {
    localStorage.setItem("spotify_access_token", token);
    window.history.replaceState({}, document.title, window.location.pathname);
  }
}

function getSavedAccessToken() {
  return localStorage.getItem("spotify_access_token");
}
