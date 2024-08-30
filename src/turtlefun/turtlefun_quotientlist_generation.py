"""src/turtlefun/turtlefun_quotientlist_generation.py

NICE TRY, BUT DO NOT USE! MUCH TO TIME CONSUMING!

SEE DEFAULT 37 FOR A FAST AND RELIABLE WAY TO CALCULATE LARGE NUMBERS OF WHOLE NUMBER QUOTIENTS RELIABLY
"""

from decimal import Decimal
from loguru import logger
from queue import Queue
from sympy import nextprime
from threading import Thread, enumerate
from time import sleep, perf_counter
from typing import Union, List

queue_numbers = None
queue_results = None
results_file = "./turtlefun_denominatorlist.py"

class Count:
    def __init__(self,start=Decimal('0')):
        self.num = start
        if type(self.num) is not Decimal:
            self.num = Decimal(str(self.num))
    def __iter__(self):
        return self
    def __next__(self):
        self.num += Decimal('1')
        return self.num
    def current(self):
        return self.num

def get_primes(number:Union[int, float, str, Decimal]) -> List[Decimal]:
    """Generate primes for a given number"""
    primes = []
    prime = 1
    number = Decimal(str(number))
    if round(number, 0) != number:
        logger.critical("Primes can only be calculated for whole numbers.")
        raise ValueError("Whole number requires.")
    while True:
        prime = nextprime(prime)
        while round(number / Decimal(str(prime)), 0) == number / Decimal(str(prime)):
            number /= Decimal(str(prime))
            primes.append(Decimal(str(prime)))
        
        if number == 1:
            break
        if prime > number:
            logger.critical("Failed to calculate prime factors!")
            raise ValueError("Failed to calculate primes.")
    return primes

def _check_denominator():
    global queue_numbers, queue_results
    
    numerator = Decimal('360')
    pre_num_primes = get_primes(numerator)
    three = Decimal('3')
    
    while not queue_numbers.empty():
            
        denominator = queue_numbers.get()
        num_primes = pre_num_primes.copy()
        den_primes = get_primes(denominator)
        
        if Decimal('7') in den_primes:
            # as 7 is not a primefactor of 360, all 7 will result in non-finite decimal representation
            continue
        
        # try to remove all threes, as they are the remaining factor for forming non-finite decimal representations    
        while three in num_primes and three in den_primes:
            num_primes.remove(three)
            den_primes.remove(three)
        # logger.trace("{} / {} was reduced to ({}) / ({})", numerator, denominator, " * ".join(str(n) for n in num_primes), " * ".join(str(n) for n in den_primes))
        
        for prime in den_primes.copy():
            if prime in [2, 5]:
                den_primes.remove(prime)
            else:
                break
        if len(den_primes) == 0:
            fraction = numerator / denominator
            alpha = ((denominator * (denominator + Decimal('1')) / Decimal('2') * fraction) % Decimal('360'))
            logger.success("{} as denominator of 360 gives a finite fraction of {}, final turtle angle is {}°", str(denominator), str(fraction), str(alpha))
            queue_results.put((fraction, denominator, alpha))
 
def _store_results():
    global queue_numbers, queue_results, results_file
    
    with open(results_file, "a") as file:
        while not queue_results.empty():
            entry = queue_results.get()
            file.write("    " + str(entry) + ",\n")
              
def create_quotient_list(my_range:int, start:int=0, cont:bool=False):
    """Create the quotient list, by going through all the qotients and check wether the fraction has a finite decimal representation"""
    global queue_numbers, queue_results, results_file
    
    queue_results = Queue()
    queue_numbers = Queue()
    
    if not cont:
        with open(results_file, "w") as file:
            file.write('"""Quotient list for calculating euler spiral quotients from 1 to ' + str(int(my_range)) + '"""' + "\n\n")
            file.write("from decimal import Decimal\n\n")          
            file.write("TURTLEFUN_QUOTIENT_LIST = [\n")
    
    count = Count(start)
    
    for _n in range(20000):
        queue_numbers.put(next(count))
        
    threads = []
    for _t in range(22):
        threads.append(Thread(target=_check_denominator))
    for thread in threads:
        thread.start()
    
    timer_start = perf_counter()
      
    while not queue_numbers.empty():
        try:
            sleep(10)
            _store_results()
            qsize = queue_numbers.qsize()
            remaining = (perf_counter() - timer_start) / (int(count.current()) - qsize ) * (my_range - int(count.current()) + qsize)
            logger.debug("{} remaining numbers, time required {}s, current queue holds {}", my_range - int(count.current()) + qsize, round(remaining, 0), qsize)
            if qsize < 10000 and count.current() < my_range:
                for _n in range(20000 - qsize):
                    queue_numbers.put(next(count))
        except KeyboardInterrupt:
            logger.warning("Exploration interrupted, but not finished. {} explorations remaining.", queue_numbers.qsize())
            queue_numbers = Queue()
            
    logger.debug("Waiting for threads to finish")
    
    while True:
        if len(enumerate()) > 1:
            logger.debug("{} remaining threads found. Waiting.", len(enumerate()) - 1)
            _store_results()
            sleep(10)
        else:
            break
    sleep(1)
    
    _store_results()
    with open(results_file, "a") as file:
        file.write("    ]\n")
        
    logger.debug("Clean exit.")      
    