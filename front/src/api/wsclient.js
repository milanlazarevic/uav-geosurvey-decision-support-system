import { Client } from "@stomp/stompjs";

let client;

export function connect(onMessage) {
  client = new Client({
    brokerURL: "ws://localhost:8080/drone-telemetry",
    reconnectDelay: 5000,
    debug: (str) => console.log(str),
    onConnect: () => {
      console.log("[+] Connected to ws");

      client.subscribe("/topic/telemetry", (message) => {
        const data = JSON.parse(message.body);
        onMessage(data);
      });
    },
    onStompError: (frame) => {
      console.error("[STOMP ERROR]", frame);
    },

    onWebSocketError: (err) => {
      console.error("[WS ERROR]", err);
    },
  });
  client.activate();
}

export function disconnect() {
  if (client) {
    client.deactivate();
  }
}
