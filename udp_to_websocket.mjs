// udp_to_websocket.mjs
import dgram from 'dgram';
import { WebSocketServer } from 'ws';

// === Configuración de puertos ===
const UDP_PORT = 5005;  // Puerto que recibe datos desde Python
const WS_PORT = 8080;   // Puerto donde se conecta el navegador (HTML)

// === Servidor UDP ===
const udpServer = dgram.createSocket('udp4');

udpServer.on('listening', () => {
  const address = udpServer.address();
  console.log(`✅ Servidor UDP escuchando en ${address.address}:${address.port}`);
});

udpServer.on('message', (msg, rinfo) => {
  try {
    const data = msg.toString();
    console.log(`📩 Datos UDP recibidos (${msg.length} bytes) de ${rinfo.address}:${rinfo.port}`);

    // Reenviar a todos los clientes WebSocket conectados
    if (wsServer.clients.size === 0) {
      console.warn("⚠️ No hay clientes WebSocket conectados. Datos no reenviados.");
    } else {
      for (const client of wsServer.clients) {
        if (client.readyState === 1) {
          client.send(data);
        }
      }
      console.log(`📤 Reenviados a ${wsServer.clients.size} cliente(s) WebSocket`);
    }
  } catch (err) {
    console.error("❌ Error procesando mensaje UDP:", err);
  }
});

udpServer.bind(UDP_PORT);

// === Servidor WebSocket ===
const wsServer = new WebSocketServer({ port: WS_PORT });

wsServer.on('listening', () => {
  console.log(`✅ Servidor WebSocket activo en ws://localhost:${WS_PORT}`);
});

wsServer.on('connection', (ws, req) => {
  console.log('🤝 Cliente conectado al WebSocket');
  ws.on('close', () => console.log('🔌 Cliente desconectado'));
});
