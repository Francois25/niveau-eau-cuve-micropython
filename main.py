from machine import *
import time, utime, network
from hcsr04 import HCSR04
import st7789
import tft_config
import vga1_bold_16x32, vga2_16x16  # font
import wificonnect

# definition pin module
led_bleu = Pin(27, Pin.OUT, 0)
led_verte1 = Pin(26, Pin.OUT, 0)
led_verte2 = Pin(25, Pin.OUT, 0)
led_jaune1 = Pin(33, Pin.OUT, 0)
led_jaune2 = Pin(32, Pin.OUT, 0)
led_rouge = Pin(12, Pin.OUT, 0)
buzzer = Pin(15, Pin.OUT, 0)

# definition du display
tft = tft_config.config()

# définition taille de la cuve
hauteur_max_eau = 1.60;   # hauteur d'eau maxi dans la cuve en m
position_capteur = 0.22;  # distance entre le capteur et le niveau maxi de la cuve en m
dimension_cuve_X = 1.10;  # taille de la cuve en X en m
dimension_cuve_Y = 5.68;  # taille de la cuve en Y en m

# definition variables:
surface_cuve = dimension_cuve_X * dimension_cuve_Y;
volume_max_cuve = round(surface_cuve * hauteur_max_eau, 2)
    
def calcul_volume():
    sensor = HCSR04(trigger_pin=22, echo_pin=21, echo_timeout_us=1000000)
    try:
        distance = sensor.distance_cm()/100
        volume_eau=round(((hauteur_max_eau + position_capteur) * surface_cuve) - (distance * surface_cuve), 2)
        print("Distance: ", distance, " cm\nVolume d'eau: ", volume_eau, " m3")
        return volume_eau
    except OSError as error:
        print('Sensor HS: ', error)
        error()

       
def affichage():
    tft.init()
    volume_disponible=calcul_volume()
    if volume_max_cuve > volume_disponible > 0:
        if volume_disponible >= 0.9 * volume_max_cuve:
            led_bleu.value(1)
        elif 0.8*volume_max_cuve <= volume_disponible < 0.9*volume_max_cuve:
            led_verte1.value(1)
        elif 0.6*volume_max_cuve <= volume_disponible < 0.8*volume_max_cuve:
            led_verte2.value(1)
        elif 0.4*volume_max_cuve <= volume_disponible < 0.6*volume_max_cuve:
            led_jaune1.value(1)
        elif 0.2*volume_max_cuve <= volume_disponible < 0.4*volume_max_cuve:
            led_jaune2.value(1)
        elif 0.1*volume_max_cuve <= volume_disponible < 0.2*volume_max_cuve:
            led_rouge.value(1)
        else:
            led_rouge.value(not led_rouge.value())
            time.sleep(1)
            buzzer.value(1)
        # affichage digital
        tft.text(vga1_bold_16x32, "NIVEAU CUVE", 35, 15, st7789.CYAN)
        tft.text(vga2_16x16, "Capacite: 10m3", 6, 60, st7789.YELLOW)
        tft.text(vga2_16x16, "Reste: ", 15, 95, st7789.GREEN)
        tft.text(vga2_16x16, str(volume_disponible), 120, 95, st7789.GREEN)
        tft.text(vga2_16x16, "m3", 190, 95, st7789.GREEN)
        time.sleep(10)
        tft.fill(st7789.BLACK)
        time.sleep(30)

    else:
        error()
        while True:
            led_rouge.value(not led_rouge.value())
            time.sleep(0.3)

def error():
    tft.init()
    tft.text(vga1_bold_16x32, "MESURE", 80, tft.height() // 3 - vga1_bold_16x32.HEIGHT//2, st7789.RED, st7789.BLACK)
    text = "ERRONEE"
    length=len(text)
    tft.text(vga1_bold_16x32, text, tft.width() // 2 - length // 2 * vga1_bold_16x32.WIDTH, 2 * tft.height() // 3 - vga1_bold_16x32.HEIGHT//2, st7789.RED, st7789.BLACK)
    utime.sleep(1)
    

wificonnect.connect()
while True:
    affichage()