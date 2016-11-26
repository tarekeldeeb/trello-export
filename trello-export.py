import os, sys, argparse, json, csv



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("inputfile", help="the json file containing trello board data")
	parser.add_argument("--outputfile", help="the json file containing trello board data")
	args = parser.parse_args()
	f = open(args.inputfile)
	json_object = json.load(f, encoding="ISO-8859-1")
	print_cards(json_object, args.outputfile)
	


def print_cards(json_object, outputfile):
	
	def checklist_data(card):
		if len(card['idChecklists']) > 0:
			checklist_id = card['idChecklists'][0]
		else:
			return ''
		checklists = sorted(json_object['checklists'], key=lambda k: k['id'])
		checklist = {}
		for check in checklists:
			if check['id'] == checklist_id:
				checklist = check
				break
		string = ''
		for item in checklist['checkItems']:
			string += item['name'] + '\n'
		return string[:-1] 

	def comments_data(card):
		card_id = card['id']
		comments = []
		for action in json_object['actions']:
			if ('card' in action['data'] and
				action['data']['card']['id'] == card_id and 
				action['type'] == 'commentCard'):
				comments.append(action['data']['text'])
		return '\n'.join(comments)

	def status(card):
		if card['closed']:
			return 'Archived'
		else:
			for single_list in json_object['lists']:
				if single_list['id'] == card['idList']:
					return single_list['name']

	def labels(card):
		label = ''
		for lbl in card['labels']:
			label += lbl['name'] + '\n'
		return label[:-1] 
	def members(card):
		member_string = ''
		for member in card['idMembers']:
			for member_obj in json_object['members']:
				if member_obj['id'] == member:
					member_string += member_obj['fullName'] + '\n'
					break
		return member_string[:-1]

	def print_types():
		actions = []
		for action in json_object['actions']:
			if action['type'] in actions:
				continue
			else:
				actions.append(action['type'])
		print actions

	def safe_string(string):
		if string != None:
			return string.encode('ascii', 'ignore')
		else:
			return ''



	cards = sorted(json_object['cards'], key=lambda k: k['idShort'])
	if outputfile != None:
		filename = outputfile
	else:
		filename = 'output.csv'
	with open(filename, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['ID', 'Story', 'Status', 'Description', 'Checklist', 'Comments', 'Labels', 'Due Date', 'Members'])
		for card in cards:
			writer.writerow([
				card['idShort'], 
				safe_string(card['name']),
				safe_string(status(card)),
				safe_string(card['desc']), 
				safe_string(checklist_data(card)),
				safe_string(comments_data(card)), 
				safe_string(labels(card)), 
				safe_string(card['due']), 
				safe_string(members(card))
			]) 

		print_types()



if __name__ == "__main__":
	main()
