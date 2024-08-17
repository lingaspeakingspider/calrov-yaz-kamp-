import cv2
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

weights_path = "yolov4.weights"
config_path = "yolov4.cfg"
names_path = "coco.names"

cap = cv2.VideoCapture(0)

try:
    net = cv2.dnn.readNet(weights_path, config_path)
except cv2.error as e:
    logging.error(f"YOLOv4 modeli yüklenirken hata: {e}")
    raise

layer_names = net.getLayerNames()
try:
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
except IndexError as e:
    logging.error(f"Layer isimleri alınırken hata: {e}")
    raise

with open(names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Kamera bağlantısı başarısız")
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([30, 150, 50])
    upper_bound = np.array([255, 255, 180])
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)

    blob = cv2.dnn.blobFromImage(filtered_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    height, width, channels = frame.shape
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Obje algılandı
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangular koordinatları
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)  # Yeşil renk
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            logging.info(f'Detected {label} with confidence {confidence:.2f}')

    cv2.imshow('Filtered Frame', filtered_frame)
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
