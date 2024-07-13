#include <ArduinoJson.h>
#include <ESP32Servo.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <SPIFFS.h>

// WiFi and MQTT setup
WiFiClient espClient;
PubSubClient client(espClient);
DynamicJsonDocument doc(1024);
Servo pitchServo;
Servo mainEngine;
Servo rearMotor;

const char* ssid = "Kexxu";
const char* password = "kexxu-1NuM4Q2g";
const char* mqttServer = "192.168.2.79";
const int mqttPort = 1883;

const int servoPin = 26;  // Pin for the pitch servo
const int motorPin = 33;  // Pin for the main engine (brushless motor)
const int rearPin = 32;   // Pin for the rear motor

int direction = 0;
int motor_speed = 10;  // Initial value for motor speed
int rear_motor = 90;

double InputEngine = 0; // Distance variable for linear control
double minDistance = 50; // Minimum distance to the marker (closest)
double maxDistance = 500; // Maximum distance to the marker (farthest)
int minPower = 100;  // Minimum power
int maxPower = 150; // Maximum power

bool markerDetected = false;

void processManualControl(byte* payload, unsigned int length) {
  DeserializationError error = deserializeJson(doc, payload, length);

  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.f_str());
    return;
  }

  if (doc.containsKey("direction")) {
    direction = doc["direction"];
    pitchServo.write(direction);
  }

  if (doc.containsKey("motor_speed")) {
    motor_speed = doc["motor_speed"];
    mainEngine.write(motor_speed);
  }

  if (doc.containsKey("rear_motor")) {
    rear_motor = doc["rear_motor"];
    rearMotor.write(rear_motor);
  }
}

void processArUcoMarker(byte* payload, unsigned int length){
  DeserializationError error = deserializeJson(doc, payload, length);

  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.f_str());
    return;
  }

  if(doc.containsKey("unknown")){
    Serial.println("I saw a thing!");
  }
}

void processAutoPilot(byte* payload, unsigned int length){
  DeserializationError error = deserializeJson(doc, payload, length);

  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.f_str());
    return;
  }

  if(doc.containsKey("distance")){
    InputEngine = doc["distance"];
    markerDetected = true;  // Set flag when marker is detected
    Serial.print("InputEngine updated: ");
    Serial.println(InputEngine);
  } 
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message: ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");

  if (strcmp(topic, "manual") == 0) {
    processManualControl(payload, length);
  }
  else if(strcmp(topic, "aruco") == 0){
    processArUcoMarker(payload, length);
  }
  else if(strcmp(topic, "auto") == 0){
    processAutoPilot(payload, length);
  }
}

void setup() {
  Serial.begin(115200);

  pitchServo.attach(servoPin);
  mainEngine.attach(motorPin, 1000, 2000);
  rearMotor.attach(rearPin);

  Serial.println("Starting WiFi connection...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  Serial.println("Starting MQTT connection...");
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("manual");
      client.subscribe("aruco");
      client.subscribe("auto");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  client.loop();

  if (markerDetected) {
    if (InputEngine > maxDistance) {
      motor_speed = maxPower;
    } else if (InputEngine < minDistance) {
      motor_speed = 0; // Set motor speed to zero when too close to the marker
    } else {
      motor_speed = map(InputEngine, minDistance, maxDistance, minPower, maxPower);
    }
    mainEngine.write(motor_speed);

    Serial.print("Input: ");  // distance 
    Serial.print(InputEngine);
    Serial.print(" Motor Speed: ");
    Serial.println(motor_speed);


    // Reset the markerDetected flag after processing
    markerDetected = false;
  }

  delay(10); // Small delay to allow for smooth operation
}
