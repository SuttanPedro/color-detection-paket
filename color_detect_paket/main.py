
import cv2
import numpy as np

framewidth = 340
frameheight = 580

cap = cv2.VideoCapture(0)

cap.set(3, framewidth)
cap.set(4, frameheight)


def empty(a):
    pass


cv2.namedWindow("Camera Settings")
cv2.resizeWindow("Camera Settings", 400, 100)
cv2.createTrackbar("Brightness", "Camera Settings", 50, 100, empty)  # Brightness dari 0 - 100
cv2.createTrackbar("Focus", "Camera Settings", 0, 100, empty)  # Fokus dari 0 - 100


cv2.namedWindow("HSV PAKET CILACAP UTARA")
cv2.resizeWindow("HSV PAKET CILACAP UTARA", 640, 240)
cv2.createTrackbar("HUE Min", "HSV PAKET CILACAP UTARA", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV PAKET CILACAP UTARA", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV PAKET CILACAP UTARA", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV PAKET CILACAP UTARA", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV PAKET CILACAP UTARA", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV PAKET CILACAP UTARA", 255, 255, empty)

cv2.namedWindow("HSV CILACAP SELATAN")
cv2.resizeWindow("HSV CILACAP SELATAN", 640, 240)
cv2.createTrackbar("HUE Min", "HSV CILACAP SELATAN", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV CILACAP SELATAN", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV CILACAP SELATAN", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV CILACAP SELATAN", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV CILACAP SELATAN", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV CILACAP SELATAN", 255, 255, empty)

while True:
    _, img = cap.read()
    
    brightness = cv2.getTrackbarPos("Brightness", "Camera Settings") / 100
    focus = cv2.getTrackbarPos("Focus", "Camera Settings")
    
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    cap.set(cv2.CAP_PROP_FOCUS, focus)
    
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    uh_min = cv2.getTrackbarPos("HUE Min", "HSV PAKET CILACAP UTARA")
    uh_max = cv2.getTrackbarPos("HUE Max", "HSV PAKET CILACAP UTARA")
    us_min = cv2.getTrackbarPos("SAT Min", "HSV PAKET CILACAP UTARA")
    us_max = cv2.getTrackbarPos("SAT Max", "HSV PAKET CILACAP UTARA")
    uv_min = cv2.getTrackbarPos("VALUE Min", "HSV PAKET CILACAP UTARA")
    uv_max = cv2.getTrackbarPos("VALUE Max", "HSV PAKET CILACAP UTARA")
    
    sh_min = cv2.getTrackbarPos("HUE Min", "HSV CILACAP SELATAN")
    sh_max = cv2.getTrackbarPos("HUE Max", "HSV CILACAP SELATAN")
    ss_min = cv2.getTrackbarPos("SAT Min", "HSV CILACAP SELATAN")
    ss_max = cv2.getTrackbarPos("SAT Max", "HSV CILACAP SELATAN")
    sv_min = cv2.getTrackbarPos("VALUE Min", "HSV CILACAP SELATAN")
    sv_max = cv2.getTrackbarPos("VALUE Max", "HSV CILACAP SELATAN")
    
    lower_clputara = np.array([uh_min, us_min, uv_min])
    upper_clputara = np.array([uh_max, us_max, uv_max])
    lower_clpsltn = np.array([sh_min, ss_min, sv_min])
    upper_clpsltn = np.array([sh_max, ss_max, sv_max])

    mask_utara = cv2.inRange(imgHsv, lower_clputara, upper_clputara)
    mask_selatan = cv2.inRange(imgHsv, lower_clpsltn, upper_clpsltn)
    
    result_utara = cv2.bitwise_and(img, img, mask=mask_utara)
    result_selatan = cv2.bitwise_and(img, img, mask=mask_selatan)
    
    mask_utara = cv2.cvtColor(mask_utara, cv2.COLOR_GRAY2BGR)
    mask_selatan = cv2.cvtColor(mask_selatan, cv2.COLOR_GRAY2BGR)
    
    
    #mask_comb = cv2.bitwise_and(mask_utara, mask_selatan)
    #mask_combo = cv2.bitwise_and(imgHsv, imgHsv, mask=mask_comb)
    #mask_combo = cv2.cvtColor(mask_combo, cv2.COLOR_GRAY2BGR)
    

    #result = cv2.bitwise_and(img, result_utara, result_selatan,)
    
    gray_mask_utara = cv2.cvtColor(mask_utara, cv2.COLOR_BGR2GRAY) if len(mask_utara.shape) == 3 else mask_utara
    contoursU, _ = cv2.findContours(gray_mask_utara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contoursU:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Paket Utara", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    gray_mask_selatan = cv2.cvtColor(mask_selatan, cv2.COLOR_BGR2GRAY) if len(mask_selatan.shape) == 3 else mask_selatan
    contoursS, _ = cv2.findContours(gray_mask_selatan, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contoursS:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Paket Selatan", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    uStack = np.hstack([img, mask_utara, result_utara])
    sStack = np.hstack([img, mask_selatan, result_selatan])

    cv2.imshow('UTARA', uStack)
    cv2.imshow('SELATAN', sStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
