# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Verisure 2GFSK Radio Channel to Data Mesagge
# Author: Francisco Nicolás Pérez Fernández
# Copyright: Verisure
# Description: A 2-GFSK reception chain for the Verisure radio channels
# GNU Radio version: 3.10.2.0

from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
import verisure2GFSKRadioChannelToDataMessage_verisure_crc_checker as verisure_crc_checker  # embedded python block
import verisure2GFSKRadioChannelToDataMessage_verisure_float_to_msg_resamp_ratio_converter as verisure_float_to_msg_resamp_ratio_converter  # embedded python block
import verisure2GFSKRadioChannelToDataMessage_verisure_tagged_bitstream_to_pdu as verisure_tagged_bitstream_to_pdu  # embedded python block







class verisure2GFSKRadioChannelToDataMessage(gr.hier_block2):
    def __init__(self, bitrate=38400, ch_enable=True, ch_number=1, crc_key=0xFFFF, crc_polynomial=0x8005, debug_log=False, debug_log_verbosity=False, demod_dc_block_time=6e-3, dewhitening_key=0x1ff, fsk_deviation=19.775e3, lo_osc_freq=869.3e6, loop_bw=0.015, loop_damping=1.4, passband_end=39e3, power_offset_calib=-15, samp_rate=13e6, samp_rate_demod=100e3, selected_ch_freq=868.15e6, squelchAlpha=300e-3, squelch_level=-40, squelch_ramp=8, stop_band_attenuation_dB=96, stopband_start=50e3, ted_gain=1, ted_max_deviation=1.5):
        gr.hier_block2.__init__(
            self, "Verisure 2GFSK Radio Channel to Data Mesagge",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature.makev(13, 13, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1]),
        )
        self.message_port_register_hier_out("message_out")

        ##################################################
        # Parameters
        ##################################################
        self.bitrate = bitrate
        self.ch_enable = ch_enable
        self.ch_number = ch_number
        self.crc_key = crc_key
        self.crc_polynomial = crc_polynomial
        self.debug_log = debug_log
        self.debug_log_verbosity = debug_log_verbosity
        self.demod_dc_block_time = demod_dc_block_time
        self.dewhitening_key = dewhitening_key
        self.fsk_deviation = fsk_deviation
        self.lo_osc_freq = lo_osc_freq
        self.loop_bw = loop_bw
        self.loop_damping = loop_damping
        self.passband_end = passband_end
        self.power_offset_calib = power_offset_calib
        self.samp_rate = samp_rate
        self.samp_rate_demod = samp_rate_demod
        self.selected_ch_freq = selected_ch_freq
        self.squelchAlpha = squelchAlpha
        self.squelch_level = squelch_level
        self.squelch_ramp = squelch_ramp
        self.stop_band_attenuation_dB = stop_band_attenuation_dB
        self.stopband_start = stopband_start
        self.ted_gain = ted_gain
        self.ted_max_deviation = ted_max_deviation

        ##################################################
        # Variables
        ##################################################
        self.transition_width = transition_width = stopband_start-passband_end
        self.filterGain = filterGain = 1
        self.decimation = decimation = int(samp_rate/samp_rate_demod)
        self.cutoff_freq = cutoff_freq = (passband_end+stopband_start)/2
        self.compensation_delay_time = compensation_delay_time = 2.1e-3

        ##################################################
        # Blocks
        ##################################################
        self.verisure_tagged_bitstream_to_pdu = verisure_tagged_bitstream_to_pdu.blk(channelNumerator=ch_number, initial_Dewhitening_key=dewhitening_key, debug_Log_frame=False, debug_Log_control_traces=False)
        self.verisure_float_to_msg_resamp_ratio_converter = verisure_float_to_msg_resamp_ratio_converter.blk(decimation=1)
        self.verisure_crc_checker = verisure_crc_checker.blk(crc_Polynomial=crc_polynomial, crc_Init_Key=crc_key, debug_Log=debug_log, high_Verbosity_Log=debug_log_verbosity)
        self.mmse_resampler_xx_0_0 = filter.mmse_resampler_ff(0, samp_rate/(decimation*bitrate))
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, samp_rate/(decimation*bitrate))
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(decimation,  firdes.low_pass_2(filterGain,samp_rate,cutoff_freq,transition_width,stop_band_attenuation_dB), selected_ch_freq - lo_osc_freq, samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(8)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(1)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_EARLY_LATE,
            samp_rate_demod/bitrate,
            loop_bw,
            loop_damping,
            ted_gain,
            ted_max_deviation,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_correlate_access_code_tag_xx_0 = digital.correlate_access_code_tag_ff("11010011100100011101001110010001", 0, "phyframe")
        self.digital_binary_slicer_fb_0_3 = digital.binary_slicer_fb()
        self.dc_blocker_xx_0_0 = filter.dc_blocker_ff(int(demod_dc_block_time*samp_rate_demod), False)
        self.blocks_uchar_to_float_0_1_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0_0.set_enabled(ch_enable)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, power_offset_calib)
        self.blocks_multiply_const_xx_0_0_0_0 = blocks.multiply_const_ff(-fsk_deviation, 1)
        self.blocks_multiply_const_xx_0_0_0 = blocks.multiply_const_ff(-2/fsk_deviation, 1)
        self.blocks_multiply_const_xx_0_0 = blocks.multiply_const_ff(0.02, 1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(64, 1/64, 1000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(64, 1/64, 1000, 1)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, int(compensation_delay_time*samp_rate_demod))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, int(compensation_delay_time*samp_rate_demod))
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(70)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/(decimation*2*math.pi*fsk_deviation))
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(squelch_level, squelchAlpha, squelch_ramp, False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.verisure_crc_checker, 'pdu_out'), (self, 'message_out'))
        self.msg_connect((self.verisure_float_to_msg_resamp_ratio_converter, 'msg_out'), (self.mmse_resampler_xx_0, 'msg_in'))
        self.msg_connect((self.verisure_float_to_msg_resamp_ratio_converter, 'msg_out'), (self.mmse_resampler_xx_0_0, 'msg_in'))
        self.msg_connect((self.verisure_tagged_bitstream_to_pdu, 'pdu_out'), (self.verisure_crc_checker, 'pdu_in'))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self, 1))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.dc_blocker_xx_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.mmse_resampler_xx_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self, 2))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_multiply_const_xx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.verisure_tagged_bitstream_to_pdu, 1))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_multiply_const_xx_0_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.verisure_tagged_bitstream_to_pdu, 2))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_multiply_const_xx_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_0, 0), (self, 11))
        self.connect((self.blocks_multiply_const_xx_0_0_0, 0), (self, 12))
        self.connect((self.blocks_multiply_const_xx_0_0_0_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self, 10))
        self.connect((self.blocks_uchar_to_float_0_1_0, 0), (self, 9))
        self.connect((self.dc_blocker_xx_0_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.dc_blocker_xx_0_0, 0), (self, 3))
        self.connect((self.dc_blocker_xx_0_0, 0), (self, 4))
        self.connect((self.digital_binary_slicer_fb_0_3, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_3, 0), (self.blocks_uchar_to_float_0_1_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_3, 0), (self.verisure_tagged_bitstream_to_pdu, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.digital_binary_slicer_fb_0_3, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_correlate_access_code_tag_xx_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self, 5))
        self.connect((self.digital_symbol_sync_xx_0, 1), (self, 6))
        self.connect((self.digital_symbol_sync_xx_0, 2), (self, 7))
        self.connect((self.digital_symbol_sync_xx_0, 3), (self, 8))
        self.connect((self.digital_symbol_sync_xx_0, 3), (self.verisure_float_to_msg_resamp_ratio_converter, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.mmse_resampler_xx_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self, 0), (self.blocks_selector_0_0, 0))


    def get_bitrate(self):
        return self.bitrate

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate
        self.mmse_resampler_xx_0.set_resamp_ratio(self.samp_rate/(self.decimation*self.bitrate))
        self.mmse_resampler_xx_0_0.set_resamp_ratio(self.samp_rate/(self.decimation*self.bitrate))

    def get_ch_enable(self):
        return self.ch_enable

    def set_ch_enable(self, ch_enable):
        self.ch_enable = ch_enable
        self.blocks_selector_0_0.set_enabled(self.ch_enable)

    def get_ch_number(self):
        return self.ch_number

    def set_ch_number(self, ch_number):
        self.ch_number = ch_number

    def get_crc_key(self):
        return self.crc_key

    def set_crc_key(self, crc_key):
        self.crc_key = crc_key

    def get_crc_polynomial(self):
        return self.crc_polynomial

    def set_crc_polynomial(self, crc_polynomial):
        self.crc_polynomial = crc_polynomial

    def get_debug_log(self):
        return self.debug_log

    def set_debug_log(self, debug_log):
        self.debug_log = debug_log

    def get_debug_log_verbosity(self):
        return self.debug_log_verbosity

    def set_debug_log_verbosity(self, debug_log_verbosity):
        self.debug_log_verbosity = debug_log_verbosity

    def get_demod_dc_block_time(self):
        return self.demod_dc_block_time

    def set_demod_dc_block_time(self, demod_dc_block_time):
        self.demod_dc_block_time = demod_dc_block_time

    def get_dewhitening_key(self):
        return self.dewhitening_key

    def set_dewhitening_key(self, dewhitening_key):
        self.dewhitening_key = dewhitening_key

    def get_fsk_deviation(self):
        return self.fsk_deviation

    def set_fsk_deviation(self, fsk_deviation):
        self.fsk_deviation = fsk_deviation
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(self.decimation*2*math.pi*self.fsk_deviation))
        self.blocks_multiply_const_xx_0_0_0.set_k(-2/self.fsk_deviation)
        self.blocks_multiply_const_xx_0_0_0_0.set_k(-self.fsk_deviation)

    def get_lo_osc_freq(self):
        return self.lo_osc_freq

    def set_lo_osc_freq(self, lo_osc_freq):
        self.lo_osc_freq = lo_osc_freq
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.selected_ch_freq - self.lo_osc_freq)

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.loop_bw)

    def get_loop_damping(self):
        return self.loop_damping

    def set_loop_damping(self, loop_damping):
        self.loop_damping = loop_damping
        self.digital_symbol_sync_xx_0.set_damping_factor(self.loop_damping)

    def get_passband_end(self):
        return self.passband_end

    def set_passband_end(self, passband_end):
        self.passband_end = passband_end
        self.set_cutoff_freq((self.passband_end+self.stopband_start)/2)
        self.set_transition_width(self.stopband_start-self.passband_end)

    def get_power_offset_calib(self):
        return self.power_offset_calib

    def set_power_offset_calib(self, power_offset_calib):
        self.power_offset_calib = power_offset_calib

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_decimation(int(self.samp_rate/self.samp_rate_demod))
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(self.decimation*2*math.pi*self.fsk_deviation))
        self.freq_xlating_fft_filter_ccc_0.set_taps( firdes.low_pass_2(self.filterGain,self.samp_rate,self.cutoff_freq,self.transition_width,self.stop_band_attenuation_dB))
        self.mmse_resampler_xx_0.set_resamp_ratio(self.samp_rate/(self.decimation*self.bitrate))
        self.mmse_resampler_xx_0_0.set_resamp_ratio(self.samp_rate/(self.decimation*self.bitrate))

    def get_samp_rate_demod(self):
        return self.samp_rate_demod

    def set_samp_rate_demod(self, samp_rate_demod):
        self.samp_rate_demod = samp_rate_demod
        self.set_decimation(int(self.samp_rate/self.samp_rate_demod))
        self.blocks_delay_0.set_dly(int(self.compensation_delay_time*self.samp_rate_demod))
        self.blocks_delay_0_0.set_dly(int(self.compensation_delay_time*self.samp_rate_demod))

    def get_selected_ch_freq(self):
        return self.selected_ch_freq

    def set_selected_ch_freq(self, selected_ch_freq):
        self.selected_ch_freq = selected_ch_freq
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.selected_ch_freq - self.lo_osc_freq)

    def get_squelchAlpha(self):
        return self.squelchAlpha

    def set_squelchAlpha(self, squelchAlpha):
        self.squelchAlpha = squelchAlpha
        self.analog_pwr_squelch_xx_0.set_alpha(self.squelchAlpha)

    def get_squelch_level(self):
        return self.squelch_level

    def set_squelch_level(self, squelch_level):
        self.squelch_level = squelch_level
        self.analog_pwr_squelch_xx_0.set_threshold(self.squelch_level)

    def get_squelch_ramp(self):
        return self.squelch_ramp

    def set_squelch_ramp(self, squelch_ramp):
        self.squelch_ramp = squelch_ramp

    def get_stop_band_attenuation_dB(self):
        return self.stop_band_attenuation_dB

    def set_stop_band_attenuation_dB(self, stop_band_attenuation_dB):
        self.stop_band_attenuation_dB = stop_band_attenuation_dB
        self.freq_xlating_fft_filter_ccc_0.set_taps( firdes.low_pass_2(self.filterGain,self.samp_rate,self.cutoff_freq,self.transition_width,self.stop_band_attenuation_dB))

    def get_stopband_start(self):
        return self.stopband_start

    def set_stopband_start(self, stopband_start):
        self.stopband_start = stopband_start
        self.set_cutoff_freq((self.passband_end+self.stopband_start)/2)
        self.set_transition_width(self.stopband_start-self.passband_end)

    def get_ted_gain(self):
        return self.ted_gain

    def set_ted_gain(self, ted_gain):
        self.ted_gain = ted_gain
        self.digital_symbol_sync_xx_0.set_ted_gain(self.ted_gain)

    def get_ted_max_deviation(self):
        return self.ted_max_deviation

    def set_ted_max_deviation(self, ted_max_deviation):
        self.ted_max_deviation = ted_max_deviation

    def get_transition_width(self):
        return self.transition_width

    def set_transition_width(self, transition_width):
        self.transition_width = transition_width
        self.freq_xlating_fft_filter_ccc_0.set_taps( firdes.low_pass_2(self.filterGain,self.samp_rate,self.cutoff_freq,self.transition_width,self.stop_band_attenuation_dB))

    def get_filterGain(self):
        return self.filterGain

    def set_filterGain(self, filterGain):
        self.filterGain = filterGain
        self.freq_xlating_fft_filter_ccc_0.set_taps( firdes.low_pass_2(self.filterGain,self.samp_rate,self.cutoff_freq,self.transition_width,self.stop_band_attenuation_dB))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(self.decimation*2*math.pi*self.fsk_deviation))
        self.mmse_resampler_xx_0.set_resamp_ratio(self.samp_rate/(self.decimation*self.bitrate))
        self.mmse_resampler_xx_0_0.set_resamp_ratio(self.samp_rate/(self.decimation*self.bitrate))

    def get_cutoff_freq(self):
        return self.cutoff_freq

    def set_cutoff_freq(self, cutoff_freq):
        self.cutoff_freq = cutoff_freq
        self.freq_xlating_fft_filter_ccc_0.set_taps( firdes.low_pass_2(self.filterGain,self.samp_rate,self.cutoff_freq,self.transition_width,self.stop_band_attenuation_dB))

    def get_compensation_delay_time(self):
        return self.compensation_delay_time

    def set_compensation_delay_time(self, compensation_delay_time):
        self.compensation_delay_time = compensation_delay_time
        self.blocks_delay_0.set_dly(int(self.compensation_delay_time*self.samp_rate_demod))
        self.blocks_delay_0_0.set_dly(int(self.compensation_delay_time*self.samp_rate_demod))

