



class Producer():

	def produce(self, queue, url, capacity):
		
		while len(queue) > capacity:
			sys.sleep(1)

		queue.append(url)


class Consumer():

	def consume(self, queue):

		if not queue:
			while not queue:
				sys.sleep(1)
		
		return queue.popleft()



