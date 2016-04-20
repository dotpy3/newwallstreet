from payutc.client import Client as payutc_client

def init_payutc_client():
	print('Connecting to Nemopay API...')
	cli = payutc_client()
	return cli


def get_articles(client):
	pass


def get_sales(client, articles):
	pass


def get_new_prices(client, sales):
	# TODO ROMAIN : Generates the new sales for the articles, with the last sales given.
	pass


def update_prices(client, new_prices):
	# TODO ROMAIN : Threads update_price for every article to update
	pass


def update_price(client, article):
	pass


def launch_wall_street():
	print('Launching Wall Street...')
	# Idea : every 30 seconds, launching request to get article sales
	cli = init_payutc_client()
	# Getting list of articles available for sale on PayUTC
	articles = get_articles(cli)
	# Getting sales
	sales = get_sales(cli, articles)
	new_prices = get_new_prices(cli, sales)
	update_prices(cli, new_prices)

if __name__ == '__main__':
	launch_wall_street()
