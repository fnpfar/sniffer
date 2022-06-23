#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Digital Filter Characterization
# Author: Francisco Nicolás Pérez Fernández
# GNU Radio version: 3.10.2.0

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

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import scipy


def snipfcn_snippet_0(self):
    # Saving the taps1 to a file----------------------------------------

    filename = "taps1.txt"
    file1 = open(filename,"w") #open file to write
    file1.writelines('{0}'.format(self.taps1))
    file1.close() #to change file access modes

    # Saving the taps2 to a file----------------------------------------

    filename = "taps2.txt"
    file1 = open(filename,"w") #open file to write
    file1.writelines('{0}'.format(self.taps2))
    file1.close() #to change file access modes

    # Plotting the frequency responses

    w1, h1 = signal.freqz(self.taps1)
    w2, h2 = signal.freqz(self.taps2)

    fig1, ax1 = plt.subplots() # freq axis
    ax1.set_title('Digital filter frequency response')

    ax1.plot(w1, 20 * np.log10(abs(h1)), '-b')
    ax1.plot(w2, 20 * np.log10(abs(h2)), '-g')
    ax1.legend(['Taps1', 'Taps2'])

    ax1.set_ylabel('Amplitude [dB]', color='k')
    ax1.set_xlabel('Frequency [rad/sample]')

    ax2 = ax1.twinx() # angle axis

    angles1 = np.unwrap(np.angle(h1))
    angles2 = np.unwrap(np.angle(h2))

    if self.plotphase: ax2.plot(w1, angles1, '-c')
    if self.plotphase: ax2.plot(w2, angles2, '-y')
    if self.plotphase: ax2.legend(['Taps1', 'Taps2'])

    ax2.set_ylabel('Phase (radians)', color='k')


    ax2.grid()
    ax2.axis('tight')

    plt.show()


def snippets_main_after_start(tb):
    snipfcn_snippet_0(tb)

from gnuradio import qtgui

class digitalFilterCharacterization(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Digital Filter Characterization", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Digital Filter Characterization")
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

        self.settings = Qt.QSettings("GNU Radio", "digitalFilterCharacterization")

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
        self.transition_width2 = transition_width2 = 13e3
        self.transition_width1 = transition_width1 = 13e3
        self.stop_band_attenuation_dB2 = stop_band_attenuation_dB2 = 96
        self.samp_rate2 = samp_rate2 = 13e6
        self.samp_rate1 = samp_rate1 = 13e6
        self.filterGain2 = filterGain2 = 1
        self.filterGain1 = filterGain1 = 1
        self.cutoff_freq2 = cutoff_freq2 = 42e3
        self.cutoff_freq1 = cutoff_freq1 = 42e3
        self.taps2 = taps2 = firdes.low_pass_2(filterGain2,samp_rate2,cutoff_freq2,transition_width2,stop_band_attenuation_dB2)
        self.taps1 = taps1 = firdes.low_pass(filterGain1, samp_rate1, cutoff_freq1,transition_width1, window.WIN_HAMMING, 6.76)
        self.plotphase = plotphase = False



    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "digitalFilterCharacterization")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_transition_width2(self):
        return self.transition_width2

    def set_transition_width2(self, transition_width2):
        self.transition_width2 = transition_width2
        self.set_taps2(firdes.low_pass_2(self.filterGain2,self.samp_rate2,self.cutoff_freq2,self.transition_width2,self.stop_band_attenuation_dB2))

    def get_transition_width1(self):
        return self.transition_width1

    def set_transition_width1(self, transition_width1):
        self.transition_width1 = transition_width1
        self.set_taps1(firdes.low_pass(self.filterGain1, self.samp_rate1, self.cutoff_freq1, self.transition_width1, window.WIN_HAMMING, 6.76))

    def get_stop_band_attenuation_dB2(self):
        return self.stop_band_attenuation_dB2

    def set_stop_band_attenuation_dB2(self, stop_band_attenuation_dB2):
        self.stop_band_attenuation_dB2 = stop_band_attenuation_dB2
        self.set_taps2(firdes.low_pass_2(self.filterGain2,self.samp_rate2,self.cutoff_freq2,self.transition_width2,self.stop_band_attenuation_dB2))

    def get_samp_rate2(self):
        return self.samp_rate2

    def set_samp_rate2(self, samp_rate2):
        self.samp_rate2 = samp_rate2
        self.set_taps2(firdes.low_pass_2(self.filterGain2,self.samp_rate2,self.cutoff_freq2,self.transition_width2,self.stop_band_attenuation_dB2))

    def get_samp_rate1(self):
        return self.samp_rate1

    def set_samp_rate1(self, samp_rate1):
        self.samp_rate1 = samp_rate1
        self.set_taps1(firdes.low_pass(self.filterGain1, self.samp_rate1, self.cutoff_freq1, self.transition_width1, window.WIN_HAMMING, 6.76))

    def get_filterGain2(self):
        return self.filterGain2

    def set_filterGain2(self, filterGain2):
        self.filterGain2 = filterGain2
        self.set_taps2(firdes.low_pass_2(self.filterGain2,self.samp_rate2,self.cutoff_freq2,self.transition_width2,self.stop_band_attenuation_dB2))

    def get_filterGain1(self):
        return self.filterGain1

    def set_filterGain1(self, filterGain1):
        self.filterGain1 = filterGain1
        self.set_taps1(firdes.low_pass(self.filterGain1, self.samp_rate1, self.cutoff_freq1, self.transition_width1, window.WIN_HAMMING, 6.76))

    def get_cutoff_freq2(self):
        return self.cutoff_freq2

    def set_cutoff_freq2(self, cutoff_freq2):
        self.cutoff_freq2 = cutoff_freq2
        self.set_taps2(firdes.low_pass_2(self.filterGain2,self.samp_rate2,self.cutoff_freq2,self.transition_width2,self.stop_band_attenuation_dB2))

    def get_cutoff_freq1(self):
        return self.cutoff_freq1

    def set_cutoff_freq1(self, cutoff_freq1):
        self.cutoff_freq1 = cutoff_freq1
        self.set_taps1(firdes.low_pass(self.filterGain1, self.samp_rate1, self.cutoff_freq1, self.transition_width1, window.WIN_HAMMING, 6.76))

    def get_taps2(self):
        return self.taps2

    def set_taps2(self, taps2):
        self.taps2 = taps2

    def get_taps1(self):
        return self.taps1

    def set_taps1(self, taps1):
        self.taps1 = taps1

    def get_plotphase(self):
        return self.plotphase

    def set_plotphase(self, plotphase):
        self.plotphase = plotphase




def main(top_block_cls=digitalFilterCharacterization, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    snippets_main_after_start(tb)
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
