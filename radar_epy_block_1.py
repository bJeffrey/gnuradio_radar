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

    # time-bandwidth product should be [75, 10,000] for LFM system
    def __init__(
        self,
        prf_khz=3,
        duty_cycle=0.06,
        time_bandwidth_product=100,
        pulse_center_freq_hz=500,
        bandwidth_khz_lower_limit=1,
        bandwidth_khz_upper_limit=100,
        bandwidth_khz=50,
        num_samples_per_pulse=128,
        samp_rate=100e3
    ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Linear Frequency Modulation',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # log levels: 
        #   trace:      Developing an algorithm and need to log specific values that it calculates
        #   debug:      Used for debugging purposes, and should not be visible under usual usage
        #   info:       Information that does not require immediate attention, but might be of interest
        #   warn:       Something might be wrong and it's probably worth looking into it
        #   error:      An error has occurred. Meaning something definitely is wrong
        #   critical:   An error that cannot be recovered from
        
        self.log = gr.logger(self.alias()) # initialize logger
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        
        # (max_unambiguous_range = c / (2 * prf) - at 30 kHz, unambiguous to 5000 m, 3.1 mi)
        self.prf_khz = prf_khz # pulse repetition frequency
        self.duty_cycle = duty_cycle # amount of time spent transmitting within a single pri
        self.time_bandwidth_product = time_bandwidth_product
        self.pulse_center_freq_hz=pulse_center_freq_hz #center freq of the linearly-modulated pulse
        self.pri_sec = 1/(self.prf_khz * 1e3) # pulse repetition interval - time per pulse
        self.tau_sec = self.pri_sec * self.duty_cycle # pulse duration

        # calculate bandwidth using TBP and Tau. Check resulting BW to ensure it's reasonable
        self.bandwidth_khz = time_bandwidth_product / self.tau_sec / 1e3 

        self.num_samples_per_pulse = num_samples_per_pulse # number of samples from both transmitting and non-transmitting portion of pulse
        self.samp_rate = samp_rate # rate (Hz) the signal is sampled

        if self.bandwidth_khz > bandwidth_khz_lower_limit or self.bandwidth_khz < bandwidth_khz_upper_limit:
            self.log.error(f"Selected bandwidth: {self.bandwidth_khz} kHz out of range")
        #else:
        #    self.log.info(f"pulse bandwidth: {self.bandwidth_khz} kHz")

    """
    Function:    work
    Description: Takes inputted in-phase (I) and quadrature (Q) channels 
                 and performs linear frequency modulation (i.e., the first step in pulse compression).
                 Refer to p. 790
    """
    def work(self, output_items):
    
        num_samples_during_pulse_tx = int(self.samp_rate * self.tau_sec)
        t = np.linspace(0, selt.tau_sec, num=num_samples_during_pulse_tx, endpoint=False)
        
        # create the LFM pulse. Note that this is NOT a mathematical addition of two vectors, but a pythonic contatenation
        # of two lists
        output_items[0][:] = np.concatenate(\
            self.amplitude * np.exp(np.imag(1) * np.pi * self.bandwidth_khz * 1e3 / self.tau_sec * t), \
            np.zeros(self.num_samples_per_pulse - num_samples_during_pulse_tx, dtype=np.complex_) \
        )        
        #self.log.error((f"Type: {output_items[[0][0]]}")
        
        #self.log.info(f"output_items[0] length: {len(output_items[0])}")
        return len(output_items[0])








