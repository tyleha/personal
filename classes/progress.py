from __future__ import print_function
import sys, time
import datetime

class ProgressBar(object):
    """Print a progress bar containing completed iterations, percent complete, elapsed time, & ETA.
    :total_iterations (int, float): the max number of iterations to be completed, or the final size
    :start_time (int, float): the number of seconds since the epoch in gm time 
    :units (str): the displayed units 
    """
    def __init__(self, total_iterations, start_time=None, units=None):

        self.total_iterations = total_iterations
        self.prog_bar = '[]'
        self.fill_char = '#'
        self.width = 50
        self._update_progbar(0)
        if start_time is not None:
            self.start_time = start_time
        else:
            self.start_time = time.time()
        if units is not None:
            self.units = units + ' '
        else:
            self.units = ''
        self.elapsed = None
        self.eta = None
    
    def __str__(self):
        return str(self.prog_bar)
    
    def animate(self, iters):
        """The outward-facing function to update the progress bar.
        :iters (int, float): the number of elapsed iterations
        """
        self.update_iteration(iters + 1)
        print('\r', self, end='')
        sys.stdout.flush()
        #self.update_iteration(iters + 1)

    def update_iteration(self, elapsed_iter):
        """Groups together all updating work
        :elapsed_iter (int, float): the number of elapsed iterations passed from animate
        """
        print_string = '{0} of {1} {5}   {2}    Time: {3}    ETA: {4}'
        fraction_complete = (elapsed_iter / float(self.total_iterations)) * 100.0
        self._update_progbar(fraction_complete)
        self._update_time(fraction_complete)
        
        if type(self.eta) != str:
            eta = str(datetime.timedelta(seconds=int(self.eta)))
        else:
            eta = self.eta
        
        if isinstance(self.total_iterations, int):
            iters = str(int(elapsed_iter))
            total = str(self.total_iterations)
        else:
            iters = '%0.1f'%elapsed_iter
            total = '%0.1f'%self.total_iterations
            
        self.prog_bar = print_string.format(iters, total, self.prog_bar, 
                                            str(datetime.timedelta(seconds=int(self.elapsed))), 
                                            eta,
                                            self.units)
    
    def _update_time(self, fraction_complete):
        """Update the elapsed time of the progress bar.
        :fraction_complete: (float) - the fraction 0 to 100 of completeness
        """
        self.elapsed = time.time() - self.start_time
        if fraction_complete > 0 and self.elapsed > 3:
            # simple eta calculation of whole length. Can update to past 10 sec or something
            self.eta = ((100.-fraction_complete)/fraction_complete)*self.elapsed 
        else:
            self.eta = '...'
            
    def _update_progbar(self, new_amount):
        percent_done = int(round((new_amount / 100.0) * 100.0))
        all_full = self.width - 2
        num_hashes = int(round((percent_done / 100.0) * all_full))
        self.prog_bar = '[' + self.fill_char * num_hashes + ' ' * (all_full - num_hashes) + ']'
        pct_place = (len(self.prog_bar) // 2) - len(str(percent_done))
        pct_string = ' %d%% ' % percent_done
        self.prog_bar = self.prog_bar[0:pct_place] + \
            (pct_string + self.prog_bar[pct_place + len(pct_string):])
    

    def field_boto_download(self, current, total):
        """Designed to interface ProgressBar with Boto's callback function.
        :current: int, float - the current number iteration you're on
        :total: int, float - the total number of iterations being completed
        """
        if total > 2**10 and total < 2**20:
            self.set_units('KB')
            self.total_iterations = total/1024.
            self.animate((current/1024.)-1) #-1 as the returned val from boto is number bytes, 
                                            # not iteration
        elif total > 2**20:
            self.set_units('MB')
            self.total_iterations = total/float(2**20)
            self.animate((current/float(2**20))-1)        
        else:
            self.total_iterations = total
            self.animate(current-1)
    
    def set_start_time(self, starttime):
        """Adjust the start time of the given pogress bar. Time is initially set at instantiation. 
        :starttime: must be in seconds since epoch in gm timethis is easiest described as the 
        output of time.time(). 
        """
        self.start_time = starttime

    def set_units(self, units):
        """Adjust the displayed units.
        :units (str): the displayed units
        """
        self.units = units + ' '

if __name__ == '__main__':
    print("A basic example...")
    p2 = ProgressBar(100, units='')
    for i in range(100):
        time.sleep(0.08)
        p2.animate(i)
