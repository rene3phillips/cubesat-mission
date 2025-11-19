#include <Arduino.h>
#include <DHT.h>

#define DHTPIN 2        // Pin connected to DHT22
#define DHTTYPE DHT22   // DHT22 sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature(); // Celsius
  float hum = dht.readHumidity();

  // Print to serial
  Serial.print("TEMP:");
  Serial.print(temp);
  Serial.print(",HUM:");
  Serial.println(hum);

  delay(2000); // 2 second delay
}
