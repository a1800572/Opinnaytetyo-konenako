import cv2

username = input("Enter ip-camera username: ")
password = input("Enter ip-camera password: ")
cameraip = "192.168.10.39:88"
#yhteys ip kameraan
cap = cv2.VideoCapture("rtsp://" + username + ":" + password + "@" + cameraip + "/videoSub")

#luodaan while loop, joka jatkuu ikuisesti, eli kamera yhteys pysyy auki
while True:
    ret, frame = cap.read()
    #nimetään kamera ikkuna, määritellään visuaalisen datan tulolähde
    cv2.imshow("ipkameranäkymä", frame)
    #käyttäjä voi katkaista while loopin painamalla näppäimistön q painiketta
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# jos while loop katkaistaan kamera näkymä sammutetaan
cap.release()
cv2.destroyAllWindows()