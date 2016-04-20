from payutc.client import Client as payutc_client

def init_payutc_client():
	cli = payutc_client()
	return cli


def get_articles(client):
	pass


def get_sales(client, articles):
	pass


def launch_wall_street():
	print('Launching Wall Street...')
	# Idea : every 30 seconds, launching request to get article sales
	print('Connecting to Nemopay API...')
	cli = init_payutc_client()
	# Getting list of articles available for sale on PayUTC
	articles = get_articles(cli)
	# Getting sales
	sales = get_sales(cli, articles)
	new_prices = get_new_prices(cli, sales)
	update_prices(cli, new_prices)

if __name__ == '__main__':
	launch_wall_street()
