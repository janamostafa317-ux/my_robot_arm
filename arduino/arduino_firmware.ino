#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

void setup() {
  Serial.begin(115200);

  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(9);
  servo5.attach(10);

  servo1.write(90);
  servo2.write(90);
  servo3.write(90);
  servo4.write(90);
  servo5.write(90);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    int angles[5];
    int index = 0;
    int lastComma = -1;

    for (int i = 0; i < data.length(); i++) {
      if (data.charAt(i) == ',') {
        if (index < 5) {
          angles[index] = data.substring(lastComma + 1, i).toInt();
          index++;
        }
        lastComma = i;
      }
    }
    if (index < 5) {
      angles[index] = data.substring(lastComma + 1).toInt();
      index++;
    }

    if (index >= 5) {
      servo1.write(angles[0]);
      servo2.write(angles[1]);
      servo3.write(angles[2]);
      servo4.write(angles[3]);
      servo5.write(angles[4]);
    }
  }
}
