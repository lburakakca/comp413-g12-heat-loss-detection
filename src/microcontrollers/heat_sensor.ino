#include <WiFi.h>
#include <WebServer.h>
#include <DHT11.h> 

const char* ssid = "ESP32-AP";   
const char* password = "12345678"; 

IPAddress local_ip(192, 168, 4, 1);
WebServer server(80); 

#define DHTPIN1 27
#define DHTPIN2 12
#define DHTPIN3 14

DHT11 dht1(DHTPIN1);
DHT11 dht2(DHTPIN2);
DHT11 dht3(DHTPIN3);

void handleSensorData() {
    float temp1 = dht1.readTemperature();
    float hum1 = dht1.readHumidity();
    float temp2 = dht2.readTemperature();
    float hum2 = dht2.readHumidity();
    float temp3 = dht3.readTemperature();
    float hum3 = dht3.readHumidity();

    String jsonData = "{";
    jsonData += "\"sensor1\": {\"temp\": " + String(temp1) + ", \"humidity\": " + String(hum1) + "},";
    jsonData += "\"sensor2\": {\"temp\": " + String(temp2) + ", \"humidity\": " + String(hum2) + "},";
    jsonData += "\"sensor3\": {\"temp\": " + String(temp3) + ", \"humidity\": " + String(hum3) + "}";
    jsonData += "}";

    server.send(200, "application/json", jsonData);
}

void setup() {
    Serial.begin(115200);



    WiFi.softAP(ssid, password);
    WiFi.softAPConfig(local_ip, local_ip, IPAddress(255, 255, 255, 0));

    server.on("/sensorData", HTTP_GET, handleSensorData);

    server.begin();
    Serial.println("ESP32 Access Point başlatıldı");
    Serial.println("IP Adresi: 192.168.4.1");
}

void loop() {
    server.handleClient();
}