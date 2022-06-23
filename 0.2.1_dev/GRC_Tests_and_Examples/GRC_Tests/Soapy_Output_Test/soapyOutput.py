#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class soapyOutput(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "soapyOutput")

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
        self.vga_gain = vga_gain = 0
        self.samp_rate = samp_rate = 16e6
        self.lo_osc_freq_err_compensation = lo_osc_freq_err_compensation = 0
        self.lo_osc_freq = lo_osc_freq = 869.3e6
        self.if_gain = if_gain = 16
        self.antialias_bw = antialias_bw = 3.5e6
        self.amp_on = amp_on = True

        ##################################################
        # Blocks
        ##################################################
        self._vga_gain_range = Range(0, 62, 2, 0, 200)
        self._vga_gain_win = RangeWidget(self._vga_gain_range, self.set_vga_gain, "LF Gain (0 to 62 dB in 2 dB steps)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._vga_gain_win)
        self._samp_rate_range = Range(1e6, 20e6, 1e6, 16e6, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, "ADC Sample Rate (1 to 20 Msps in 1 Msps steps)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._samp_rate_win)
        self._lo_osc_freq_range = Range(700e6, 900e6, 1e3, 869.3e6, 200)
        self._lo_osc_freq_win = RangeWidget(self._lo_osc_freq_range, self.set_lo_osc_freq, "Local Oscillator Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._lo_osc_freq_win)
        # Create the options list
        self._if_gain_options = [0, 8, 16, 24, 32, 40]
        # Create the labels list
        self._if_gain_labels = ['0 dB', '+8 dB', '+16 dB', '+24 dB', '+32 dB', '+40 dB']
        # Create the combo box
        self._if_gain_tool_bar = Qt.QToolBar(self)
        self._if_gain_tool_bar.addWidget(Qt.QLabel("IF Gain (0 to 40 dB in 8 dB steps)" + ": "))
        self._if_gain_combo_box = Qt.QComboBox()
        self._if_gain_tool_bar.addWidget(self._if_gain_combo_box)
        for _label in self._if_gain_labels: self._if_gain_combo_box.addItem(_label)
        self._if_gain_callback = lambda i: Qt.QMetaObject.invokeMethod(self._if_gain_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._if_gain_options.index(i)))
        self._if_gain_callback(self.if_gain)
        self._if_gain_combo_box.currentIndexChanged.connect(
            lambda i: self.set_if_gain(self._if_gain_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._if_gain_tool_bar)
        # Create the options list
        self._antialias_bw_options = [1750000.0, 2500000.0, 3500000.0, 5000000.0, 5500000.0, 6000000.0, 7000000.0, 8000000.0, 9000000.0, 10000000.0, 12000000.0, 14000000.0, 15000000.0, 20000000.0, 24000000.0, 28000000.0]
        # Create the labels list
        self._antialias_bw_labels = ['1.75', '2.5', '3.5', '5', '5.5', '6', '7', '8', '9', '10', '12', '14', '15', '20', '24', '28']
        # Create the combo box
        self._antialias_bw_tool_bar = Qt.QToolBar(self)
        self._antialias_bw_tool_bar.addWidget(Qt.QLabel("Antialiass Filter Bandwidth" + ": "))
        self._antialias_bw_combo_box = Qt.QComboBox()
        self._antialias_bw_tool_bar.addWidget(self._antialias_bw_combo_box)
        for _label in self._antialias_bw_labels: self._antialias_bw_combo_box.addItem(_label)
        self._antialias_bw_callback = lambda i: Qt.QMetaObject.invokeMethod(self._antialias_bw_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._antialias_bw_options.index(i)))
        self._antialias_bw_callback(self.antialias_bw)
        self._antialias_bw_combo_box.currentIndexChanged.connect(
            lambda i: self.set_antialias_bw(self._antialias_bw_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._antialias_bw_tool_bar)
        if int == bool:
        	self._amp_on_choices = {'Pressed': bool(True), 'Released': bool(False)}
        elif int == str:
        	self._amp_on_choices = {'Pressed': "True".replace("'",""), 'Released': "False".replace("'","")}
        else:
        	self._amp_on_choices = {'Pressed': True, 'Released': False}

        _amp_on_toggle_button = qtgui.GrToggleSwitch(self.set_amp_on, 'RF Amp on (+11 dB aprox)', self._amp_on_choices, True,"green","gray",4, 50, 1, 1,self,"'value'".replace("'",""))
        self.amp_on = _amp_on_toggle_button

        self.top_layout.addWidget(_amp_on_toggle_button)
        self.soapy_hackrf_source_0_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0_0.set_bandwidth(0, antialias_bw)
        self.soapy_hackrf_source_0_0.set_frequency(0, lo_osc_freq+lo_osc_freq_err_compensation)
        self.soapy_hackrf_source_0_0.set_gain(0, 'AMP', amp_on)
        self.soapy_hackrf_source_0_0.set_gain(0, 'LNA', min(max(if_gain, 0.0), 40.0))
        self.soapy_hackrf_source_0_0.set_gain(0, 'VGA', min(max(vga_gain, 0.0), 62.0))
        self.qtgui_time_sink_x_0_0_1_0_0_0_0 = qtgui.time_sink_c(
            96000, #size
            samp_rate, #samp_rate
            "Soapy HW Output", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_update_time(0.001)
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_y_axis(-1.2, 1.2)

        self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.enable_stem_plot(False)


        labels = ['In Phase (Re)', 'Quadrature (Im)', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'green', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_0_0_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            8192, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            lo_osc_freq, #fc
            samp_rate, #bw
            "Soapy HW Output Spectrum", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/60)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.soapy_hackrf_source_0_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.soapy_hackrf_source_0_0, 0), (self.qtgui_time_sink_x_0_0_1_0_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "soapyOutput")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_vga_gain(self):
        return self.vga_gain

    def set_vga_gain(self, vga_gain):
        self.vga_gain = vga_gain
        self.soapy_hackrf_source_0_0.set_gain(0, 'VGA', min(max(self.vga_gain, 0.0), 62.0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0_0.set_frequency_range(self.lo_osc_freq, self.samp_rate)
        self.qtgui_time_sink_x_0_0_1_0_0_0_0.set_samp_rate(self.samp_rate)
        self.soapy_hackrf_source_0_0.set_sample_rate(0, self.samp_rate)

    def get_lo_osc_freq_err_compensation(self):
        return self.lo_osc_freq_err_compensation

    def set_lo_osc_freq_err_compensation(self, lo_osc_freq_err_compensation):
        self.lo_osc_freq_err_compensation = lo_osc_freq_err_compensation
        self.soapy_hackrf_source_0_0.set_frequency(0, self.lo_osc_freq+self.lo_osc_freq_err_compensation)

    def get_lo_osc_freq(self):
        return self.lo_osc_freq

    def set_lo_osc_freq(self, lo_osc_freq):
        self.lo_osc_freq = lo_osc_freq
        self.qtgui_sink_x_0_0.set_frequency_range(self.lo_osc_freq, self.samp_rate)
        self.soapy_hackrf_source_0_0.set_frequency(0, self.lo_osc_freq+self.lo_osc_freq_err_compensation)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self._if_gain_callback(self.if_gain)
        self.soapy_hackrf_source_0_0.set_gain(0, 'LNA', min(max(self.if_gain, 0.0), 40.0))

    def get_antialias_bw(self):
        return self.antialias_bw

    def set_antialias_bw(self, antialias_bw):
        self.antialias_bw = antialias_bw
        self._antialias_bw_callback(self.antialias_bw)
        self.soapy_hackrf_source_0_0.set_bandwidth(0, self.antialias_bw)

    def get_amp_on(self):
        return self.amp_on

    def set_amp_on(self, amp_on):
        self.amp_on = amp_on
        self.soapy_hackrf_source_0_0.set_gain(0, 'AMP', self.amp_on)




def main(top_block_cls=soapyOutput, options=None):

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
