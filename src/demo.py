from mapper import PixelMapper
import json 
import numpy as np


import argparse   
import cv2
import numpy as np
import json
import os


def draw_dot(img, x, y, id):
    print(x,y)
    cv2.circle(img, (x,y), 5, (255, 0, 0), 2)
    cv2.putText(img, str(id), (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):
    image = params[0]
    image2 = params[1]
    pixelMapperFct = params[2]
    
    #right-click event value is 2
    if event == 2:
        x_, y_= pixelMapperFct(np.array([[x,y]]))[0]
        draw_dot(image2, int(x_), int(y_), str(x)+" "+str(y))

            
        
def shape_window(img, display_scale):
    window_width = int(img.shape[1] * display_scale)
    window_height = int(img.shape[0] * display_scale)
    return window_width, window_height

def setup_window(img, key_points, display_scale, name_window):
    cv2.namedWindow(name_window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name_window, shape_window(img, display_scale))
    

def get_name_image(image_path):
    return image_path.split("\\")[-1].split("/")[-1].split(".")[-2]
    
def run(pathMapImage, pathImage, output_dir, display_scale):
    
    pixelMapper = None
    with open('data/output/map1-image1/key_points.json') as json_file:
        data = json.load(json_file)
        pixelMapper = PixelMapper(np.array(data["image"]), np.array(data["map"]))
        
    
    map_image = cv2.imread(pathMapImage,1)
    image = cv2.imread(pathImage,1)
    
    name_map = get_name_image(pathMapImage)
    name_image = get_name_image(pathImage)
    

    key_points_map = []
    key_points_image = []
    
    setup_window(image, key_points_image, display_scale, name_image)
    setup_window(map_image, key_points_map, display_scale, name_map)
    
    cv2.setMouseCallback(name_map, mouse_callback, [map_image, image, pixelMapper.map_to_image])
    cv2.setMouseCallback(name_image, mouse_callback, [image, map_image, pixelMapper.image_to_map])
    while (True):
        cv2.imshow(name_image, image)
        cv2.imshow(name_map, map_image)
        
        if cv2.waitKey(20) == 27:
            break
        
        
    
    try:
        output_dir = output_dir + name_map + "-" + name_image + "/"
        os.mkdir(output_dir)
    except OSError:
        print ("Creation of the directory %s failed" % output_dir)
    
    
    
    cv2.destroyAllWindows()
    

def parse_args():
    """Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Key point extractor for converting the position of a point on the MapImage to Image")
    parser.add_argument(
        "--mapImage",
        default="./data/map/map1.png",
        help="Path Input MapImage.")
    parser.add_argument(
        "--image",
        default="./data/image/image1.png",
        help="Path Input Image.")
    parser.add_argument(
        "--output_dir", 
        help="output_dir for the keypoints file and map/image with drawing",
        default="./data/output/")
    parser.add_argument(
        "--display_scale",
        default=1)
    
    return parser.parse_args()


def main():
    args = parse_args()
    run(args.mapImage, args.image, args.output_dir, float(args.display_scale))


if __name__ == "__main__":
    main()

