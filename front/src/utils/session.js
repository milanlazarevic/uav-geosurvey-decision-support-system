export function getSessionId() {
  let id = localStorage.getItem("sessionId");

  if (!id) {
    id =
      "session-" + Date.now() + "-" + Math.random().toString(36).substr(2, 6);

    localStorage.setItem("sessionId", id);
  }

  return id;
}
