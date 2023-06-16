import cv2
import matplotlib.pyplot as plt


class ImageProcessingUtils:

    @staticmethod
    def pre_process(image, resize_height=32, resize=False, hist=False,
                   noise_red=False, thresh=False):

        # Convert to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Resize the image
        if image.shape[0] < 32 and resize:
            width = int(image.shape[1] * (resize_height / image.shape[0]))
            image = cv2.resize(image, (width, resize_height))

        if hist:
            # Adaptive histogram equalization
            image = cv2.createCLAHE(
                clipLimit=1.0, tileGridSize=(4, 2)).apply(image)
        
        if noise_red:
            # Apply median filter
            image = cv2.medianBlur(image, 3)

        if thresh:
            # Apply adaptive thresholding
            image = cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, resize_height-1, 7)

        return image

    @staticmethod
    def show_img(image: list, titl: str):
        fig = plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.title(titl)
        plt.show()
        
