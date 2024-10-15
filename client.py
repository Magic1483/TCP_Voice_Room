import pyaudio
import numpy 
import numpy
import soundfile as sf
import io
import socket
import sys
import threading
import argparse
import traceback
from pydub import AudioSegment

RATE = 22000
CHANNELS = 1
FRAMERATE = 1024

def RAW_2_OGG(raw_chunk):
    byte_io = io.BytesIO()
    signal = numpy.frombuffer(raw_chunk,dtype=numpy.float32)
    old = sys.getsizeof(raw_chunk)#!log

    sf.write(byte_io,signal,FRAMERATE,format='OGG')

    b = bytes(byte_io.getbuffer())
    return b

def OGG_2_RAW(ogg_chunk):
    byte_io = io.BytesIO()
    byte_io.write(ogg_chunk)
    byte_io.seek(0)

    data = sf.read(byte_io)
    return numpy.float32(data)

class TCP_CLIENT:
    def __init__(self,host='192.168.100.5', port=6000,not_rec = False):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((host,port))

        self.stop_event = threading.Event()
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        output=True,
                        frames_per_buffer=FRAMERATE)
        
        
        
        self.rec_th =  threading.Thread(target=self.recieve,name='VoiceRecieveThread')
        self.send_th = threading.Thread(target=self.send,name='[Test] VoiceSendThread')

        self.send_th.start()
        if not_rec != True:
            self.rec_th.start()

        
    
    def send(self):#recorder
        while True:
            if self.stop_event.is_set(): break
            try:
                data = self.stream.read(FRAMERATE)
                self.client.sendall(data)
            except:
                print('server close connection')
                traceback.print_exc()
                self.stop_event.set()
            
    
    
    def recieve(self):
        while True:
            if self.stop_event.is_set(): break
            try:
                data = self.client.recv(FRAMERATE*4)
                
                if data:
                    self.stream.write(data)
                else:
                    print('no data')
            except:
                print('server close connection')
                traceback.print_exc()
                self.stop_event.set()
            
    
    def stop(self):
        print("stop TCP CLIENT")
        self.client.close()
        self.stop_event.set()
        

        

        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--addr",help="addres of server format: 127.0.0.1:6000")
    parser.add_argument("-t","--test",action='store_true')

    args = parser.parse_args()
    
    client = TCP_CLIENT(args.addr.split(':')[0],int(args.addr.split(':')[-1]),not_rec=args.test)


    while client.stop_event.is_set() != True:
        inp = input(">")
        match inp:
            case "\help":
                print("<<--------->>")
                print("help message")
                print("\close for disconnect")
                print("<<--------->>")
            case "\close":
                client.stop()
                sys.exit(0)