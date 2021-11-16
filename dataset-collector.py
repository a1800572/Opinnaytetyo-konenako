import cv2
import os
username = input("Enter ip-camera username: ")
password = input("Enter ip-camera password: ")
cameraip = "192.168.10.39:88"
paakansio = "Kuvat"
alakansio = input("Syötä alakansion nimi: ")
alakansioninkramentti = 1

#pääkansion luominen
if not os.path.exists(paakansio):
    print("Kansio nimeltä: " + paakansio + " ei ole olemassa...")
    print("Luodaan kansiota nimeltä: " + paakansio)
    os.makedirs(paakansio)
else:
    print("Kansio nimeltä: " + paakansio + " on jo olemassa")

#alakansion luominen, uudellen nimeäminen
if not os.path.exists(paakansio+"/"+alakansio):
    os.makedirs(paakansio + "/" + alakansio)
    print("Luodaan alakansiota nimeltä: " + alakansio + "...")
else:
    while os.path.exists(paakansio + "/" + alakansio + (str(alakansioninkramentti))):
        alakansioninkramentti += 1
    os.makedirs(paakansio+"/"+alakansio + (str(alakansioninkramentti)))
    print("Alakansio: " + alakansio + " on olemassa, uudelleen nimetään kansio nimellä: " + alakansio + (str(alakansioninkramentti)))

#yhteys ip kameraan
cap = cv2.VideoCapture("rtsp://" + username + ":" + password + "@" + cameraip + "/videoSub")
#jos primaarinen kamera ei ole saatavilla yhdistetään sekundääriseen kameraan
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(0)
    print("Ip-kamera ei ole saatavilla tarkista käyttäjätunnus ja salasana, yhdistetään web-kameraan")
else:
    print("Ip-kamera saatavilla, yhdistetään ip-kameraan")

kuvainkramentti = 0
#luodaan while loop, joka jatkuu ikuisesti, eli kamera yhteys pysyy auki
while True:
    ret, frame = cap.read()
    # nimetään kamera ikkuna, määritellään visuaalisen datan tulolähde
    cv2.imshow("kameranäkymä", frame)
    if os.path.exists(paakansio+"/"+alakansio+(str(alakansioninkramentti))):
        kuvanimi = paakansio + "/" + alakansio + (str(alakansioninkramentti)) + "/%d.jpg" % kuvainkramentti
    else:
        kuvanimi = paakansio + "/" + alakansio + "/%d.jpg" % kuvainkramentti
    cv2.imwrite(kuvanimi, frame)
    kuvainkramentti += 1
    # käyttäjä voi katkaista while loopin painamalla näppäimistön q painiketta
    if kuvainkramentti == 2 or cv2.waitKey(1) & 0xFF == ord('q'):
        break
#konsoli viesti kuvien sijainnista
if os.path.exists(paakansio+"/"+alakansio+(str(alakansioninkramentti))):
    print("Kuvat luotu kansioon: " +alakansio+(str(alakansioninkramentti)))
else:
    print("Kuvat luotu kansioon: " + alakansio)
# jos while loop katkaistaan kamera näkymä sammutetaan
cap.release()
cv2.destroyAllWindows()