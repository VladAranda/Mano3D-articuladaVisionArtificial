import cv2
import mediapipe as mp
import socket
import json
import time

# =========================
# CONFIGURACIÓN
# =========================
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MAX_HZ = 30  # tasa máxima de envío (FPS)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# =========================
# INICIALIZAR CÁMARA
# =========================
print("🔍 Buscando cámara disponible...")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ No se puede acceder a la cámara principal. Probando otros índices...")
    for i in range(1, 5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"✅ Cámara encontrada en índice {i}")
            break
    else:
        print("🚫 Ninguna cámara disponible. Verifica permisos o conexión física.")
        exit()

print("🎥 Cámara iniciada correctamente.\n")

# =========================
# DETECCIÓN DE MANO Y ENVÍO UDP
# =========================
with mp_hands.Hands(max_num_hands=1,
                    min_detection_confidence=0.6,
                    min_tracking_confidence=0.6) as hands:
    last = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ No se pudo leer frame de la cámara.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        payload = {"ts": time.time(), "found": False, "landmarks": []}

        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            for lm in hand.landmark:
                payload["landmarks"].append({
                    "x": lm.x,  # 0..1 (ancho)
                    "y": lm.y,  # 0..1 (alto)
                    "z": lm.z   # relativo (más negativo = más cerca)
                })
            payload["found"] = True

            # Dibujar mano
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            # Enviar datos UDP (JSON)
            data = json.dumps(payload).encode('utf-8')
            sock.sendto(data, (UDP_IP, UDP_PORT))
            print(f"📡 Enviando datos UDP: {len(payload['landmarks'])} puntos")

        cv2.imshow("Hand Tracking", frame)

        # Limitar tasa de envío
        if (time.time() - last) < (1.0 / MAX_HZ):
            pass
        last = time.time()

        # Salir con tecla ESC
        if cv2.waitKey(1) & 0xFF == 27:
            print("👋 Saliendo...")
            break

cap.release()
cv2.destroyAllWindows()
print("✅ Cámara liberada. Programa finalizado.")
