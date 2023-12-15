#include <WiFi.h>
#include <SocketIoClient.h>

/// WIFI Settings ///
const char* ssid = "ssid";
const char* password = "password";

/// Socket.IO Settings ///
char host[] = "192.168.1.6";                           // Socket.IO Server Address
int port = 5000;                                        // Socket.IO Port Address
char path[] = "/socket.io/?EIO=4&transport=websocket";  // Socket.IO Base Path


/////////////////////////////////////
////// ESP32 Socket.IO Client //////
///////////////////////////////////

SocketIoClient webSocket;
WiFiClient client;


bool buzzDrowsy = false;
bool buzzSleeping = false;
bool buzzYawning = false;
bool buzzNoFace = false;
String stream_link = "";

void socket_response(const char* payload, size_t length) {
  Serial.print("Response: ");
  
  if (String(payload)== "Drowsy"){
    Serial.println(payload);
    buzzDrowsy = true;
  }  if (String(payload)== "Sleeping"){
    Serial.println(payload);
    buzzSleeping = true;
  } if (String(payload)== "Yawning"){
    Serial.println(payload);
    buzzYawning = true;
  }
  if (String(payload) == "No face deteceted") {
    Serial.println(payload);
    buzzNoFace = true;
  } 
}

void socket_connected(const char* payload, size_t length) {
  Serial.print("Socket.IO Connected!: ");
  Serial.println(payload);
  
  String pay = "{\"link\":\"" + stream_link + "\"}";
  webSocket.emit("stream", pay.c_str());
}

void setup() {
  Serial.begin(115200);
  pinMode(4, OUTPUT);
  pinMode(13, OUTPUT);

  // begin wifi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // start websocket
  webSocket.begin(host, port, path);

  webSocket.on("connect", socket_connected);
  webSocket.on("response", socket_response);

  if (false) {
    stream_link = "http://" + WiFi.localIP().toString() + ":91/stream";
  } else {
    stream_link = "http://" + String(host) + ":" + String(port) + "/stream";
  }

  // emit stream link
  // String payload = "{\"link\":\"" + link + "\"}";
  // webSocket.emit("stream", payload.c_str());
}


bool buzzer(bool buzzerOn = false,int frequency = 1000, int duration = 5){
  static unsigned long previousBuzzerMillis = 0;
  static int buzzerState = LOW;
  static int buzzerCount = 0;
  unsigned long currentMillis = millis();
  if (currentMillis - previousBuzzerMillis > frequency) {
    previousBuzzerMillis = currentMillis;

    if (buzzerOn) {
      if (buzzerState == LOW) {
        buzzerState = HIGH;
      } else {
        buzzerState = LOW;
      }

      Serial.print("Buzzer State: ");
      Serial.println(buzzerState);
      digitalWrite(13, buzzerState);
      buzzerCount += 1;
    }

    if (buzzerCount > duration*2) {
      buzzerOn = false;
      digitalWrite(13, LOW);
      buzzerCount = 0;


    }

    Serial.println(buzzerOn);
  }
  return buzzerOn;
}


void loop() {
  webSocket.loop();
  if(buzzYawning){
    buzzYawning = buzzer(buzzYawning, 300, 4);
  }
  if(buzzNoFace){
    buzzNoFace = buzzer(buzzNoFace, 100);
  }
  if (buzzDrowsy){
    buzzDrowsy = buzzer(buzzDrowsy, 500, 2);

  }
  if (buzzSleeping){
    buzzSleeping = buzzer(buzzSleeping, 800);
  }
  
  
}