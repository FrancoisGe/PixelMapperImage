import numpy as np
import cv2


class PixelMapper(object):
    """
    Create an object for converting pixels to geographic coordinates,
    using four points with known locations which form a quadrilteral in both planes
    Parameters
    ----------
    image_array : (4,2) shape numpy array
        The (x,y) pixel coordinates corresponding to the top left, top right, bottom right, bottom left
        pixels of the known region
    map_array : (4,2) shape numpy array
        The (lon, lat) coordinates corresponding to the top left, top right, bottom right, bottom left
        pixels of the known region
    """
    def __init__(self, image_array, map_array):
        assert image_array.shape==(4,2), "Need (4,2) input array"
        assert map_array.shape==(4,2), "Need (4,2) input array"
        self.M = cv2.getPerspectiveTransform(np.float32(image_array),np.float32(map_array))
        self.invM = cv2.getPerspectiveTransform(np.float32(map_array),np.float32(image_array))
        
    def image_to_map(self, pixel):
        """
        Convert a set of pixel coordinates to lon-lat coordinates
        Parameters
        ----------
        pixel : (N,2) numpy array or (x,y) tuple
            The (x,y) pixel coordinates to be converted
        Returns
        -------
        (N,2) numpy array
            The corresponding (lon, lat) coordinates
        """
        if type(pixel) != np.ndarray:
            pixel = np.array(pixel).reshape(1,2)
        assert pixel.shape[1]==2, "Need (N,2) input array" 
        pixel = np.concatenate([pixel, np.ones((pixel.shape[0],1))], axis=1)
        xy_map = np.dot(self.M,pixel.T)
        
        return (xy_map[:2,:]/xy_map[2,:]).T
    
    def map_to_image(self, xy_map):
        """
        Convert a set of lon-lat coordinates to pixel coordinates
        Parameters
        ----------
        xy_map : (N,2) numpy array or (x,y) tuple
            The (lon,lat) coordinates to be converted
        Returns
        -------
        (N,2) numpy array
            The corresponding (x, y) pixel coordinates
        """
        if type(xy_map) != np.ndarray:
            xy_map = np.array(xy_map).reshape(1,2)
        assert xy_map.shape[1]==2, "Need (N,2) input array" 
        xy_map = np.concatenate([xy_map, np.ones((xy_map.shape[0],1))], axis=1)
        pixel = np.dot(self.invM,xy_map.T)
        
        return (pixel[:2,:]/pixel[2,:]).T

