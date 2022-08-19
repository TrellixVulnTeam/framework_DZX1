# Custom resources folder

Place here all resources (e.g. images, videos, PDFs, etc.) that should be accessible during the evaluation.
The relative path in relation to the `custom_resources` folder will be used in the URL path on which the resource will be served.

### Example 1
An image called `image.png` is placed within the `custom_resources` folder.
The server will host this image at `DOMAIN/resources/custom/image.png`

### Example 2
A video called `video.mp4` is placed within the `custom_resources` folder in a subfolder called `CSP`.
The server will host this image at `DOMAIN/resources/custom/CSP/video.mp4`.
