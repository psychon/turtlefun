"""src/turtlefun/turtle_explorer.py"""

from decimal import Decimal
from loguru import logger
from queue import Queue
from threading import Thread, enumerate
from time import sleep

from .turtlent import TurtleNT

queue_theta = None
thread_path = None
thread_iterations = None

def _euler_spiral_calculation():
    """Calculate Euler Spiral and create report"""
    global queue_theta, thread_iterations, thread_path

    while not queue_theta.empty():
        theta = queue_theta.get()

        t = TurtleNT(path=thread_path, theta=theta, steplimit=10000000)        
        if t.file_exists():
            logger.warning("Skipping theta={} as data exists.", theta)
        else:
            logger.info("Starting caclulation of euler spiral for theta={}", theta)
            
            if t.euler_spiral():
                t.save_image()
                logger.success("Finish caclulation of euler spiral for theta={}", theta)
            else:
                logger.error("Failed to compute euler sprial for theta={}", theta)
        del t

def explore_euler_spiral_no_return() -> None:
    """Explore the Euler spiral with values in ./no-return.txt"""
    global queue_theta, thread_path, thread_iterations
    
    thread_path = "/backup/turtlefunexploration"
    
    queue_theta = Queue()
    
    with open("./no-return.txt", "r") as fp:
        for line in fp:
            try:
                theta = Decimal(line)
                queue_theta.put(theta) if theta > 85 else None
            except:
                logger.warning("Failed to convert {} to Decimal!", line)
        
    threads = []
    for _t in range(10):
        threads.append(Thread(target=_euler_spiral_calculation))
        
    for thread in threads:
        thread.start()
        
    while not queue_theta.empty():
        try:
            sleep(1)
        except KeyboardInterrupt:
            logger.warning("Exploration interrupted, but nor finished. {} explorations remaining.", queue_theta.qsize())
            queue_theta = Queue()
            
    logger.debug("Waiting for threads to finish")
    
    while True:
        if len(enumerate()) > 1:
            logger.debug("{} remaining threads found. Waiting.", len(enumerate()) - 1)
            sleep(5)
        else:
            break

    logger.debug("Clean exit.")