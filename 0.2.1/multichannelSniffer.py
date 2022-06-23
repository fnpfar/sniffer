#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Multichannel Sniffer
# Author: Francisco Nicolás Pérez Fernández
# Copyright: Verisure 2021-2022
# Description: A multichannel TCP server sniffer for the Verisure ISM Channels
# GNU Radio version: 3.10.2.0

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from verisure2GFSKRadioChannelToDataMessage import verisure2GFSKRadioChannelToDataMessage  # grc-generated hier_block
from verisure4GFSKRadioChannelToDataMessage import verisure4GFSKRadioChannelToDataMessage  # grc-generated hier_block
import configparser
import multichannelSniffer_verisure_tcp_server_sink as verisure_tcp_server_sink  # embedded python block


def snipfcn_snippet_0_0(self):
    print('End of the execution.')
    sys.exit(0)

def snipfcn_snippet_0_0_0(self):
    # Starts the server at "Verisure TCP Server Sink" block
    self.verisure_tcp_server_sink.start_TCP_server()

    print("Started TCP server at specified adress and port in multichannelSnifferConfig.conf file:")
    print(self.tcp_host_ipv4_address,":",self.tcp_host_port_number)
    print("Starting to receive frames.")

def snipfcn_snippet_1(self):
    # This snippet edits the property "log_level" from the
    # section "LOG" of the following config file:
    # <prefix>/etc/gnuradio/conf.d/gnuradio-runtime.conf
    # in order to change the level of logging from DEBUG (default)
    # to FATAL and thus preventing polluting the console with
    # logging info from GR blocks.
    # For more info read:
    # https://wiki.gnuradio.org/index.php?title=Logging
    # https://wiki.gnuradio.org/index.php?title=Configuration_Files
    # https://www.gnuradio.org/doc/doxygen/classgr_1_1prefs.html
    # Note that the log levels can be:
    # DEBUG, INFO, WARN, TRACE, ERROR, ALERT, CRIT, FATAL, EMERG

    p = gr.prefs() # loads propiertys
    p.set_string("LOG","log_level","EMERG") # sets the propiery
    try:
    	p.save() # saves settings to ${HOME}/.gnuradio/config.conf
    except:
    	pass
    print("Verisure Safety Multichannel Sniffer has been initialized successfully.")
    print("The current channel setup in use is:",self.configFile)


def snippets_main_after_init(tb):
    snipfcn_snippet_1(tb)

def snippets_main_after_start(tb):
    snipfcn_snippet_0_0_0(tb)

def snippets_main_after_stop(tb):
    snipfcn_snippet_0_0(tb)


class multichannelSniffer(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Multichannel Sniffer", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self._configFile_config = configparser.ConfigParser()
        self._configFile_config.read('multichannelSnifferConfig.conf')
        try: configFile = self._configFile_config.get('CONFIG_FILES', 'channel_configuration_file')
        except: configFile = 'multichannelSnifferConfigEurope.conf'
        self.configFile = configFile
        self._vga_gain_config = configparser.ConfigParser()
        self._vga_gain_config.read(configFile)
        try: vga_gain = self._vga_gain_config.getint('HW_SOURCE_CONFIG', 'pre_adc_amplifier_gain')
        except: vga_gain = 0
        self.vga_gain = vga_gain
        self._ted_max_deviation_s_config = configparser.ConfigParser()
        self._ted_max_deviation_s_config.read(configFile)
        try: ted_max_deviation_s = self._ted_max_deviation_s_config.getfloat('2GFSK_CHANNELS', 'timing_error_detector_max_deviation')
        except: ted_max_deviation_s = 1.5
        self.ted_max_deviation_s = ted_max_deviation_s
        self._ted_max_deviation_800_h_config = configparser.ConfigParser()
        self._ted_max_deviation_800_h_config.read(configFile)
        try: ted_max_deviation_800_h = self._ted_max_deviation_800_h_config.getfloat('4GFSK_CHANNELS', 'timing_error_detector_max_deviation_ch800')
        except: ted_max_deviation_800_h = 1.5
        self.ted_max_deviation_800_h = ted_max_deviation_800_h
        self._ted_max_deviation_600_h_config = configparser.ConfigParser()
        self._ted_max_deviation_600_h_config.read(configFile)
        try: ted_max_deviation_600_h = self._ted_max_deviation_600_h_config.getfloat('4GFSK_CHANNELS', 'timing_error_detector_max_deviation_ch600')
        except: ted_max_deviation_600_h = 1.5
        self.ted_max_deviation_600_h = ted_max_deviation_600_h
        self._ted_max_deviation_200_h_config = configparser.ConfigParser()
        self._ted_max_deviation_200_h_config.read(configFile)
        try: ted_max_deviation_200_h = self._ted_max_deviation_200_h_config.getfloat('4GFSK_CHANNELS', 'timing_error_detector_max_deviation_ch200')
        except: ted_max_deviation_200_h = 1.5
        self.ted_max_deviation_200_h = ted_max_deviation_200_h
        self._ted_max_deviation_100_h_config = configparser.ConfigParser()
        self._ted_max_deviation_100_h_config.read(configFile)
        try: ted_max_deviation_100_h = self._ted_max_deviation_100_h_config.getfloat('4GFSK_CHANNELS', 'timing_error_detector_max_deviation_ch100')
        except: ted_max_deviation_100_h = 1.5
        self.ted_max_deviation_100_h = ted_max_deviation_100_h
        self._ted_gain_s_config = configparser.ConfigParser()
        self._ted_gain_s_config.read(configFile)
        try: ted_gain_s = self._ted_gain_s_config.getfloat('2GFSK_CHANNELS', 'timing_error_detector_gain')
        except: ted_gain_s = 1.0
        self.ted_gain_s = ted_gain_s
        self._ted_gain_800_h_config = configparser.ConfigParser()
        self._ted_gain_800_h_config.read(configFile)
        try: ted_gain_800_h = self._ted_gain_800_h_config.getfloat('4GFSK_CHANNELS', 'timing_error_detector_gain_ch800')
        except: ted_gain_800_h = 1.0
        self.ted_gain_800_h = ted_gain_800_h
        self._ted_gain_600_h_config = configparser.ConfigParser()
        self._ted_gain_600_h_config.read(configFile)
        try: ted_gain_600_h = self._ted_gain_600_h_config.getfloat('4GFSK_CHANNELS', 'timing_error_detector_gain_ch600')
        except: ted_gain_600_h = 1.0
        self.ted_gain_600_h = ted_gain_600_h
        self._ted_gain_200_h_config = configparser.ConfigParser()
        self._ted_gain_200_h_config.read(configFile)
        try: ted_gain_200_h = self._ted_gain_200_h_config.getfloat('4GFSK_CHANNELS', 'timing_error_detector_gain_ch200')
        except: ted_gain_200_h = 1.0
        self.ted_gain_200_h = ted_gain_200_h
        self._ted_gain_100_h_config = configparser.ConfigParser()
        self._ted_gain_100_h_config.read(configFile)
        try: ted_gain_100_h = self._ted_gain_100_h_config.getfloat('4GFSK_CHANNELS', 'timing_error_detector_gain_ch100')
        except: ted_gain_100_h = 1.0
        self.ted_gain_100_h = ted_gain_100_h
        self._tcp_host_port_number_config = configparser.ConfigParser()
        self._tcp_host_port_number_config.read('multichannelSnifferConfig.conf')
        try: tcp_host_port_number = self._tcp_host_port_number_config.getint('TCP_SERVER', 'port_number')
        except: tcp_host_port_number = 1337
        self.tcp_host_port_number = tcp_host_port_number
        self._tcp_host_ipv4_address_config = configparser.ConfigParser()
        self._tcp_host_ipv4_address_config.read('multichannelSnifferConfig.conf')
        try: tcp_host_ipv4_address = self._tcp_host_ipv4_address_config.get('TCP_SERVER', 'ipv4_address')
        except: tcp_host_ipv4_address = '127.0.0.1'
        self.tcp_host_ipv4_address = tcp_host_ipv4_address
        self._stopband_start_s_config = configparser.ConfigParser()
        self._stopband_start_s_config.read(configFile)
        try: stopband_start_s = self._stopband_start_s_config.getfloat('2GFSK_CHANNELS', 'channel_stopband_start_frequency')
        except: stopband_start_s = 49e3
        self.stopband_start_s = stopband_start_s
        self._stopband_start_800_h_config = configparser.ConfigParser()
        self._stopband_start_800_h_config.read(configFile)
        try: stopband_start_800_h = self._stopband_start_800_h_config.getfloat('4GFSK_CHANNELS', 'ch800_stopband_start_frequency')
        except: stopband_start_800_h = 375e3
        self.stopband_start_800_h = stopband_start_800_h
        self._stopband_start_600_h_config = configparser.ConfigParser()
        self._stopband_start_600_h_config.read(configFile)
        try: stopband_start_600_h = self._stopband_start_600_h_config.getfloat('4GFSK_CHANNELS', 'ch600_stopband_start_frequency')
        except: stopband_start_600_h = 295e3
        self.stopband_start_600_h = stopband_start_600_h
        self._stopband_start_200_h_config = configparser.ConfigParser()
        self._stopband_start_200_h_config.read(configFile)
        try: stopband_start_200_h = self._stopband_start_200_h_config.getfloat('4GFSK_CHANNELS', 'ch200_stopband_start_frequency')
        except: stopband_start_200_h = 135e3
        self.stopband_start_200_h = stopband_start_200_h
        self._stopband_start_100_h_config = configparser.ConfigParser()
        self._stopband_start_100_h_config.read(configFile)
        try: stopband_start_100_h = self._stopband_start_100_h_config.getfloat('4GFSK_CHANNELS', 'ch100_stopband_start_frequency')
        except: stopband_start_100_h = 90e3
        self.stopband_start_100_h = stopband_start_100_h
        self._stop_band_attenuation_dB_s_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_s_config.read(configFile)
        try: stop_band_attenuation_dB_s = self._stop_band_attenuation_dB_s_config.getint('2GFSK_CHANNELS', 'channel_stopband_attenuation')
        except: stop_band_attenuation_dB_s = 96
        self.stop_band_attenuation_dB_s = stop_band_attenuation_dB_s
        self._stop_band_attenuation_dB_800_h_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_800_h_config.read(configFile)
        try: stop_band_attenuation_dB_800_h = self._stop_band_attenuation_dB_800_h_config.getint('4GFSK_CHANNELS', 'ch800_stopband_attenuation')
        except: stop_band_attenuation_dB_800_h = 96
        self.stop_band_attenuation_dB_800_h = stop_band_attenuation_dB_800_h
        self._stop_band_attenuation_dB_600_h_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_600_h_config.read(configFile)
        try: stop_band_attenuation_dB_600_h = self._stop_band_attenuation_dB_600_h_config.getint('4GFSK_CHANNELS', 'ch600_stopband_attenuation')
        except: stop_band_attenuation_dB_600_h = 96
        self.stop_band_attenuation_dB_600_h = stop_band_attenuation_dB_600_h
        self._stop_band_attenuation_dB_200_h_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_200_h_config.read(configFile)
        try: stop_band_attenuation_dB_200_h = self._stop_band_attenuation_dB_200_h_config.getint('4GFSK_CHANNELS', 'ch200_stopband_attenuation')
        except: stop_band_attenuation_dB_200_h = 96
        self.stop_band_attenuation_dB_200_h = stop_band_attenuation_dB_200_h
        self._stop_band_attenuation_dB_100_h_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_100_h_config.read(configFile)
        try: stop_band_attenuation_dB_100_h = self._stop_band_attenuation_dB_100_h_config.getint('4GFSK_CHANNELS', 'ch100_stopband_attenuation')
        except: stop_band_attenuation_dB_100_h = 96
        self.stop_band_attenuation_dB_100_h = stop_band_attenuation_dB_100_h
        self._squelch_ramp_s_config = configparser.ConfigParser()
        self._squelch_ramp_s_config.read(configFile)
        try: squelch_ramp_s = self._squelch_ramp_s_config.getint('2GFSK_CHANNELS', 'squelch_ramp')
        except: squelch_ramp_s = 8
        self.squelch_ramp_s = squelch_ramp_s
        self._squelch_ramp_800_h_config = configparser.ConfigParser()
        self._squelch_ramp_800_h_config.read(configFile)
        try: squelch_ramp_800_h = self._squelch_ramp_800_h_config.getint('4GFSK_CHANNELS', 'squelch_ramp_ch800')
        except: squelch_ramp_800_h = 8
        self.squelch_ramp_800_h = squelch_ramp_800_h
        self._squelch_ramp_600_h_config = configparser.ConfigParser()
        self._squelch_ramp_600_h_config.read(configFile)
        try: squelch_ramp_600_h = self._squelch_ramp_600_h_config.getint('4GFSK_CHANNELS', 'squelch_ramp_ch600')
        except: squelch_ramp_600_h = 8
        self.squelch_ramp_600_h = squelch_ramp_600_h
        self._squelch_ramp_200_h_config = configparser.ConfigParser()
        self._squelch_ramp_200_h_config.read(configFile)
        try: squelch_ramp_200_h = self._squelch_ramp_200_h_config.getint('4GFSK_CHANNELS', 'squelch_ramp_ch200')
        except: squelch_ramp_200_h = 8
        self.squelch_ramp_200_h = squelch_ramp_200_h
        self._squelch_ramp_100_h_config = configparser.ConfigParser()
        self._squelch_ramp_100_h_config.read(configFile)
        try: squelch_ramp_100_h = self._squelch_ramp_100_h_config.getint('4GFSK_CHANNELS', 'squelch_ramp_ch100')
        except: squelch_ramp_100_h = 8
        self.squelch_ramp_100_h = squelch_ramp_100_h
        self._squelch_level_s_config = configparser.ConfigParser()
        self._squelch_level_s_config.read(configFile)
        try: squelch_level_s = self._squelch_level_s_config.getint('2GFSK_CHANNELS', 'squelch_level')
        except: squelch_level_s = -62
        self.squelch_level_s = squelch_level_s
        self._squelch_level_800_h_config = configparser.ConfigParser()
        self._squelch_level_800_h_config.read(configFile)
        try: squelch_level_800_h = self._squelch_level_800_h_config.getint('4GFSK_CHANNELS', 'squelch_level_ch800')
        except: squelch_level_800_h = -50
        self.squelch_level_800_h = squelch_level_800_h
        self._squelch_level_600_h_config = configparser.ConfigParser()
        self._squelch_level_600_h_config.read(configFile)
        try: squelch_level_600_h = self._squelch_level_600_h_config.getint('4GFSK_CHANNELS', 'squelch_level_ch600')
        except: squelch_level_600_h = -50
        self.squelch_level_600_h = squelch_level_600_h
        self._squelch_level_200_h_config = configparser.ConfigParser()
        self._squelch_level_200_h_config.read(configFile)
        try: squelch_level_200_h = self._squelch_level_200_h_config.getint('4GFSK_CHANNELS', 'squelch_level_ch200')
        except: squelch_level_200_h = -50
        self.squelch_level_200_h = squelch_level_200_h
        self._squelch_level_100_h_config = configparser.ConfigParser()
        self._squelch_level_100_h_config.read(configFile)
        try: squelch_level_100_h = self._squelch_level_100_h_config.getint('4GFSK_CHANNELS', 'squelch_level_ch100')
        except: squelch_level_100_h = -58
        self.squelch_level_100_h = squelch_level_100_h
        self._squelchAlpha_s_config = configparser.ConfigParser()
        self._squelchAlpha_s_config.read(configFile)
        try: squelchAlpha_s = self._squelchAlpha_s_config.getfloat('2GFSK_CHANNELS', 'squelch_alpha')
        except: squelchAlpha_s = 0.3
        self.squelchAlpha_s = squelchAlpha_s
        self._squelchAlpha_800_h_config = configparser.ConfigParser()
        self._squelchAlpha_800_h_config.read(configFile)
        try: squelchAlpha_800_h = self._squelchAlpha_800_h_config.getfloat('4GFSK_CHANNELS', 'squelch_alpha_ch800')
        except: squelchAlpha_800_h = 0.3
        self.squelchAlpha_800_h = squelchAlpha_800_h
        self._squelchAlpha_600_h_config = configparser.ConfigParser()
        self._squelchAlpha_600_h_config.read(configFile)
        try: squelchAlpha_600_h = self._squelchAlpha_600_h_config.getfloat('4GFSK_CHANNELS', 'squelch_alpha_ch600')
        except: squelchAlpha_600_h = 0.3
        self.squelchAlpha_600_h = squelchAlpha_600_h
        self._squelchAlpha_200_h_config = configparser.ConfigParser()
        self._squelchAlpha_200_h_config.read(configFile)
        try: squelchAlpha_200_h = self._squelchAlpha_200_h_config.getfloat('4GFSK_CHANNELS', 'squelch_alpha_ch200')
        except: squelchAlpha_200_h = 0.3
        self.squelchAlpha_200_h = squelchAlpha_200_h
        self._squelchAlpha_100_h_config = configparser.ConfigParser()
        self._squelchAlpha_100_h_config.read(configFile)
        try: squelchAlpha_100_h = self._squelchAlpha_100_h_config.getfloat('4GFSK_CHANNELS', 'squelch_alpha_ch100')
        except: squelchAlpha_100_h = 0.3
        self.squelchAlpha_100_h = squelchAlpha_100_h
        self._samp_rate_demod_s_config = configparser.ConfigParser()
        self._samp_rate_demod_s_config.read(configFile)
        try: samp_rate_demod_s = self._samp_rate_demod_s_config.getint('2GFSK_CHANNELS', 'demodulation_sample_rate')
        except: samp_rate_demod_s = 100000
        self.samp_rate_demod_s = samp_rate_demod_s
        self._samp_rate_demod_800_h_config = configparser.ConfigParser()
        self._samp_rate_demod_800_h_config.read(configFile)
        try: samp_rate_demod_800_h = self._samp_rate_demod_800_h_config.getint('4GFSK_CHANNELS', 'demodulation_sample_rate_ch800')
        except: samp_rate_demod_800_h = 812500
        self.samp_rate_demod_800_h = samp_rate_demod_800_h
        self._samp_rate_demod_600_h_config = configparser.ConfigParser()
        self._samp_rate_demod_600_h_config.read(configFile)
        try: samp_rate_demod_600_h = self._samp_rate_demod_600_h_config.getint('4GFSK_CHANNELS', 'demodulation_sample_rate_ch600')
        except: samp_rate_demod_600_h = 650000
        self.samp_rate_demod_600_h = samp_rate_demod_600_h
        self._samp_rate_demod_200_h_config = configparser.ConfigParser()
        self._samp_rate_demod_200_h_config.read(configFile)
        try: samp_rate_demod_200_h = self._samp_rate_demod_200_h_config.getint('4GFSK_CHANNELS', 'demodulation_sample_rate_ch200')
        except: samp_rate_demod_200_h = 325000
        self.samp_rate_demod_200_h = samp_rate_demod_200_h
        self._samp_rate_demod_100_h_config = configparser.ConfigParser()
        self._samp_rate_demod_100_h_config.read(configFile)
        try: samp_rate_demod_100_h = self._samp_rate_demod_100_h_config.getint('4GFSK_CHANNELS', 'demodulation_sample_rate_ch100')
        except: samp_rate_demod_100_h = 260000
        self.samp_rate_demod_100_h = samp_rate_demod_100_h
        self._samp_rate_config = configparser.ConfigParser()
        self._samp_rate_config.read(configFile)
        try: samp_rate = self._samp_rate_config.getint('HW_SOURCE_CONFIG', 'sample_rate')
        except: samp_rate = 13000000
        self.samp_rate = samp_rate
        self._rssi_calib_offset_s_config = configparser.ConfigParser()
        self._rssi_calib_offset_s_config.read(configFile)
        try: rssi_calib_offset_s = self._rssi_calib_offset_s_config.getfloat('2GFSK_CHANNELS', 'rssi_offset_calibration')
        except: rssi_calib_offset_s = -5.0
        self.rssi_calib_offset_s = rssi_calib_offset_s
        self._rssi_calib_offset_800_h_config = configparser.ConfigParser()
        self._rssi_calib_offset_800_h_config.read(configFile)
        try: rssi_calib_offset_800_h = self._rssi_calib_offset_800_h_config.getfloat('4GFSK_CHANNELS', 'rssi_offset_calibration_ch800')
        except: rssi_calib_offset_800_h = -5.0
        self.rssi_calib_offset_800_h = rssi_calib_offset_800_h
        self._rssi_calib_offset_600_h_config = configparser.ConfigParser()
        self._rssi_calib_offset_600_h_config.read(configFile)
        try: rssi_calib_offset_600_h = self._rssi_calib_offset_600_h_config.getfloat('4GFSK_CHANNELS', 'rssi_offset_calibration_ch600')
        except: rssi_calib_offset_600_h = -5.0
        self.rssi_calib_offset_600_h = rssi_calib_offset_600_h
        self._rssi_calib_offset_200_h_config = configparser.ConfigParser()
        self._rssi_calib_offset_200_h_config.read(configFile)
        try: rssi_calib_offset_200_h = self._rssi_calib_offset_200_h_config.getfloat('4GFSK_CHANNELS', 'rssi_offset_calibration_ch200')
        except: rssi_calib_offset_200_h = -5.0
        self.rssi_calib_offset_200_h = rssi_calib_offset_200_h
        self._rssi_calib_offset_100_h_config = configparser.ConfigParser()
        self._rssi_calib_offset_100_h_config.read(configFile)
        try: rssi_calib_offset_100_h = self._rssi_calib_offset_100_h_config.getfloat('4GFSK_CHANNELS', 'rssi_offset_calibration_ch100')
        except: rssi_calib_offset_100_h = -5.0
        self.rssi_calib_offset_100_h = rssi_calib_offset_100_h
        self.qt_gui_display_time_before_symbolSink = qt_gui_display_time_before_symbolSink = 64e-3
        self.qt_gui_display_time_before_decimation = qt_gui_display_time_before_decimation = 64e-3
        self.qt_gui_display_time_after_symbolSink = qt_gui_display_time_after_symbolSink = 32e-3
        self._passband_end_s_config = configparser.ConfigParser()
        self._passband_end_s_config.read(configFile)
        try: passband_end_s = self._passband_end_s_config.getfloat('2GFSK_CHANNELS', 'channel_passband_end_frequency')
        except: passband_end_s = 39e3
        self.passband_end_s = passband_end_s
        self._passband_end_800_h_config = configparser.ConfigParser()
        self._passband_end_800_h_config.read(configFile)
        try: passband_end_800_h = self._passband_end_800_h_config.getfloat('4GFSK_CHANNELS', 'ch800_passband_end_frequency')
        except: passband_end_800_h = 365e3
        self.passband_end_800_h = passband_end_800_h
        self._passband_end_600_h_config = configparser.ConfigParser()
        self._passband_end_600_h_config.read(configFile)
        try: passband_end_600_h = self._passband_end_600_h_config.getfloat('4GFSK_CHANNELS', 'ch600_passband_end_frequency')
        except: passband_end_600_h = 285e3
        self.passband_end_600_h = passband_end_600_h
        self._passband_end_200_h_config = configparser.ConfigParser()
        self._passband_end_200_h_config.read(configFile)
        try: passband_end_200_h = self._passband_end_200_h_config.getfloat('4GFSK_CHANNELS', 'ch200_passband_end_frequency')
        except: passband_end_200_h = 125e3
        self.passband_end_200_h = passband_end_200_h
        self._passband_end_100_h_config = configparser.ConfigParser()
        self._passband_end_100_h_config.read(configFile)
        try: passband_end_100_h = self._passband_end_100_h_config.getfloat('4GFSK_CHANNELS', 'ch100_passband_end_frequency')
        except: passband_end_100_h = 84e3
        self.passband_end_100_h = passband_end_100_h
        self._message_debug_config = configparser.ConfigParser()
        self._message_debug_config.read('multichannelSnifferConfig.conf')
        try: message_debug = self._message_debug_config.getboolean('DEBUG_LOG', 'individual_channel_log')
        except: message_debug = False
        self.message_debug = message_debug
        self._loop_damping_s_config = configparser.ConfigParser()
        self._loop_damping_s_config.read(configFile)
        try: loop_damping_s = self._loop_damping_s_config.getfloat('2GFSK_CHANNELS', 'symbol_sync_loop_damping')
        except: loop_damping_s = 1.4
        self.loop_damping_s = loop_damping_s
        self._loop_damping_800_h_config = configparser.ConfigParser()
        self._loop_damping_800_h_config.read(configFile)
        try: loop_damping_800_h = self._loop_damping_800_h_config.getfloat('4GFSK_CHANNELS', 'symbol_sync_loop_damping_ch800')
        except: loop_damping_800_h = 1.4
        self.loop_damping_800_h = loop_damping_800_h
        self._loop_damping_600_h_config = configparser.ConfigParser()
        self._loop_damping_600_h_config.read(configFile)
        try: loop_damping_600_h = self._loop_damping_600_h_config.getfloat('4GFSK_CHANNELS', 'symbol_sync_loop_damping_ch600')
        except: loop_damping_600_h = 1.4
        self.loop_damping_600_h = loop_damping_600_h
        self._loop_damping_200_h_config = configparser.ConfigParser()
        self._loop_damping_200_h_config.read(configFile)
        try: loop_damping_200_h = self._loop_damping_200_h_config.getfloat('4GFSK_CHANNELS', 'symbol_sync_loop_damping_ch200')
        except: loop_damping_200_h = 1.4
        self.loop_damping_200_h = loop_damping_200_h
        self._loop_damping_100_h_config = configparser.ConfigParser()
        self._loop_damping_100_h_config.read(configFile)
        try: loop_damping_100_h = self._loop_damping_100_h_config.getfloat('4GFSK_CHANNELS', 'symbol_sync_loop_damping_ch100')
        except: loop_damping_100_h = 1.4
        self.loop_damping_100_h = loop_damping_100_h
        self._loop_bw_s_config = configparser.ConfigParser()
        self._loop_bw_s_config.read(configFile)
        try: loop_bw_s = self._loop_bw_s_config.getfloat('2GFSK_CHANNELS', 'symbol_sync_loop_bandwidth')
        except: loop_bw_s = 0.015
        self.loop_bw_s = loop_bw_s
        self._loop_bw_800_h_config = configparser.ConfigParser()
        self._loop_bw_800_h_config.read(configFile)
        try: loop_bw_800_h = self._loop_bw_800_h_config.getfloat('4GFSK_CHANNELS', 'symbol_sync_loop_bandwidth_ch800')
        except: loop_bw_800_h = 0.015
        self.loop_bw_800_h = loop_bw_800_h
        self._loop_bw_600_h_config = configparser.ConfigParser()
        self._loop_bw_600_h_config.read(configFile)
        try: loop_bw_600_h = self._loop_bw_600_h_config.getfloat('4GFSK_CHANNELS', 'symbol_sync_loop_bandwidth_ch600')
        except: loop_bw_600_h = 0.015
        self.loop_bw_600_h = loop_bw_600_h
        self._loop_bw_200_h_config = configparser.ConfigParser()
        self._loop_bw_200_h_config.read(configFile)
        try: loop_bw_200_h = self._loop_bw_200_h_config.getfloat('4GFSK_CHANNELS', 'symbol_sync_loop_bandwidth_ch200')
        except: loop_bw_200_h = 0.015
        self.loop_bw_200_h = loop_bw_200_h
        self._loop_bw_100_h_config = configparser.ConfigParser()
        self._loop_bw_100_h_config.read(configFile)
        try: loop_bw_100_h = self._loop_bw_100_h_config.getfloat('4GFSK_CHANNELS', 'symbol_sync_loop_bandwidth_ch100')
        except: loop_bw_100_h = 0.015
        self.loop_bw_100_h = loop_bw_100_h
        self._lo_osc_freq_error_correction_config = configparser.ConfigParser()
        self._lo_osc_freq_error_correction_config.read(configFile)
        try: lo_osc_freq_error_correction = self._lo_osc_freq_error_correction_config.getfloat('HW_SOURCE_CONFIG', 'local_oscillator_frequency_correction')
        except: lo_osc_freq_error_correction = 0.0
        self.lo_osc_freq_error_correction = lo_osc_freq_error_correction
        self._lo_osc_freq_config = configparser.ConfigParser()
        self._lo_osc_freq_config.read(configFile)
        try: lo_osc_freq = self._lo_osc_freq_config.getfloat('HW_SOURCE_CONFIG', 'local_oscillator_frequency')
        except: lo_osc_freq = 869.3e6
        self.lo_osc_freq = lo_osc_freq
        self._lna_on_config = configparser.ConfigParser()
        self._lna_on_config.read(configFile)
        try: lna_on = self._lna_on_config.getboolean('HW_SOURCE_CONFIG', 'enable_rf_low_noise_amplifier')
        except: lna_on = True
        self.lna_on = lna_on
        self._if_gain_config = configparser.ConfigParser()
        self._if_gain_config.read(configFile)
        try: if_gain = self._if_gain_config.getint('HW_SOURCE_CONFIG', 'intermediate_frequency_amplifier_gain')
        except: if_gain = 16
        self.if_gain = if_gain
        self._high_verbosity_debug_config = configparser.ConfigParser()
        self._high_verbosity_debug_config.read('multichannelSnifferConfig.conf')
        try: high_verbosity_debug = self._high_verbosity_debug_config.getboolean('DEBUG_LOG', 'high_verbosity_individual_channel_log')
        except: high_verbosity_debug = False
        self.high_verbosity_debug = high_verbosity_debug
        self._high_verbosity_all_channel_log_config = configparser.ConfigParser()
        self._high_verbosity_all_channel_log_config.read('multichannelSnifferConfig.conf')
        try: high_verbosity_all_channel_log = self._high_verbosity_all_channel_log_config.getboolean('DEBUG_LOG', 'high_verbosity_all_channel_log')
        except: high_verbosity_all_channel_log = False
        self.high_verbosity_all_channel_log = high_verbosity_all_channel_log
        self._fsk_deviation_s_config = configparser.ConfigParser()
        self._fsk_deviation_s_config.read(configFile)
        try: fsk_deviation_s = self._fsk_deviation_s_config.getfloat('2GFSK_CHANNELS', 'frequency_deviation')
        except: fsk_deviation_s = 19.775e3
        self.fsk_deviation_s = fsk_deviation_s
        self._fsk_deviation_800_h_config = configparser.ConfigParser()
        self._fsk_deviation_800_h_config.read(configFile)
        try: fsk_deviation_800_h = self._fsk_deviation_800_h_config.getfloat('4GFSK_CHANNELS', 'frequency_deviation_ch800')
        except: fsk_deviation_800_h = 165000.0
        self.fsk_deviation_800_h = fsk_deviation_800_h
        self._fsk_deviation_600_h_config = configparser.ConfigParser()
        self._fsk_deviation_600_h_config.read(configFile)
        try: fsk_deviation_600_h = self._fsk_deviation_600_h_config.getfloat('4GFSK_CHANNELS', 'frequency_deviation_ch600')
        except: fsk_deviation_600_h = 135000.0
        self.fsk_deviation_600_h = fsk_deviation_600_h
        self._fsk_deviation_200_h_config = configparser.ConfigParser()
        self._fsk_deviation_200_h_config.read(configFile)
        try: fsk_deviation_200_h = self._fsk_deviation_200_h_config.getfloat('4GFSK_CHANNELS', 'frequency_deviation_ch200')
        except: fsk_deviation_200_h = 75000.0
        self.fsk_deviation_200_h = fsk_deviation_200_h
        self._fsk_deviation_100_h_config = configparser.ConfigParser()
        self._fsk_deviation_100_h_config.read(configFile)
        try: fsk_deviation_100_h = self._fsk_deviation_100_h_config.getfloat('4GFSK_CHANNELS', 'frequency_deviation_ch100')
        except: fsk_deviation_100_h = 60000.0
        self.fsk_deviation_100_h = fsk_deviation_100_h
        self._dewhitening_key_config = configparser.ConfigParser()
        self._dewhitening_key_config.read('multichannelSnifferConfig.conf')
        try: dewhitening_key = self._dewhitening_key_config.getint('FRAME_DECODING', 'dewhitening_key')
        except: dewhitening_key = 0x1ff
        self.dewhitening_key = dewhitening_key
        self._demod_dc_block_time_s_config = configparser.ConfigParser()
        self._demod_dc_block_time_s_config.read(configFile)
        try: demod_dc_block_time_s = self._demod_dc_block_time_s_config.getfloat('2GFSK_CHANNELS', 'dc_blocking_time')
        except: demod_dc_block_time_s = 6e-3
        self.demod_dc_block_time_s = demod_dc_block_time_s
        self._demod_dc_block_time_800_h_config = configparser.ConfigParser()
        self._demod_dc_block_time_800_h_config.read(configFile)
        try: demod_dc_block_time_800_h = self._demod_dc_block_time_800_h_config.getfloat('4GFSK_CHANNELS', 'dc_blocking_time_ch800')
        except: demod_dc_block_time_800_h = 6e-3
        self.demod_dc_block_time_800_h = demod_dc_block_time_800_h
        self._demod_dc_block_time_600_h_config = configparser.ConfigParser()
        self._demod_dc_block_time_600_h_config.read(configFile)
        try: demod_dc_block_time_600_h = self._demod_dc_block_time_600_h_config.getfloat('4GFSK_CHANNELS', 'dc_blocking_time_ch600')
        except: demod_dc_block_time_600_h = 6e-3
        self.demod_dc_block_time_600_h = demod_dc_block_time_600_h
        self._demod_dc_block_time_200_h_config = configparser.ConfigParser()
        self._demod_dc_block_time_200_h_config.read(configFile)
        try: demod_dc_block_time_200_h = self._demod_dc_block_time_200_h_config.getfloat('4GFSK_CHANNELS', 'dc_blocking_time_ch200')
        except: demod_dc_block_time_200_h = 6e-3
        self.demod_dc_block_time_200_h = demod_dc_block_time_200_h
        self._demod_dc_block_time_100_h_config = configparser.ConfigParser()
        self._demod_dc_block_time_100_h_config.read(configFile)
        try: demod_dc_block_time_100_h = self._demod_dc_block_time_100_h_config.getfloat('4GFSK_CHANNELS', 'dc_blocking_time_ch100')
        except: demod_dc_block_time_100_h = 6e-3
        self.demod_dc_block_time_100_h = demod_dc_block_time_100_h
        self._debug_log_server_config = configparser.ConfigParser()
        self._debug_log_server_config.read('multichannelSnifferConfig.conf')
        try: debug_log_server = self._debug_log_server_config.getboolean('DEBUG_LOG', 'server_debug_log')
        except: debug_log_server = True
        self.debug_log_server = debug_log_server
        self._crc_polynomial_config = configparser.ConfigParser()
        self._crc_polynomial_config.read('multichannelSnifferConfig.conf')
        try: crc_polynomial = self._crc_polynomial_config.getint('FRAME_DECODING', 'crc_polynomial')
        except: crc_polynomial = 0x8005
        self.crc_polynomial = crc_polynomial
        self._crc_key_config = configparser.ConfigParser()
        self._crc_key_config.read('multichannelSnifferConfig.conf')
        try: crc_key = self._crc_key_config.getint('FRAME_DECODING', 'crc_key')
        except: crc_key = 0xFFFF
        self.crc_key = crc_key
        self._ch800freq_h_config = configparser.ConfigParser()
        self._ch800freq_h_config.read(configFile)
        try: ch800freq_h = self._ch800freq_h_config.getfloat('4GFSK_CHANNELS', 'ch800_center_freq')
        except: ch800freq_h = 868.3e6
        self.ch800freq_h = ch800freq_h
        self._ch800enable_config = configparser.ConfigParser()
        self._ch800enable_config.read(configFile)
        try: ch800enable = self._ch800enable_config.getboolean('4GFSK_CHANNELS', 'ch_800_enable')
        except: ch800enable = True
        self.ch800enable = ch800enable
        self._ch800Bitrate_h_config = configparser.ConfigParser()
        self._ch800Bitrate_h_config.read(configFile)
        try: ch800Bitrate_h = self._ch800Bitrate_h_config.getint('4GFSK_CHANNELS', 'baseband_bitrate_ch800')
        except: ch800Bitrate_h = 800000
        self.ch800Bitrate_h = ch800Bitrate_h
        self._ch600freq_h_config = configparser.ConfigParser()
        self._ch600freq_h_config.read(configFile)
        try: ch600freq_h = self._ch600freq_h_config.getfloat('4GFSK_CHANNELS', 'ch600_center_freq')
        except: ch600freq_h = 868.975e6
        self.ch600freq_h = ch600freq_h
        self._ch600enable_config = configparser.ConfigParser()
        self._ch600enable_config.read(configFile)
        try: ch600enable = self._ch600enable_config.getboolean('4GFSK_CHANNELS', 'ch_600_enable')
        except: ch600enable = True
        self.ch600enable = ch600enable
        self._ch600Bitrate_h_config = configparser.ConfigParser()
        self._ch600Bitrate_h_config.read(configFile)
        try: ch600Bitrate_h = self._ch600Bitrate_h_config.getint('4GFSK_CHANNELS', 'baseband_bitrate_ch600')
        except: ch600Bitrate_h = 600000
        self.ch600Bitrate_h = ch600Bitrate_h
        self._ch5freq_s_config = configparser.ConfigParser()
        self._ch5freq_s_config.read(configFile)
        try: ch5freq_s = self._ch5freq_s_config.getfloat('2GFSK_CHANNELS', 'ch_5_center_freq')
        except: ch5freq_s = 869.050e6
        self.ch5freq_s = ch5freq_s
        self._ch5enable_config = configparser.ConfigParser()
        self._ch5enable_config.read(configFile)
        try: ch5enable = self._ch5enable_config.getboolean('2GFSK_CHANNELS', 'ch_5_enable')
        except: ch5enable = True
        self.ch5enable = ch5enable
        self._ch5_number_s_config = configparser.ConfigParser()
        self._ch5_number_s_config.read(configFile)
        try: ch5_number_s = self._ch5_number_s_config.getint('2GFSK_CHANNELS', 'ch5_override_ch_number')
        except: ch5_number_s = 5
        self.ch5_number_s = ch5_number_s
        self._ch4freq_s_config = configparser.ConfigParser()
        self._ch4freq_s_config.read(configFile)
        try: ch4freq_s = self._ch4freq_s_config.getfloat('2GFSK_CHANNELS', 'ch_4_center_freq')
        except: ch4freq_s = 868.900e6
        self.ch4freq_s = ch4freq_s
        self._ch4enable_config = configparser.ConfigParser()
        self._ch4enable_config.read(configFile)
        try: ch4enable = self._ch4enable_config.getboolean('2GFSK_CHANNELS', 'ch_4_enable')
        except: ch4enable = True
        self.ch4enable = ch4enable
        self._ch4_number_s_config = configparser.ConfigParser()
        self._ch4_number_s_config.read(configFile)
        try: ch4_number_s = self._ch4_number_s_config.getint('2GFSK_CHANNELS', 'ch4_override_ch_number')
        except: ch4_number_s = 4
        self.ch4_number_s = ch4_number_s
        self._ch3freq_s_config = configparser.ConfigParser()
        self._ch3freq_s_config.read(configFile)
        try: ch3freq_s = self._ch3freq_s_config.getfloat('2GFSK_CHANNELS', 'ch_3_center_freq')
        except: ch3freq_s = 868.450e6
        self.ch3freq_s = ch3freq_s
        self._ch3enable_config = configparser.ConfigParser()
        self._ch3enable_config.read(configFile)
        try: ch3enable = self._ch3enable_config.getboolean('2GFSK_CHANNELS', 'ch_3_enable')
        except: ch3enable = True
        self.ch3enable = ch3enable
        self._ch3_number_s_config = configparser.ConfigParser()
        self._ch3_number_s_config.read(configFile)
        try: ch3_number_s = self._ch3_number_s_config.getint('2GFSK_CHANNELS', 'ch3_override_ch_number')
        except: ch3_number_s = 3
        self.ch3_number_s = ch3_number_s
        self._ch2freq_s_config = configparser.ConfigParser()
        self._ch2freq_s_config.read(configFile)
        try: ch2freq_s = self._ch2freq_s_config.getfloat('2GFSK_CHANNELS', 'ch_2_center_freq')
        except: ch2freq_s = 868.300e6
        self.ch2freq_s = ch2freq_s
        self._ch2enable_config = configparser.ConfigParser()
        self._ch2enable_config.read(configFile)
        try: ch2enable = self._ch2enable_config.getboolean('2GFSK_CHANNELS', 'ch_2_enable')
        except: ch2enable = True
        self.ch2enable = ch2enable
        self._ch2_number_s_config = configparser.ConfigParser()
        self._ch2_number_s_config.read(configFile)
        try: ch2_number_s = self._ch2_number_s_config.getint('2GFSK_CHANNELS', 'ch2_override_ch_number')
        except: ch2_number_s = 2
        self.ch2_number_s = ch2_number_s
        self._ch200freq_h_config = configparser.ConfigParser()
        self._ch200freq_h_config.read(configFile)
        try: ch200freq_h = self._ch200freq_h_config.getfloat('4GFSK_CHANNELS', 'ch200_center_freq')
        except: ch200freq_h = 869.525e6
        self.ch200freq_h = ch200freq_h
        self._ch200enable_config = configparser.ConfigParser()
        self._ch200enable_config.read(configFile)
        try: ch200enable = self._ch200enable_config.getboolean('4GFSK_CHANNELS', 'ch_200_enable')
        except: ch200enable = True
        self.ch200enable = ch200enable
        self._ch200Bitrate_h_config = configparser.ConfigParser()
        self._ch200Bitrate_h_config.read(configFile)
        try: ch200Bitrate_h = self._ch200Bitrate_h_config.getint('4GFSK_CHANNELS', 'baseband_bitrate_ch200')
        except: ch200Bitrate_h = 200000
        self.ch200Bitrate_h = ch200Bitrate_h
        self._ch1freq_s_config = configparser.ConfigParser()
        self._ch1freq_s_config.read(configFile)
        try: ch1freq_s = self._ch1freq_s_config.getfloat('2GFSK_CHANNELS', 'ch_1_center_freq')
        except: ch1freq_s = 868.150e6
        self.ch1freq_s = ch1freq_s
        self._ch1enable_config = configparser.ConfigParser()
        self._ch1enable_config.read(configFile)
        try: ch1enable = self._ch1enable_config.getboolean('2GFSK_CHANNELS', 'ch_1_enable')
        except: ch1enable = True
        self.ch1enable = ch1enable
        self._ch1_number_s_config = configparser.ConfigParser()
        self._ch1_number_s_config.read(configFile)
        try: ch1_number_s = self._ch1_number_s_config.getint('2GFSK_CHANNELS', 'ch1_override_ch_number')
        except: ch1_number_s = 1
        self.ch1_number_s = ch1_number_s
        self._ch100freq_h_config = configparser.ConfigParser()
        self._ch100freq_h_config.read(configFile)
        try: ch100freq_h = self._ch100freq_h_config.getfloat('4GFSK_CHANNELS', 'ch100_center_freq')
        except: ch100freq_h = 869.525e6
        self.ch100freq_h = ch100freq_h
        self._ch100enable_config = configparser.ConfigParser()
        self._ch100enable_config.read(configFile)
        try: ch100enable = self._ch100enable_config.getboolean('4GFSK_CHANNELS', 'ch_100_enable')
        except: ch100enable = True
        self.ch100enable = ch100enable
        self._ch100Bitrate_h_config = configparser.ConfigParser()
        self._ch100Bitrate_h_config.read(configFile)
        try: ch100Bitrate_h = self._ch100Bitrate_h_config.getint('4GFSK_CHANNELS', 'baseband_bitrate_ch100')
        except: ch100Bitrate_h = 100000
        self.ch100Bitrate_h = ch100Bitrate_h
        self._bitrate_s_config = configparser.ConfigParser()
        self._bitrate_s_config.read(configFile)
        try: bitrate_s = self._bitrate_s_config.getint('2GFSK_CHANNELS', 'baseband_bitrate')
        except: bitrate_s = 38400
        self.bitrate_s = bitrate_s
        self._antialiass_filter_bw_config = configparser.ConfigParser()
        self._antialiass_filter_bw_config.read(configFile)
        try: antialiass_filter_bw = self._antialiass_filter_bw_config.getfloat('HW_SOURCE_CONFIG', 'antialiasing_filter_bandwidth')
        except: antialiass_filter_bw = 3.5e6
        self.antialiass_filter_bw = antialiass_filter_bw
        self._all_channel_log_config = configparser.ConfigParser()
        self._all_channel_log_config.read('multichannelSnifferConfig.conf')
        try: all_channel_log = self._all_channel_log_config.getboolean('DEBUG_LOG', 'all_channel_log')
        except: all_channel_log = False
        self.all_channel_log = all_channel_log

        ##################################################
        # Blocks
        ##################################################
        self.verisure_tcp_server_sink = verisure_tcp_server_sink.blk(block_Failed_CRC_frames=False, host=tcp_host_ipv4_address, port=tcp_host_port_number, server_mode=1, debug_Log_Frame=all_channel_log, high_Verbosity_Frame_Log=high_verbosity_all_channel_log, debug_Log_Server=debug_log_server)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0 = verisure4GFSKRadioChannelToDataMessage(
            bitrate=ch800Bitrate_h,
            ch_enable=ch800enable,
            ch_number=13,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_800_h,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_800_h,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_800_h,
            loop_damping=loop_damping_800_h,
            passband_end=passband_end_800_h,
            power_offset_calib=rssi_calib_offset_800_h,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_800_h,
            selected_ch_freq=ch800freq_h,
            squelchAlpha=squelchAlpha_800_h,
            squelch_level=squelch_level_800_h,
            squelch_ramp=squelch_ramp_800_h,
            stop_band_attenuation_dB=stop_band_attenuation_dB_800_h,
            stopband_start=stopband_start_800_h,
            ted_gain=ted_gain_800_h,
            ted_max_deviation=ted_max_deviation_800_h,
        )
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0 = verisure4GFSKRadioChannelToDataMessage(
            bitrate=ch600Bitrate_h,
            ch_enable=ch600enable,
            ch_number=12,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_600_h,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_600_h,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_600_h,
            loop_damping=loop_damping_600_h,
            passband_end=passband_end_600_h,
            power_offset_calib=rssi_calib_offset_600_h,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_600_h,
            selected_ch_freq=ch600freq_h,
            squelchAlpha=squelchAlpha_600_h,
            squelch_level=squelch_level_600_h,
            squelch_ramp=squelch_ramp_600_h,
            stop_band_attenuation_dB=stop_band_attenuation_dB_600_h,
            stopband_start=stopband_start_600_h,
            ted_gain=ted_gain_600_h,
            ted_max_deviation=ted_max_deviation_600_h,
        )
        self.verisure4GFSKRadioChannelToDataMessage_0_0 = verisure4GFSKRadioChannelToDataMessage(
            bitrate=ch200Bitrate_h,
            ch_enable=ch200enable,
            ch_number=11,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_200_h,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_200_h,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_200_h,
            loop_damping=loop_damping_200_h,
            passband_end=passband_end_200_h,
            power_offset_calib=rssi_calib_offset_200_h,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_200_h,
            selected_ch_freq=ch200freq_h,
            squelchAlpha=squelchAlpha_200_h,
            squelch_level=squelch_level_200_h,
            squelch_ramp=squelch_ramp_200_h,
            stop_band_attenuation_dB=stop_band_attenuation_dB_200_h,
            stopband_start=stopband_start_200_h,
            ted_gain=ted_gain_200_h,
            ted_max_deviation=ted_max_deviation_200_h,
        )
        self.verisure4GFSKRadioChannelToDataMessage_0 = verisure4GFSKRadioChannelToDataMessage(
            bitrate=ch100Bitrate_h,
            ch_enable=ch100enable,
            ch_number=10,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_100_h,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_100_h,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_100_h,
            loop_damping=loop_damping_100_h,
            passband_end=passband_end_100_h,
            power_offset_calib=rssi_calib_offset_100_h,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_100_h,
            selected_ch_freq=ch100freq_h,
            squelchAlpha=squelchAlpha_100_h,
            squelch_level=squelch_level_100_h,
            squelch_ramp=squelch_ramp_100_h,
            stop_band_attenuation_dB=stop_band_attenuation_dB_100_h,
            stopband_start=stopband_start_100_h,
            ted_gain=ted_gain_100_h,
            ted_max_deviation=ted_max_deviation_100_h,
        )
        self.verisure2GFSKRadioChannelToDataMessage_0_3 = verisure2GFSKRadioChannelToDataMessage(
            bitrate=bitrate_s,
            ch_enable=ch5enable,
            ch_number=ch5_number_s,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_s,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_s,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_s,
            loop_damping=loop_damping_s,
            passband_end=passband_end_s,
            power_offset_calib=rssi_calib_offset_s,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_s,
            selected_ch_freq=ch5freq_s,
            squelchAlpha=squelchAlpha_s,
            squelch_level=squelch_level_s,
            squelch_ramp=squelch_ramp_s,
            stop_band_attenuation_dB=stop_band_attenuation_dB_s,
            stopband_start=stopband_start_s,
            ted_gain=ted_gain_s,
            ted_max_deviation=ted_max_deviation_s,
        )
        self.verisure2GFSKRadioChannelToDataMessage_0_2 = verisure2GFSKRadioChannelToDataMessage(
            bitrate=bitrate_s,
            ch_enable=ch4enable,
            ch_number=ch4_number_s,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_s,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_s,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_s,
            loop_damping=loop_damping_s,
            passband_end=passband_end_s,
            power_offset_calib=rssi_calib_offset_s,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_s,
            selected_ch_freq=ch4freq_s,
            squelchAlpha=squelchAlpha_s,
            squelch_level=squelch_level_s,
            squelch_ramp=squelch_ramp_s,
            stop_band_attenuation_dB=stop_band_attenuation_dB_s,
            stopband_start=stopband_start_s,
            ted_gain=ted_gain_s,
            ted_max_deviation=ted_max_deviation_s,
        )
        self.verisure2GFSKRadioChannelToDataMessage_0_1 = verisure2GFSKRadioChannelToDataMessage(
            bitrate=bitrate_s,
            ch_enable=ch3enable,
            ch_number=ch3_number_s,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_s,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_s,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_s,
            loop_damping=loop_damping_s,
            passband_end=passband_end_s,
            power_offset_calib=rssi_calib_offset_s,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_s,
            selected_ch_freq=ch3freq_s,
            squelchAlpha=squelchAlpha_s,
            squelch_level=squelch_level_s,
            squelch_ramp=squelch_ramp_s,
            stop_band_attenuation_dB=stop_band_attenuation_dB_s,
            stopband_start=stopband_start_s,
            ted_gain=ted_gain_s,
            ted_max_deviation=ted_max_deviation_s,
        )
        self.verisure2GFSKRadioChannelToDataMessage_0_0 = verisure2GFSKRadioChannelToDataMessage(
            bitrate=bitrate_s,
            ch_enable=ch2enable,
            ch_number=ch2_number_s,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_s,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_s,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_s,
            loop_damping=loop_damping_s,
            passband_end=passband_end_s,
            power_offset_calib=rssi_calib_offset_s,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_s,
            selected_ch_freq=ch2freq_s,
            squelchAlpha=squelchAlpha_s,
            squelch_level=squelch_level_s,
            squelch_ramp=squelch_ramp_s,
            stop_band_attenuation_dB=stop_band_attenuation_dB_s,
            stopband_start=stopband_start_s,
            ted_gain=ted_gain_s,
            ted_max_deviation=ted_max_deviation_s,
        )
        self.verisure2GFSKRadioChannelToDataMessage_0 = verisure2GFSKRadioChannelToDataMessage(
            bitrate=bitrate_s,
            ch_enable=ch1enable,
            ch_number=ch1_number_s,
            crc_key=crc_key,
            crc_polynomial=crc_polynomial,
            debug_log=message_debug,
            debug_log_verbosity=high_verbosity_debug,
            demod_dc_block_time=demod_dc_block_time_s,
            dewhitening_key=dewhitening_key,
            fsk_deviation=fsk_deviation_s,
            lo_osc_freq=lo_osc_freq,
            loop_bw=loop_bw_s,
            loop_damping=loop_damping_s,
            passband_end=passband_end_s,
            power_offset_calib=rssi_calib_offset_s,
            samp_rate=samp_rate,
            samp_rate_demod=samp_rate_demod_s,
            selected_ch_freq=ch1freq_s,
            squelchAlpha=squelchAlpha_s,
            squelch_level=squelch_level_s,
            squelch_ramp=squelch_ramp_s,
            stop_band_attenuation_dB=stop_band_attenuation_dB_s,
            stopband_start=stopband_start_s,
            ted_gain=ted_gain_s,
            ted_max_deviation=ted_max_deviation_s,
        )
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, antialiass_filter_bw)
        self.soapy_hackrf_source_0.set_frequency(0, lo_osc_freq+lo_osc_freq_error_correction)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', lna_on)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(if_gain, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(vga_gain, 0.0), 62.0))
        self.blocks_null_sink_2_2_1_0_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_2_1_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_2_1_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_2_1_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_2_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_2_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_2_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_2_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_1_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_9_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_8_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_7_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_6_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_5_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_4_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_3_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_2_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_2_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_2_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_2 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_10 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_0_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_0_0_1_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_0_0_1_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_1_0_0_0_1_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2_0_0_1_0_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_0_0_1_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_0_0_1_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_0_0_1_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_0_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_0_0_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_0_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.verisure2GFSKRadioChannelToDataMessage_0, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.msg_connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.msg_connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.msg_connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.msg_connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.msg_connect((self.verisure4GFSKRadioChannelToDataMessage_0, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.msg_connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.msg_connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.msg_connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 'message_out'), (self.verisure_tcp_server_sink, 'pdu_in'))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure2GFSKRadioChannelToDataMessage_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure2GFSKRadioChannelToDataMessage_0_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure2GFSKRadioChannelToDataMessage_0_1, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure2GFSKRadioChannelToDataMessage_0_2, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure2GFSKRadioChannelToDataMessage_0_3, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure4GFSKRadioChannelToDataMessage_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure4GFSKRadioChannelToDataMessage_0_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 1), (self.blocks_null_sink_2_0_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 2), (self.blocks_null_sink_2_1_0_10_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 11), (self.blocks_null_sink_2_1_0_1_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 12), (self.blocks_null_sink_2_1_0_1_0_1_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 10), (self.blocks_null_sink_2_1_0_2_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 9), (self.blocks_null_sink_2_1_0_3_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 8), (self.blocks_null_sink_2_1_0_4_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 7), (self.blocks_null_sink_2_1_0_5_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 6), (self.blocks_null_sink_2_1_0_6_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 5), (self.blocks_null_sink_2_1_0_7_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 3), (self.blocks_null_sink_2_1_0_8_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 4), (self.blocks_null_sink_2_1_0_9_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0, 0), (self.blocks_null_sink_2_2_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 1), (self.blocks_null_sink_2_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 3), (self.blocks_null_sink_2_1_0_10, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 12), (self.blocks_null_sink_2_1_0_1_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 11), (self.blocks_null_sink_2_1_0_2_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 10), (self.blocks_null_sink_2_1_0_3_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 9), (self.blocks_null_sink_2_1_0_4_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 8), (self.blocks_null_sink_2_1_0_5_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 7), (self.blocks_null_sink_2_1_0_6_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 6), (self.blocks_null_sink_2_1_0_7_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 4), (self.blocks_null_sink_2_1_0_8_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 5), (self.blocks_null_sink_2_1_0_9_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 2), (self.blocks_null_sink_2_1_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_0, 0), (self.blocks_null_sink_2_2, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 1), (self.blocks_null_sink_2_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 3), (self.blocks_null_sink_2_1_0_10_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 12), (self.blocks_null_sink_2_1_0_1_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 2), (self.blocks_null_sink_2_1_0_1_0_0_1, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 11), (self.blocks_null_sink_2_1_0_2_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 10), (self.blocks_null_sink_2_1_0_3_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 9), (self.blocks_null_sink_2_1_0_4_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 8), (self.blocks_null_sink_2_1_0_5_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 7), (self.blocks_null_sink_2_1_0_6_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 6), (self.blocks_null_sink_2_1_0_7_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 4), (self.blocks_null_sink_2_1_0_8_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 5), (self.blocks_null_sink_2_1_0_9_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_1, 0), (self.blocks_null_sink_2_2_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 1), (self.blocks_null_sink_2_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 3), (self.blocks_null_sink_2_1_0_10_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 12), (self.blocks_null_sink_2_1_0_1_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 11), (self.blocks_null_sink_2_1_0_2_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 10), (self.blocks_null_sink_2_1_0_3_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 9), (self.blocks_null_sink_2_1_0_4_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 8), (self.blocks_null_sink_2_1_0_5_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 7), (self.blocks_null_sink_2_1_0_6_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 6), (self.blocks_null_sink_2_1_0_7_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 4), (self.blocks_null_sink_2_1_0_8_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 5), (self.blocks_null_sink_2_1_0_9_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 2), (self.blocks_null_sink_2_1_1_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_2, 0), (self.blocks_null_sink_2_2_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 1), (self.blocks_null_sink_2_0_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 3), (self.blocks_null_sink_2_1_0_10_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 12), (self.blocks_null_sink_2_1_0_1_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 11), (self.blocks_null_sink_2_1_0_2_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 10), (self.blocks_null_sink_2_1_0_3_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 9), (self.blocks_null_sink_2_1_0_4_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 8), (self.blocks_null_sink_2_1_0_5_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 7), (self.blocks_null_sink_2_1_0_6_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 6), (self.blocks_null_sink_2_1_0_7_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 4), (self.blocks_null_sink_2_1_0_8_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 5), (self.blocks_null_sink_2_1_0_9_0_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 2), (self.blocks_null_sink_2_1_1_0_0_0, 0))
        self.connect((self.verisure2GFSKRadioChannelToDataMessage_0_3, 0), (self.blocks_null_sink_2_2_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 1), (self.blocks_null_sink_2_0_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 13), (self.blocks_null_sink_2_1_0_0_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 3), (self.blocks_null_sink_2_1_0_10_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 12), (self.blocks_null_sink_2_1_0_1_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 2), (self.blocks_null_sink_2_1_0_1_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 14), (self.blocks_null_sink_2_1_0_1_0_1_0_1, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 11), (self.blocks_null_sink_2_1_0_2_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 10), (self.blocks_null_sink_2_1_0_3_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 9), (self.blocks_null_sink_2_1_0_4_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 8), (self.blocks_null_sink_2_1_0_5_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 7), (self.blocks_null_sink_2_1_0_6_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 6), (self.blocks_null_sink_2_1_0_7_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 4), (self.blocks_null_sink_2_1_0_8_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 5), (self.blocks_null_sink_2_1_0_9_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0, 0), (self.blocks_null_sink_2_2_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 1), (self.blocks_null_sink_2_0_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 13), (self.blocks_null_sink_2_1_0_0_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 3), (self.blocks_null_sink_2_1_0_10_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 2), (self.blocks_null_sink_2_1_0_1_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 14), (self.blocks_null_sink_2_1_0_1_0_1_0_1_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 12), (self.blocks_null_sink_2_1_0_1_0_1_0_2, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 11), (self.blocks_null_sink_2_1_0_2_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 10), (self.blocks_null_sink_2_1_0_3_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 9), (self.blocks_null_sink_2_1_0_4_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 8), (self.blocks_null_sink_2_1_0_5_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 7), (self.blocks_null_sink_2_1_0_6_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 6), (self.blocks_null_sink_2_1_0_7_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 4), (self.blocks_null_sink_2_1_0_8_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 5), (self.blocks_null_sink_2_1_0_9_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0, 0), (self.blocks_null_sink_2_2_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 1), (self.blocks_null_sink_2_0_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 13), (self.blocks_null_sink_2_1_0_0_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 3), (self.blocks_null_sink_2_1_0_10_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 2), (self.blocks_null_sink_2_1_0_1_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 14), (self.blocks_null_sink_2_1_0_1_0_1_0_1_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 12), (self.blocks_null_sink_2_1_0_1_0_1_0_2_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 11), (self.blocks_null_sink_2_1_0_2_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 10), (self.blocks_null_sink_2_1_0_3_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 9), (self.blocks_null_sink_2_1_0_4_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 8), (self.blocks_null_sink_2_1_0_5_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 7), (self.blocks_null_sink_2_1_0_6_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 6), (self.blocks_null_sink_2_1_0_7_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 4), (self.blocks_null_sink_2_1_0_8_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 5), (self.blocks_null_sink_2_1_0_9_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0, 0), (self.blocks_null_sink_2_2_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 1), (self.blocks_null_sink_2_0_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 13), (self.blocks_null_sink_2_1_0_0_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 3), (self.blocks_null_sink_2_1_0_10_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 2), (self.blocks_null_sink_2_1_0_1_0_1_0_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 14), (self.blocks_null_sink_2_1_0_1_0_1_0_1_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 12), (self.blocks_null_sink_2_1_0_1_0_1_0_2_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 11), (self.blocks_null_sink_2_1_0_2_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 10), (self.blocks_null_sink_2_1_0_3_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 9), (self.blocks_null_sink_2_1_0_4_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 8), (self.blocks_null_sink_2_1_0_5_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 7), (self.blocks_null_sink_2_1_0_6_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 6), (self.blocks_null_sink_2_1_0_7_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 4), (self.blocks_null_sink_2_1_0_8_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 5), (self.blocks_null_sink_2_1_0_9_0_1_0_0_0_0, 0))
        self.connect((self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0, 0), (self.blocks_null_sink_2_2_1_0_0_0_0, 0))


    def get_configFile(self):
        return self.configFile

    def set_configFile(self, configFile):
        self.configFile = configFile
        self._antialiass_filter_bw_config = configparser.ConfigParser()
        self._antialiass_filter_bw_config.read(self.configFile)
        if not self._antialiass_filter_bw_config.has_section('HW_SOURCE_CONFIG'):
        	self._antialiass_filter_bw_config.add_section('HW_SOURCE_CONFIG')
        self._antialiass_filter_bw_config.set('HW_SOURCE_CONFIG', 'antialiasing_filter_bandwidth', str(None))
        self._antialiass_filter_bw_config.write(open(self.configFile, 'w'))
        self._bitrate_s_config = configparser.ConfigParser()
        self._bitrate_s_config.read(self.configFile)
        if not self._bitrate_s_config.has_section('2GFSK_CHANNELS'):
        	self._bitrate_s_config.add_section('2GFSK_CHANNELS')
        self._bitrate_s_config.set('2GFSK_CHANNELS', 'baseband_bitrate', str(None))
        self._bitrate_s_config.write(open(self.configFile, 'w'))
        self._ch100Bitrate_h_config = configparser.ConfigParser()
        self._ch100Bitrate_h_config.read(self.configFile)
        if not self._ch100Bitrate_h_config.has_section('4GFSK_CHANNELS'):
        	self._ch100Bitrate_h_config.add_section('4GFSK_CHANNELS')
        self._ch100Bitrate_h_config.set('4GFSK_CHANNELS', 'baseband_bitrate_ch100', str(None))
        self._ch100Bitrate_h_config.write(open(self.configFile, 'w'))
        self._ch100enable_config = configparser.ConfigParser()
        self._ch100enable_config.read(self.configFile)
        if not self._ch100enable_config.has_section('4GFSK_CHANNELS'):
        	self._ch100enable_config.add_section('4GFSK_CHANNELS')
        self._ch100enable_config.set('4GFSK_CHANNELS', 'ch_100_enable', str(None))
        self._ch100enable_config.write(open(self.configFile, 'w'))
        self._ch100freq_h_config = configparser.ConfigParser()
        self._ch100freq_h_config.read(self.configFile)
        if not self._ch100freq_h_config.has_section('4GFSK_CHANNELS'):
        	self._ch100freq_h_config.add_section('4GFSK_CHANNELS')
        self._ch100freq_h_config.set('4GFSK_CHANNELS', 'ch100_center_freq', str(None))
        self._ch100freq_h_config.write(open(self.configFile, 'w'))
        self._ch1_number_s_config = configparser.ConfigParser()
        self._ch1_number_s_config.read(self.configFile)
        if not self._ch1_number_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch1_number_s_config.add_section('2GFSK_CHANNELS')
        self._ch1_number_s_config.set('2GFSK_CHANNELS', 'ch1_override_ch_number', str(None))
        self._ch1_number_s_config.write(open(self.configFile, 'w'))
        self._ch1enable_config = configparser.ConfigParser()
        self._ch1enable_config.read(self.configFile)
        if not self._ch1enable_config.has_section('2GFSK_CHANNELS'):
        	self._ch1enable_config.add_section('2GFSK_CHANNELS')
        self._ch1enable_config.set('2GFSK_CHANNELS', 'ch_1_enable', str(None))
        self._ch1enable_config.write(open(self.configFile, 'w'))
        self._ch1freq_s_config = configparser.ConfigParser()
        self._ch1freq_s_config.read(self.configFile)
        if not self._ch1freq_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch1freq_s_config.add_section('2GFSK_CHANNELS')
        self._ch1freq_s_config.set('2GFSK_CHANNELS', 'ch_1_center_freq', str(None))
        self._ch1freq_s_config.write(open(self.configFile, 'w'))
        self._ch200Bitrate_h_config = configparser.ConfigParser()
        self._ch200Bitrate_h_config.read(self.configFile)
        if not self._ch200Bitrate_h_config.has_section('4GFSK_CHANNELS'):
        	self._ch200Bitrate_h_config.add_section('4GFSK_CHANNELS')
        self._ch200Bitrate_h_config.set('4GFSK_CHANNELS', 'baseband_bitrate_ch200', str(None))
        self._ch200Bitrate_h_config.write(open(self.configFile, 'w'))
        self._ch200enable_config = configparser.ConfigParser()
        self._ch200enable_config.read(self.configFile)
        if not self._ch200enable_config.has_section('4GFSK_CHANNELS'):
        	self._ch200enable_config.add_section('4GFSK_CHANNELS')
        self._ch200enable_config.set('4GFSK_CHANNELS', 'ch_200_enable', str(None))
        self._ch200enable_config.write(open(self.configFile, 'w'))
        self._ch200freq_h_config = configparser.ConfigParser()
        self._ch200freq_h_config.read(self.configFile)
        if not self._ch200freq_h_config.has_section('4GFSK_CHANNELS'):
        	self._ch200freq_h_config.add_section('4GFSK_CHANNELS')
        self._ch200freq_h_config.set('4GFSK_CHANNELS', 'ch200_center_freq', str(None))
        self._ch200freq_h_config.write(open(self.configFile, 'w'))
        self._ch2_number_s_config = configparser.ConfigParser()
        self._ch2_number_s_config.read(self.configFile)
        if not self._ch2_number_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch2_number_s_config.add_section('2GFSK_CHANNELS')
        self._ch2_number_s_config.set('2GFSK_CHANNELS', 'ch2_override_ch_number', str(None))
        self._ch2_number_s_config.write(open(self.configFile, 'w'))
        self._ch2enable_config = configparser.ConfigParser()
        self._ch2enable_config.read(self.configFile)
        if not self._ch2enable_config.has_section('2GFSK_CHANNELS'):
        	self._ch2enable_config.add_section('2GFSK_CHANNELS')
        self._ch2enable_config.set('2GFSK_CHANNELS', 'ch_2_enable', str(None))
        self._ch2enable_config.write(open(self.configFile, 'w'))
        self._ch2freq_s_config = configparser.ConfigParser()
        self._ch2freq_s_config.read(self.configFile)
        if not self._ch2freq_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch2freq_s_config.add_section('2GFSK_CHANNELS')
        self._ch2freq_s_config.set('2GFSK_CHANNELS', 'ch_2_center_freq', str(None))
        self._ch2freq_s_config.write(open(self.configFile, 'w'))
        self._ch3_number_s_config = configparser.ConfigParser()
        self._ch3_number_s_config.read(self.configFile)
        if not self._ch3_number_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch3_number_s_config.add_section('2GFSK_CHANNELS')
        self._ch3_number_s_config.set('2GFSK_CHANNELS', 'ch3_override_ch_number', str(None))
        self._ch3_number_s_config.write(open(self.configFile, 'w'))
        self._ch3enable_config = configparser.ConfigParser()
        self._ch3enable_config.read(self.configFile)
        if not self._ch3enable_config.has_section('2GFSK_CHANNELS'):
        	self._ch3enable_config.add_section('2GFSK_CHANNELS')
        self._ch3enable_config.set('2GFSK_CHANNELS', 'ch_3_enable', str(None))
        self._ch3enable_config.write(open(self.configFile, 'w'))
        self._ch3freq_s_config = configparser.ConfigParser()
        self._ch3freq_s_config.read(self.configFile)
        if not self._ch3freq_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch3freq_s_config.add_section('2GFSK_CHANNELS')
        self._ch3freq_s_config.set('2GFSK_CHANNELS', 'ch_3_center_freq', str(None))
        self._ch3freq_s_config.write(open(self.configFile, 'w'))
        self._ch4_number_s_config = configparser.ConfigParser()
        self._ch4_number_s_config.read(self.configFile)
        if not self._ch4_number_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch4_number_s_config.add_section('2GFSK_CHANNELS')
        self._ch4_number_s_config.set('2GFSK_CHANNELS', 'ch4_override_ch_number', str(None))
        self._ch4_number_s_config.write(open(self.configFile, 'w'))
        self._ch4enable_config = configparser.ConfigParser()
        self._ch4enable_config.read(self.configFile)
        if not self._ch4enable_config.has_section('2GFSK_CHANNELS'):
        	self._ch4enable_config.add_section('2GFSK_CHANNELS')
        self._ch4enable_config.set('2GFSK_CHANNELS', 'ch_4_enable', str(None))
        self._ch4enable_config.write(open(self.configFile, 'w'))
        self._ch4freq_s_config = configparser.ConfigParser()
        self._ch4freq_s_config.read(self.configFile)
        if not self._ch4freq_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch4freq_s_config.add_section('2GFSK_CHANNELS')
        self._ch4freq_s_config.set('2GFSK_CHANNELS', 'ch_4_center_freq', str(None))
        self._ch4freq_s_config.write(open(self.configFile, 'w'))
        self._ch5_number_s_config = configparser.ConfigParser()
        self._ch5_number_s_config.read(self.configFile)
        if not self._ch5_number_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch5_number_s_config.add_section('2GFSK_CHANNELS')
        self._ch5_number_s_config.set('2GFSK_CHANNELS', 'ch5_override_ch_number', str(None))
        self._ch5_number_s_config.write(open(self.configFile, 'w'))
        self._ch5enable_config = configparser.ConfigParser()
        self._ch5enable_config.read(self.configFile)
        if not self._ch5enable_config.has_section('2GFSK_CHANNELS'):
        	self._ch5enable_config.add_section('2GFSK_CHANNELS')
        self._ch5enable_config.set('2GFSK_CHANNELS', 'ch_5_enable', str(None))
        self._ch5enable_config.write(open(self.configFile, 'w'))
        self._ch5freq_s_config = configparser.ConfigParser()
        self._ch5freq_s_config.read(self.configFile)
        if not self._ch5freq_s_config.has_section('2GFSK_CHANNELS'):
        	self._ch5freq_s_config.add_section('2GFSK_CHANNELS')
        self._ch5freq_s_config.set('2GFSK_CHANNELS', 'ch_5_center_freq', str(None))
        self._ch5freq_s_config.write(open(self.configFile, 'w'))
        self._ch600Bitrate_h_config = configparser.ConfigParser()
        self._ch600Bitrate_h_config.read(self.configFile)
        if not self._ch600Bitrate_h_config.has_section('4GFSK_CHANNELS'):
        	self._ch600Bitrate_h_config.add_section('4GFSK_CHANNELS')
        self._ch600Bitrate_h_config.set('4GFSK_CHANNELS', 'baseband_bitrate_ch600', str(None))
        self._ch600Bitrate_h_config.write(open(self.configFile, 'w'))
        self._ch600enable_config = configparser.ConfigParser()
        self._ch600enable_config.read(self.configFile)
        if not self._ch600enable_config.has_section('4GFSK_CHANNELS'):
        	self._ch600enable_config.add_section('4GFSK_CHANNELS')
        self._ch600enable_config.set('4GFSK_CHANNELS', 'ch_600_enable', str(None))
        self._ch600enable_config.write(open(self.configFile, 'w'))
        self._ch600freq_h_config = configparser.ConfigParser()
        self._ch600freq_h_config.read(self.configFile)
        if not self._ch600freq_h_config.has_section('4GFSK_CHANNELS'):
        	self._ch600freq_h_config.add_section('4GFSK_CHANNELS')
        self._ch600freq_h_config.set('4GFSK_CHANNELS', 'ch600_center_freq', str(None))
        self._ch600freq_h_config.write(open(self.configFile, 'w'))
        self._ch800Bitrate_h_config = configparser.ConfigParser()
        self._ch800Bitrate_h_config.read(self.configFile)
        if not self._ch800Bitrate_h_config.has_section('4GFSK_CHANNELS'):
        	self._ch800Bitrate_h_config.add_section('4GFSK_CHANNELS')
        self._ch800Bitrate_h_config.set('4GFSK_CHANNELS', 'baseband_bitrate_ch800', str(None))
        self._ch800Bitrate_h_config.write(open(self.configFile, 'w'))
        self._ch800enable_config = configparser.ConfigParser()
        self._ch800enable_config.read(self.configFile)
        if not self._ch800enable_config.has_section('4GFSK_CHANNELS'):
        	self._ch800enable_config.add_section('4GFSK_CHANNELS')
        self._ch800enable_config.set('4GFSK_CHANNELS', 'ch_800_enable', str(None))
        self._ch800enable_config.write(open(self.configFile, 'w'))
        self._ch800freq_h_config = configparser.ConfigParser()
        self._ch800freq_h_config.read(self.configFile)
        if not self._ch800freq_h_config.has_section('4GFSK_CHANNELS'):
        	self._ch800freq_h_config.add_section('4GFSK_CHANNELS')
        self._ch800freq_h_config.set('4GFSK_CHANNELS', 'ch800_center_freq', str(None))
        self._ch800freq_h_config.write(open(self.configFile, 'w'))
        self._demod_dc_block_time_100_h_config = configparser.ConfigParser()
        self._demod_dc_block_time_100_h_config.read(self.configFile)
        if not self._demod_dc_block_time_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._demod_dc_block_time_100_h_config.add_section('4GFSK_CHANNELS')
        self._demod_dc_block_time_100_h_config.set('4GFSK_CHANNELS', 'dc_blocking_time_ch100', str(None))
        self._demod_dc_block_time_100_h_config.write(open(self.configFile, 'w'))
        self._demod_dc_block_time_200_h_config = configparser.ConfigParser()
        self._demod_dc_block_time_200_h_config.read(self.configFile)
        if not self._demod_dc_block_time_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._demod_dc_block_time_200_h_config.add_section('4GFSK_CHANNELS')
        self._demod_dc_block_time_200_h_config.set('4GFSK_CHANNELS', 'dc_blocking_time_ch200', str(None))
        self._demod_dc_block_time_200_h_config.write(open(self.configFile, 'w'))
        self._demod_dc_block_time_600_h_config = configparser.ConfigParser()
        self._demod_dc_block_time_600_h_config.read(self.configFile)
        if not self._demod_dc_block_time_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._demod_dc_block_time_600_h_config.add_section('4GFSK_CHANNELS')
        self._demod_dc_block_time_600_h_config.set('4GFSK_CHANNELS', 'dc_blocking_time_ch600', str(None))
        self._demod_dc_block_time_600_h_config.write(open(self.configFile, 'w'))
        self._demod_dc_block_time_800_h_config = configparser.ConfigParser()
        self._demod_dc_block_time_800_h_config.read(self.configFile)
        if not self._demod_dc_block_time_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._demod_dc_block_time_800_h_config.add_section('4GFSK_CHANNELS')
        self._demod_dc_block_time_800_h_config.set('4GFSK_CHANNELS', 'dc_blocking_time_ch800', str(None))
        self._demod_dc_block_time_800_h_config.write(open(self.configFile, 'w'))
        self._demod_dc_block_time_s_config = configparser.ConfigParser()
        self._demod_dc_block_time_s_config.read(self.configFile)
        if not self._demod_dc_block_time_s_config.has_section('2GFSK_CHANNELS'):
        	self._demod_dc_block_time_s_config.add_section('2GFSK_CHANNELS')
        self._demod_dc_block_time_s_config.set('2GFSK_CHANNELS', 'dc_blocking_time', str(None))
        self._demod_dc_block_time_s_config.write(open(self.configFile, 'w'))
        self._fsk_deviation_100_h_config = configparser.ConfigParser()
        self._fsk_deviation_100_h_config.read(self.configFile)
        if not self._fsk_deviation_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._fsk_deviation_100_h_config.add_section('4GFSK_CHANNELS')
        self._fsk_deviation_100_h_config.set('4GFSK_CHANNELS', 'frequency_deviation_ch100', str(None))
        self._fsk_deviation_100_h_config.write(open(self.configFile, 'w'))
        self._fsk_deviation_200_h_config = configparser.ConfigParser()
        self._fsk_deviation_200_h_config.read(self.configFile)
        if not self._fsk_deviation_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._fsk_deviation_200_h_config.add_section('4GFSK_CHANNELS')
        self._fsk_deviation_200_h_config.set('4GFSK_CHANNELS', 'frequency_deviation_ch200', str(None))
        self._fsk_deviation_200_h_config.write(open(self.configFile, 'w'))
        self._fsk_deviation_600_h_config = configparser.ConfigParser()
        self._fsk_deviation_600_h_config.read(self.configFile)
        if not self._fsk_deviation_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._fsk_deviation_600_h_config.add_section('4GFSK_CHANNELS')
        self._fsk_deviation_600_h_config.set('4GFSK_CHANNELS', 'frequency_deviation_ch600', str(None))
        self._fsk_deviation_600_h_config.write(open(self.configFile, 'w'))
        self._fsk_deviation_800_h_config = configparser.ConfigParser()
        self._fsk_deviation_800_h_config.read(self.configFile)
        if not self._fsk_deviation_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._fsk_deviation_800_h_config.add_section('4GFSK_CHANNELS')
        self._fsk_deviation_800_h_config.set('4GFSK_CHANNELS', 'frequency_deviation_ch800', str(None))
        self._fsk_deviation_800_h_config.write(open(self.configFile, 'w'))
        self._fsk_deviation_s_config = configparser.ConfigParser()
        self._fsk_deviation_s_config.read(self.configFile)
        if not self._fsk_deviation_s_config.has_section('2GFSK_CHANNELS'):
        	self._fsk_deviation_s_config.add_section('2GFSK_CHANNELS')
        self._fsk_deviation_s_config.set('2GFSK_CHANNELS', 'frequency_deviation', str(None))
        self._fsk_deviation_s_config.write(open(self.configFile, 'w'))
        self._if_gain_config = configparser.ConfigParser()
        self._if_gain_config.read(self.configFile)
        if not self._if_gain_config.has_section('HW_SOURCE_CONFIG'):
        	self._if_gain_config.add_section('HW_SOURCE_CONFIG')
        self._if_gain_config.set('HW_SOURCE_CONFIG', 'intermediate_frequency_amplifier_gain', str(None))
        self._if_gain_config.write(open(self.configFile, 'w'))
        self._lna_on_config = configparser.ConfigParser()
        self._lna_on_config.read(self.configFile)
        if not self._lna_on_config.has_section('HW_SOURCE_CONFIG'):
        	self._lna_on_config.add_section('HW_SOURCE_CONFIG')
        self._lna_on_config.set('HW_SOURCE_CONFIG', 'enable_rf_low_noise_amplifier', str(None))
        self._lna_on_config.write(open(self.configFile, 'w'))
        self._lo_osc_freq_config = configparser.ConfigParser()
        self._lo_osc_freq_config.read(self.configFile)
        if not self._lo_osc_freq_config.has_section('HW_SOURCE_CONFIG'):
        	self._lo_osc_freq_config.add_section('HW_SOURCE_CONFIG')
        self._lo_osc_freq_config.set('HW_SOURCE_CONFIG', 'local_oscillator_frequency', str(None))
        self._lo_osc_freq_config.write(open(self.configFile, 'w'))
        self._lo_osc_freq_error_correction_config = configparser.ConfigParser()
        self._lo_osc_freq_error_correction_config.read(self.configFile)
        if not self._lo_osc_freq_error_correction_config.has_section('HW_SOURCE_CONFIG'):
        	self._lo_osc_freq_error_correction_config.add_section('HW_SOURCE_CONFIG')
        self._lo_osc_freq_error_correction_config.set('HW_SOURCE_CONFIG', 'local_oscillator_frequency_correction', str(None))
        self._lo_osc_freq_error_correction_config.write(open(self.configFile, 'w'))
        self._loop_bw_100_h_config = configparser.ConfigParser()
        self._loop_bw_100_h_config.read(self.configFile)
        if not self._loop_bw_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._loop_bw_100_h_config.add_section('4GFSK_CHANNELS')
        self._loop_bw_100_h_config.set('4GFSK_CHANNELS', 'symbol_sync_loop_bandwidth_ch100', str(None))
        self._loop_bw_100_h_config.write(open(self.configFile, 'w'))
        self._loop_bw_200_h_config = configparser.ConfigParser()
        self._loop_bw_200_h_config.read(self.configFile)
        if not self._loop_bw_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._loop_bw_200_h_config.add_section('4GFSK_CHANNELS')
        self._loop_bw_200_h_config.set('4GFSK_CHANNELS', 'symbol_sync_loop_bandwidth_ch200', str(None))
        self._loop_bw_200_h_config.write(open(self.configFile, 'w'))
        self._loop_bw_600_h_config = configparser.ConfigParser()
        self._loop_bw_600_h_config.read(self.configFile)
        if not self._loop_bw_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._loop_bw_600_h_config.add_section('4GFSK_CHANNELS')
        self._loop_bw_600_h_config.set('4GFSK_CHANNELS', 'symbol_sync_loop_bandwidth_ch600', str(None))
        self._loop_bw_600_h_config.write(open(self.configFile, 'w'))
        self._loop_bw_800_h_config = configparser.ConfigParser()
        self._loop_bw_800_h_config.read(self.configFile)
        if not self._loop_bw_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._loop_bw_800_h_config.add_section('4GFSK_CHANNELS')
        self._loop_bw_800_h_config.set('4GFSK_CHANNELS', 'symbol_sync_loop_bandwidth_ch800', str(None))
        self._loop_bw_800_h_config.write(open(self.configFile, 'w'))
        self._loop_bw_s_config = configparser.ConfigParser()
        self._loop_bw_s_config.read(self.configFile)
        if not self._loop_bw_s_config.has_section('2GFSK_CHANNELS'):
        	self._loop_bw_s_config.add_section('2GFSK_CHANNELS')
        self._loop_bw_s_config.set('2GFSK_CHANNELS', 'symbol_sync_loop_bandwidth', str(None))
        self._loop_bw_s_config.write(open(self.configFile, 'w'))
        self._loop_damping_100_h_config = configparser.ConfigParser()
        self._loop_damping_100_h_config.read(self.configFile)
        if not self._loop_damping_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._loop_damping_100_h_config.add_section('4GFSK_CHANNELS')
        self._loop_damping_100_h_config.set('4GFSK_CHANNELS', 'symbol_sync_loop_damping_ch100', str(None))
        self._loop_damping_100_h_config.write(open(self.configFile, 'w'))
        self._loop_damping_200_h_config = configparser.ConfigParser()
        self._loop_damping_200_h_config.read(self.configFile)
        if not self._loop_damping_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._loop_damping_200_h_config.add_section('4GFSK_CHANNELS')
        self._loop_damping_200_h_config.set('4GFSK_CHANNELS', 'symbol_sync_loop_damping_ch200', str(None))
        self._loop_damping_200_h_config.write(open(self.configFile, 'w'))
        self._loop_damping_600_h_config = configparser.ConfigParser()
        self._loop_damping_600_h_config.read(self.configFile)
        if not self._loop_damping_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._loop_damping_600_h_config.add_section('4GFSK_CHANNELS')
        self._loop_damping_600_h_config.set('4GFSK_CHANNELS', 'symbol_sync_loop_damping_ch600', str(None))
        self._loop_damping_600_h_config.write(open(self.configFile, 'w'))
        self._loop_damping_800_h_config = configparser.ConfigParser()
        self._loop_damping_800_h_config.read(self.configFile)
        if not self._loop_damping_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._loop_damping_800_h_config.add_section('4GFSK_CHANNELS')
        self._loop_damping_800_h_config.set('4GFSK_CHANNELS', 'symbol_sync_loop_damping_ch800', str(None))
        self._loop_damping_800_h_config.write(open(self.configFile, 'w'))
        self._loop_damping_s_config = configparser.ConfigParser()
        self._loop_damping_s_config.read(self.configFile)
        if not self._loop_damping_s_config.has_section('2GFSK_CHANNELS'):
        	self._loop_damping_s_config.add_section('2GFSK_CHANNELS')
        self._loop_damping_s_config.set('2GFSK_CHANNELS', 'symbol_sync_loop_damping', str(None))
        self._loop_damping_s_config.write(open(self.configFile, 'w'))
        self._passband_end_100_h_config = configparser.ConfigParser()
        self._passband_end_100_h_config.read(self.configFile)
        if not self._passband_end_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._passband_end_100_h_config.add_section('4GFSK_CHANNELS')
        self._passband_end_100_h_config.set('4GFSK_CHANNELS', 'ch100_passband_end_frequency', str(None))
        self._passband_end_100_h_config.write(open(self.configFile, 'w'))
        self._passband_end_200_h_config = configparser.ConfigParser()
        self._passband_end_200_h_config.read(self.configFile)
        if not self._passband_end_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._passband_end_200_h_config.add_section('4GFSK_CHANNELS')
        self._passband_end_200_h_config.set('4GFSK_CHANNELS', 'ch200_passband_end_frequency', str(None))
        self._passband_end_200_h_config.write(open(self.configFile, 'w'))
        self._passband_end_600_h_config = configparser.ConfigParser()
        self._passband_end_600_h_config.read(self.configFile)
        if not self._passband_end_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._passband_end_600_h_config.add_section('4GFSK_CHANNELS')
        self._passband_end_600_h_config.set('4GFSK_CHANNELS', 'ch600_passband_end_frequency', str(None))
        self._passband_end_600_h_config.write(open(self.configFile, 'w'))
        self._passband_end_800_h_config = configparser.ConfigParser()
        self._passband_end_800_h_config.read(self.configFile)
        if not self._passband_end_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._passband_end_800_h_config.add_section('4GFSK_CHANNELS')
        self._passband_end_800_h_config.set('4GFSK_CHANNELS', 'ch800_passband_end_frequency', str(None))
        self._passband_end_800_h_config.write(open(self.configFile, 'w'))
        self._passband_end_s_config = configparser.ConfigParser()
        self._passband_end_s_config.read(self.configFile)
        if not self._passband_end_s_config.has_section('2GFSK_CHANNELS'):
        	self._passband_end_s_config.add_section('2GFSK_CHANNELS')
        self._passband_end_s_config.set('2GFSK_CHANNELS', 'channel_passband_end_frequency', str(None))
        self._passband_end_s_config.write(open(self.configFile, 'w'))
        self._rssi_calib_offset_100_h_config = configparser.ConfigParser()
        self._rssi_calib_offset_100_h_config.read(self.configFile)
        if not self._rssi_calib_offset_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._rssi_calib_offset_100_h_config.add_section('4GFSK_CHANNELS')
        self._rssi_calib_offset_100_h_config.set('4GFSK_CHANNELS', 'rssi_offset_calibration_ch100', str(None))
        self._rssi_calib_offset_100_h_config.write(open(self.configFile, 'w'))
        self._rssi_calib_offset_200_h_config = configparser.ConfigParser()
        self._rssi_calib_offset_200_h_config.read(self.configFile)
        if not self._rssi_calib_offset_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._rssi_calib_offset_200_h_config.add_section('4GFSK_CHANNELS')
        self._rssi_calib_offset_200_h_config.set('4GFSK_CHANNELS', 'rssi_offset_calibration_ch200', str(None))
        self._rssi_calib_offset_200_h_config.write(open(self.configFile, 'w'))
        self._rssi_calib_offset_600_h_config = configparser.ConfigParser()
        self._rssi_calib_offset_600_h_config.read(self.configFile)
        if not self._rssi_calib_offset_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._rssi_calib_offset_600_h_config.add_section('4GFSK_CHANNELS')
        self._rssi_calib_offset_600_h_config.set('4GFSK_CHANNELS', 'rssi_offset_calibration_ch600', str(None))
        self._rssi_calib_offset_600_h_config.write(open(self.configFile, 'w'))
        self._rssi_calib_offset_800_h_config = configparser.ConfigParser()
        self._rssi_calib_offset_800_h_config.read(self.configFile)
        if not self._rssi_calib_offset_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._rssi_calib_offset_800_h_config.add_section('4GFSK_CHANNELS')
        self._rssi_calib_offset_800_h_config.set('4GFSK_CHANNELS', 'rssi_offset_calibration_ch800', str(None))
        self._rssi_calib_offset_800_h_config.write(open(self.configFile, 'w'))
        self._rssi_calib_offset_s_config = configparser.ConfigParser()
        self._rssi_calib_offset_s_config.read(self.configFile)
        if not self._rssi_calib_offset_s_config.has_section('2GFSK_CHANNELS'):
        	self._rssi_calib_offset_s_config.add_section('2GFSK_CHANNELS')
        self._rssi_calib_offset_s_config.set('2GFSK_CHANNELS', 'rssi_offset_calibration', str(None))
        self._rssi_calib_offset_s_config.write(open(self.configFile, 'w'))
        self._samp_rate_config = configparser.ConfigParser()
        self._samp_rate_config.read(self.configFile)
        if not self._samp_rate_config.has_section('HW_SOURCE_CONFIG'):
        	self._samp_rate_config.add_section('HW_SOURCE_CONFIG')
        self._samp_rate_config.set('HW_SOURCE_CONFIG', 'sample_rate', str(None))
        self._samp_rate_config.write(open(self.configFile, 'w'))
        self._samp_rate_demod_100_h_config = configparser.ConfigParser()
        self._samp_rate_demod_100_h_config.read(self.configFile)
        if not self._samp_rate_demod_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._samp_rate_demod_100_h_config.add_section('4GFSK_CHANNELS')
        self._samp_rate_demod_100_h_config.set('4GFSK_CHANNELS', 'demodulation_sample_rate_ch100', str(None))
        self._samp_rate_demod_100_h_config.write(open(self.configFile, 'w'))
        self._samp_rate_demod_200_h_config = configparser.ConfigParser()
        self._samp_rate_demod_200_h_config.read(self.configFile)
        if not self._samp_rate_demod_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._samp_rate_demod_200_h_config.add_section('4GFSK_CHANNELS')
        self._samp_rate_demod_200_h_config.set('4GFSK_CHANNELS', 'demodulation_sample_rate_ch200', str(None))
        self._samp_rate_demod_200_h_config.write(open(self.configFile, 'w'))
        self._samp_rate_demod_600_h_config = configparser.ConfigParser()
        self._samp_rate_demod_600_h_config.read(self.configFile)
        if not self._samp_rate_demod_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._samp_rate_demod_600_h_config.add_section('4GFSK_CHANNELS')
        self._samp_rate_demod_600_h_config.set('4GFSK_CHANNELS', 'demodulation_sample_rate_ch600', str(None))
        self._samp_rate_demod_600_h_config.write(open(self.configFile, 'w'))
        self._samp_rate_demod_800_h_config = configparser.ConfigParser()
        self._samp_rate_demod_800_h_config.read(self.configFile)
        if not self._samp_rate_demod_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._samp_rate_demod_800_h_config.add_section('4GFSK_CHANNELS')
        self._samp_rate_demod_800_h_config.set('4GFSK_CHANNELS', 'demodulation_sample_rate_ch800', str(None))
        self._samp_rate_demod_800_h_config.write(open(self.configFile, 'w'))
        self._samp_rate_demod_s_config = configparser.ConfigParser()
        self._samp_rate_demod_s_config.read(self.configFile)
        if not self._samp_rate_demod_s_config.has_section('2GFSK_CHANNELS'):
        	self._samp_rate_demod_s_config.add_section('2GFSK_CHANNELS')
        self._samp_rate_demod_s_config.set('2GFSK_CHANNELS', 'demodulation_sample_rate', str(None))
        self._samp_rate_demod_s_config.write(open(self.configFile, 'w'))
        self._squelchAlpha_100_h_config = configparser.ConfigParser()
        self._squelchAlpha_100_h_config.read(self.configFile)
        if not self._squelchAlpha_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelchAlpha_100_h_config.add_section('4GFSK_CHANNELS')
        self._squelchAlpha_100_h_config.set('4GFSK_CHANNELS', 'squelch_alpha_ch100', str(None))
        self._squelchAlpha_100_h_config.write(open(self.configFile, 'w'))
        self._squelchAlpha_200_h_config = configparser.ConfigParser()
        self._squelchAlpha_200_h_config.read(self.configFile)
        if not self._squelchAlpha_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelchAlpha_200_h_config.add_section('4GFSK_CHANNELS')
        self._squelchAlpha_200_h_config.set('4GFSK_CHANNELS', 'squelch_alpha_ch200', str(None))
        self._squelchAlpha_200_h_config.write(open(self.configFile, 'w'))
        self._squelchAlpha_600_h_config = configparser.ConfigParser()
        self._squelchAlpha_600_h_config.read(self.configFile)
        if not self._squelchAlpha_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelchAlpha_600_h_config.add_section('4GFSK_CHANNELS')
        self._squelchAlpha_600_h_config.set('4GFSK_CHANNELS', 'squelch_alpha_ch600', str(None))
        self._squelchAlpha_600_h_config.write(open(self.configFile, 'w'))
        self._squelchAlpha_800_h_config = configparser.ConfigParser()
        self._squelchAlpha_800_h_config.read(self.configFile)
        if not self._squelchAlpha_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelchAlpha_800_h_config.add_section('4GFSK_CHANNELS')
        self._squelchAlpha_800_h_config.set('4GFSK_CHANNELS', 'squelch_alpha_ch800', str(None))
        self._squelchAlpha_800_h_config.write(open(self.configFile, 'w'))
        self._squelchAlpha_s_config = configparser.ConfigParser()
        self._squelchAlpha_s_config.read(self.configFile)
        if not self._squelchAlpha_s_config.has_section('2GFSK_CHANNELS'):
        	self._squelchAlpha_s_config.add_section('2GFSK_CHANNELS')
        self._squelchAlpha_s_config.set('2GFSK_CHANNELS', 'squelch_alpha', str(None))
        self._squelchAlpha_s_config.write(open(self.configFile, 'w'))
        self._squelch_level_100_h_config = configparser.ConfigParser()
        self._squelch_level_100_h_config.read(self.configFile)
        if not self._squelch_level_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelch_level_100_h_config.add_section('4GFSK_CHANNELS')
        self._squelch_level_100_h_config.set('4GFSK_CHANNELS', 'squelch_level_ch100', str(None))
        self._squelch_level_100_h_config.write(open(self.configFile, 'w'))
        self._squelch_level_200_h_config = configparser.ConfigParser()
        self._squelch_level_200_h_config.read(self.configFile)
        if not self._squelch_level_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelch_level_200_h_config.add_section('4GFSK_CHANNELS')
        self._squelch_level_200_h_config.set('4GFSK_CHANNELS', 'squelch_level_ch200', str(None))
        self._squelch_level_200_h_config.write(open(self.configFile, 'w'))
        self._squelch_level_600_h_config = configparser.ConfigParser()
        self._squelch_level_600_h_config.read(self.configFile)
        if not self._squelch_level_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelch_level_600_h_config.add_section('4GFSK_CHANNELS')
        self._squelch_level_600_h_config.set('4GFSK_CHANNELS', 'squelch_level_ch600', str(None))
        self._squelch_level_600_h_config.write(open(self.configFile, 'w'))
        self._squelch_level_800_h_config = configparser.ConfigParser()
        self._squelch_level_800_h_config.read(self.configFile)
        if not self._squelch_level_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelch_level_800_h_config.add_section('4GFSK_CHANNELS')
        self._squelch_level_800_h_config.set('4GFSK_CHANNELS', 'squelch_level_ch800', str(None))
        self._squelch_level_800_h_config.write(open(self.configFile, 'w'))
        self._squelch_level_s_config = configparser.ConfigParser()
        self._squelch_level_s_config.read(self.configFile)
        if not self._squelch_level_s_config.has_section('2GFSK_CHANNELS'):
        	self._squelch_level_s_config.add_section('2GFSK_CHANNELS')
        self._squelch_level_s_config.set('2GFSK_CHANNELS', 'squelch_level', str(None))
        self._squelch_level_s_config.write(open(self.configFile, 'w'))
        self._squelch_ramp_100_h_config = configparser.ConfigParser()
        self._squelch_ramp_100_h_config.read(self.configFile)
        if not self._squelch_ramp_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelch_ramp_100_h_config.add_section('4GFSK_CHANNELS')
        self._squelch_ramp_100_h_config.set('4GFSK_CHANNELS', 'squelch_ramp_ch100', str(None))
        self._squelch_ramp_100_h_config.write(open(self.configFile, 'w'))
        self._squelch_ramp_200_h_config = configparser.ConfigParser()
        self._squelch_ramp_200_h_config.read(self.configFile)
        if not self._squelch_ramp_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelch_ramp_200_h_config.add_section('4GFSK_CHANNELS')
        self._squelch_ramp_200_h_config.set('4GFSK_CHANNELS', 'squelch_ramp_ch200', str(None))
        self._squelch_ramp_200_h_config.write(open(self.configFile, 'w'))
        self._squelch_ramp_600_h_config = configparser.ConfigParser()
        self._squelch_ramp_600_h_config.read(self.configFile)
        if not self._squelch_ramp_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelch_ramp_600_h_config.add_section('4GFSK_CHANNELS')
        self._squelch_ramp_600_h_config.set('4GFSK_CHANNELS', 'squelch_ramp_ch600', str(None))
        self._squelch_ramp_600_h_config.write(open(self.configFile, 'w'))
        self._squelch_ramp_800_h_config = configparser.ConfigParser()
        self._squelch_ramp_800_h_config.read(self.configFile)
        if not self._squelch_ramp_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._squelch_ramp_800_h_config.add_section('4GFSK_CHANNELS')
        self._squelch_ramp_800_h_config.set('4GFSK_CHANNELS', 'squelch_ramp_ch800', str(None))
        self._squelch_ramp_800_h_config.write(open(self.configFile, 'w'))
        self._squelch_ramp_s_config = configparser.ConfigParser()
        self._squelch_ramp_s_config.read(self.configFile)
        if not self._squelch_ramp_s_config.has_section('2GFSK_CHANNELS'):
        	self._squelch_ramp_s_config.add_section('2GFSK_CHANNELS')
        self._squelch_ramp_s_config.set('2GFSK_CHANNELS', 'squelch_ramp', str(None))
        self._squelch_ramp_s_config.write(open(self.configFile, 'w'))
        self._stop_band_attenuation_dB_100_h_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_100_h_config.read(self.configFile)
        if not self._stop_band_attenuation_dB_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._stop_band_attenuation_dB_100_h_config.add_section('4GFSK_CHANNELS')
        self._stop_band_attenuation_dB_100_h_config.set('4GFSK_CHANNELS', 'ch100_stopband_attenuation', str(None))
        self._stop_band_attenuation_dB_100_h_config.write(open(self.configFile, 'w'))
        self._stop_band_attenuation_dB_200_h_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_200_h_config.read(self.configFile)
        if not self._stop_band_attenuation_dB_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._stop_band_attenuation_dB_200_h_config.add_section('4GFSK_CHANNELS')
        self._stop_band_attenuation_dB_200_h_config.set('4GFSK_CHANNELS', 'ch200_stopband_attenuation', str(None))
        self._stop_band_attenuation_dB_200_h_config.write(open(self.configFile, 'w'))
        self._stop_band_attenuation_dB_600_h_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_600_h_config.read(self.configFile)
        if not self._stop_band_attenuation_dB_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._stop_band_attenuation_dB_600_h_config.add_section('4GFSK_CHANNELS')
        self._stop_band_attenuation_dB_600_h_config.set('4GFSK_CHANNELS', 'ch600_stopband_attenuation', str(None))
        self._stop_band_attenuation_dB_600_h_config.write(open(self.configFile, 'w'))
        self._stop_band_attenuation_dB_800_h_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_800_h_config.read(self.configFile)
        if not self._stop_band_attenuation_dB_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._stop_band_attenuation_dB_800_h_config.add_section('4GFSK_CHANNELS')
        self._stop_band_attenuation_dB_800_h_config.set('4GFSK_CHANNELS', 'ch800_stopband_attenuation', str(None))
        self._stop_band_attenuation_dB_800_h_config.write(open(self.configFile, 'w'))
        self._stop_band_attenuation_dB_s_config = configparser.ConfigParser()
        self._stop_band_attenuation_dB_s_config.read(self.configFile)
        if not self._stop_band_attenuation_dB_s_config.has_section('2GFSK_CHANNELS'):
        	self._stop_band_attenuation_dB_s_config.add_section('2GFSK_CHANNELS')
        self._stop_band_attenuation_dB_s_config.set('2GFSK_CHANNELS', 'channel_stopband_attenuation', str(None))
        self._stop_band_attenuation_dB_s_config.write(open(self.configFile, 'w'))
        self._stopband_start_100_h_config = configparser.ConfigParser()
        self._stopband_start_100_h_config.read(self.configFile)
        if not self._stopband_start_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._stopband_start_100_h_config.add_section('4GFSK_CHANNELS')
        self._stopband_start_100_h_config.set('4GFSK_CHANNELS', 'ch100_stopband_start_frequency', str(None))
        self._stopband_start_100_h_config.write(open(self.configFile, 'w'))
        self._stopband_start_200_h_config = configparser.ConfigParser()
        self._stopband_start_200_h_config.read(self.configFile)
        if not self._stopband_start_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._stopband_start_200_h_config.add_section('4GFSK_CHANNELS')
        self._stopband_start_200_h_config.set('4GFSK_CHANNELS', 'ch200_stopband_start_frequency', str(None))
        self._stopband_start_200_h_config.write(open(self.configFile, 'w'))
        self._stopband_start_600_h_config = configparser.ConfigParser()
        self._stopband_start_600_h_config.read(self.configFile)
        if not self._stopband_start_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._stopband_start_600_h_config.add_section('4GFSK_CHANNELS')
        self._stopband_start_600_h_config.set('4GFSK_CHANNELS', 'ch600_stopband_start_frequency', str(None))
        self._stopband_start_600_h_config.write(open(self.configFile, 'w'))
        self._stopband_start_800_h_config = configparser.ConfigParser()
        self._stopband_start_800_h_config.read(self.configFile)
        if not self._stopband_start_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._stopband_start_800_h_config.add_section('4GFSK_CHANNELS')
        self._stopband_start_800_h_config.set('4GFSK_CHANNELS', 'ch800_stopband_start_frequency', str(None))
        self._stopband_start_800_h_config.write(open(self.configFile, 'w'))
        self._stopband_start_s_config = configparser.ConfigParser()
        self._stopband_start_s_config.read(self.configFile)
        if not self._stopband_start_s_config.has_section('2GFSK_CHANNELS'):
        	self._stopband_start_s_config.add_section('2GFSK_CHANNELS')
        self._stopband_start_s_config.set('2GFSK_CHANNELS', 'channel_stopband_start_frequency', str(None))
        self._stopband_start_s_config.write(open(self.configFile, 'w'))
        self._ted_gain_100_h_config = configparser.ConfigParser()
        self._ted_gain_100_h_config.read(self.configFile)
        if not self._ted_gain_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._ted_gain_100_h_config.add_section('4GFSK_CHANNELS')
        self._ted_gain_100_h_config.set('4GFSK_CHANNELS', 'timing_error_detector_gain_ch100', str(None))
        self._ted_gain_100_h_config.write(open(self.configFile, 'w'))
        self._ted_gain_200_h_config = configparser.ConfigParser()
        self._ted_gain_200_h_config.read(self.configFile)
        if not self._ted_gain_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._ted_gain_200_h_config.add_section('4GFSK_CHANNELS')
        self._ted_gain_200_h_config.set('4GFSK_CHANNELS', 'timing_error_detector_gain_ch200', str(None))
        self._ted_gain_200_h_config.write(open(self.configFile, 'w'))
        self._ted_gain_600_h_config = configparser.ConfigParser()
        self._ted_gain_600_h_config.read(self.configFile)
        if not self._ted_gain_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._ted_gain_600_h_config.add_section('4GFSK_CHANNELS')
        self._ted_gain_600_h_config.set('4GFSK_CHANNELS', 'timing_error_detector_gain_ch600', str(None))
        self._ted_gain_600_h_config.write(open(self.configFile, 'w'))
        self._ted_gain_800_h_config = configparser.ConfigParser()
        self._ted_gain_800_h_config.read(self.configFile)
        if not self._ted_gain_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._ted_gain_800_h_config.add_section('4GFSK_CHANNELS')
        self._ted_gain_800_h_config.set('4GFSK_CHANNELS', 'timing_error_detector_gain_ch800', str(None))
        self._ted_gain_800_h_config.write(open(self.configFile, 'w'))
        self._ted_gain_s_config = configparser.ConfigParser()
        self._ted_gain_s_config.read(self.configFile)
        if not self._ted_gain_s_config.has_section('2GFSK_CHANNELS'):
        	self._ted_gain_s_config.add_section('2GFSK_CHANNELS')
        self._ted_gain_s_config.set('2GFSK_CHANNELS', 'timing_error_detector_gain', str(None))
        self._ted_gain_s_config.write(open(self.configFile, 'w'))
        self._ted_max_deviation_100_h_config = configparser.ConfigParser()
        self._ted_max_deviation_100_h_config.read(self.configFile)
        if not self._ted_max_deviation_100_h_config.has_section('4GFSK_CHANNELS'):
        	self._ted_max_deviation_100_h_config.add_section('4GFSK_CHANNELS')
        self._ted_max_deviation_100_h_config.set('4GFSK_CHANNELS', 'timing_error_detector_max_deviation_ch100', str(None))
        self._ted_max_deviation_100_h_config.write(open(self.configFile, 'w'))
        self._ted_max_deviation_200_h_config = configparser.ConfigParser()
        self._ted_max_deviation_200_h_config.read(self.configFile)
        if not self._ted_max_deviation_200_h_config.has_section('4GFSK_CHANNELS'):
        	self._ted_max_deviation_200_h_config.add_section('4GFSK_CHANNELS')
        self._ted_max_deviation_200_h_config.set('4GFSK_CHANNELS', 'timing_error_detector_max_deviation_ch200', str(None))
        self._ted_max_deviation_200_h_config.write(open(self.configFile, 'w'))
        self._ted_max_deviation_600_h_config = configparser.ConfigParser()
        self._ted_max_deviation_600_h_config.read(self.configFile)
        if not self._ted_max_deviation_600_h_config.has_section('4GFSK_CHANNELS'):
        	self._ted_max_deviation_600_h_config.add_section('4GFSK_CHANNELS')
        self._ted_max_deviation_600_h_config.set('4GFSK_CHANNELS', 'timing_error_detector_max_deviation_ch600', str(None))
        self._ted_max_deviation_600_h_config.write(open(self.configFile, 'w'))
        self._ted_max_deviation_800_h_config = configparser.ConfigParser()
        self._ted_max_deviation_800_h_config.read(self.configFile)
        if not self._ted_max_deviation_800_h_config.has_section('4GFSK_CHANNELS'):
        	self._ted_max_deviation_800_h_config.add_section('4GFSK_CHANNELS')
        self._ted_max_deviation_800_h_config.set('4GFSK_CHANNELS', 'timing_error_detector_max_deviation_ch800', str(None))
        self._ted_max_deviation_800_h_config.write(open(self.configFile, 'w'))
        self._ted_max_deviation_s_config = configparser.ConfigParser()
        self._ted_max_deviation_s_config.read(self.configFile)
        if not self._ted_max_deviation_s_config.has_section('2GFSK_CHANNELS'):
        	self._ted_max_deviation_s_config.add_section('2GFSK_CHANNELS')
        self._ted_max_deviation_s_config.set('2GFSK_CHANNELS', 'timing_error_detector_max_deviation', str(None))
        self._ted_max_deviation_s_config.write(open(self.configFile, 'w'))
        self._vga_gain_config = configparser.ConfigParser()
        self._vga_gain_config.read(self.configFile)
        if not self._vga_gain_config.has_section('HW_SOURCE_CONFIG'):
        	self._vga_gain_config.add_section('HW_SOURCE_CONFIG')
        self._vga_gain_config.set('HW_SOURCE_CONFIG', 'pre_adc_amplifier_gain', str(None))
        self._vga_gain_config.write(open(self.configFile, 'w'))

    def get_vga_gain(self):
        return self.vga_gain

    def set_vga_gain(self, vga_gain):
        self.vga_gain = vga_gain
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(self.vga_gain, 0.0), 62.0))

    def get_ted_max_deviation_s(self):
        return self.ted_max_deviation_s

    def set_ted_max_deviation_s(self, ted_max_deviation_s):
        self.ted_max_deviation_s = ted_max_deviation_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_ted_max_deviation(self.ted_max_deviation_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_ted_max_deviation(self.ted_max_deviation_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_ted_max_deviation(self.ted_max_deviation_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_ted_max_deviation(self.ted_max_deviation_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_ted_max_deviation(self.ted_max_deviation_s)

    def get_ted_max_deviation_800_h(self):
        return self.ted_max_deviation_800_h

    def set_ted_max_deviation_800_h(self, ted_max_deviation_800_h):
        self.ted_max_deviation_800_h = ted_max_deviation_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_ted_max_deviation(self.ted_max_deviation_800_h)

    def get_ted_max_deviation_600_h(self):
        return self.ted_max_deviation_600_h

    def set_ted_max_deviation_600_h(self, ted_max_deviation_600_h):
        self.ted_max_deviation_600_h = ted_max_deviation_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_ted_max_deviation(self.ted_max_deviation_600_h)

    def get_ted_max_deviation_200_h(self):
        return self.ted_max_deviation_200_h

    def set_ted_max_deviation_200_h(self, ted_max_deviation_200_h):
        self.ted_max_deviation_200_h = ted_max_deviation_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_ted_max_deviation(self.ted_max_deviation_200_h)

    def get_ted_max_deviation_100_h(self):
        return self.ted_max_deviation_100_h

    def set_ted_max_deviation_100_h(self, ted_max_deviation_100_h):
        self.ted_max_deviation_100_h = ted_max_deviation_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_ted_max_deviation(self.ted_max_deviation_100_h)

    def get_ted_gain_s(self):
        return self.ted_gain_s

    def set_ted_gain_s(self, ted_gain_s):
        self.ted_gain_s = ted_gain_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_ted_gain(self.ted_gain_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_ted_gain(self.ted_gain_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_ted_gain(self.ted_gain_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_ted_gain(self.ted_gain_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_ted_gain(self.ted_gain_s)

    def get_ted_gain_800_h(self):
        return self.ted_gain_800_h

    def set_ted_gain_800_h(self, ted_gain_800_h):
        self.ted_gain_800_h = ted_gain_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_ted_gain(self.ted_gain_800_h)

    def get_ted_gain_600_h(self):
        return self.ted_gain_600_h

    def set_ted_gain_600_h(self, ted_gain_600_h):
        self.ted_gain_600_h = ted_gain_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_ted_gain(self.ted_gain_600_h)

    def get_ted_gain_200_h(self):
        return self.ted_gain_200_h

    def set_ted_gain_200_h(self, ted_gain_200_h):
        self.ted_gain_200_h = ted_gain_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_ted_gain(self.ted_gain_200_h)

    def get_ted_gain_100_h(self):
        return self.ted_gain_100_h

    def set_ted_gain_100_h(self, ted_gain_100_h):
        self.ted_gain_100_h = ted_gain_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_ted_gain(self.ted_gain_100_h)

    def get_tcp_host_port_number(self):
        return self.tcp_host_port_number

    def set_tcp_host_port_number(self, tcp_host_port_number):
        self.tcp_host_port_number = tcp_host_port_number

    def get_tcp_host_ipv4_address(self):
        return self.tcp_host_ipv4_address

    def set_tcp_host_ipv4_address(self, tcp_host_ipv4_address):
        self.tcp_host_ipv4_address = tcp_host_ipv4_address

    def get_stopband_start_s(self):
        return self.stopband_start_s

    def set_stopband_start_s(self, stopband_start_s):
        self.stopband_start_s = stopband_start_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_stopband_start(self.stopband_start_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_stopband_start(self.stopband_start_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_stopband_start(self.stopband_start_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_stopband_start(self.stopband_start_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_stopband_start(self.stopband_start_s)

    def get_stopband_start_800_h(self):
        return self.stopband_start_800_h

    def set_stopband_start_800_h(self, stopband_start_800_h):
        self.stopband_start_800_h = stopband_start_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_stopband_start(self.stopband_start_800_h)

    def get_stopband_start_600_h(self):
        return self.stopband_start_600_h

    def set_stopband_start_600_h(self, stopband_start_600_h):
        self.stopband_start_600_h = stopband_start_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_stopband_start(self.stopband_start_600_h)

    def get_stopband_start_200_h(self):
        return self.stopband_start_200_h

    def set_stopband_start_200_h(self, stopband_start_200_h):
        self.stopband_start_200_h = stopband_start_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_stopband_start(self.stopband_start_200_h)

    def get_stopband_start_100_h(self):
        return self.stopband_start_100_h

    def set_stopband_start_100_h(self, stopband_start_100_h):
        self.stopband_start_100_h = stopband_start_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_stopband_start(self.stopband_start_100_h)

    def get_stop_band_attenuation_dB_s(self):
        return self.stop_band_attenuation_dB_s

    def set_stop_band_attenuation_dB_s(self, stop_band_attenuation_dB_s):
        self.stop_band_attenuation_dB_s = stop_band_attenuation_dB_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_s)

    def get_stop_band_attenuation_dB_800_h(self):
        return self.stop_band_attenuation_dB_800_h

    def set_stop_band_attenuation_dB_800_h(self, stop_band_attenuation_dB_800_h):
        self.stop_band_attenuation_dB_800_h = stop_band_attenuation_dB_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_800_h)

    def get_stop_band_attenuation_dB_600_h(self):
        return self.stop_band_attenuation_dB_600_h

    def set_stop_band_attenuation_dB_600_h(self, stop_band_attenuation_dB_600_h):
        self.stop_band_attenuation_dB_600_h = stop_band_attenuation_dB_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_600_h)

    def get_stop_band_attenuation_dB_200_h(self):
        return self.stop_band_attenuation_dB_200_h

    def set_stop_band_attenuation_dB_200_h(self, stop_band_attenuation_dB_200_h):
        self.stop_band_attenuation_dB_200_h = stop_band_attenuation_dB_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_200_h)

    def get_stop_band_attenuation_dB_100_h(self):
        return self.stop_band_attenuation_dB_100_h

    def set_stop_band_attenuation_dB_100_h(self, stop_band_attenuation_dB_100_h):
        self.stop_band_attenuation_dB_100_h = stop_band_attenuation_dB_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_stop_band_attenuation_dB(self.stop_band_attenuation_dB_100_h)

    def get_squelch_ramp_s(self):
        return self.squelch_ramp_s

    def set_squelch_ramp_s(self, squelch_ramp_s):
        self.squelch_ramp_s = squelch_ramp_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_squelch_ramp(self.squelch_ramp_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_squelch_ramp(self.squelch_ramp_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_squelch_ramp(self.squelch_ramp_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_squelch_ramp(self.squelch_ramp_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_squelch_ramp(self.squelch_ramp_s)

    def get_squelch_ramp_800_h(self):
        return self.squelch_ramp_800_h

    def set_squelch_ramp_800_h(self, squelch_ramp_800_h):
        self.squelch_ramp_800_h = squelch_ramp_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_squelch_ramp(self.squelch_ramp_800_h)

    def get_squelch_ramp_600_h(self):
        return self.squelch_ramp_600_h

    def set_squelch_ramp_600_h(self, squelch_ramp_600_h):
        self.squelch_ramp_600_h = squelch_ramp_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_squelch_ramp(self.squelch_ramp_600_h)

    def get_squelch_ramp_200_h(self):
        return self.squelch_ramp_200_h

    def set_squelch_ramp_200_h(self, squelch_ramp_200_h):
        self.squelch_ramp_200_h = squelch_ramp_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_squelch_ramp(self.squelch_ramp_200_h)

    def get_squelch_ramp_100_h(self):
        return self.squelch_ramp_100_h

    def set_squelch_ramp_100_h(self, squelch_ramp_100_h):
        self.squelch_ramp_100_h = squelch_ramp_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_squelch_ramp(self.squelch_ramp_100_h)

    def get_squelch_level_s(self):
        return self.squelch_level_s

    def set_squelch_level_s(self, squelch_level_s):
        self.squelch_level_s = squelch_level_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_squelch_level(self.squelch_level_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_squelch_level(self.squelch_level_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_squelch_level(self.squelch_level_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_squelch_level(self.squelch_level_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_squelch_level(self.squelch_level_s)

    def get_squelch_level_800_h(self):
        return self.squelch_level_800_h

    def set_squelch_level_800_h(self, squelch_level_800_h):
        self.squelch_level_800_h = squelch_level_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_squelch_level(self.squelch_level_800_h)

    def get_squelch_level_600_h(self):
        return self.squelch_level_600_h

    def set_squelch_level_600_h(self, squelch_level_600_h):
        self.squelch_level_600_h = squelch_level_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_squelch_level(self.squelch_level_600_h)

    def get_squelch_level_200_h(self):
        return self.squelch_level_200_h

    def set_squelch_level_200_h(self, squelch_level_200_h):
        self.squelch_level_200_h = squelch_level_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_squelch_level(self.squelch_level_200_h)

    def get_squelch_level_100_h(self):
        return self.squelch_level_100_h

    def set_squelch_level_100_h(self, squelch_level_100_h):
        self.squelch_level_100_h = squelch_level_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_squelch_level(self.squelch_level_100_h)

    def get_squelchAlpha_s(self):
        return self.squelchAlpha_s

    def set_squelchAlpha_s(self, squelchAlpha_s):
        self.squelchAlpha_s = squelchAlpha_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_squelchAlpha(self.squelchAlpha_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_squelchAlpha(self.squelchAlpha_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_squelchAlpha(self.squelchAlpha_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_squelchAlpha(self.squelchAlpha_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_squelchAlpha(self.squelchAlpha_s)

    def get_squelchAlpha_800_h(self):
        return self.squelchAlpha_800_h

    def set_squelchAlpha_800_h(self, squelchAlpha_800_h):
        self.squelchAlpha_800_h = squelchAlpha_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_squelchAlpha(self.squelchAlpha_800_h)

    def get_squelchAlpha_600_h(self):
        return self.squelchAlpha_600_h

    def set_squelchAlpha_600_h(self, squelchAlpha_600_h):
        self.squelchAlpha_600_h = squelchAlpha_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_squelchAlpha(self.squelchAlpha_600_h)

    def get_squelchAlpha_200_h(self):
        return self.squelchAlpha_200_h

    def set_squelchAlpha_200_h(self, squelchAlpha_200_h):
        self.squelchAlpha_200_h = squelchAlpha_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_squelchAlpha(self.squelchAlpha_200_h)

    def get_squelchAlpha_100_h(self):
        return self.squelchAlpha_100_h

    def set_squelchAlpha_100_h(self, squelchAlpha_100_h):
        self.squelchAlpha_100_h = squelchAlpha_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_squelchAlpha(self.squelchAlpha_100_h)

    def get_samp_rate_demod_s(self):
        return self.samp_rate_demod_s

    def set_samp_rate_demod_s(self, samp_rate_demod_s):
        self.samp_rate_demod_s = samp_rate_demod_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_samp_rate_demod(self.samp_rate_demod_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_samp_rate_demod(self.samp_rate_demod_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_samp_rate_demod(self.samp_rate_demod_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_samp_rate_demod(self.samp_rate_demod_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_samp_rate_demod(self.samp_rate_demod_s)

    def get_samp_rate_demod_800_h(self):
        return self.samp_rate_demod_800_h

    def set_samp_rate_demod_800_h(self, samp_rate_demod_800_h):
        self.samp_rate_demod_800_h = samp_rate_demod_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_samp_rate_demod(self.samp_rate_demod_800_h)

    def get_samp_rate_demod_600_h(self):
        return self.samp_rate_demod_600_h

    def set_samp_rate_demod_600_h(self, samp_rate_demod_600_h):
        self.samp_rate_demod_600_h = samp_rate_demod_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_samp_rate_demod(self.samp_rate_demod_600_h)

    def get_samp_rate_demod_200_h(self):
        return self.samp_rate_demod_200_h

    def set_samp_rate_demod_200_h(self, samp_rate_demod_200_h):
        self.samp_rate_demod_200_h = samp_rate_demod_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_samp_rate_demod(self.samp_rate_demod_200_h)

    def get_samp_rate_demod_100_h(self):
        return self.samp_rate_demod_100_h

    def set_samp_rate_demod_100_h(self, samp_rate_demod_100_h):
        self.samp_rate_demod_100_h = samp_rate_demod_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_samp_rate_demod(self.samp_rate_demod_100_h)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.soapy_hackrf_source_0.set_sample_rate(0, self.samp_rate)
        self.verisure2GFSKRadioChannelToDataMessage_0.set_samp_rate(self.samp_rate)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_samp_rate(self.samp_rate)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_samp_rate(self.samp_rate)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_samp_rate(self.samp_rate)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_samp_rate(self.samp_rate)
        self.verisure4GFSKRadioChannelToDataMessage_0.set_samp_rate(self.samp_rate)
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_samp_rate(self.samp_rate)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_samp_rate(self.samp_rate)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_samp_rate(self.samp_rate)

    def get_rssi_calib_offset_s(self):
        return self.rssi_calib_offset_s

    def set_rssi_calib_offset_s(self, rssi_calib_offset_s):
        self.rssi_calib_offset_s = rssi_calib_offset_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_power_offset_calib(self.rssi_calib_offset_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_power_offset_calib(self.rssi_calib_offset_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_power_offset_calib(self.rssi_calib_offset_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_power_offset_calib(self.rssi_calib_offset_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_power_offset_calib(self.rssi_calib_offset_s)

    def get_rssi_calib_offset_800_h(self):
        return self.rssi_calib_offset_800_h

    def set_rssi_calib_offset_800_h(self, rssi_calib_offset_800_h):
        self.rssi_calib_offset_800_h = rssi_calib_offset_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_power_offset_calib(self.rssi_calib_offset_800_h)

    def get_rssi_calib_offset_600_h(self):
        return self.rssi_calib_offset_600_h

    def set_rssi_calib_offset_600_h(self, rssi_calib_offset_600_h):
        self.rssi_calib_offset_600_h = rssi_calib_offset_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_power_offset_calib(self.rssi_calib_offset_600_h)

    def get_rssi_calib_offset_200_h(self):
        return self.rssi_calib_offset_200_h

    def set_rssi_calib_offset_200_h(self, rssi_calib_offset_200_h):
        self.rssi_calib_offset_200_h = rssi_calib_offset_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_power_offset_calib(self.rssi_calib_offset_200_h)

    def get_rssi_calib_offset_100_h(self):
        return self.rssi_calib_offset_100_h

    def set_rssi_calib_offset_100_h(self, rssi_calib_offset_100_h):
        self.rssi_calib_offset_100_h = rssi_calib_offset_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_power_offset_calib(self.rssi_calib_offset_100_h)

    def get_qt_gui_display_time_before_symbolSink(self):
        return self.qt_gui_display_time_before_symbolSink

    def set_qt_gui_display_time_before_symbolSink(self, qt_gui_display_time_before_symbolSink):
        self.qt_gui_display_time_before_symbolSink = qt_gui_display_time_before_symbolSink

    def get_qt_gui_display_time_before_decimation(self):
        return self.qt_gui_display_time_before_decimation

    def set_qt_gui_display_time_before_decimation(self, qt_gui_display_time_before_decimation):
        self.qt_gui_display_time_before_decimation = qt_gui_display_time_before_decimation

    def get_qt_gui_display_time_after_symbolSink(self):
        return self.qt_gui_display_time_after_symbolSink

    def set_qt_gui_display_time_after_symbolSink(self, qt_gui_display_time_after_symbolSink):
        self.qt_gui_display_time_after_symbolSink = qt_gui_display_time_after_symbolSink

    def get_passband_end_s(self):
        return self.passband_end_s

    def set_passband_end_s(self, passband_end_s):
        self.passband_end_s = passband_end_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_passband_end(self.passband_end_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_passband_end(self.passband_end_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_passband_end(self.passband_end_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_passband_end(self.passband_end_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_passband_end(self.passband_end_s)

    def get_passband_end_800_h(self):
        return self.passband_end_800_h

    def set_passband_end_800_h(self, passband_end_800_h):
        self.passband_end_800_h = passband_end_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_passband_end(self.passband_end_800_h)

    def get_passband_end_600_h(self):
        return self.passband_end_600_h

    def set_passband_end_600_h(self, passband_end_600_h):
        self.passband_end_600_h = passband_end_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_passband_end(self.passband_end_600_h)

    def get_passband_end_200_h(self):
        return self.passband_end_200_h

    def set_passband_end_200_h(self, passband_end_200_h):
        self.passband_end_200_h = passband_end_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_passband_end(self.passband_end_200_h)

    def get_passband_end_100_h(self):
        return self.passband_end_100_h

    def set_passband_end_100_h(self, passband_end_100_h):
        self.passband_end_100_h = passband_end_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_passband_end(self.passband_end_100_h)

    def get_message_debug(self):
        return self.message_debug

    def set_message_debug(self, message_debug):
        self.message_debug = message_debug
        self.verisure2GFSKRadioChannelToDataMessage_0.set_debug_log(self.message_debug)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_debug_log(self.message_debug)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_debug_log(self.message_debug)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_debug_log(self.message_debug)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_debug_log(self.message_debug)
        self.verisure4GFSKRadioChannelToDataMessage_0.set_debug_log(self.message_debug)
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_debug_log(self.message_debug)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_debug_log(self.message_debug)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_debug_log(self.message_debug)

    def get_loop_damping_s(self):
        return self.loop_damping_s

    def set_loop_damping_s(self, loop_damping_s):
        self.loop_damping_s = loop_damping_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_loop_damping(self.loop_damping_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_loop_damping(self.loop_damping_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_loop_damping(self.loop_damping_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_loop_damping(self.loop_damping_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_loop_damping(self.loop_damping_s)

    def get_loop_damping_800_h(self):
        return self.loop_damping_800_h

    def set_loop_damping_800_h(self, loop_damping_800_h):
        self.loop_damping_800_h = loop_damping_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_loop_damping(self.loop_damping_800_h)

    def get_loop_damping_600_h(self):
        return self.loop_damping_600_h

    def set_loop_damping_600_h(self, loop_damping_600_h):
        self.loop_damping_600_h = loop_damping_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_loop_damping(self.loop_damping_600_h)

    def get_loop_damping_200_h(self):
        return self.loop_damping_200_h

    def set_loop_damping_200_h(self, loop_damping_200_h):
        self.loop_damping_200_h = loop_damping_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_loop_damping(self.loop_damping_200_h)

    def get_loop_damping_100_h(self):
        return self.loop_damping_100_h

    def set_loop_damping_100_h(self, loop_damping_100_h):
        self.loop_damping_100_h = loop_damping_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_loop_damping(self.loop_damping_100_h)

    def get_loop_bw_s(self):
        return self.loop_bw_s

    def set_loop_bw_s(self, loop_bw_s):
        self.loop_bw_s = loop_bw_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_loop_bw(self.loop_bw_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_loop_bw(self.loop_bw_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_loop_bw(self.loop_bw_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_loop_bw(self.loop_bw_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_loop_bw(self.loop_bw_s)

    def get_loop_bw_800_h(self):
        return self.loop_bw_800_h

    def set_loop_bw_800_h(self, loop_bw_800_h):
        self.loop_bw_800_h = loop_bw_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_loop_bw(self.loop_bw_800_h)

    def get_loop_bw_600_h(self):
        return self.loop_bw_600_h

    def set_loop_bw_600_h(self, loop_bw_600_h):
        self.loop_bw_600_h = loop_bw_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_loop_bw(self.loop_bw_600_h)

    def get_loop_bw_200_h(self):
        return self.loop_bw_200_h

    def set_loop_bw_200_h(self, loop_bw_200_h):
        self.loop_bw_200_h = loop_bw_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_loop_bw(self.loop_bw_200_h)

    def get_loop_bw_100_h(self):
        return self.loop_bw_100_h

    def set_loop_bw_100_h(self, loop_bw_100_h):
        self.loop_bw_100_h = loop_bw_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_loop_bw(self.loop_bw_100_h)

    def get_lo_osc_freq_error_correction(self):
        return self.lo_osc_freq_error_correction

    def set_lo_osc_freq_error_correction(self, lo_osc_freq_error_correction):
        self.lo_osc_freq_error_correction = lo_osc_freq_error_correction
        self.soapy_hackrf_source_0.set_frequency(0, self.lo_osc_freq+self.lo_osc_freq_error_correction)

    def get_lo_osc_freq(self):
        return self.lo_osc_freq

    def set_lo_osc_freq(self, lo_osc_freq):
        self.lo_osc_freq = lo_osc_freq
        self.soapy_hackrf_source_0.set_frequency(0, self.lo_osc_freq+self.lo_osc_freq_error_correction)
        self.verisure2GFSKRadioChannelToDataMessage_0.set_lo_osc_freq(self.lo_osc_freq)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_lo_osc_freq(self.lo_osc_freq)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_lo_osc_freq(self.lo_osc_freq)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_lo_osc_freq(self.lo_osc_freq)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_lo_osc_freq(self.lo_osc_freq)
        self.verisure4GFSKRadioChannelToDataMessage_0.set_lo_osc_freq(self.lo_osc_freq)
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_lo_osc_freq(self.lo_osc_freq)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_lo_osc_freq(self.lo_osc_freq)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_lo_osc_freq(self.lo_osc_freq)

    def get_lna_on(self):
        return self.lna_on

    def set_lna_on(self, lna_on):
        self.lna_on = lna_on
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', self.lna_on)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(self.if_gain, 0.0), 40.0))

    def get_high_verbosity_debug(self):
        return self.high_verbosity_debug

    def set_high_verbosity_debug(self, high_verbosity_debug):
        self.high_verbosity_debug = high_verbosity_debug
        self.verisure2GFSKRadioChannelToDataMessage_0.set_debug_log_verbosity(self.high_verbosity_debug)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_debug_log_verbosity(self.high_verbosity_debug)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_debug_log_verbosity(self.high_verbosity_debug)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_debug_log_verbosity(self.high_verbosity_debug)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_debug_log_verbosity(self.high_verbosity_debug)
        self.verisure4GFSKRadioChannelToDataMessage_0.set_debug_log_verbosity(self.high_verbosity_debug)
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_debug_log_verbosity(self.high_verbosity_debug)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_debug_log_verbosity(self.high_verbosity_debug)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_debug_log_verbosity(self.high_verbosity_debug)

    def get_high_verbosity_all_channel_log(self):
        return self.high_verbosity_all_channel_log

    def set_high_verbosity_all_channel_log(self, high_verbosity_all_channel_log):
        self.high_verbosity_all_channel_log = high_verbosity_all_channel_log

    def get_fsk_deviation_s(self):
        return self.fsk_deviation_s

    def set_fsk_deviation_s(self, fsk_deviation_s):
        self.fsk_deviation_s = fsk_deviation_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_fsk_deviation(self.fsk_deviation_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_fsk_deviation(self.fsk_deviation_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_fsk_deviation(self.fsk_deviation_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_fsk_deviation(self.fsk_deviation_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_fsk_deviation(self.fsk_deviation_s)

    def get_fsk_deviation_800_h(self):
        return self.fsk_deviation_800_h

    def set_fsk_deviation_800_h(self, fsk_deviation_800_h):
        self.fsk_deviation_800_h = fsk_deviation_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_fsk_deviation(self.fsk_deviation_800_h)

    def get_fsk_deviation_600_h(self):
        return self.fsk_deviation_600_h

    def set_fsk_deviation_600_h(self, fsk_deviation_600_h):
        self.fsk_deviation_600_h = fsk_deviation_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_fsk_deviation(self.fsk_deviation_600_h)

    def get_fsk_deviation_200_h(self):
        return self.fsk_deviation_200_h

    def set_fsk_deviation_200_h(self, fsk_deviation_200_h):
        self.fsk_deviation_200_h = fsk_deviation_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_fsk_deviation(self.fsk_deviation_200_h)

    def get_fsk_deviation_100_h(self):
        return self.fsk_deviation_100_h

    def set_fsk_deviation_100_h(self, fsk_deviation_100_h):
        self.fsk_deviation_100_h = fsk_deviation_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_fsk_deviation(self.fsk_deviation_100_h)

    def get_dewhitening_key(self):
        return self.dewhitening_key

    def set_dewhitening_key(self, dewhitening_key):
        self.dewhitening_key = dewhitening_key
        self.verisure2GFSKRadioChannelToDataMessage_0.set_dewhitening_key(self.dewhitening_key)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_dewhitening_key(self.dewhitening_key)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_dewhitening_key(self.dewhitening_key)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_dewhitening_key(self.dewhitening_key)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_dewhitening_key(self.dewhitening_key)
        self.verisure4GFSKRadioChannelToDataMessage_0.set_dewhitening_key(self.dewhitening_key)
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_dewhitening_key(self.dewhitening_key)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_dewhitening_key(self.dewhitening_key)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_dewhitening_key(self.dewhitening_key)

    def get_demod_dc_block_time_s(self):
        return self.demod_dc_block_time_s

    def set_demod_dc_block_time_s(self, demod_dc_block_time_s):
        self.demod_dc_block_time_s = demod_dc_block_time_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_demod_dc_block_time(self.demod_dc_block_time_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_demod_dc_block_time(self.demod_dc_block_time_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_demod_dc_block_time(self.demod_dc_block_time_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_demod_dc_block_time(self.demod_dc_block_time_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_demod_dc_block_time(self.demod_dc_block_time_s)

    def get_demod_dc_block_time_800_h(self):
        return self.demod_dc_block_time_800_h

    def set_demod_dc_block_time_800_h(self, demod_dc_block_time_800_h):
        self.demod_dc_block_time_800_h = demod_dc_block_time_800_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_demod_dc_block_time(self.demod_dc_block_time_800_h)

    def get_demod_dc_block_time_600_h(self):
        return self.demod_dc_block_time_600_h

    def set_demod_dc_block_time_600_h(self, demod_dc_block_time_600_h):
        self.demod_dc_block_time_600_h = demod_dc_block_time_600_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_demod_dc_block_time(self.demod_dc_block_time_600_h)

    def get_demod_dc_block_time_200_h(self):
        return self.demod_dc_block_time_200_h

    def set_demod_dc_block_time_200_h(self, demod_dc_block_time_200_h):
        self.demod_dc_block_time_200_h = demod_dc_block_time_200_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_demod_dc_block_time(self.demod_dc_block_time_200_h)

    def get_demod_dc_block_time_100_h(self):
        return self.demod_dc_block_time_100_h

    def set_demod_dc_block_time_100_h(self, demod_dc_block_time_100_h):
        self.demod_dc_block_time_100_h = demod_dc_block_time_100_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_demod_dc_block_time(self.demod_dc_block_time_100_h)

    def get_debug_log_server(self):
        return self.debug_log_server

    def set_debug_log_server(self, debug_log_server):
        self.debug_log_server = debug_log_server

    def get_crc_polynomial(self):
        return self.crc_polynomial

    def set_crc_polynomial(self, crc_polynomial):
        self.crc_polynomial = crc_polynomial
        self.verisure2GFSKRadioChannelToDataMessage_0.set_crc_polynomial(self.crc_polynomial)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_crc_polynomial(self.crc_polynomial)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_crc_polynomial(self.crc_polynomial)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_crc_polynomial(self.crc_polynomial)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_crc_polynomial(self.crc_polynomial)
        self.verisure4GFSKRadioChannelToDataMessage_0.set_crc_polynomial(self.crc_polynomial)
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_crc_polynomial(self.crc_polynomial)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_crc_polynomial(self.crc_polynomial)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_crc_polynomial(self.crc_polynomial)

    def get_crc_key(self):
        return self.crc_key

    def set_crc_key(self, crc_key):
        self.crc_key = crc_key
        self.verisure2GFSKRadioChannelToDataMessage_0.set_crc_key(self.crc_key)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_crc_key(self.crc_key)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_crc_key(self.crc_key)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_crc_key(self.crc_key)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_crc_key(self.crc_key)
        self.verisure4GFSKRadioChannelToDataMessage_0.set_crc_key(self.crc_key)
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_crc_key(self.crc_key)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_crc_key(self.crc_key)
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_crc_key(self.crc_key)

    def get_ch800freq_h(self):
        return self.ch800freq_h

    def set_ch800freq_h(self, ch800freq_h):
        self.ch800freq_h = ch800freq_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_selected_ch_freq(self.ch800freq_h)

    def get_ch800enable(self):
        return self.ch800enable

    def set_ch800enable(self, ch800enable):
        self.ch800enable = ch800enable
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_ch_enable(self.ch800enable)

    def get_ch800Bitrate_h(self):
        return self.ch800Bitrate_h

    def set_ch800Bitrate_h(self, ch800Bitrate_h):
        self.ch800Bitrate_h = ch800Bitrate_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0_0.set_bitrate(self.ch800Bitrate_h)

    def get_ch600freq_h(self):
        return self.ch600freq_h

    def set_ch600freq_h(self, ch600freq_h):
        self.ch600freq_h = ch600freq_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_selected_ch_freq(self.ch600freq_h)

    def get_ch600enable(self):
        return self.ch600enable

    def set_ch600enable(self, ch600enable):
        self.ch600enable = ch600enable
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_ch_enable(self.ch600enable)

    def get_ch600Bitrate_h(self):
        return self.ch600Bitrate_h

    def set_ch600Bitrate_h(self, ch600Bitrate_h):
        self.ch600Bitrate_h = ch600Bitrate_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0_0.set_bitrate(self.ch600Bitrate_h)

    def get_ch5freq_s(self):
        return self.ch5freq_s

    def set_ch5freq_s(self, ch5freq_s):
        self.ch5freq_s = ch5freq_s
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_selected_ch_freq(self.ch5freq_s)

    def get_ch5enable(self):
        return self.ch5enable

    def set_ch5enable(self, ch5enable):
        self.ch5enable = ch5enable
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_ch_enable(self.ch5enable)

    def get_ch5_number_s(self):
        return self.ch5_number_s

    def set_ch5_number_s(self, ch5_number_s):
        self.ch5_number_s = ch5_number_s
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_ch_number(self.ch5_number_s)

    def get_ch4freq_s(self):
        return self.ch4freq_s

    def set_ch4freq_s(self, ch4freq_s):
        self.ch4freq_s = ch4freq_s
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_selected_ch_freq(self.ch4freq_s)

    def get_ch4enable(self):
        return self.ch4enable

    def set_ch4enable(self, ch4enable):
        self.ch4enable = ch4enable
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_ch_enable(self.ch4enable)

    def get_ch4_number_s(self):
        return self.ch4_number_s

    def set_ch4_number_s(self, ch4_number_s):
        self.ch4_number_s = ch4_number_s
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_ch_number(self.ch4_number_s)

    def get_ch3freq_s(self):
        return self.ch3freq_s

    def set_ch3freq_s(self, ch3freq_s):
        self.ch3freq_s = ch3freq_s
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_selected_ch_freq(self.ch3freq_s)

    def get_ch3enable(self):
        return self.ch3enable

    def set_ch3enable(self, ch3enable):
        self.ch3enable = ch3enable
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_ch_enable(self.ch3enable)

    def get_ch3_number_s(self):
        return self.ch3_number_s

    def set_ch3_number_s(self, ch3_number_s):
        self.ch3_number_s = ch3_number_s
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_ch_number(self.ch3_number_s)

    def get_ch2freq_s(self):
        return self.ch2freq_s

    def set_ch2freq_s(self, ch2freq_s):
        self.ch2freq_s = ch2freq_s
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_selected_ch_freq(self.ch2freq_s)

    def get_ch2enable(self):
        return self.ch2enable

    def set_ch2enable(self, ch2enable):
        self.ch2enable = ch2enable
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_ch_enable(self.ch2enable)

    def get_ch2_number_s(self):
        return self.ch2_number_s

    def set_ch2_number_s(self, ch2_number_s):
        self.ch2_number_s = ch2_number_s
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_ch_number(self.ch2_number_s)

    def get_ch200freq_h(self):
        return self.ch200freq_h

    def set_ch200freq_h(self, ch200freq_h):
        self.ch200freq_h = ch200freq_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_selected_ch_freq(self.ch200freq_h)

    def get_ch200enable(self):
        return self.ch200enable

    def set_ch200enable(self, ch200enable):
        self.ch200enable = ch200enable
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_ch_enable(self.ch200enable)

    def get_ch200Bitrate_h(self):
        return self.ch200Bitrate_h

    def set_ch200Bitrate_h(self, ch200Bitrate_h):
        self.ch200Bitrate_h = ch200Bitrate_h
        self.verisure4GFSKRadioChannelToDataMessage_0_0.set_bitrate(self.ch200Bitrate_h)

    def get_ch1freq_s(self):
        return self.ch1freq_s

    def set_ch1freq_s(self, ch1freq_s):
        self.ch1freq_s = ch1freq_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_selected_ch_freq(self.ch1freq_s)

    def get_ch1enable(self):
        return self.ch1enable

    def set_ch1enable(self, ch1enable):
        self.ch1enable = ch1enable
        self.verisure2GFSKRadioChannelToDataMessage_0.set_ch_enable(self.ch1enable)

    def get_ch1_number_s(self):
        return self.ch1_number_s

    def set_ch1_number_s(self, ch1_number_s):
        self.ch1_number_s = ch1_number_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_ch_number(self.ch1_number_s)

    def get_ch100freq_h(self):
        return self.ch100freq_h

    def set_ch100freq_h(self, ch100freq_h):
        self.ch100freq_h = ch100freq_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_selected_ch_freq(self.ch100freq_h)

    def get_ch100enable(self):
        return self.ch100enable

    def set_ch100enable(self, ch100enable):
        self.ch100enable = ch100enable
        self.verisure4GFSKRadioChannelToDataMessage_0.set_ch_enable(self.ch100enable)

    def get_ch100Bitrate_h(self):
        return self.ch100Bitrate_h

    def set_ch100Bitrate_h(self, ch100Bitrate_h):
        self.ch100Bitrate_h = ch100Bitrate_h
        self.verisure4GFSKRadioChannelToDataMessage_0.set_bitrate(self.ch100Bitrate_h)

    def get_bitrate_s(self):
        return self.bitrate_s

    def set_bitrate_s(self, bitrate_s):
        self.bitrate_s = bitrate_s
        self.verisure2GFSKRadioChannelToDataMessage_0.set_bitrate(self.bitrate_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_0.set_bitrate(self.bitrate_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_1.set_bitrate(self.bitrate_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_2.set_bitrate(self.bitrate_s)
        self.verisure2GFSKRadioChannelToDataMessage_0_3.set_bitrate(self.bitrate_s)

    def get_antialiass_filter_bw(self):
        return self.antialiass_filter_bw

    def set_antialiass_filter_bw(self, antialiass_filter_bw):
        self.antialiass_filter_bw = antialiass_filter_bw
        self.soapy_hackrf_source_0.set_bandwidth(0, self.antialiass_filter_bw)

    def get_all_channel_log(self):
        return self.all_channel_log

    def set_all_channel_log(self, all_channel_log):
        self.all_channel_log = all_channel_log




def main(top_block_cls=multichannelSniffer, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls()
    snippets_main_after_init(tb)
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        snippets_main_after_stop(tb)
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    snippets_main_after_start(tb)
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
    snippets_main_after_stop(tb)

if __name__ == '__main__':
    main()
