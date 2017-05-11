
import math
MaxX = 0.85

for x in range(-40, 40, 1):

    scaled_x = 0.67 + abs(x)/100.0
    scaled_x = math.copysign(scaled_x, x)

    scaled_x = max(min(MaxX, scaled_x), -MaxX)
    print (x, scaled_x)
