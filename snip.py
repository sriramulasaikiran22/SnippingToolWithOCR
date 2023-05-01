import cv2
import numpy as np
import pyautogui
import pytesseract

# Take a screenshot of the entire screen
image = pyautogui.screenshot()
image = np.array(image)


# Save the screenshot to a file
# screenshot.save("screenshot.png")


# Create a named window to display the image
cv2.namedWindow("Image")

# Define the initial coordinates of the rectangle
x, y, w, h = 0, 0, 0, 0

# Define a flag variable to indicate if the user is currently drawing the rectangle
drawing = False
done = False


def mouse_callback(event, x_pos, y_pos, flags, params):
    global x, y, w, h, drawing, done

    if event == cv2.EVENT_LBUTTONDOWN:
        # The user has started drawing the rectangle
        drawing = True
        x, y = x_pos, y_pos

    elif event == cv2.EVENT_MOUSEMOVE:
        # The user is moving the mouse, update the rectangle dimensions
        if drawing:
            w, h = x_pos - x, y_pos - y

    elif event == cv2.EVENT_LBUTTONUP:
        # The user has finished drawing the rectangle
        drawing = False
        done = True


def increase_brightness(img, val):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - val
    v[v > lim] = 255
    v[v <= lim] += val
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def get_text_from_image(img):

    br_img = increase_brightness(img, 50)
    gray = cv2.cvtColor(br_img, cv2.COLOR_BGR2GRAY)

    # Invert the image to make the text white and the background black
    # inverted = cv2.bitwise_not(gray)
    _, th = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Apply OCR to recognize text in the image
    br_text = pytesseract.image_to_string(gray)

    return br_text


# Set the mouse callback function for the window
cv2.setMouseCallback("Image", mouse_callback)

while True:
    # Create a copy of the original image to draw on
    image_copy = image.copy()
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_RGB2BGR)

    # Draw the rectangle on the image
    cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), -1,)
    alpha = 0.2
    image_copy = cv2.addWeighted(image_copy, alpha, image, 1 - alpha, 0)

    # Display the image in the window
    cv2.imshow("Image", image_copy)

    # Wait for a key event
    key = cv2.waitKey(1) & 0xFF

    # Check if the user pressed the 'q' key to quit the program
    if key == ord("d") or key == 27 or done:
        break
cv2.destroyAllWindows()

crop_image = image[y:y+h, x:x+w]
print(crop_image, len(crop_image), crop_image.shape, x, x+w)
if crop_image.size > 0:
    cv2.imshow('Cropped Image', crop_image)
    text = get_text_from_image(crop_image)
    print(text)
    cv2.waitKey(0)

# Release the window and exit the program
cv2.destroyAllWindows()
