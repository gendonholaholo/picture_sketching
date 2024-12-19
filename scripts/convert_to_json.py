import cv2
import numpy as np
import json
from PIL import Image
from torchvision import transforms

def load_image(image_path):
    image = Image.open(image_path)
    return np.array(image)

def preprocess_image(image):
    if image.shape[-1] == 4:  
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)  

    preprocess = transforms.Compose([
        transforms.ToPILImage(),        
        transforms.Resize(256),         
        transforms.CenterCrop(224),     
        transforms.ToTensor(),          
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  
    ])

    image = preprocess(image)
    return image

def find_contours(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def extract_color(image, contour):
    color_points = []
    for point in contour:
        x, y = point[0]
        color = image[y, x]  
        color_points.append([int(c) for c in color])  
    return color_points

def contours_to_json(contours, image):
    contour_data = []
    for contour in contours:
        contour_points = contour.squeeze().tolist()  
        contour_colors = extract_color(image, contour)  
        contour_data.append({"points": contour_points, "colors": contour_colors})  
    return contour_data

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

def main(image_path, output_json):
    image = load_image(image_path)  
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
    )

    contours = find_contours(thresh)

    inverted_image = cv2.bitwise_not(thresh)
    inverted_contours = find_contours(inverted_image)

    all_contours = contours + inverted_contours

    contour_data = contours_to_json(all_contours, image)

    save_to_json(contour_data, output_json)
    print(f"JSON successfully saved at {output_json}")

if __name__ == '__main__':
    image_path = 'E:\\Developer\\Program\\Python\\photo_drawing_turtle\\images\\image4.png'  
    output_json = 'E:\\Developer\\Program\\Python\\photo_drawing_turtle\\output\\image.json'  
    main(image_path, output_json)
