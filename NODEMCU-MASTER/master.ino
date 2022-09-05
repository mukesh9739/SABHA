#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>

// Set these to run example.
#define FIREBASE_HOST "nodemcu-17c74.firebaseio.com"
#define FIREBASE_AUTH "tt1J5M522Ww8UJpCGRCIqoxue1zTVb9Il1HzRAEp"
#define WIFI_SSID "sairam"
#define WIFI_PASSWORD "mukesh9739"

void setup() {

  Serial.begin(9600);
  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);

  }

  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  pinMode(D0,INPUT);
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

}

void loop() {

  // set value
  int a=0;
  a=digitalRead(D0);
  if(a==1)
     Firebase.setInt("number", 1);   
  if(a==0)
     Firebase.setInt("number", 0); 

}
