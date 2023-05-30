#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np
import radar_epy_block_1 as epy_block_1  # embedded python block
import radar_epy_block_3 as epy_block_3  # embedded python block



from gnuradio import qtgui

class radar(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "radar")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 4e6
        self.pulse_center_freq_hz = pulse_center_freq_hz = 10.0e3
        self.prf_khz = prf_khz = 3.90625
        self.c = c = 299792458
        self.pri_sec = pri_sec = 1/(prf_khz * 1e3)
        self.num_samples_per_pulse = num_samples_per_pulse = int(float(samp_rate) / (float(prf_khz) * 1e3))
        self.lambda_m = lambda_m = c / pulse_center_freq_hz
        self.duty_cycle = duty_cycle = 0.06
        self.time_bandwidth_product = time_bandwidth_product = 10.0
        self.tau_sec = tau_sec = pri_sec * duty_cycle
        self.num_samples_during_pulse_tx = num_samples_during_pulse_tx = int(num_samples_per_pulse * duty_cycle)
        self.max_unambiguous_vel_mps = max_unambiguous_vel_mps = prf_khz  * 1.0e3 * lambda_m / 4.0
        self.max_unambiguous_range_m = max_unambiguous_range_m = c * pri_sec
        self.target_vel_mps = target_vel_mps = max_unambiguous_vel_mps / 2
        self.range_to_target = range_to_target = 500
        self.num_samples_during_pulse_silence = num_samples_during_pulse_silence = num_samples_per_pulse - num_samples_during_pulse_tx
        self.num_pulses_per_cpi = num_pulses_per_cpi = 18
        self.distance_to_target_m = distance_to_target_m = max_unambiguous_range_m / 0.5
        self.bandwidth_khz_upper_limit = bandwidth_khz_upper_limit = 6000.0
        self.bandwidth_khz_lower_limit = bandwidth_khz_lower_limit = 1.0
        self.bandwidth_khz = bandwidth_khz = time_bandwidth_product / tau_sec / 1e3
        self.amplitude = amplitude = 2.0

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_0 = qtgui.sink_c(
            2048, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            prf_khz * 1e3, #fc
            10e6, #bw
            "LFM Pulse", #name
            True, #plotfreq
            False, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.epy_block_3 = epy_block_3.blk(c=c, distance_to_target_m=distance_to_target_m, target_vel_mps=target_vel_mps, lambda_m=lambda_m, pri_sec=pri_sec, samp_rate=samp_rate)
        self.epy_block_1 = epy_block_1.blk(prf_khz=None, pri_sec=None, duty_cycle=None, tau_sec=tau_sec, time_bandwidth_product=None, pulse_center_freq_hz=pulse_center_freq_hz, bandwidth_khz_lower_limit=bandwidth_khz_lower_limit, bandwidth_khz_upper_limit=bandwidth_khz_upper_limit, bandwidth_khz=bandwidth_khz, num_samples_per_pulse=num_samples_per_pulse, num_samples_during_pulse_tx=num_samples_during_pulse_tx, num_samples_during_pulse_silence=None, samp_rate=None, t=None, amplitude=amplitude, phase_ramp=None)
        self.blocks_vector_to_stream_0_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, num_samples_per_pulse*num_pulses_per_cpi)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, num_samples_per_pulse)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*num_samples_per_pulse, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, num_samples_per_pulse*num_pulses_per_cpi)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_to_vector_0, 0), (self.epy_block_3, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_throttle_0, 0))
        self.connect((self.epy_block_3, 0), (self.blocks_vector_to_stream_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "radar")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_num_samples_per_pulse(int(float(self.samp_rate) / (float(self.prf_khz) * 1e3)))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.epy_block_3.samp_rate = self.samp_rate

    def get_pulse_center_freq_hz(self):
        return self.pulse_center_freq_hz

    def set_pulse_center_freq_hz(self, pulse_center_freq_hz):
        self.pulse_center_freq_hz = pulse_center_freq_hz
        self.set_lambda_m(self.c / self.pulse_center_freq_hz)
        self.epy_block_1.pulse_center_freq_hz = self.pulse_center_freq_hz

    def get_prf_khz(self):
        return self.prf_khz

    def set_prf_khz(self, prf_khz):
        self.prf_khz = prf_khz
        self.set_max_unambiguous_vel_mps(self.prf_khz  * 1.0e3 * self.lambda_m / 4.0)
        self.set_num_samples_per_pulse(int(float(self.samp_rate) / (float(self.prf_khz) * 1e3)))
        self.set_pri_sec(1/(self.prf_khz * 1e3))
        self.qtgui_sink_x_0.set_frequency_range(self.prf_khz * 1e3, 10e6)

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c
        self.set_lambda_m(self.c / self.pulse_center_freq_hz)
        self.set_max_unambiguous_range_m(self.c * self.pri_sec)
        self.epy_block_3.c = self.c

    def get_pri_sec(self):
        return self.pri_sec

    def set_pri_sec(self, pri_sec):
        self.pri_sec = pri_sec
        self.set_max_unambiguous_range_m(self.c * self.pri_sec)
        self.set_tau_sec(self.pri_sec * self.duty_cycle)
        self.epy_block_3.pri_sec = self.pri_sec

    def get_num_samples_per_pulse(self):
        return self.num_samples_per_pulse

    def set_num_samples_per_pulse(self, num_samples_per_pulse):
        self.num_samples_per_pulse = num_samples_per_pulse
        self.set_num_samples_during_pulse_silence(self.num_samples_per_pulse - self.num_samples_during_pulse_tx)
        self.set_num_samples_during_pulse_tx(int(self.num_samples_per_pulse * self.duty_cycle))
        self.epy_block_1.num_samples_per_pulse = self.num_samples_per_pulse

    def get_lambda_m(self):
        return self.lambda_m

    def set_lambda_m(self, lambda_m):
        self.lambda_m = lambda_m
        self.set_max_unambiguous_vel_mps(self.prf_khz  * 1.0e3 * self.lambda_m / 4.0)
        self.epy_block_3.lambda_m = self.lambda_m

    def get_duty_cycle(self):
        return self.duty_cycle

    def set_duty_cycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
        self.set_num_samples_during_pulse_tx(int(self.num_samples_per_pulse * self.duty_cycle))
        self.set_tau_sec(self.pri_sec * self.duty_cycle)

    def get_time_bandwidth_product(self):
        return self.time_bandwidth_product

    def set_time_bandwidth_product(self, time_bandwidth_product):
        self.time_bandwidth_product = time_bandwidth_product
        self.set_bandwidth_khz(self.time_bandwidth_product / self.tau_sec / 1e3)

    def get_tau_sec(self):
        return self.tau_sec

    def set_tau_sec(self, tau_sec):
        self.tau_sec = tau_sec
        self.set_bandwidth_khz(self.time_bandwidth_product / self.tau_sec / 1e3)
        self.epy_block_1.tau_sec = self.tau_sec

    def get_num_samples_during_pulse_tx(self):
        return self.num_samples_during_pulse_tx

    def set_num_samples_during_pulse_tx(self, num_samples_during_pulse_tx):
        self.num_samples_during_pulse_tx = num_samples_during_pulse_tx
        self.set_num_samples_during_pulse_silence(self.num_samples_per_pulse - self.num_samples_during_pulse_tx)
        self.epy_block_1.num_samples_during_pulse_tx = self.num_samples_during_pulse_tx

    def get_max_unambiguous_vel_mps(self):
        return self.max_unambiguous_vel_mps

    def set_max_unambiguous_vel_mps(self, max_unambiguous_vel_mps):
        self.max_unambiguous_vel_mps = max_unambiguous_vel_mps
        self.set_target_vel_mps(self.max_unambiguous_vel_mps / 2)

    def get_max_unambiguous_range_m(self):
        return self.max_unambiguous_range_m

    def set_max_unambiguous_range_m(self, max_unambiguous_range_m):
        self.max_unambiguous_range_m = max_unambiguous_range_m
        self.set_distance_to_target_m(self.max_unambiguous_range_m / 0.5)

    def get_target_vel_mps(self):
        return self.target_vel_mps

    def set_target_vel_mps(self, target_vel_mps):
        self.target_vel_mps = target_vel_mps
        self.epy_block_3.target_vel_mps = self.target_vel_mps

    def get_range_to_target(self):
        return self.range_to_target

    def set_range_to_target(self, range_to_target):
        self.range_to_target = range_to_target

    def get_num_samples_during_pulse_silence(self):
        return self.num_samples_during_pulse_silence

    def set_num_samples_during_pulse_silence(self, num_samples_during_pulse_silence):
        self.num_samples_during_pulse_silence = num_samples_during_pulse_silence

    def get_num_pulses_per_cpi(self):
        return self.num_pulses_per_cpi

    def set_num_pulses_per_cpi(self, num_pulses_per_cpi):
        self.num_pulses_per_cpi = num_pulses_per_cpi

    def get_distance_to_target_m(self):
        return self.distance_to_target_m

    def set_distance_to_target_m(self, distance_to_target_m):
        self.distance_to_target_m = distance_to_target_m
        self.epy_block_3.distance_to_target_m = self.distance_to_target_m

    def get_bandwidth_khz_upper_limit(self):
        return self.bandwidth_khz_upper_limit

    def set_bandwidth_khz_upper_limit(self, bandwidth_khz_upper_limit):
        self.bandwidth_khz_upper_limit = bandwidth_khz_upper_limit

    def get_bandwidth_khz_lower_limit(self):
        return self.bandwidth_khz_lower_limit

    def set_bandwidth_khz_lower_limit(self, bandwidth_khz_lower_limit):
        self.bandwidth_khz_lower_limit = bandwidth_khz_lower_limit

    def get_bandwidth_khz(self):
        return self.bandwidth_khz

    def set_bandwidth_khz(self, bandwidth_khz):
        self.bandwidth_khz = bandwidth_khz
        self.epy_block_1.bandwidth_khz = self.bandwidth_khz

    def get_amplitude(self):
        return self.amplitude

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude
        self.epy_block_1.amplitude = self.amplitude




def main(top_block_cls=radar, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
