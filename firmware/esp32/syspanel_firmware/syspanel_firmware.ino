#include <WiFi.h>

const char* WIFI_SSID = "Happy Cow";
const char* WIFI_PASSWORD = "Redfern40#";

WiFiServer server(8765);

void setup()
{
    Serial.begin(115200);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    Serial.print("Connecting");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println("Connected to Wi-Fi");

    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    server.begin();

    Serial.println("SysPanel server ready");
}

void loop()
{
    WiFiClient client = server.available();

    if (!client)
    {
        return;
    }

    Serial.println("PC connected");

    while (client.connected())
    {
        while (client.available())
        {
            char c = client.read();
            Serial.write(c);
        }
    }

    client.stop();

    Serial.println();
    Serial.println("PC disconnected");
}