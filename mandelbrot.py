import matplotlib.pyplot
import numpy as np
import multiprocessing
import time

def mandelbrot(c, queue=None, max_iterations=100):
    z = 0
    for i in range(max_iterations):
        if abs(z) > 2:
            if queue != None:
                queue.put(i)
            return i
        z = z**2 + c
    if queue != None:
        queue.put(0)
    return 0

def mandelbrot_serial(xmin, xmax, ymin, ymax, N=100):
    x = [i for i in np.arange(xmin,xmax+1,(xmax-xmin+1)/N)]
    y = list(reversed([i for i in np.arange(ymin,ymax+1,(ymax-ymin+1)/N)]))
    big_list = [[mandelbrot(r+i*1j) for r in x] for i in y]
    return big_list



def mandelbrot_static(xmin, xmax, ymin, ymax, N=100):
    x = [i for i in np.arange(xmin,xmax+1,(xmax-xmin+1)/N)]
    y = list(reversed([i for i in np.arange(ymin,ymax+1,(ymax-ymin+1)/N)]))
    big_list = [[r+i*1j for r in x] for i in y]
    final_list = []
    q = multiprocessing.Queue()
    for i in big_list:
        mini_list = []
        for j in i:
            p1 = multiprocessing.Process(target=mandelbrot, args=(j, q))
            p1.start()
            mini_list.append(q.get())
        final_list.append(mini_list)
    return final_list


def mandelbrot_dynamic(xmin, xmax, ymin, ymax, N=100):
    x = [i for i in np.arange(xmin,xmax+1,(xmax-xmin+1)/N)]
    y = list(reversed([i for i in np.arange(ymin,ymax+1,(ymax-ymin+1)/N)]))
    big_list = [[r+i*1j for r in x] for i in y]
    with multiprocessing.Pool(8) as pool:
        final_list = [pool.map(mandelbrot, big_list[i]) for i in range(len(big_list))]
    return final_list


def main():

    #serial
    start = time.clock()
    matplotlib.pyplot.imshow(mandelbrot_serial(-2,2,-2,2))
    matplotlib.pyplot.show()
    end = time.clock()
    print('time: ',end-start)

    #static
    start = time.clock()
    matplotlib.pyplot.imshow(mandelbrot_static(-2,2,-2,2))
    matplotlib.pyplot.show()
    end = time.clock()
    print('time: ',end - start)

    #dynamic
    start = time.clock()
    matplotlib.pyplot.imshow(mandelbrot_dynamic(-2,2,-2,2))
    matplotlib.pyplot.show()
    end = time.clock()
    print('time: ',end - start)

    #saving image
    matplotlib.pyplot.imshow(mandelbrot_serial(-3,2,-2,2))
    matplotlib.pyplot.savefig('mandelbrot.png')



if __name__ == '__main__':
    main()
