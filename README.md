# PixelMapperImage

## Extract keypoint
Afin de créer la matrice de perspective nous avons besoins de 4 points clées sur l'image de base et sur la carte.
Tool_config_pixel.py permet de facilement récuperer ces points
Exemple
'''
python .\src\tool_config_pixel.py --mapImage=.\data\map\map1.png --image=.\data\image\image1.jpg --output_dir=.\data\output\ --display_scale=0.5
'''

## Demo Mapper
Dans demo.py, on peut trouver un exemple de l'utilisation de PixelMapper afin de convertir un point sélectioné sur la map et l'affiché sur l'image et vice-versa

'''
python .\src\demo.py --mapImage=.\data\map\map1.png --image=.\data\image\image1.jpg  --display_scale=0.5
'''