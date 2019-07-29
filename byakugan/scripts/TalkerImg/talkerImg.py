#!/usr/bin/env python

import cv2

camera = cv2.VideoCapture(2)

while True:
	ret, frame = camera.read()
	frame = cv2.resize(frame, (200,200))
	cv2.imshow('frame', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

camera.release()
cv2.destroyAllWindows()
