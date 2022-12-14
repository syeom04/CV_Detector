#Created by Seungyun YEOM 
#syeom04

#MAIN HELP and credits to: https://pysource.com/2021/10/19/simple-color-recognition-with-opencv-and-python/
import cv2
import time

# Elif statements for other colors beside the RED and BLUE
"""
elif hue_value < 22:
    color = "ORANGE"
elif hue_value < 33:
    color = "YELLOW"
elif hue_value < 78:
    color = "GREEN"

"""

"""
elif hue_value < 170:
    color = "VIOLET"
    
""" 
#List will count the number of times each color appears. 
#red_freq = []
#blue_freq = []

#Open the camera in serial PORT 1 NOT the Laptop front facing camera. 
cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#Infite loop to keep searching for colors and QR codes. 
while True:
  
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    # Pick pixel value
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    color = "Undefined"
    if hue_value < 10:
        color = "RED"
        print("RED/BOMB", time.localtime().tm_sec)

      
    #Maybe alter the hue_value to strictly identify the colors. 
    elif hue_value >= 78 and hue_value < 131:
        color = "BLUE"
        print("BLUE/GENERAL", time.localtime().tm_sec)

        
    # Run the QR code scanner if RED and BLUE are not detected. 
        
    else:
        #Maybe if cannot color cannot be detected (for a period of time), search for the QR code instead. 
        color = "Undefined"
        
        detector = cv2.QRCodeDetector()

        # Capture the video frame by frame
        ret, frame = cap.read()
        data, bbox, straight_qrcode = detector.detectAndDecode(frame)

        """
        If this is general, transmit the general data to the UART
            Else if this is bomb, transmit the bomb data to the UART
        """
        
        
        if len(data) > 0:
            print(data, time.localtime().tm_sec)
        else:
            print('null')
        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        

        
    

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

    cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
    cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    

cap.release()
cv2.destroyAllWindows()