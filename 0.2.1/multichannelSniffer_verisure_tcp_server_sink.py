"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

from concurrent.futures.thread import _threads_queues
import numpy as np
from gnuradio import gr
import pmt
from datetime import datetime  # for timestamping recovering
import socketserver  # for TCP server
# import socket # for TCP server, deprecated
import threading
import queue
import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Verisure TCP Server Sink block class"""

    # constructor for the block class:
    def __init__(self, block_Failed_CRC_frames=False, host='127.0.0.1', port=1337, server_mode=1,  debug_Log_Frame=False, high_Verbosity_Frame_Log=False,  debug_Log_Server=False):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Verisure TCP Server Sink',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )

        # input message port definition
        self.message_port_register_in(pmt.intern('pdu_in'))
        # asociation of handler function to input
        self.set_msg_handler(pmt.intern('pdu_in'), self.handle_pdu)

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.hostIp = host
        self.portIp = port
        self.serverMode = server_mode
        self.blockFailedCRC = block_Failed_CRC_frames
        self.log = debug_Log_Frame
        self.highLogVerbosity = high_Verbosity_Frame_Log
        global logServer
        logServer = debug_Log_Server

        # maxQueueSize = 100 # optional param for queue.Queue()
        global tcpQueue  # thread-safe FIFO queue for sending data to the conection handler
        tcpQueue = queue.Queue()  # used when mode=0

        global threadsQueues
        # dictionary with key=threadId and value=(queue for a certain thread). Used when mode=1
        threadsQueues = {}

        if self.log:  # Debug Log
            self.msgCount = 0
            self.crcPassCount = 0
            self.crcFailCount = 0

        """
        # TCP server init
        try:
            self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET == IPv4, SCOKET_STREAM == TCP
            if self.log: print ("Socket successfully created")
        except self.tcpSocket.error as err:
            print ("socket creation failed with error %s" %(err))
        
        self.tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.tcpSocket.bind((hostIp, portIp)) #Binding == allocating a port number to a socket
        self.tcpSocket.listen(maxClients)

        # maxQueueSize = 100 # optional param for queue.Queue()
        self.tcpQueue = queue.Queue() # thread-safe FIFO queue for sending data to the server thread

        self.thread = threading.Thread(target=self.serverMain, args=(self.tcpSocket, self.tcpQueue))
        self.thread.start()
        """

    def handle_pdu(self, pdu):  # called when a pdu has been published to 'pdu_in' message port

        # access to the pdu parts:
        pduMetadataDictionary = pmt.car(pdu)  # first field of pdu extracted

        timeStamp = pmt.to_python(pmt.dict_ref(pduMetadataDictionary, pmt.intern(
            "timestamp"), pmt.PMT_NIL))  # access to timestamp
        date_time = datetime.fromtimestamp(timeStamp)
        hh = date_time.hour
        mm = date_time.minute
        ss = date_time.second
        ms = int(date_time.microsecond * 0.001)

        power = pmt.to_python(pmt.dict_ref(pduMetadataDictionary, pmt.intern(
            "power"), pmt.PMT_NIL))  # access to power
        # format to 3 digits whole number padding with non significative zeros
        rssi = "{:03.0f}".format(power)

        lqi = 1  # not suported by Verisure link frame. set as default

        freqError = pmt.to_python(pmt.dict_ref(pduMetadataDictionary, pmt.intern(
            "freq_error"), pmt.PMT_NIL))  # access to power
        # format to 4 digits whole number padding with non significative zeros
        f_err = "{:04.0f}".format(freqError)

        channel = int(pmt.to_python(pmt.dict_ref(pduMetadataDictionary, pmt.intern(
            "channel_number"), pmt.PMT_NIL)))  # access to channel number

        packetOk = int(pmt.to_python(pmt.dict_ref(pduMetadataDictionary, pmt.intern(
            "crc_check"), pmt.PMT_NIL)))  # access to crc check

        payloadLength = pmt.to_python(pmt.dict_ref(pduMetadataDictionary, pmt.intern(
            "payload_length"), pmt.PMT_NIL))  # access to payload_length key

        # second field of pdu extracted, which is the payload vector
        pduPayloadVector = pmt.to_python(pmt.cdr(pdu))
        tcpPayload = ""

        # converts payload list of bytes to a hex formatted string
        for i in range(0, len(pduPayloadVector) - 1):
            tcpPayload = tcpPayload + \
                "{:02X}".format(pduPayloadVector[i]) + " "
        tcpPayload = tcpPayload + \
            "{:02X}".format(pduPayloadVector[len(
                pduPayloadVector) - 1])  # last element

        msg = f"T{hh}:{mm}:{ss}.{ms},R{rssi},L{lqi},E{f_err},A{channel},C{packetOk},X0*{tcpPayload}#\n"

        if self.log:  # Debug
            if self.msgCount == 0:
                print('')  # spacer
                print('')
            if self.highLogVerbosity:
                print('   Verisure TPC Server Sink message:')
                print(' .----------------------------------------->')
                print(' | Timestamp:', timeStamp)
                print(' | Date and Time:', datetime.fromtimestamp(timeStamp))
                print(' | |-> Hour:', hh)
                print(' | |-> Minute:', mm)
                print(' | |-> Second:', ss)
                print(' | |-> Millisecond:', ms)
                print(' | RSSI:', rssi)
                print(' | LQI:', lqi)
                print(' | Frequency Error in Hz:', f_err)
                print(' | Channel Number:', channel)
                print(' | CRC Check:', 'PASSED' if packetOk else 'FAILED')
                print(' | Payload Length:', payloadLength)
                print(' | Dewhitened Payload Data in DEC:', pduPayloadVector)
                print(' | Payload Formatted String (HEX):', tcpPayload)
                print(' | Final Formatted String:', msg + " |")
                print(' | TCP Queue Size:', tcpQueue.qsize())
                print(' *----------------------------------------->')
            else:
                self.msgCount += 1
                if packetOk:
                    self.crcPassCount += 1
                else:
                    self.crcFailCount += 1
                passPercentage = (self.crcPassCount/(self.msgCount))*100
                passPercentage = "{:03.4f}".format(passPercentage)
                fixedDigitsMs = "{:03.0f}".format(ms)
                print(f">{hh}:{mm}:{ss}.{fixedDigitsMs} | Ch = {channel} | RSSI = {rssi} | freq.Err = {f_err} Hz | PayloadLength = {payloadLength} | CRC Check: {'PASSED' if packetOk else 'FAILED'} | CRCPass = {passPercentage} % | (FailedCRC/AllReceivedCount) = {self.crcFailCount} / {self.msgCount} | Total Passed Count = {self.crcPassCount}")

        if self.blockFailedCRC:
            if packetOk:
                self.putPDUIntoQueues(msg)
        else:
            self.putPDUIntoQueues(msg)

    def putPDUIntoQueues(self, pdu):

        if self.serverMode == 0:
            global tcpQueue
            # puts the pdu into queue for sending. If queue is full, raises Full exception
            tcpQueue.put(pdu, block=False)
        elif self.serverMode == 1:
            global threadsQueues
            for threadId in threadsQueues.keys():  # puts the pdu in all queues of the dictionary "threadsQueues"
                try:
                    # puts the pdu into queue for sending. If queue is full, raises Full exception
                    threadsQueues[threadId].put(pdu, block=False)
                except:
                    pass

    # def set_channel(self, channel): # setter method for updating channel from the exterior (grc) -> Deprecated
    #    self.channel = channel

    def start_TCP_server(self):  # called at Python Snippet after start of the flowgraph
        server = None
        if self.serverMode == 0:  # only sends PDUs to last client connection
            server = self.ThreadedTCPServer(
                (self.hostIp, self.portIp), self.ThreadedTCPRequestHandlerSingleConnection)
        elif self.serverMode == 1:  # sends PDUs to all client connections
            server = self.ThreadedTCPServer(
                (self.hostIp, self.portIp), self.ThreadedTCPRequestHandlerMultipleConnections)
        else:
            raise Exception('server_mode ', self.serverMode,
                            ' is not defined.')

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True  # TODO read documentation
        server_thread.start()

        global allThreadIds
        allThreadIds = []  # ids list for conection threads
        global logServer
        if logServer:
            print("Server loop running in thread:", server_thread.name)

    """
    def serverMain(self, socket, queue): # waits for conections and sends queued data
    
        try:
            clientsocket, clientAddress = socket.accept() # stablishes conection. this method is blocking (waits for client to connect)
        except:
            return # called for example if the sniffer is terminated before connecting to te client. kills the thread
        
        while True:
            
            msg = queue.get(block=True, timeout=None) # block if necessary until an item is available
            if msg == "tcpCloseClientConection": # sent from the closing snippet in order to close the TCP socket
                clientsocket.close()
                print('Client TCP socket has been closed') 
                socket.close() 
                print('Server TCP socket has been closed') 
            else: 
                clientsocket.send(bytes(msg, "ascii")) # sends string to client
    """

    # Server auxiliar inner classes: ~~~~~~~~~~~~~~~~~~~~

    # inherits from socketserver.BaseRequestHandler
    class ThreadedTCPRequestHandlerSingleConnection(socketserver.BaseRequestHandler):
        """
        The request handler class for our server.
        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
        """
        # only sends PDUs to last client connection

        def handle(self):  # overrides default method which does nothing. Listens to a request and sends data
            # self.request is the TCP socket connected to the client
            current_thread = threading.current_thread()
            thread_id = current_thread.ident
            global allThreadIds
            allThreadIds.append(thread_id)
            # in sec. Allows other conection threads to end conection because of queue timeout
            time.sleep(0.4)
            global logServer
            if logServer:
                print('TCP Server: A new conection request has been received from {}'.format(
                    self.client_address))
                print(
                    'TCP Server: That conection will be processed on thread {}'.format(thread_id))
            global tcpQueue
            while True:
                # only send PDU if we are in last conection
                if thread_id == allThreadIds[len(allThreadIds)-1]:

                    try:  # blocking version with timeout
                        # block if necessary until an item is available
                        msg = tcpQueue.get(block=True, timeout=0.1)
                        # if queue is empty for timeout seconds then an exception is raised and the while loop is started again
                        # this assures that the condition thread_id == allThreadIds[len(allThreadIds)-1] is met
                        # lowering the timeout increases CPU usage, but reduces risk of losing packets in changes of port
                        self.request.send(bytes(msg, "ascii"))
                    except:  # launched if tcpQueue is empty
                        pass
                else:
                    return

    # inherits from socketserver.BaseRequestHandler
    class ThreadedTCPRequestHandlerMultipleConnections(socketserver.BaseRequestHandler):
        """
        The request handler class for our server.
        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
        """
        # sends PDUs to all client connections

        def handle(self):  # overrides default method which does nothing. Listens to a request and sends data
            # self.request is the TCP socket connected to the client
            current_thread = threading.current_thread()
            thread_id = current_thread.ident

            global threadsQueues
            # thread-safe FIFO queue init. which is updated with incoming PDUs
            threadsQueues[thread_id] = queue.Queue()

            time.sleep(0.4)  # in sec.

            global logServer
            if logServer:
                print('TCP Server: A new conection request has been received from {}'.format(
                    self.client_address))
                print(
                    'TCP Server: That conection will be processed on thread {}'.format(thread_id))

            while True:

                try:  # blocking version
                    # block if necessary until an item is available
                    msg = threadsQueues[thread_id].get(
                        block=True, timeout=None)
                    # if queue is empty then an exception is raised and the while loop is started again
                    self.request.send(bytes(msg, "ascii"))
                except:  # launched if tcpQueue is empty
                    pass

    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass
