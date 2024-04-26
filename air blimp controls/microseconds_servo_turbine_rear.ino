#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <ESP32Servo.h>
#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient client(espClient);
JsonDocument doc;
Servo pitchServo;
Servo mainEngine;
Servo rearMotor;

const char* ssid = "Kexxu";
const char* password = "kexxu-1NuM4Q2g";
const char* mqttServer = "192.168.2.79";
const int mqttPort = 1883;

const int servoPin = 26;  //servo
const int motorPin = 33;  //motor
const int rearPin = 32;   //rear

const float k = 3.428571;


int direction = 0;
int motor_speed = 10;
int rear_motor = 90;


void processJSONPayload(byte* payload, unsigned int length) {

  deserializeJson(doc, payload);
  if (doc.containsKey("direction")){
    direction = doc["direction"];
  }
  pitchServo.writeMicroseconds(direction);

  if (doc.containsKey("motor_speed")){
    motor_speed = doc["motor_speed"];
  }
  mainEngine.write(motor_speed);

  if (doc.containsKey("rear_motor")){
    rear_motor = doc["rear_motor"];
  }
  rearMotor.write(rear_motor);
}


void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  Serial.println("-----------------------");
  processJSONPayload(payload, length);
}

void setup() {

  pitchServo.attach(servoPin);
  mainEngine.attach(motorPin, 1000, 2000);
  rearMotor.attach(rearPin);
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP32Client")) {

      Serial.println("connected");

    } else {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  
  client.subscribe("servo");
  }
}

void loop() {
  client.loop();
}