const clientId = "7eee20d5ef9d400998fd8a8ee3bfe5c9";
const redirectUri = "https://rrgmqkq2-8000.asse.devtunnels.ms/callback.html";
const scopes = [
  "user-read-recently-played",
  "user-top-read",
  "user-read-email"
];

// 코드 챌린지 생성 (SHA256)
async function generateCodeChallenge(codeVerifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

// 임의 코드 검증자 생성
function generateCodeVerifier(length = 128) {
  const possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let text = "";
  for (let i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

// 로그인 요청
async function redirectToSpotifyLogin() {
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);
  localStorage.setItem("code_verifier", codeVerifier);

  const authUrl = "https://accounts.spotify.com/authorize" +
    `?response_type=code` +
    `&client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&scope=${encodeURIComponent(scopes.join(" "))}` +
    `&code_challenge_method=S256` +
    `&code_challenge=${codeChallenge}`;
console.log("이동할 authUrl:", authUrl);
  window.location.href = authUrl;
}
