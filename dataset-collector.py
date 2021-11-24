import cv2
import os
import np
import pyautogui

username = input("Enter ip-camera username: ")
password = input("Enter ip-camera password: ")
cameraip = "192.168.10.39:88"
paakansio = "Kuvat"
alakansio = input("Syötä alakansion nimi: ")
alakansioninkramentti = 1
haluttukuvamaara = input("Syötä tallennettavien kuvien lukumäärä: ")
kuvienkokonaismaara = 0
alakansioidenkokonaismaara = 0
haluttuvarikanava = input(
    "Värikanava vaihtoehdot: 1 = normaali, 2 = harmaa, 3 = punainen, 4 = vihreä, 5 = sininen, valitse värikanava: ")

# pääkansion luominen
if not os.path.exists(paakansio):
    print("Kansio nimeltä: " + paakansio + " ei ole olemassa...")
    print("Luodaan kansiota nimeltä: " + paakansio)
    os.makedirs(paakansio)
else:
    print("Kansio nimeltä: " + paakansio + " on jo olemassa")

# alakansion luominen, uudellen nimeäminen
if not os.path.exists(paakansio + "/" + alakansio):
    os.makedirs(paakansio + "/" + alakansio)
    print("Luodaan alakansiota nimeltä: " + alakansio + "...")
else:
    while os.path.exists(paakansio + "/" + alakansio + (str(alakansioninkramentti))):
        alakansioninkramentti += 1
    os.makedirs(paakansio + "/" + alakansio + (str(alakansioninkramentti)))
    print("Alakansio: " + alakansio + " on olemassa, uudelleen nimetään kansio nimellä: " + alakansio + (
        str(alakansioninkramentti)))

# yhteys ip kameraan
cap = cv2.VideoCapture("rtsp://" + username + ":" + password + "@" + cameraip + "/videoSub")
# jos primaarinen kamera ei ole saatavilla yhdistetään sekundääriseen kameraan
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(0)
    print("Ip-kamera ei ole saatavilla tarkista käyttäjätunnus ja salasana, yhdistetään web-kameraan")
else:
    print("Ip-kamera saatavilla, yhdistetään ip-kameraan")

# dynaaminen kuvien nimeäminen, kuvien lukumäärän selvittäminen
for polku, kansiot, tiedostot in os.walk(paakansio):
    kuvienkokonaismaara += len(tiedostot)
    alakansioidenkokonaismaara += len(kansiot)
    kuvainkramentti = kuvienkokonaismaara
print(paakansio + " kansio sisältää: " + (str(alakansioidenkokonaismaara)) + " alakansiota")
print("Alakansiot sisältävät: " + (str(kuvienkokonaismaara)) + " kuvaa")

# luodaan while loop, joka jatkuu ikuisesti, eli kamera yhteys pysyy auki
while True:
    ret, frame = cap.read()
    # ratkaistaan visuaalisen syötteen tulolähteen leveys ja korkeus
    kuvanleveys = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    kuvankorkeus = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # ratkaistaa ruudun leveys, korkeus
    ruudunleveys = pyautogui.size().width
    ruudunkorkeus = pyautogui.size().height
    resoluutio = str(kuvanleveys) + "x" + str(kuvankorkeus)
    fontti = cv2.FONT_HERSHEY_SIMPLEX
    kuvalaskuri = str(kuvainkramentti - kuvienkokonaismaara) + "/" + str(haluttukuvamaara)
    cv2.putText(frame, kuvalaskuri, (10, int(kuvankorkeus) - 30), fontti, 0.5, (255, 255, 255), 1, cv2.LINE_4)
    cv2.putText(frame, resoluutio, (10, int(kuvankorkeus) - 10), fontti, 0.5, (255, 255, 255), 1, cv2.LINE_4)
    cv2.imshow("kameranäkymä", frame)
    cv2.moveWindow("kameranäkymä", int(ruudunleveys / 2 - kuvanleveys / 2), int(ruudunkorkeus / 2 - kuvankorkeus / 2))

    mitoitus = cv2.resize(frame, (1024, 1024))
    harmaa = cv2.cvtColor(mitoitus, cv2.COLOR_BGR2GRAY)
    nollamatriisi = np.zeros(mitoitus.shape[:2], dtype="uint8")
    (punainen, vihrea, sininen) = cv2.split(mitoitus)
    punainen = cv2.merge([nollamatriisi, nollamatriisi, punainen])
    vihrea = cv2.merge([nollamatriisi, vihrea, nollamatriisi])
    sininen = cv2.merge([sininen, nollamatriisi, nollamatriisi])
    # nimetään kamera ikkuna, määritellään visuaalisen datan tulolähde

    if os.path.exists(paakansio + "/" + alakansio + (str(alakansioninkramentti))):
        kuvanimi = paakansio + "/" + alakansio + (str(alakansioninkramentti)) + "/%d.jpg" % kuvainkramentti
    else:
        kuvanimi = paakansio + "/" + alakansio + "/%d.jpg" % kuvainkramentti

    if int(haluttuvarikanava) == 1:
        cv2.imwrite(kuvanimi, mitoitus)
    elif int(haluttuvarikanava) == 2:
        cv2.imwrite(kuvanimi, harmaa)
    elif int(haluttuvarikanava) == 3:
        cv2.imwrite(kuvanimi, punainen)
    elif int(haluttuvarikanava) == 4:
        cv2.imwrite(kuvanimi, vihrea)
    elif int(haluttuvarikanava) == 5:
        cv2.imwrite(kuvanimi, sininen)
    else:
        cv2.imwrite(kuvanimi, mitoitus)

    kuvainkramentti += 1
    # käyttäjä voi katkaista while loopin painamalla näppäimistön q painiketta
    if kuvainkramentti == int(haluttukuvamaara) + int(kuvienkokonaismaara) or cv2.waitKey(1) & 0xFF == ord('q'):
        break
# konsoli viesti kuvien sijainnista
if os.path.exists(paakansio + "/" + alakansio + (str(alakansioninkramentti))):
    print("Kuvat luotu kansioon: " + alakansio + (str(alakansioninkramentti)))
else:
    print("Kuvat luotu kansioon: " + alakansio)
# jos while loop katkaistaan kamera näkymä sammutetaan
cap.release()
cv2.destroyAllWindows()
