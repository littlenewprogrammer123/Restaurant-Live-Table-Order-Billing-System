import axios from "axios";

function getCSRFToken() {
  const name = "csrftoken=";
  const cookies = document.cookie.split(";");

  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name)) {
      return cookie.substring(name.length);
    }
  }
  return null;
}

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const csrfToken = getCSRFToken();
  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }
  return config;
});

export default api;
