# This is the documentation of Image Manipulation Project

Main idea: Work with Manipulate class in `ImageManipulator.py` that will have the created effects and will also keep 
track of the effect history with the help of `@save_history` decorator

## Target:
An edge detection filter and use that data to create the original image from simple lines

## Use Example

````python
from image_manipulation.v2.ImageManipulator import Manipulate
img = Manipulate()

img.default().show()
img.history()
````

