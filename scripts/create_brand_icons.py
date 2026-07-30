from PIL import Image

source = "assets/brand/logo/free_basics_logo.png"

img = Image.open(source)

sizes = {
    "assets/brand/logo/favicon-16x16.png": (16,16),
    "assets/brand/logo/favicon-32x32.png": (32,32),
    "assets/brand/logo/apple-touch-icon.png": (180,180),
}


for path, size in sizes.items():

    icon = img.convert("RGBA")

    icon.thumbnail(
        size,
        Image.LANCZOS
    )

    canvas = Image.new(
        "RGBA",
        size,
        (255,255,255,0)
    )

    x = (size[0]-icon.width)//2
    y = (size[1]-icon.height)//2

    canvas.paste(
        icon,
        (x,y),
        icon
    )

    canvas.save(
        path
    )


img.resize(
    (32,32)
).save(
    "assets/brand/logo/favicon.ico"
)


print("Brand icons created")
