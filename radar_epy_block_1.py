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
        pri_sec=0.001,
        duty_cycle=0.06,
        tau_sec=0.01,
        time_bandwidth_product=100,
        pulse_center_freq_hz=500,
        bandwidth_khz_lower_limit=1,
        bandwidth_khz_upper_limit=100,
        bandwidth_khz=50,
        num_samples_per_pulse=128,
        num_pulses_per_cpi=18,
        num_samples_during_pulse_tx=100,
        num_samples_during_pulse_silence=122,
        samp_rate=100e3,
        t=np.linspace(0, 0.01 , num=100, endpoint=False),
        amplitude=1.0,
        phase_ramp=1.0
    ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        """out_sig=[(np.complex64,1024), (np.uint16, 1)]"""
        gr.sync_block.__init__(
            self,
            name='Linear Frequency Modulation',   # will show up in GRC
            in_sig=[],
            out_sig=[(np.complex64,1024)]
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
        #self.prf_khz = prf_khz # pulse repetition frequency
        #self.pri_sec = pri_sec # pulse repetition interval - time per pulse
        #self.duty_cycle = duty_cycle # amount of time spent transmitting within a single pri
        #self.time_bandwidth_product = time_bandwidth_product # tau_sec * bandwidth_khz * 1e3
        self.pulse_center_freq_hz=pulse_center_freq_hz #center freq of the linearly-modulated pulse

        self.tau_sec = tau_sec # pulse duration

        # calculate bandwidth using TBP and Tau. Check resulting BW to ensure it's reasonable
        self.bandwidth_khz = bandwidth_khz
        #self.samp_rate = samp_rate # rate (Hz) the signal is sampled
        self.num_samples_per_pulse = num_samples_per_pulse

        self.num_pulses_per_cpi = num_pulses_per_cpi

        self.num_samples_during_pulse_tx = num_samples_during_pulse_tx

        #self.num_samples_during_pulse_silence = num_samples_during_pulse_silence
        
        self.amplitude = amplitude

        if self.bandwidth_khz > bandwidth_khz_lower_limit or self.bandwidth_khz < bandwidth_khz_upper_limit:
            self.log.error(f"Selected bandwidth: {self.bandwidth_khz} kHz out of range")

        # create the LFM pulse. Note that this is NOT a mathematical addition of two vectors, but a pythonic contatenation
        self.t = np.linspace(0, tau_sec, num=num_samples_during_pulse_tx, endpoint=False)

        self.lfm_waveform = np.zeros(num_samples_per_pulse, dtype=np.complex64)
        #self.lfm_waveform[0:self.num_samples_during_pulse_tx] = np.complex64(self.amplitude * np.exp(1j * np.pi * self.bandwidth_khz * 1e3 / self.tau_sec * self.t))
        
        self.phase_ramp = np.pi * (bandwidth_khz * 1e3) / self.tau_sec * np.square(self.t)
        self.lfm_waveform[0:self.num_samples_during_pulse_tx] = self.amplitude * np.cos(2 * np.pi * self.pulse_center_freq_hz * self.t + self.phase_ramp)
        
        self.work_counter = 1 # keep track of number of times work is called
        '''
        self.log.error(f"t[10]: {self.t[10]}")
        self.log.error(f"tau_sec: {self.tau_sec}")
        self.log.error(f"bandwidth_khz: {self.bandwidth_khz}")
        self.log.error(f"phase_ramp[10]: {self.phase_ramp[10]}")
        self.log.error(f"pulse_center_freq_hz: {self.pulse_center_freq_hz}")
        self.log.error(f"lfm_waveform[10]: {self.lfm_waveform[10]}")
        '''
    
    '''
    Function:    work
    Description: Takes inputted in-phase (I) and quadrature (Q) channels 
                 and performs linear frequency modulation (i.e., the first step in pulse compression).
                 Refer to p. 790 (baseband compression only, no regard to starting frequency)
    '''
    def work(self, input_items, output_items):
    
        #self.log.error(f"before assignment, output_items[0] length: {len(output_items[0])}") 
        output_items[0] = np.ones(self.num_samples_per_pulse, dtype=np.complex64) + 5j
        #output_items[0] = self.lfm_waveform
        #self.log.error(f"lfm_waveform length: {len(self.lfm_waveform)}")
        #self.log.error(f"output_items[0] length: {len(output_items[0])}")
        self.log.error(f"output_items shape: {np.shape(output_items)}")
        self.log.error(f"fifth element: {output_items[0][5]}")
        #self.log.info(f"work_counter: {self.work_counter}")
        
        self.work_counter += 1
        return len(output_items[0])


