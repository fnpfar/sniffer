"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    # only default arguments here
    def __init__(self, crc_Polynomial=0x8005, crc_Init_Key=0xFFFF, debug_Log=False, high_Verbosity_Log=False):
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Verisure CRC Checker',   # will show up in GRC
            in_sig=None,  # there is no input stream
            out_sig=None  # there is no output stream
        )

        # input message port definition
        self.message_port_register_in(pmt.intern('pdu_in'))
        # output message port definition
        self.message_port_register_out(pmt.intern('pdu_out'))
        # asociation of handler function to input
        self.set_msg_handler(pmt.intern('pdu_in'), self.handle_pdu)

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.crcInit = crc_Init_Key
        self.crcPoly = crc_Polynomial
        self.log = debug_Log
        self.highVerbosity = high_Verbosity_Log

        if self.log:  # Debug
            self.msgNumber = -1  # message indexer for debug
            self.crcPassCount = 0  # message counter for debug
            self.crcFailCount = 0  # message counter for debug

    def handle_pdu(self, pdu):  # called when a pdu has been published to 'pdu_in' message port

        # access to the pdu parts:
        pduMetadataDictionary = pmt.car(pdu)  # first field of pdu extracted
        # second field of pdu extracted, which is the payload vector
        pduPayloadVector = pmt.to_python(pmt.cdr(pdu))

        frameCrc = pmt.to_python(pmt.dict_ref(
            pduMetadataDictionary, pmt.intern("crc"), pmt.PMT_NIL))  # access to crc key
        frameCrc16bit = self.bytes_to_16bit(frameCrc)

        # crc is calculated over the byte of the length + bytes of the payload
        lengthAndPayload = pduPayloadVector.copy()
        # length byte is inserted at position 0
        lengthAndPayload.insert(0, len(pduPayloadVector))
        # lengthAndPayload.append(len(pduPayloadVector))

        calculatedCrc = self.calculate_crc(lengthAndPayload)  # calculates crc
        # checks calculated and frame crc
        packetOk = 1 if frameCrc16bit == calculatedCrc else 0

        if self.log:  # Debug log
            channel = int(pmt.to_python(pmt.dict_ref(pduMetadataDictionary, pmt.intern(
                "channel_number"), pmt.PMT_NIL)))  # access to channel number
            self.debug_log(channel, packetOk, pduPayloadVector,
                           lengthAndPayload, frameCrc, frameCrc16bit, calculatedCrc)

        pduMetadataDictionary = pmt.dict_add(pduMetadataDictionary, pmt.intern(
            "calculated_crc"),  pmt.from_long(calculatedCrc))
        pduMetadataDictionary = pmt.dict_add(
            pduMetadataDictionary, pmt.intern("crc_check"),  pmt.from_long(packetOk))

        # builds a GNU Radio standarized PDU
        pdu = pmt.cons(pduMetadataDictionary, pmt.to_pmt(pduPayloadVector))
        # publishes PDU. args: port, message
        self.message_port_pub(pmt.intern('pdu_out'), pdu)

    # Update CRC register with new byte (ported code from c)

    def update_crc(self, data, crc_reg):
        bitMask8 = 0xFF  # a bit mask to make Python variables behave like u8_t when shifting
        bitMask16 = 0xFFFF  # a bit mask to make Python variables behave like u16_t when shifting
        data &= bitMask8
        for i in range(0, 8):
            if (bitMask16 & ((crc_reg & 0x8000) >> 8)) ^ (data & 0x80):
                crc_reg = (bitMask16 & (crc_reg << 1)) ^ self.crcPoly
            else:
                crc_reg = bitMask16 & (crc_reg << 1)
            data = bitMask8 & (data << 1)
        return crc_reg

    # Calculate CRC value on byte array using above function (ported code from c)
    def calculate_crc(self, data):
        crc = self.crcInit
        for byte in data:
            crc = self.update_crc(byte, crc)
        return crc

    # Converts a list of two bytes into a big-endian 16 bit value
    def bytes_to_16bit(self, list):
        try:
            return ((list[0] & 0xFF) << 8) | (0xFF & list[1])
        except:  # if by any reason one of the positions of the list is not defined
            return 0

    # Converts a list of two bytes into a big-endian 16 bit value (for DEBUG)

    def from16bit_to_bytes(self, value):
        out = [None]*2  # initializing a 2 element list
        value = 0xFFFF & value
        out[0] = (0xFF00 & value) >> 8
        out[1] = (0x00FF & value)
        return out

    # Log
    def debug_log(self, channel, packetOk, pduPayloadVector, lengthAndPayload, frameCrc, frameCrc16bit, calculatedCrc):

        self.msgNumber += 1
        if packetOk:
            self.crcPassCount += 1
        else:
            self.crcFailCount += 1
        passPercentage = (self.crcPassCount/(self.msgNumber + 1))*100
        failPercentage = (self.crcFailCount/(self.msgNumber + 1))*100

        if self.highVerbosity:  # high verbosity mode
            calculatedCRCinBytes = self.from16bit_to_bytes(calculatedCrc)
            print('')
            print('  Verisure CRC Checker debug message:')
            print(' .----------------------------------------->')
            print(' | Channel:', channel)
            print(' | ----------------------------------------')
            print(' | Payload Length:', len(pduPayloadVector))
            print(' | Length + Dewhitened Payload Data in DEC:', lengthAndPayload)
            print(' | Length + Dewhitened Payload Data in HEX:',
                  [format(byte, "02X") for byte in lengthAndPayload])
            print(' | ----------------------------------------')
            print(' | Frame CRC in DEC (2-byte representation):', frameCrc)
            print(' | Calculated CRC in DEC (2-byte representation):',
                  calculatedCRCinBytes)
            print(' | ----------------------------------------')
            print(' | Frame CRC in BIN      (2-byte representation):',
                  [format(byte, "08b") for byte in frameCrc])
            print(' | Calculated CRC in BIN (2-byte representation):',
                  [format(byte, "08b") for byte in calculatedCRCinBytes])
            print(' | ----------------------------------------')
            print(' | Frame CRC in DEC (16 bit representation):', frameCrc16bit)
            print(' | Calculated CRC in DEC (16 bit representation):', calculatedCrc)
            print(' | ----------------------------------------')
            print(' | Msg. number (first is number 0):', self.msgNumber)
            print(' | CRC Check:', 'PASSED' if packetOk else 'FAILED')
            print(' | ----------------------------------------')
            print(' | Pass rate:', passPercentage, '%')
            print(' | Failure rate:', failPercentage, '%')
            print(' *----------------------------------------->')
            print('')
        else:  # low verbosity mode
            """
            print ('')
            print ('   2. Verisure CRC Checker debug message:')
            print (' .----------------------------------------->')
            print (' | Msg. number (from #0):', self.msgNumber )     
            print (' | CRC Check:', 'PASSED' if packetOk else 'FAILED!')
            print (' | Pass rate:', passPercentage, '%' )  
            print (' | Failure rate:', failPercentage, '%' )  
            print (' | (Packets with failed CRC / All packets received):', self.crcFailCount, '/', self.msgNumber + 1 )
            print (' *----------------------------------------->')  
            print ('')
            """
            print('Channel:', channel, 'Msg. number (first is number 0):', self.msgNumber, 'CRC Check:', 'PASSED' if packetOk else 'FAILED!',
                  '(Packets with failed CRC / All packets received):', self.crcFailCount, '/', self.msgNumber + 1)
