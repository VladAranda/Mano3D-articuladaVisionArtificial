// udp_to_websocket.mjs
import { WebSocketServer } from "ws";

// === Configuración de puerto dinámico (Render) ===
const PORT = process.env.PORT || 8080;

// === Servidor WebSocket ===
const wsServer = new WebSocketServer({ port: PORT });

wsServer.on("listening", () => {
  console.log(`✅ Servidor WebSocket activo en ws://localhost:${PORT}`);
});

wsServer.on("connection", (ws) => {
  console.log("🤝 Cliente conectado al WebSocket");

  ws.on("message", (msg) => {
    // Aquí puedes procesar datos entrantes si los necesitas
    console.log("📩 Mensaje recibido:", msg.toString());
  });

  ws.on("close", () => console.log("🔌 Cliente desconectado"));
});

console.log("🚀 Servidor WebSocket iniciado.");
