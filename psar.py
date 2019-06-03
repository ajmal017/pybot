function get_psar(data):
	
	last_min = data[0]
	last_max = data[0]
	stop = data[0] - 0.001
	
	acc = 0.01
	
	long_short = 'L'
	
	psar_list = []
	psar_obj = {}
	
	for i in range(data.length):
		
		if long_short == 'L':
					
			if data[i] < stop: #ausgestoppt
				
				long_short = 'S'
				stop = last_min
				acc = 0.01
			
			
			else:
				
				if data[i] > last_max: #bei neuem Hoch

					last_max = data[i]
					
					if acc < 0.1:
						acc = acc + 0.01
				
				stop = stop + acc*(last_max-stop)	
			
		elif not long_short == 'S':
			
			if data[i] > stop: #ausgestoppt
				
				long_short = 'L'
				stop = last_max
				acc = 0.01
			
			
			else:
				
				if data[i] > last_max: #bei neuem Tief

					last_min = data[i]
					
					if acc < 0.1:
						acc = acc + 0.01
				
				stop = stop + acc*(last_max-stop)
				
		psar_obj = {'pos':long_short, 'stop':stop}
		psar[i] = psar_obj