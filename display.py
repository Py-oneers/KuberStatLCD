import subprocess
import shlex
import json
from time import sleep
import drivers

display = drivers.Lcd()

display.lcd_display_string("Kubernetes", 1)  # Write line of text to first line of display
display.lcd_display_string("Cluster on Pi", 2)
sleep(5)
display.lcd_clear()

def long_string(display, text='', num_line=1, num_cols=16):
        """ 
        Parameters: (driver, string to print, number of line to print, number of columns of your display)
        Return: This function send to display your scrolling string.
        """
        if len(text) > num_cols:
            display.lcd_display_string(text[:num_cols], num_line)
            sleep(1)
            for i in range(len(text) - num_cols + 1):
                text_to_print = text[i:i+num_cols]
                display.lcd_display_string(text_to_print, num_line)
                sleep(0.2)
            sleep(1)
        else:
            display.lcd_display_string(text, num_line)
            
long_string(display, "Kubernetes Cluster on Raspberry Pi", 1)
long_string(display, "By Py-oneers", 2)
sleep(5)

def job():
    command = shlex.split("sudo kubectl get deployments k3s-deploy -o=json")
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, err = process.communicate()
    txt = str(output).strip()
    txt = json.loads(txt)
    value = txt['status']['conditions'][1]['reason']
    if(value == "MinimumReplicasAvailable"):
        long_string(display, "Application Status: ON", 1)
    else:
        long_string(display, "Application Status: OFF", 1)
    long_string(display, value, 2)
    display.lcd_clear()
    sleep(1)
    print(value);


while True:
    job()

    #sleep(10)
