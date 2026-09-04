#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

void setup()
{
    Serial.begin(9600);

    lcd.init();
    lcd.backlight();
    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("Waiting for PC...");
}

void loop()
{
    if (Serial.available() > 0)
    {
        String message = Serial.readStringUntil('>');

        int start = message.indexOf('<');

        if (start == -1)
        {
            return;
        }

        message = message.substring(start + 1);

        int position = 0;

        for (int row = 0; row < 4; ++row)
        {
            int newline = message.indexOf('\n', position);

            String line;

            if (newline == -1)
            {
                line = message.substring(position);
            }
            else
            {
                line = message.substring(position, newline);
                position = newline + 1;
            }

            while (line.length() < 20)
            {
                line += ' ';
            }

            line = line.substring(0, 20);

            lcd.setCursor(0, row);
            lcd.print(line);
        }
    }
}