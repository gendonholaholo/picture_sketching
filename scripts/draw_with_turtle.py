import json
import turtle

def load_json_data(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)

def rgb_to_turtle_color(rgb):
    if len(rgb) == 4:  
        return tuple(c / 255 for c in rgb[:3])  
    elif len(rgb) == 3:  
        return tuple(c / 255 for c in rgb)  
    else:
        raise ValueError("Invalid color format, expected 3 or 4 values in RGB or RGBA.")

def draw_with_turtle(contours, scale=10):
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("black")  
    screen.title("Turtle Drawing")  
    turtle.tracer(200, 0)  

    t = turtle.Turtle()
    t.speed(0)
    t.pensize(1)  

    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')

    for contour in contours:
        points = contour['points']
        for point in points:
            if isinstance(point, list) and len(point) == 2:  
                x, y = point
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    t.penup()
    t.goto(-center_x / scale, center_y / scale)  
    t.pendown()

    # Menggambar setiap kontur
    for contour in contours:
        points = contour['points']  
        colors = contour['colors']  

        t.penup()

        for i, point in enumerate(points):
            if isinstance(point, list) and len(point) == 2:  
                x, y = point
                t.goto((x - center_x) / scale, (center_y - y) / scale)  

                if i == 0:  
                    t.pendown()

                turtle_color = rgb_to_turtle_color(colors[i])  
                t.pencolor(turtle_color)  

            if i < len(points) - 1:  
                next_point = points[i + 1]
                if isinstance(next_point, list) and len(next_point) == 2:
                    x2, y2 = next_point
                    t.goto((x2 - center_x) / scale, (center_y - y2) / scale)  

    turtle.update()  
    turtle.done()

def main(json_path):
    contour_data = load_json_data(json_path)
    draw_with_turtle(contour_data, scale=1)  

json_path = 'E:\\Developer\\Program\\Python\\photo_drawing_turtle\\output\\image.json'  
main(json_path)
