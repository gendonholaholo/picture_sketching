import argparse
import os
from convert_to_json import main as convert_to_json_main  
from draw_with_turtle import main as draw_with_turtle_main  

def parse_args():
    parser = argparse.ArgumentParser(description="Convert image to contours and draw with Turtle.")
    parser.add_argument('--img', required=True, help="Path to the input image.")
    return parser.parse_args()

def main():
    args = parse_args()

    if not os.path.exists(args.img):
        print(f"Error: File {args.img} tidak ditemukan.")
        return

    output_json = os.path.splitext(args.img)[0] + ".json"
    
    print(f"Converting image {args.img} to JSON at {output_json}...")
    convert_to_json_main(args.img, output_json)

    print(f"Drawing contours from {output_json}...")
    draw_with_turtle_main(output_json)

    print("Process completed successfully.")

if __name__ == '__main__':
    main()
