import requests
import pandas as pd

token = 'e6e1f104e6e1f104e6e1f10406e68e8992ee6e1e6e1f104b8d6e6a14b7ae74f3c198eea'

def get_subs_amount(group, token):
	# Получаем количетво подписчиков сообщества
	response = requests.get('https://api.vk.com/method/groups.getMembers', params={'group_id': group, 'v': 5.95, 'access_token': token})
	try:
		subscribers = response.json()['response']['count']
	except KeyError:
		return 'lol'

	try:
		return subscribers
	except UnboundLocalError:
		return 'KEK'



def get_wall_of_public(group, token):
	url = 'https://api.vk.com/method/wall.get'
	params = {
    	'domain': group,
    	'filter': 'owner',
    	'count': 100,
    	'offset': 0,
    	'access_token': token,
    	'v': 5.95
	}
	response = requests.get(url, params = params)
	return response.json()

def count_smm_parameters(parameter, data):
	i = 0
	parameter_amount = 0
	for x in data[parameter]:
		parameter_amount += data[parameter][i]['count']
		i += 1
	return parameter_amount

def get_smm_index(group, token):

	# Получаем количетво подписчиков сообщества
	subscribers = get_subs_amount(group, token)
	if type(subscribers) is not int:
		return 'Такой группы нет, либо к ней нет доступа, либо сервера вк упали'
	else:
		# Делаем запрос к VK API, чтобы получить стену паблика
		response = get_wall_of_public(group, token)

		# Запихиваем все в датафрейм потому, что - чё по кайфу, то и делаю
		df = pd.DataFrame(response['response']['items'])

		# Считаем параметры
		comments_sum = count_smm_parameters('comments', df)
		likes_sum = count_smm_parameters('likes', df)
		reposts_sum = count_smm_parameters('reposts', df)
		views = count_smm_parameters('views', df)
		
		interest_of_subs = ( likes_sum / views ) / 0.02 * 100
		if interest_of_subs > 100:
			interest_of_subs = 100

		# Считаем смм индекс
		amount_of_live_subs = ( comments_sum + likes_sum + reposts_sum ) / subscribers * 100
		if amount_of_live_subs > 100:
			amount_of_live_subs = 100
		return group, amount_of_live_subs, interest_of_subs

print(get_smm_index('boevayaclassicakrasnodar', token))