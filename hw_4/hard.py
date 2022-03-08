import multiprocessing as mp
from multiprocessing.connection import PipeConnection
from threading import Thread
from time import sleep
import logging

STOP = b''


def child_a(queue: mp.Queue, pipe: PipeConnection):
    for recv in iter(queue.get, STOP):
        pipe.send(recv.lower())
        sleep(5)
    pipe.send(STOP)


def child_b(pipe_a: PipeConnection, pipe_main: PipeConnection):
    rot13 = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                          'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')
    for recv in iter(pipe_a.recv, STOP):
        s = recv.translate(rot13)
        pipe_main.send(s)
    pipe_main.send(STOP)


def input_thread(queue: mp.Queue):
    for s in iter(input, ''):
        logging.info(f'input: {s}')
        queue.put(s)
    queue.put(STOP)


def output_thread(pipe: mp.Pipe):
    for recv in iter(pipe.recv, STOP):
        logging.info(f'output: {recv}')
        print(recv)


def main():
    logging.basicConfig(filename='artifacts/hard.txt', level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)03d %(message)s',
                        datefmt='%H:%M:%S')
    A_queue = mp.Queue()
    send_to_b, recv_from_a = mp.Pipe()
    send_to_main, recv_from_b = mp.Pipe()
    thr_and_proc = [Thread(target=input_thread, args=(A_queue,)),
                    Thread(target=output_thread, args=(recv_from_b,)),
                    mp.Process(target=child_a, args=(A_queue, send_to_b)),
                    mp.Process(target=child_b, args=(recv_from_a, send_to_main))]
    [obj.start() for obj in thr_and_proc]
    [obj.join() for obj in thr_and_proc]


if __name__ == '__main__':
    main()
