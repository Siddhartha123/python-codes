#include <iostream>
#include "SerialPort.h"
#include <stdio.h>
#include <string.h>

using namespace std;

char* portName = "\\\\.\\COM20";

#define MAX_DATA_LENGTH 255

char incomingData[MAX_DATA_LENGTH], s[MAX_DATA_LENGTH];

//Control signals for turning on and turning off the led
//Check arduino code
char ledON[] = "ON\n";
char ledOFF[] = "OFF\n";

//Arduino SerialPort object
SerialPort *arduino;

//Blinking Delay
const unsigned int BLINKING_DELAY = 1000;

//If you want to send data then define "SEND" else comment it out
#define SEND

void exampleReceiveData(void)
{
    int readResult = arduino->readSerialPort(incomingData, MAX_DATA_LENGTH);
    printf("%s", incomingData);
    Sleep(10);
}

void exampleWriteData(unsigned int delayTime)
{
    arduino->writeSerialPort(ledON, MAX_DATA_LENGTH);
    Sleep(delayTime);
    arduino->writeSerialPort(ledOFF, MAX_DATA_LENGTH);
    Sleep(delayTime);
}

int main()
{
	char d;
    arduino = new SerialPort(portName);

    //Checking if arduino is connected or not
    if (arduino->isConnected()){
        std::cout << "Connection established at port " << portName << endl;
    }

	while (1) {
		cout << "Enter character: ";
		cin >> d;
		rotate_right(d);
	}
}

void rotate_right(char c) {
	if (arduino->isConnected()) {
		arduino->writeSerialPort(c, MAX_DATA_LENGTH);
		while (arduino->readSerialPort(s, MAX_DATA_LENGTH) == 0);
		cout << s;
	}
}