# AutoSpriter for Pulltop VNs

This tool automatically generates sprite images for Visual Novels by Pulltop and others, tested with:

* If My Heart Had Wings / Konosora (この大空に、翼をひろげて)
* A Sky Full of Stars / Miazora (見上げてごらん、夜空の星を)

and all related fandiscs.

## Usage

    python autospriter.py <base_dir> <file_prefix> <layer_number1> <layer_number2> [...] 
    
Where `base_dir` is the directory containing all the sprite images and layer.txt files, 
`file_prefix` is the prefix of the relevant sprite set file (e.g. A`_KOT_01L`) and the layer numbers are the three digit 
indexes of the sprite images.

To make use of AutoSpriter, you must extract the sprites into their own folder (the `base_dir`).
This can be usually be achieved by using `exoozoarc.exe` on the `GRAPHIC.arc` file which is found in the game directory.

This script requires Pillow and a copy of `unpremultiply.exe` (to be placed in the same directory as the script).

Both `exoozoarc` and `unpremultiply` are available from [here](http://asmodean.reverse.net/pages/exoozoarc.html).

## Example

Considering the Konosora English patch:

    python autospriter.py [base_dir] A_KOT_01L 007 049 058
    
would produce the following image:

![A smiling Kotori in casual clothes, sitting in her wheelchair](images/example.png)