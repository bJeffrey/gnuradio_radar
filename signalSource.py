'''
Program:        signalSource.py
Description:    Sets a linear frequency modulated pulse  with characteristics defined
                by the input parameters
'''

import numpy as np
from gnuradio import gr # This import, without using gnu logging, is likely unnecessary
import matplotlib.pyplot as plt

def generate_lfm_pulse( \
    prf_khz=3.0,
    duty_cycle=0.06,
    amplitude=1.0,
    time_bandwidth_product=100.0,
    pulse_center_freq_hz=500.0,
    bandwidth_khz_lower_limit=1.0,
    bandwidth_khz_upper_limit=100.0,
    bandwidth_khz=50.0,
    num_samples_per_pulse=2048,
    samp_rate=4.0e6
    ): 

    # log levels: 
    #   trace:      Developing an algorithm and need to log specific values that it calculates
    #   debug:      Used for debugging purposes, and should not be visible under usual usage
    #   info:       Information that does not require immediate attention, but might be of interest
    #   warn:       Something might be wrong and it's probably worth looking into it
    #   error:      An error has occurred. Meaning something definitely is wrong
    #   critical:   An error that cannot be recovered from

    #log = gr.logger(gr.alias()) # initialize logger
    # if an attribute with the same name as a parameter is found,
    # a callback is registered (properties work, too).
    
    # (max_unambiguous_range = c / (2 * prf) - at 30 kHz, unambiguous to 5000 m, 3.1 mi)
    pri_sec = 1/(prf_khz * 1e3) # pulse repetition interval - time per pulse
    tau_sec = pri_sec * duty_cycle # pulse duration

    # calculate bandwidth using TBP and Tau. Check resulting BW to ensure it's reasonable
    bandwidth_khz = time_bandwidth_product / tau_sec / 1e3 

    #if bandwidth_khz > bandwidth_khz_lower_limit or bandwidth_khz < bandwidth_khz_upper_limit:
    #    print(f"Selected bandwidth: {bandwidth_khz} kHz out of range")
        #log.error(f"Selected bandwidth: {bandwidth_khz} kHz out of range")
    #else:
    #    log.info(f"pulse bandwidth: {bandwidth_khz} kHz")

    # samples during pulse tx (not pulse tx plus no tx between pulses)
    num_samples_during_pulse_tx = int(samp_rate * tau_sec)
    
    #print(f"samp_rate type: {type(samp_rate)}\t value: {samp_rate}")
    #print(f"tau_sec type: {type(tau_sec)}\t value: {tau_sec}")
    #print(f"num_samples_during_pulse_tx type: {type(num_samples_during_pulse_tx)}\t value: {num_samples_during_pulse_tx}")
    # time indices during transmitted pulse
    
    t = np.linspace(0, tau_sec, num=num_samples_during_pulse_tx, endpoint=False, dtype=complex)
    
    num_samples_during_no_tx = num_samples_per_pulse - num_samples_during_pulse_tx
    #num_samples_during_no_tx = int((pri_sec - tau_sec) * samp_rate)

    #print(f"t length: {len(t)}")
    #print(f"num_samples_during_pulse_tx: {num_samples_during_pulse_tx}")
    #print(f"num_samples_during_no_tx: {num_samples_during_no_tx}")

    # create the LFM pulse.
    
    #print(f"first part type: {type(first)} \t size: {np.shape(first)}")
    #print(f"second part type: {type(second)} \t size: {np.shape(second)}")
    lfm_pulse = np.concatenate( \
        (amplitude * np.exp(np.imag(1) * np.pi * bandwidth_khz * 1e3 / tau_sec * t), \
        np.zeros(num_samples_during_no_tx, dtype=np.complex_)) \
    )
    #print(f"Type: {type(np.real(lfm_pulse[0]))}")
    
    #log.info(f"output_items[0] length: {len(output_items[0])}")
    return lfm_pulse

def generate_sin(samp_rate, num_samples_per_pulse):

    # np.singlecomplex and np.complex64 both print with type <class 'numpy.complex64'>
    #t = np.linspace(0, 1.0 / 3000.0, num_samples_per_pulse, endpoint=False, dtype=np.singlecomplex)
    t = np.linspace(0, 1.0 / 3000.0, num_samples_per_pulse, endpoint=False, dtype=np.complex64)
    x = np.sin(t)
    print(f"x type: {type(x)} \t x[0] type: {type(x[0])} \t size: {np.shape(x)}")
    return x

def generate_plots(signal, samp_rate):

    #t = np.linspace(0.0, 1.0/(prf_khz * 1.0e3), num=len(signal), endpoint=False, dtype=float)
    t = np.linspace(0.0, len(signal) / samp_rate, num=len(signal), endpoint=False, dtype=float)
    print(len(t))
    plt.plot(t, np.real(signal))
    plt.ylabel('Amplitude (V)')
    plt.ylabel('time (sec)')
    plt.show()

if __name__ == "__main__":
    samp_rate = 4.0e6

    lfm_pulse = generate_lfm_pulse()

    # generate very simple signal for testing
    #sin_wave = generate_sin(samp_rate, int(float(samp_rate) / (float(prf_khz) * 1e3)))

    generate_plots(lfm_pulse, samp_rate)



