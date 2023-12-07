#include <WiFi.h>
#include <SocketIoClient.h>
#include <ArduinoJson.h>
#include "esp_camera.h"
#include "esp_timer.h"
#include <base64.h>
/////////////////////////////////////
////// USER DEFINED VARIABLES //////
///////////////////////////////////
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

/// WIFI Settings ///
const char* ssid     = "PLDTHOMEFIBR3b578";
const char* password = "PLDTWIFIsb5e7";

/// Socket.IO Settings ///
char host[] = "192.168.1.7"; // Socket.IO Server Address
int port = 5000; // Socket.IO Port Address
char path[] = "/socket.io/?EIO=4&transport=websocket"; // Socket.IO Base Path
bool useSSL = false; // Use SSL Authentication
const char * sslFingerprint = "";  // SSL Certificate Fingerprint
bool useAuth = false; // use Socket.IO Authentication
const char * serverUsername = "socketIOUsername";
const char * serverPassword = "socketIOPassword";

/// Pin Settings ///
int LEDPin = 2;
int buttonPin = 0;


/////////////////////////////////////
////// ESP32 Socket.IO Client //////
///////////////////////////////////

SocketIoClient webSocket;
WiFiClient client;
base64 b64;

bool LEDState = false;


void socket_Connected(const char * payload, size_t length) {
  Serial.print("Socket.IO Connected!: ");
  Serial.println(payload);
}

void socket_statusCheck(const char * payload, size_t length) {
  char* message = "\"OFF\"";
  if (!LEDState) {
    message = "\"ON\"";
  }
  webSocket.emit("status", message);
}

void socket_event(const char * payload, size_t length) {
  Serial.print("got message: ");
  Serial.println(payload);
}

void socket_response(const char * payload, size_t length) {
  Serial.print("Response: ");
  Serial.println(payload);
}

void socket_pushButton(const char * payload, size_t length) {
  LEDStateChange(!LEDState);
}



void LEDStateChange(const bool newState) {
  char* message = "\"OFF\"";
  if (!newState) {
    message = "\"ON\"";
  } 
  webSocket.emit("state_change", message);
  LEDState = newState;
  Serial.print("LED state has changed: ");
  Serial.println(message);
}

esp_err_t init_camera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // parameters for image quality and size
  config.frame_size = FRAMESIZE_VGA; // FRAMESIZE_ + QVGA|CIF|VGA|SVGA|XGA|SXGA|UXGA
  config.jpeg_quality = 15; //10-63 lower number means higher quality
  config.fb_count = 2;
  
  
  // Camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("camera init FAIL: 0x%x", err);
    return err;
  }
  sensor_t * s = esp_camera_sensor_get();
  s->set_framesize(s, FRAMESIZE_VGA);
  Serial.println("camera init OK");
  return ESP_OK;
};


void camera_capture(){
    //capture a frame
    while(true){
      camera_fb_t * fb = esp_camera_fb_get();
      if (!fb) {
          Serial.println("img capture failed");
        esp_camera_fb_return(fb);
        ESP.restart();
      }

      String payload = "{\"frame\":\"data:image/jpeg;base64," + String(b64.encode(fb->buf, fb->len)) + "\"}";
      
      webSocket.emit("camera_stream", payload.c_str());


      //return the frame buffer back to be reused
      esp_camera_fb_return(fb);
      delay(1000/10);
    }
    
}


void checkLEDState() {
  digitalWrite(LEDPin, LEDState);
  const bool newState = digitalRead(buttonPin); // See if button is physically pushed
  if (!newState) {
    LEDStateChange(!LEDState);
    delay(500);
  }
}

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(LEDPin, OUTPUT);
  pinMode(buttonPin, INPUT);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Setup 'on' listen events
  webSocket.on("connect", socket_Connected);
  webSocket.on("event", socket_event);
  webSocket.on("status", socket_statusCheck);
  webSocket.on("response", socket_response);
  webSocket.on("state_change_request", socket_pushButton);

  // Setup Connection
  if (useSSL) {
    webSocket.beginSSL(host, port, path, sslFingerprint);
  } else {
    webSocket.begin(host, port, path);
  }
  
  // Handle Authentication
  if (useAuth) {
    webSocket.setAuthorization(serverUsername, serverPassword);
  }
  webSocket.emit("stream", "{\"message\":\"hello1\"}");
  init_camera();

  camera_capture();

}

void loop() {
  
  webSocket.loop();
  // checkLEDState();
  
}