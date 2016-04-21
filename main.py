from payutc.client import Client as payutc_client

def init_payutc_client():
	print('Connecting to Nemopay API...')
	cli = payutc_client()
	return cli


def get_articles(client):
	pass


def get_sales(client, articles):
	pass


def calculate_price(product, ref_sales):
    if product['sales'] == ref_sales:
        return product['original_price']
    elif product['sales'] > ref_sales:
        return product['actual_price'] + 2
    elif (product['actual_price'] - 2) >= int(product['original_price'] * 0.8):
        return product['actual_price'] - 2
    return product['actual_price']


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
    sorted_liste = sorted(products, key=lambda beer: beer['sales'])

    median_nb = int(len(liste) * 0.3) - 1
    median = sorted_liste[median_nb]

    #print "\n\nElected median", median

    for beer in sorted_liste:
        beer['new_price'] = calculate_price(beer, median['sales'])

    return sorted_liste


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
