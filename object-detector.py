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
while True:
    ret, frame = cap.read()
    #tunnistimen hienosäätö
    objekti = tunnistin.detectMultiScale(frame, 1.1, 4)
    #laatikon piirtäminen objektin ympärille
    for (x, y, w, h) in objekti:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

    cv2.imshow("objectdetection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()