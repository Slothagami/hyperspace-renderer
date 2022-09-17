from PIL import Image
im = Image.open("gifs/6-cube-cell-thicc-big.gif")

n = 0
while True:
    try:
        im.seek(n)
        im.save(f"frames/{n}.png")
        n += 12
    except EOFError:
        break