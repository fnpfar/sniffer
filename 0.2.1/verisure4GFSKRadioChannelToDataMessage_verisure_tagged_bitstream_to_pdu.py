"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import pmt
from datetime import datetime # for timestamping
# import queue

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    class Frame(): # auxiliar inner class for storing all the data requiered to parse a frame
        def __init__(self, tagAbsolutePosition, timestamp, power, freqError, initial_PRBS_key): # Constructor
            
            self.tagAbsolutePosition = tagAbsolutePosition # absolute offset in the stream of the tag of the frame
            self.timestamp = timestamp # timestamp of tag of the frame
            self.power = power # measure of the power of the signal at the time of the tag
            self.freqError = freqError # measure of the power of the signal at the time of the tag
            
            self.nextBitIndexToParse = 0 # index of the next bite of the frame to process
            self.byteBitMask = 0x80 # bit mask for parsing bits in the bytes of the frame
            self.currentByteBeingParsed = 0 # stores current byte of the payload being parsed
            
            self.payloadLength = 0 # length of the payload expressed in bytes (not including CRC)
            self.payload = [] # list of bytes of the payload, big endian
            self.crc = [] # list of bytes of the crc, big endian
            
            self.currentDewhiteningKey = initial_PRBS_key # initial key for dewhitening
            
            
    # Constructor
    def __init__(self, channelNumerator=1, initial_Dewhitening_key=0x1FF, debug_Log_frame=False, debug_Log_control_traces=False):  # default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__( # father constructor call
            self,
            name='Verisure Tagged Bistream to PDU',   # will show up in GRC
            in_sig=[np.int8,np.float32,np.float32],
            out_sig=None # there is no output stream
        )

        self.message_port_register_out(pmt.intern('pdu_out')) # output message port definition

        # block constants definition
        self.BITS_IN_A_BYTE = 8
        self.CRC_LENGTH = 16 # in bits

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.channelNumber = channelNumerator # number of channel for displaying on RfAnalyzer
        self.dewhitening_key_init = initial_Dewhitening_key
        self.logBlock = debug_Log_frame # debug log switch for frame info
        self.logCtrl = debug_Log_control_traces # debug log switch for internal block control depuration traces

        # block atributes initialization (retain data between calls of the work function) 
        self.currentFrameInProcess = None # stores the Frame being parsed between two calls of the work function
        
        # self.msb_0 = 0x80 # Used in Carlos dewhitening algorithm
        # self.msb_1 = 0x80

    def work(self, input_items, output_items): # called for every buffer of samples received
        
        # finish processing the currentFrameInProcess from the previous call to the work function
        if self.currentFrameInProcess != None:
            processedFrame, returnValue = self.continueFrameProcessing(input_items, self.currentFrameInProcess)
            if returnValue == 1:      # if the parsing of the currentFrameInProcess from the previous window is finished then clean currentFrameInProcess
                self.currentFrameInProcess = None  
            elif returnValue == 0:    # else, currentFrameInProcess will be updated to be processed on next window
                self.currentFrameInProcess = processedFrame

        tags = self.get_tags_in_window(0, 0, len(input_items[0])) # gets all tags in current buffer. Params: input, rel. start, rel. end
        
        for tag in tags: # itereate over all tags of the window in chronological order. 
                         # on case of error of a length field, a new tag always has priority over the last
                         # that is why self.currentFrameInProcess can be overwrited multiple times

            if self.logCtrl: print ('New tag has been detected')

            tagAbsPosition = tag.offset # absolute position of the tag in the stream

            if self.logBlock: # Debug
                key = pmt.to_python(tag.key) # convert from PMT to python string
                value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
                index = tagAbsPosition - self.nitems_read(0) # index == relative position of the tag in the current buffer
                print ('')
                print ('   1. Verisure Tagged Bistream to PDU debug message:')
                print (' .----------------------------------------->')
                print (' | Channel Number:', self.channelNumber)
                print (' | Input tag key:', key)
                print (' | Input tag value:', value)
                print (' | Input tag value type:', type(value))
                print (' | Input tag abs. position (offset):', tagAbsPosition)
                print (' | Input tag rel. position (offset):', index)

            processedFrame, returnValue = self.startFrameProcessing(tagAbsPosition, input_items) 
            if returnValue == 1:      # if the parsing of the frame is finished then clean currentFrameInProcess
                self.currentFrameInProcess = None  
            elif returnValue == 0:    # else, last frame will be overwrited
                self.currentFrameInProcess = processedFrame
            
        return len(input_items[0])
    
    
    def startFrameProcessing(self, tagAbsoluteOffset, input_items): # initiates the process of a frame (called when a tag is found in the stream)

        if self.logCtrl: print ('Start Frame Processing')

        # initializing values for a new frame
        timestamp = datetime.timestamp(datetime.now()) # getting the timestamp from datetime
        power = input_items[1][tagAbsoluteOffset - self.nitems_read(0)] # reads power input @ tag time
        freqError = input_items[2][tagAbsoluteOffset - self.nitems_read(0)] # reads freq. error input @ tag time
        
        currentFrame = self.Frame(tagAbsoluteOffset, timestamp, power, freqError, self.dewhitening_key_init) # creates a frame object
        return self.continueFrameProcessing(input_items, currentFrame)
        
    
    def continueFrameProcessing(self, input_items, currentFrame): # parses a frame until the actual buffer is empty or the last bite of the crc is parsed

        if self.logCtrl: print ('Continue Frame Processing')
        
        # position of tag in current window (may be < 0 if the tag was captured in a previous call to the work function)
        frameTagRelativePosition = currentFrame.tagAbsolutePosition - self.nitems_read(0) 
        
        while frameTagRelativePosition + currentFrame.nextBitIndexToParse < len(input_items[0]): # iterate over current window samples
            
            # 1. [HEADER LENGTH] field parsing
            if currentFrame.nextBitIndexToParse < self.BITS_IN_A_BYTE: 

                if input_items[0][frameTagRelativePosition + currentFrame.nextBitIndexToParse] != 0: 
                    currentFrame.payloadLength |= currentFrame.byteBitMask # raises a bit in the length byte
                currentFrame.byteBitMask >>= 1  # updates bitmask

                if currentFrame.nextBitIndexToParse == self.BITS_IN_A_BYTE - 1: # last bite of the whitened length field is saved
                    currentFrame.payloadLength = (0xFF & (currentFrame.payloadLength ^ currentFrame.currentDewhiteningKey)) # dewhitening
                    currentFrame.byteBitMask = 0x80 # resets the bit mask for reusing it in payload parsing

            # 2. [PAYLOAD] parsing   
            elif currentFrame.nextBitIndexToParse < self.BITS_IN_A_BYTE + self.BITS_IN_A_BYTE * currentFrame.payloadLength: 

                if input_items[0][frameTagRelativePosition + currentFrame.nextBitIndexToParse] != 0:
                    currentFrame.currentByteBeingParsed |= currentFrame.byteBitMask # raises a bit in the current byte
                currentFrame.byteBitMask >>= 1 # updates bitmask

                if (currentFrame.nextBitIndexToParse - self.BITS_IN_A_BYTE) % self.BITS_IN_A_BYTE == self.BITS_IN_A_BYTE - 1:  # last bit of the byte
                    currentFrame.currentDewhiteningKey = self.calculateNextPRBSkey(currentFrame.currentDewhiteningKey) # updates dewhitening key
                    dewhitenedByte = 0xFF & (currentFrame.currentByteBeingParsed ^ currentFrame.currentDewhiteningKey) # aplies dewhitening with the key
                    currentFrame.payload.append(dewhitenedByte) # stores current byte
                    currentFrame.byteBitMask = 0x80 # resets the bit mask
                    currentFrame.currentByteBeingParsed = 0 # resets the current byte (starts over from 0)

            # 3. [CRC] parsing
            elif currentFrame.nextBitIndexToParse < self.BITS_IN_A_BYTE + self.BITS_IN_A_BYTE * currentFrame.payloadLength + self.CRC_LENGTH: 
               
                if input_items[0][frameTagRelativePosition + currentFrame.nextBitIndexToParse] != 0:
                    currentFrame.currentByteBeingParsed |= currentFrame.byteBitMask # raises a bit in the current byte
                currentFrame.byteBitMask >>= 1 # updates bitmask

                if (currentFrame.nextBitIndexToParse - self.BITS_IN_A_BYTE) % self.BITS_IN_A_BYTE == self.BITS_IN_A_BYTE - 1:  # last bit of the byte
                    currentFrame.currentDewhiteningKey = self.calculateNextPRBSkey(currentFrame.currentDewhiteningKey) # updates dewhitening key
                    dewhitenedByte = 0xFF & (currentFrame.currentByteBeingParsed ^ currentFrame.currentDewhiteningKey) # aplies dewhitening with the key
                    currentFrame.crc.append(dewhitenedByte) # stores current byte
                    currentFrame.byteBitMask = 0x80 # resets the bit mask
                    currentFrame.currentByteBeingParsed = 0 # resets the current byte (starts over from 0)     
               
            # 4. END
            else: # end of frame (the last bit of the crc has been parsed)
                self.endFrameProcessing(currentFrame)
                return currentFrame, 1 # == the current frame has been parsed successfully (end of the frame)
                
            currentFrame.nextBitIndexToParse += 1 # process next bit
            
        return currentFrame, 0 # == the current frame will have to continue being parsed on next call to work function


    def endFrameProcessing(self, currentFrame): # finish processing of frame and packs & sends the PDU through message port

        if self.logCtrl: print ('End Frame Processing')

        if self.logBlock: # Debug
            binaryPayload = []
            for byte in currentFrame.payload:
                binaryPayload.append(format(byte, "08b"))
            print (' | Payload length:', currentFrame.payloadLength)
            print (' | Captured payload in DEC:', currentFrame.payload)
            print (' | Captured payload in BIN:', binaryPayload)
            print (' | Captured CRC in DEC:', currentFrame.crc)
            print (' | Timestamp:', currentFrame.timestamp)
            print (' | Date and Time:', datetime.fromtimestamp(currentFrame.timestamp))
            print (' | Power:', currentFrame.power)
            print (' | Freq. error:', currentFrame.freqError)
            print (' *----------------------------------------->')
            print ('')
            
            
        metadataDictionary = pmt.make_dict()
        metadataDictionary = pmt.dict_add(metadataDictionary, pmt.intern("channel_number"), pmt.from_double(self.channelNumber))
        metadataDictionary = pmt.dict_add(metadataDictionary, pmt.intern("payload_length"), pmt.from_long(currentFrame.payloadLength)) # args: dictionary, key, value
        metadataDictionary = pmt.dict_add(metadataDictionary, pmt.intern("crc"),  pmt.to_pmt(currentFrame.crc)) 
        metadataDictionary = pmt.dict_add(metadataDictionary, pmt.intern("timestamp"),  pmt.from_double(currentFrame.timestamp)) 
        metadataDictionary = pmt.dict_add(metadataDictionary, pmt.intern("power"),  pmt.from_double(float(currentFrame.power))) 
        metadataDictionary = pmt.dict_add(metadataDictionary, pmt.intern("freq_error"),  pmt.from_double(float(currentFrame.freqError))) 
        pdu = pmt.cons(metadataDictionary, pmt.to_pmt(currentFrame.payload)) # builds a GNU Radio standarized PDU
        self.message_port_pub(pmt.intern('pdu_out'), pdu) # publishes PDU to subscriber blocks. args: port, message
        
  
    # DEWHITENING-----------
       
    def calculateNextPRBSkey(self, currentKey): # calculates the next key of the pseudo random binary sequence with PRBS9 polynomial (DEWHITENING)
        key = currentKey
        for i in range (0,8):
            msb = 0x1 & (key ^ (key >> 5)) # 1 bit, corresponds to the xor operation between bits 0 and 5 of the last key
            nextKeyLsbByte = 0xFF & (key >> 1) # generates the 8 lsb's of the new key by shifting
            key = (msb << 8) | nextKeyLsbByte # adds the precalculated msb to the 8 lsbs
        return key
    
    """
    # Carlos Algorithm (produces same result)
    def calculateNextPRBSkey(self, currentKey): # calculates the next key of the pseudo random binary sequence with PRBS9 polynomial (DEWHITENING)
        key = currentKey
        for i in range (0,8):
            self.msb_1 = 0xFF & (((key & 0x01) ^ ((key & 0x20)>>5))<<7)
            key = (key>>1) | (0xFF & self.msb_0)
            self.msb_0 = (0xFF & self.msb_1)
        return key
    """    
