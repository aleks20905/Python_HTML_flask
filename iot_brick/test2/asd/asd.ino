#include <ESP8266WiFi.h>

const char* ssid = "MSAT";
const char* password = "83827525";

const char* host = "192.168.11.209";
const uint16_t port = 8080;

WiFiClient client;

void setup() {
  Serial.begin(115200);

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("connecting to ");
  Serial.print(host);
  Serial.print(':');
  Serial.println(port);
}

void loop() {
  
  if (!client.connected()) {

    client.connect(host, port);
     if (!client.connected()) {
      Serial.println("connection failed");
      delay(5000);
      return;

     }  
  }

  if (client.connected()) {

    sendString("device", "Esp8266");
    sendfloat("temp1", random(0,100));
    sendfloat("temp2", random(0,100));
    sendfloat("temp3", random(-30,30));
    sendfloat("temp4", random(10,70));
    sendBool("state1", true);
    delay(2000);

    clientSend();
  }
  

  //clientSend("device | esp8266 | chaimber | -5.56 | freon | 20 | outsideT | 15 | outsidT | 1 ");
  //delay(2000);


}

String mainString = "";

void sendfloat(String str, float value){
  if(mainString==""){
    mainString += str + " | " + String(value,3);
  }
  else {
    mainString += " | "+ str + " | " + String(value,3);
  }


}
void sendString(String str, String value){
  if(mainString==""){
    mainString += str + " | " + value;
  }
  else {
    mainString += " | "+ str + " | " + value;
  }


}
void sendBool(String str, bool value){
  if(mainString==""){
    mainString += str + " | " + boolstr(value);
  }
  else {
    mainString += " | "+ str + " | " + boolstr(value);
  }


}
String boolstr(bool a){
  if(a)
    return "TRUE";
  return "FALSE";
}


void clientSend(){

  Serial.println("sending data to server");
  Serial.println(mainString);

  client.print("&"+mainString);
  mainString = "";
  
}
