import cv2

unchange = cv2.imread('/home/piai/umbr.jpg',cv2.IMREAD_COLOR)
cv2.imshow('Unchange',unchange)

cv2.waitKey(0)
cv2.destroyAllWindows()