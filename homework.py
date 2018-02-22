import requests

# Формирование ссылки для получения токена
# APP_ID = '681e96b42ed347bbb2b5e2798d8e69f7'
# params = {
#     'response_type': 'token',
#     'client_id': APP_ID
# }
# print('?'.join(('https://oauth.yandex.ru/authorize', urlencode(params))))

TOKEN = 'СЮДА ВСТАВИТЬ СВОЙ ТОКЕН'


class YMbase:
    token = None

    @property
    def headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def __init__(self, token):
        self.token = token


class YMcounters(YMbase):
    url = 'https://api-metrika.yandex.ru/management/v1/counters'

    def get_counter_list(self):
        response = requests.get(self.url, headers=self.headers)
        counter_ids = []
        for counter in response.json()['counters']:
            counter_ids.append(counter['id'])
        return counter_ids


class YMrepots(YMbase):
    url = 'https://api-metrika.yandex.ru/stat/v1/data'
    params = {}

    def __init__(self, counter_id, token):
        self.params['ids'] = counter_id
        super().__init__(token)

    def get_metric(self, metric):
        self.params['metrics'] = metric
        response = requests.get(self.url, self.params, headers=self.headers)
        self.params.pop('metrics')
        return response.json()['data'][0]['metrics'][0]

    @property
    def visits(self):
        return self.get_metric('ym:s:visits')

    @property
    def pageviews(self):
        return self.get_metric('ym:s:pageviews')

    @property
    def users(self):
        return self.get_metric('ym:s:users')


all_counters = YMcounters(TOKEN).get_counter_list()

for counter in all_counters:
    report = YMrepots(counter, TOKEN)
    print('Счетчик номер {}'.format(counter))
    print('Количество визитов: {}'.format(report.visits))
    print('Количество просмотров: {}'.format(report.pageviews))
    print('Количество посетителей: {}'.format(report.users))

