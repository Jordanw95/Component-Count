# Component Count
OpenCV and used with live Basler camera image, to count a high number of small components on a backlit image. Two inferfaces, Counting and reference - both built
using Tkinter. 

Project built based on use case of logistics centers, where counting of small components is required. Logistics centers can be working with
over 10,000 different components and require accurate counting of all of them. Following this, it is important that time taken to program for each individual component is kept low, whilst keeping counting
accurate and fast for use in production. Reference Interface allows quick programming to add new components to database. Counting page can then be used by logistics
workers to allow them to quickly, scan barcode, present on backlit board (with little care needed for presentation) and receive accurate,
live feedback for number of parts presented. 

## Reference Interface
This interface is used to add new component information to the database so that they can then be counted using the couting page.
Parts presented in reference image must be seperated and not touching (number of blobs recorded should match number of parts). Binarisation of
threshold and minimum detectable blob can then be adjusted using sliders. Adjust until number of blobs match number of parts and the difference max 
difference seen between blob sizes is smallest. 

Once correct, press save with name and barcode. This will save the data required for this part to be counted by counting page.

## Counting Page
Page shows a live stream of image from Basler Camera. Present parts in any order, overlapping or touching on backlit image. Enter name or barcode to collect 
data required to count that part. Counting page will then give live feedback (updated 10 times a second) of number of parts on backlight. If parts are overlapping to severely to provied 
accurate count, a warning will be shown for severe overlap and a box will be drawn on the live image to indicate which cluster of parts are causing the
innacuracy. 

