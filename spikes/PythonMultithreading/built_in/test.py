from queue import Queue
from time import sleep
from threading import Thread

def print_num(thread_id, queue):
	while not queue.empty():
		data = queue.get()
		print(str(data)+" printed by thread "+str(thread_id))
		sleep(.25)

def main():
	nums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
	queue = Queue(len(nums))
	threads = []
	n = 5

	#load the queue	
	for num in nums:
		queue.put(num)
	
	#create n threads
	for i in range(1,n+1):
		threads.append(Thread(target = print_num, args = (i, queue)))
	
	#start threads
	for thread in threads:
		thread.start()

	#wait for threads to finish
	for thread in threads:
		thread.join()

if __name__ == "__main__":
	main()	
