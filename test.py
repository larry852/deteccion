# Algoritmo de deteccion de triangulos
# Por Glar3
#
#
# Detecta triangulos azules

# Librerias
import cv2
import numpy as np
# Iniciar camara
# captura = cv2.VideoCapture(0)


# while(1):

# Caputrar una imagen y convertirla a hsv
imagen = cv2.imread('figuras.png')
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Guardamos el rango de colores hsv (azules)
bajos = np.array([67, 40, 105], dtype=np.uint8)
altos = np.array([129, 255, 182], dtype=np.uint8)

# Crear una mascara que detecte los colores
mask = cv2.inRange(hsv, bajos, altos)

# Filtrar el ruido con un CLOSE seguido de un OPEN
kernel = np.ones((6, 6), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Difuminamos la mascara para suavizar los contornos y aplicamos filtro canny
blur = cv2.GaussianBlur(mask, (5, 5), 0)
edges = cv2.Canny(mask, 1, 2)

# Si el area blanca de la mascara es superior a 500px, no se trata de ruido
_, contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(c) for c in contours]
i = 0
for extension in areas:
    actual = contours[i]
    approx = cv2.approxPolyDP(actual, 0.05 * cv2.arcLength(actual, True), True)
    cv2.drawContours(imagen, [actual], 0, (0, 0, 255), 2)
    cv2.drawContours(mask, [actual], 0, (0, 0, 255), 2)
    i = i + 1

# Mostrar la mascara final y la imagen
cv2.imshow('Finale', mask)
cv2.imshow('Imagen', imagen)

# Salir con ESC
while(1):
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

cv2.destroyAllWindows()
