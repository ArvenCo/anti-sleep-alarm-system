from server.controller.system import process
from imports import *
import time

image = cv.imread('samples/sample image.jpg')

start = time.time()

print(process(image))

print(f"\nfinished at {time.time()- start} seconds")