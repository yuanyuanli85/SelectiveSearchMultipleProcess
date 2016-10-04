from multiprocessing import Process, Queue, cpu_count
import random
import time
import os
import argparse
import cv2
import selectivesearch

def calc_ss_box(xfile, outpath, bsavebox=False):

    img = cv2.imread(xfile)   
    if len(img.shape) != 3:
        return 
    
    # perform selective search
    img_lbl, regions = selectivesearch.selective_search(
        img, scale=500, sigma=0.9, min_size=32)

    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 100x100 pixels
        if r['size'] < 10000:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 3 or h / w > 3:
            continue
        candidates.add(r['rect'])
   
    outfile = open(os.path.join(outpath, os.path.basename(xfile)+".ss"), 'w')
    for x, y, w, h in candidates:
        if bsavebox:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),2)
        outfile.write(str(x)+"\t"+str(y)+"\t"+str(w)+"\t"+str(h)+"\r\n")                        
    outfile.close()
    if bsavebox:
        cv2.imwrite(outpath+os.path.basename(xfile), img)
    

def serve(queue, xfilelst):
    for xfile in xfilelst:
        queue.put(xfile)


def work(id, queue, outpath):
    while True:
        xfile = queue.get()
        if xfile is None:
            break
        print "%d task:" % id, xfile
        calc_ss_box(xfile, outpath)
    queue.put(None)


class Scheduler:
    def __init__(self):
        self.queue = Queue()
        self.retqueue = Queue()
        self.pathlst = list()

    def start(self, cpu_num, xlist, outpath):
        print "starting %d workers " % cpu_num
        print "processing %d files" % len(xlist)
        self.workers = [Process(target=work, args=(i, self.queue, outpath))
                        for i in xrange(cpu_num)]
        for w in self.workers:
            w.start()

        serve(self.queue, xlist)

    def stop(self):
        
        self.queue.put(None)
        
        for i in range(len(self.workers)):
            self.workers[i].join()
        print "all of workers have been done"
        
        self.queue.close()
        
        while not self.retqueue.empty():
            item = self.retqueue.get()
            print "xx " , item
                

def run(img_path, out_path, cpu_num):
    #scan all files under img_path
    xlist = list()
    for xfile in os.listdir(img_path):
        xlist.append(os.path.join(img_path, xfile))
    
    #init scheduler
    x = Scheduler()
    
    #start processing and wait for complete 
    x.start(cpu_num, xlist, out_path)
    x.stop()
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--imgpath", help="path to your images to be proceed")
    parser.add_argument("--outpath", help="path to store generated selective box results")
    parser.add_argument("--cpunum", type=int, help="number of processor")
    
    args = parser.parse_args()
    run(args.imgpath, args.outpath, args.cpunum)
    