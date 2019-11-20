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
    key_points = params[1]
    nb_key_points = len(key_points)
    #right-click event value is 2
    if event == 2:
        
        if nb_key_points < 4:
            #store the new key_point
            key_points.append([x, y])
        
            draw_dot(image, x, y, len(key_points))
            
            if nb_key_points == 3:
                cv2.line(image, (key_points[0][0], key_points[0][1]), (key_points[-1][0], key_points[-1][1]),(255, 0, 0), 1) 
                
            if nb_key_points >= 1 :
                cv2.line(image, (key_points[-1][0], key_points[-1][1]), (key_points[-2][0], key_points[-2][1]),(255, 0, 0), 1)  
        print (key_points)
        
def shape_window(img, display_scale):
    window_width = int(img.shape[1] * display_scale)
    window_height = int(img.shape[0] * display_scale)
    return window_width, window_height

def setup_window(img, key_points, display_scale, name_window):
    cv2.namedWindow(name_window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name_window, shape_window(img, display_scale))
    cv2.setMouseCallback(name_window, mouse_callback, [img, key_points])

def get_name_image(image_path):
    return image_path.split("\\")[-1].split("/")[-1].split(".")[-2]
    
def run(pathMapImage, pathImage, output_dir, display_scale):
    map_image = cv2.imread(pathMapImage,1)
    image = cv2.imread(pathImage,1)
    
    name_map = get_name_image(pathMapImage)
    name_image = get_name_image(pathImage)
    print(name_map)
    print(name_image)
    key_points_map = []
    key_points_image = []
    
    setup_window(image, key_points_image, display_scale, name_image)
    setup_window(map_image, key_points_map, display_scale, name_map)
    
    while (True):
        cv2.imshow(name_image, image)
        cv2.imshow(name_map, map_image)
        
        if cv2.waitKey(20) == 27:
            break
        
        if len(key_points_image) == 4 and len(key_points_map) == 4:
            break
    
    try:
        output_dir = output_dir + name_map + "-" + name_image + "/"
        os.mkdir(output_dir)
    except OSError:
        print ("Creation of the directory %s failed" % output_dir)
    
    
    cv2.imwrite(output_dir + name_image + ".png", image)
    cv2.imwrite(output_dir + name_map + ".png", map_image)
    
    key_point = {}
    key_point["image"] = key_points_image
    key_point["map"] = key_points_map
    
    with open(output_dir+'key_points.json', 'w') as outfile:
        json.dump(key_point, outfile)
    
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