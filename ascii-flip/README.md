![ascii_preview](https://github.com/s-sandra/creativecode/blob/master/novel/ascii_aquarium.gif)
# ASCII Flipbook
## Project Description
Created for [NaNoGenMo 2019](https://github.com/NaNoGenMo/2019/issues/106), this python program generates a PDF flipbook that contains pages of ASCII art, which transforms into an animation as you scroll through the document. Like impressionist pieces, the images are best viewed when zoomed out, in a PDF reader like Adobe Acrobat. I created the text using [a short snippet of code written by Christian Diener]( https://gist.github.com/cdiener/10567484).

## Contents
### ASCII Ocean
- ascii_beach.pdf: Calming Ocean Waves (Tobago). [YouTube]( https://www.youtube.com/watch?v=oNBX7Ag2Wgc).
- ascii_waves.pdf: Ocean Waves Slow Motion Video. [YouTube]( https://www.youtube.com/watch?v=dJhOgDoKZmI).
- ascii_aquarium.pdf: Underwater Marine Life. [YouTube](https://www.youtube.com/watch?v=ou9lYK9g2G8).

### ASCII Slow Mo
- drop.pdf: HD Slo mo Water Drop. [YouTube](https://www.youtube.com/watch?v=gS_tU6chC4A).
- ice.pdf: Ice Cubes Into Glass of Water. [YouTube](https://www.youtube.com/watch?v=sa1C1BzhjQs).
- ink.pdf: Ink in Water Background. [YouTube](https://www.youtube.com/watch?v=W6ZTB6_P6mY).

### Other
- grape_vine.pdf: A video of my backyard that I used for testing.
- earth.pdf: Earth zoom out. [YouTube](https://www.youtube.com/watch?v=PESDQ84Yd8U).

## Dependencies
To generate your own ASCII flipbook, you will need to install OpenCV for video processing, Pillow and NumPy for image processing and ReportLab for PDF generation. If you would like to combine your generated flipbooks into one PDF, you will need to have installed PyPDF2. This can be done by running the following commands.

```
pip install opencv-python
pip install reportlab
pip install pypdf2
pip install Pillow
pip install numpy
```

## How It Works
To create the animation, I took a short video file and split it into individual frames using OpenCV. I then fed all the images through the asciinator and wrote their results to a PDF using ReportLab. The latter step was the most challenging, since I wanted to size the PDF pages to fit the content of the ASCII image, rather than default to a standard document size. This required passing a row of ASCII text to `stringWidth()`, a function from ReportLab’s pdfmetrics module, to compute the image width. I estimated the image height by multiplying the number of rows in the ASCII image by the font size and 1.2 (since ReportLab uses a gap of 20 percent of the font size to space out lines of text).

## Output
The ASCII flipbook generator creates a PDF file and a text file, as well as a folder that contains the individual video frames. It also prints out an estimation of the novel’s word count, by splitting the output string on spaces. The sample animations included in this repository are derived from personal and YouTube videos, but the generator can theoretically turn any video files (ideally less than 1000 frames) into novels, so long as they are supported by OpenCV. You may have to play with asciinator’s intensity attribute to get recognizable images.

## Merging Flipbooks
Once you have created several flipbook PDFs, you can merge them into one giant flipbook using `merge.py`. It accepts the name of the outputted PDF, followed by a list of the PDF files you wish to combine. They will be merged in the order specified. Below is an example command that creates an ASCII Ocean PDF in the current directory.

```
python3 merge.py ascii_ocean.pdf ascii_beach.pdf ascii_waves.pdf ascii_aquarium.pdf
```

