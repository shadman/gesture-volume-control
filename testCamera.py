import cv2
cv2.destroyAllWindows()
# For video capture normally we use
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows() 
