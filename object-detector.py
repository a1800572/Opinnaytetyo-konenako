import cv2

username = input("Enter ip-camera username: ")
password = input("Enter ip-camera password: ")
cameraip = "192.168.10.39:88"

# yhteys ip kameraan
cap = cv2.VideoCapture("rtsp://" + username + ":" + password + "@" + cameraip + "/videoSub")
# jos primaarinen kamera ei ole saatavilla yhdistetään sekundääriseen kameraan
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(0)
    print("Ip-kamera ei ole saatavilla tarkista käyttäjätunnus ja salasana, yhdistetään web-kameraan")
else:
    print("Ip-kamera saatavilla, yhdistetään ip-kameraan")

# alkeellinen tunnistin, ohjelman käynnistämistä, kokeilua varten
tunnistin = cv2.CascadeClassifier('custom-cascades\cascadetest.xml')
# selvitetään ikkunan leveys sekä korkeus, perusteella määritellään loppupiste koordinaatit
leveys = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
korkeus = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
while True:
    ret, frame = cap.read()
    #tunnistimen hienosäätö
    objekti = tunnistin.detectMultiScale(frame, 1.1, 4)
    #laatikon piirtäminen objektin ympärille
    for (x, y, w, h) in objekti:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)
        # viiva ylhäällä, lopetuspisteeksi voidaan määritellä ikuinen -y koordinaatti
        cv2.line(frame, (int(x) + int(w/2), int(y)), (int(x) + int(w/2), int(-korkeus)), (255, 255, 255), 1)
        # viiva vasemmalla, lopetuspisteeksi voidaan vääritellä ikuinen -x koordinaatti
        cv2.line(frame, (int(x), int(y) + int(h/2)), (int(-leveys), int(y) + int(h/2)), (255, 255, 255), 1)
        # viiva alhaalla, lopetuspisteeksi ei voida määritellä ikuista y koordinaattia
        cv2.line(frame, (int(x) + int(w/2), int(y) + int(h)), (int(x) + int(w/2), int(korkeus)), (255, 255, 255), 1)
        # viiva oikealla, lopetuspisteeksi ei voida määritellä ikuista x koordinaattia
        cv2.line(frame, (int(x) + int(w), int(y) + int(h/2)), (int(leveys), int(y) + int(h/2)), (255, 255, 255), 1)
    cv2.imshow("objectdetection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()