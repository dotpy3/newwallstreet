from payutc.client import Client as payutc_client

def init_payutc_client():
	print('Connecting to Nemopay API...')
	cli = payutc_client()
	return cli


def get_articles(client):
	pass


def get_sales(client, articles):
	pass

""" Get the new prices
:products Python list of objects
    products = [{'id': 565, 'sales': 50, 'actual_price': 150, 'original_price': 155}, ...]
    id: product's id
    sales: number of sales in the last 10minutes
    actual_price: in cents
    original_price: in cents
:returns the same list, each product gets a new property 'new_price'
"""
def get_new_prices(products):
	# TODO ROMAIN : Generates the new sales for the articles, with the last sales given.
        # 1. We sort the products according to their sales units like
        # 2. Get the 3rd decile value
        # 3. if (current_beer.sales == median) ==> restore the original price
        #    else if (... < median ) ==> we lower the price. current_price - 2 (until we reach original_price * 0.8)
        #    else current_price + 2

	pass

def update_prices(client, new_prices):
	# TODO ROMAIN : Threads update_price for every article to update (one update_price per thread)
	pass


def update_price(client, article):
        # TODO Eric
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
