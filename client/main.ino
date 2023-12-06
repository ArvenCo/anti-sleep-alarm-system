#include <WiFi.h>
#include <WebSocketsClient.h>

// WiFi credentials
#define WIFI_SSID "PLDTHOMEFIBR3b578"
#define WIFI_PASSWORD "PLDTWIFIsb5e7"

// Socket.IO server details
#define SERVER_ADDRESS "192.168.1.6"
#define SERVER_PORT 5000

WebSocketsClient webSocket;

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to Socket.IO server
  webSocket.begin(SERVER_ADDRESS, SERVER_PORT, "/socket.io/?EIO=4");

  
}

void loop() {
  // Add a delay before sending the first message
  delay(2000);

  // Emit data to server
  webSocket.sendTXT("42[\"print\", {\"word\":\"Hello, world!\"}]");

  // Set up event handler
  webSocket.onEvent(webSocketEvent);

  webSocket.loop();
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.println("[WSc] Disconnected!");
      break;
    case WStype_CONNECTED:
      Serial.println("[WSc] Connected to url: ");
      break;
    case WStype_TEXT:
      Serial.println("[WSc] Received text: ");
      Serial.println(String((char *)payload));
      break;
    case WStype_BIN:
      Serial.println("[WSc] Received binary data, length: " + String(length));
      break;
  }
}
