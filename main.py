# coding: utf8

from datetime import datetime, timedelta
import traceback
from time import sleep

from config.settings import BEER_CATEGORIES

from payutc.client import Client as payutc_client

def get_category_name(id):
	if id == 10:
		return 'Bouteille'
	if id == 11:
		return 'Pression'

""" Get a connected PayUTC client

:returns the connected client
"""
def init_payutc_client():
	print('Connecting to Nemopay API...')
	cli = payutc_client()
	cli.loginApp()
	cli.loginBadge()
	print('Connexion complete!')
	return cli


""" Get all the articles in the selected categories
:client Connected PayUTC client
:all_products If we want to get all the articles, or only the ones available for sale

:returns a Python list of objects
	return = [{'name': 'Delirium Tremens', 'price': 180, 'categorie_id': 10, ...}]
	name: name of the product
	price: price of the product in cents
	categorie_id: category of the article
	image_path: S3 path of the image (for the nemopay API)
	image_url: url of the image
"""
def get_articles(client, all_products=False):
	articles_list = []
	for product in client.call('GESARTICLE', 'getProducts', fun_ids=[2]):
		if not all_products and not product['active']:
			continue
		if product['categorie_id'] not in BEER_CATEGORIES:
			continue
		if all_products:
			print('Loading ' + product['name'] + ' (' + get_category_name(product['categorie_id']) + ')' + '...')
		product_detail = client.call('GESARTICLE', 'getProduct', fun_id=2, obj_id=product['id'])['success']
		articles_list.append({
			'name': product_detail['name'],
			'actual_price': product_detail['price'],
			'id': product_detail['id'],
			'categorie_id': product_detail['categorie_id'],
			'image_path': product_detail['image_path'],
			'active': product_detail['active'],
			})
	return articles_list


def get_sales(client, articles):
	for article in articles:
		article['sales'] = 0
	ten_minutes_before = datetime.now() - timedelta(minutes=10, hours=2)
	export = client.call('TRESO', 'getExport', fun_id=2, start=ten_minutes_before.isoformat(),
		end=datetime.now().isoformat(), group_applications=False,
		group_locations=False, group_objects=True)
	for sale in export:
		for article in articles:
			if article['id'] == sale['obj_id']:
				article['sales'] += sale['quantity']
	return articles


""" Calculate the new price
:product Individual product
:ref_sales Reference of sales

:returns the product with an updated price
"""
def calculate_price(product, ref_sales):
	if product['sales'] == ref_sales:
		print(product['name'] + ' is selling average : price does not change.')
		return product['actual_price']
	elif product['sales'] > ref_sales:
		print(product['name'] + ' is selling very good : price goes up to ' + str((product['actual_price'] + 3) / 100) + '!')
		return product['actual_price'] + 3
	elif (product['actual_price'] - 2) >= int(product['original_price'] * 0.8):
		print(product['name'] + ' is selling badly : price goes down to ' + str((product['actual_price'] - 3) / 100) + '...')
		return product['actual_price'] - 3
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

	median_nb = int(len(products) * 0.3) - 1
	median = sorted_liste[median_nb]
	print('Median value: ' + median['name'] + ', with '+ str(median['sales']))

	for beer in sorted_liste:
		beer['new_price'] = calculate_price(beer, median['sales'])

	return sorted_liste


def update_prices(client, new_prices, restore=False):
	# TODO ROMAIN : Threads update_price for every article to update (one update_price per thread)
	for article in new_prices:
		update_price(client, article, restore)


def update_price(client, article, restore):
	if restore:
		print('Restoring '+article['name'] + '...')
	else:
		print('Updating '+article['name'] + ' to ' + str(article['new_price']/100.0) + '...')
	client.call('GESARTICLE', 'setProduct',
		fun_id=2, 
		name=article['name'],
		active=article['active'],
		alcool=True,
		cotisant=True,
		image_path=article['image_path'],
		obj_id=article['id'],
		parent=article['categorie_id'],
		prix=article['new_price'],
		stock=0,
		tva=20,
		)


def wall_street_active(iteration):
	if (iteration % 70 < 60):
		# wall street active
		return True
	else:
		# contrôle fiscal !
		return False


def controle_fiscal(articles, iteration):
	step = (iteration % 70) - 60
	print('Fiscal control - step ' + step + '!')
	for article in articles:
		article['new_price'] = article['actual_price'] + (article['original_price'] - article['actual_price']) / step
	return articles


def get_articles_with_original_price(client, all_articles):
	articles = get_articles(client)
	for article in articles:
		for article_original in all_articles:
			if article['id'] == article_original['id']:
				article['original_price'] = article_original['actual_price']
	return articles


def restore_original_prices(client, all_articles):
	print('Restoring prices...')
	for article in all_articles:
		article['new_price'] = article['actual_price']
	update_prices(client, all_articles, True)
	print('Restoration complete. Bye bye!')


def wall_street_loop(client, all_articles):
	iteration = 0
	while(True):
		# Getting list of articles available for sale on PayUTC
		articles = get_articles_with_original_price(client, all_articles)
		if wall_street_active(iteration):
			print('Analysis ongoing!')
			# Getting sales
			sales = get_sales(client, articles)
			new_prices = get_new_prices(sales)
		else:
			new_prices = controle_fiscal(articles, iteration)
		update_prices(client, new_prices)
		sleep(30)
		iteration += 1


def launch_wall_street():
	print('Launching Wall Street...')
	# Idea : every 30 seconds, launching request to get article sales
	cli = init_payutc_client()
	# Getting preleminary list of articles in case
	print('Getting all articles...')
	all_articles = get_articles(cli, True)
	print('Getting all articles: done!')
	try:
		wall_street_loop(cli, all_articles)
	except KeyboardInterrupt:
		restore_original_prices(cli, all_articles)
	except Exception as e:
		traceback.print_exc()
		restore_original_prices(cli, all_articles)

if __name__ == '__main__':
	launch_wall_street()
