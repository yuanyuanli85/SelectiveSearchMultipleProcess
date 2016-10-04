Selective Search Multiple Processes
===================


Selective search is a very good algorithm to generate detection proposals for a single image.  It usually takes 1-2 seconds to process single image. if you have lot of images to process, you will suffer from the long execution time. The code in this repo tries to schedule the jobs on multiple processes on you machine and process the images in parallel.  

----------


How to use it
-------------

 **Dependency:**

> - Selective Search
	>  pip install selective_search
> - OpenCV


 **Command:**
User need to tell the path of image to be proceed and the path to store box results. if there is a image named "cat.jpg",  its file to store selective search box results will be generated as "outpath/cat.jpg.ss".

> - usage: ssearch_mulprocess.py [-h] [--imgpath IMGPATH] [--outpath OUTPATH] [--cpunum CPUNUM]

>  --imgpath IMGPATH  path to your images to be proceed
    --outpath OUTPATH  path to store generated selective search box results
    --cpunum CPUNUM    number of processor
  
