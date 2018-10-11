from PIL import Image
import sys, os, subprocess, random

"""
Reads a layers.txt file and returns a dict representing the contained information
"""
def parse_layers(filename):
    layerdata = {
        "img_width": 0,
        "img_height": 0,
        "layers": []
    }
    with open(filename, "r") as f:
        lidx = 0
        for line in f:
            line = line.strip()
            if lidx == 0:
                dimensions = line.split(" ")
                layerdata["img_width"] = int(dimensions[0])
                layerdata["img_height"] = int(dimensions[1])
            else:
                data = line.split("\t")
                layerdata["layers"].append({
                    "z_index": int(data[0].strip()),
                    "x": int(data[1].strip()),
                    "y": int(data[2].strip()),
                    "w": int(data[3].strip()),
                    "h": int(data[4].strip()),
                    "filename": data[5].strip(),
                })
            lidx += 1
    return layerdata

"""
Reverts the premultiplication on the layers
"""
def unpremultiply(filename):
    newfn = os.path.abspath("temp-" + str(random.randint(0, 1000)) + ".png")
    try:
        subprocess.call(["unpremultiply.exe", filename, newfn])
        return newfn
    except Exception as e:
        print(e)
        print("Unable to run unpremultiply.exe, check it is in the script directory.")
        exit(1)

"""
Sorting helper function
"""
def sort_drawdata(layer):
    return layer["z_index"]

"""
Actually generates the image
"""
def generate_image(drawdata, width, height):
    img = Image.new("RGBA", (width, height), None)
    for layerdata in drawdata:
        layer = Image.open(layerdata["filename"])
        img.alpha_composite(layer, dest=(layerdata["x"], layerdata["y"]))
        layer.close()
        os.unlink(layerdata["filename"])
    img.save("output.png")

"""
Outputs the usage information to the console
"""
def print_usage():
    print("AutoSpriter for Pulltop VNs")
    print("By Zudo (github.com/ZudoMC)")
    print("")
    print("Usage: autospriter.py <base_dir> <file_prefix> <layer_number1> <layer_number2> [...]")


"""
Main entry point for AutoSpriter
"""
def main():
    if len(sys.argv) < 4:
        print_usage()
        exit(1)
    else:
        dir = os.path.abspath(sys.argv[1])
        prefix = sys.argv[2]
        layers_raw = sys.argv[3:]

        print("Generating a sprite with " + str(len(layers_raw)) + " layers.")

        print("Parsing layer data")
        layers_filename = os.path.join(dir, prefix + "+PNAP+layers.txt")
        layerdata = parse_layers(layers_filename)

        drawdata = []
        layers = []

        for layer in layers_raw:
            layers.append(prefix + "+PNAP+" + layer + ".png")

        print("Reverting premultiplication")
        for layer in layerdata["layers"]:
            if layer["filename"] in layers:
                drawdata.append({
                    "filename": unpremultiply(os.path.join(dir, layer["filename"])),
                    "x": layer["x"],
                    "y": layer["y"],
                    "w": layer["w"],
                    "h": layer["h"],
                    "z_index": layer["z_index"]
                })

        drawdata.sort(key=sort_drawdata)

        print("Generating image")
        generate_image(drawdata, layerdata["img_width"], layerdata["img_height"])

        print("Saved to output.png")


if __name__ == "__main__":
    main()