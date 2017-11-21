def string_comparison(string1, string2):
	if string1 == string2:
		return 1
	elif len(string1) > len(string2):
		return 2
	elif string2 == 'learn':
		return 3