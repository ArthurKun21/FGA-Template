# FGA Template Helper

This project is created to help the creation of the template images for FGA

Current plans.

1. `Create` - Given the original `Left`, `Right`, `Top`, `Bottom` and the `original reference image` it would then create the template image.

2. `Reverse` - Given the template `Left`, `Right`, `Top`, `Bottom` and `another reference image`. It would reverse the calculations of the template sizes and fit it to the another reference image to create a template image based from the another reference image.
   1. `Normal` - uses the normal calculation
   2. `From Center` - uses the center of the template image as the reference point
   3. `From Right` - uses the right side of the template image as the reference point

3. `Draw`
   1. Location - Given the template `Left`, `Right`, `Top`, `Bottom` and the `original reference image` it would then draw a cross mark to the location.
   2. Region - Given the template `Left`, `Right`, `Top`, `Bottom` and the `original reference image` it would then draw a rectangle to the region.

4. `Match`
   1. `Template` - Given the template image and the region it resides in the original reference image. It would then match the template image to the region of the reference image using opencv.
   2. `Find` - Given the template image and an reference image. It would check the reference image for the region where it has the highest match rate with the template image.

5. `GUI` - A simple GUI to help with the usage of the program. Currently considering `pysimplegui` as the GUI library.