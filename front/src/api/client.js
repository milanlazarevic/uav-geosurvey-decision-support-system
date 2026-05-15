import axios from "axios";

const API_BASE = "http://localhost:8080";

export const api = axios.create({
  baseURL: API_BASE,
});

export const sendStep = (sessionId, body) =>
  api.post(`/api/simulation/step?sessionId=${sessionId}`, body);

export const resetSession = (sessionId) =>
  api.post(`/api/simulation/reset/${sessionId}`);
