from os import listdir
import imageio

frames = listdir("frames/")
frames.sort(key=lambda x: int(x[:-4]))

with imageio.get_writer('gifs/6-cube-cell-thicc.gif', mode='I', duration=.15) as writer:
    for frame in frames:
        image = imageio.imread("frames/" + frame)
        writer.append_data(image)