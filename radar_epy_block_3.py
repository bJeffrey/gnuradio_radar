"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,
        num_samples_per_pulse=1024,
        num_pulses_per_cpi=18,
        c=3.00e8,
        distance_to_target_m=100.0 * 1.0e3,
        target_vel_mps=100.0 * 1.0e3,
        lambda_m=2,
        pri_sec=1.0/3.0e3,
        samp_rate=4e6
    ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Target Injection',
            in_sig=[(np.complex64,1024)], # single pulse
            out_sig=[(np.complex64,1024*18)] # 1 CPI worth of data
        )
        
        self.log = gr.logger(self.alias())
        
        # set CPI parameters
        self.num_samples_per_pulse = num_samples_per_pulse
        self.num_pulses_per_cpi = num_pulses_per_cpi
        self.pulses = np.zeros((self.num_samples_per_pulse, self.num_pulses_per_cpi), dtype=np.complex64)
        self.pulse_idx = -1 #initialize to -1, increment at every call to work() at beginning of work()
        
        # set target parameters
        self.c = c
        self.distance_to_target_m = distance_to_target_m        
        self.target_vel_mps = target_vel_mps
        self.lambda_m = lambda_m
        self.pri_sec = pri_sec
        self.samp_rate = samp_rate
        # calculate range bin and doppler shift of target
        self.num_samples_to_target = self.distance_to_target_m * self.samp_rate / self.c

        self.doppler_shift_hz = 2 * self.target_vel_mps / self.lambda_m

        self.log.info(f"pulses shape: {self.pulses.shape}")

    def work(self, input_items, output_items):
        self.pulse_idx += 1 # first thing that should happen is this value incrementing
        #self.log.info(f"length of vector: {len(input_items[0][:])}")
        #self.log.info(f"last: {input_items[0][1024*18]}")
        my_temp_1 = self.pulses[:,self.pulse_idx]
        self.log.info(f"my_temp_1.shape: {my_temp_1.shape})") # ((1024,))
        my_temp_2 = self.pulses[self.pulse_idx,:]
        self.log.info(f"my_temp_2.shape: {my_temp_2.shape}") # (18,)
        my_temp_3 = self.pulses
        self.log.info(f"my_temp_3.shape: {my_temp_3.shape}") # (1024,18)
        
        
        self.log.error(f"input_items shape: {np.shape(input_items)}") #(1, 2, 1024)
        self.log.info(f"array_equal: {np.array_equal(input_items[0][0], input_items[0][1])}")
        self.log.info(f"fifth element 0: {input_items[0][0][5]}")
        self.log.info(f"fifth element 1: {input_items[0][1][5]}")
        self.pulses[:,self.pulse_idx] = input_items[0][0][:] # need to loop through this, because I'm getting an input_item that is too large
        
        if self.pulse_idx < self.num_pulses_per_cpi:
            self.log.info(f"output_items[0]: {len(output_items[0])}")
            output_items[0] = np.zeros(self.num_samples_per_pulse * self.num_pulses_per_cpi, dtype=np.complex64)
            self.log.error(f"output_items[0] length: {len(output_items[0][:])}")
            return len(output_items[0])

        self.log.info(f"I made it! I have {self.pulse_idx} pulses!")            
        # if we made it to this line, it is assumed that we have a full CPI of data.

        all_pulses = self.pulses.flatten()
        self.log.info(f"all_pulses length: {len(all_pulses)}")
        output_items[0] = self.pulses.flatten()
        
        self.pulse_idx = -1 # reset the pulse_idx - remember that this is incremented at the top of work before it is used
        return len(output_items[0])








