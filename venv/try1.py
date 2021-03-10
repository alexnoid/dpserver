"""
import vk_api
import csv

login = '+375447022103'
passwd = '6626816'

def write_csv(data):
    with open('vk_news.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow((data['author'],
                         data['text']))

def get_data(posts_count, posts):
    for i in range(0, posts_count):
            print(i)
            url = str(posts['items'][i]['owner_id'])
            print(url)
            if url[:1] == '-':
                author = 'https://vk.com/public' + url[1:]
            else:
                author = 'https://vk.com/id' + url
            print(author)
            text = posts['items'][i]['text']
            post = []
            post.append(text)
            print(post)
            print(10*'-')
            data = {
                'author': author,
                'text': post
                }
            print(data)
            write_csv(data)

def main():
    vk_session = vk_api.VkApi(login, passwd)
    vk_session.auth()
    vk = vk_session.get_api()
    request = str(input('Введите запрос:\n'))
    posts_count = int(input('Введите количество постов:\n'))
    next_from = 0
    if posts_count <= 200:
        posts = vk.newsfeed.search(q = request, count = posts_count, startfrom = next_from)
        print(posts)
        get_data(posts_count, posts)
    else:
        req_times = posts_count // 200
        last_req = posts_count % 200
        for k in range(0, req_times):
            posts = vk.newsfeed.search(q = request, count = 200, startfrom = next_from)
            next_from = posts['next_from']
            get_data(200, posts)
        posts = vk.newsfeed.search(q = request, count = last_req, startfrom = next_from)
        get_data(last_req, posts)

if __name__ == "__main__":
    main()
"""
import vk_api
import json

vk_session = vk_api.VkApi('+375447022103', '6626816')
vk_session.auth()

vk = vk_session.get_api()

posts = vk.newsfeed.get(start_from='50/5')
post = posts['items']
post4 = post[4]
posta = post4['attachments']
photo = posta[0]
sizes = photo['photo']
sizes1 = sizes['sizes']
size4 = sizes1[4]
# data = {}
#
#
# data['message1'] = []
# data['message1'].append({
#     'id': '1',
#     'photo.id': '1',
#     'text': 'текст поста1'
# })
# data['message2'] = []
# data['message2'].append({
#     'id': '2',
#     'photo.id': '2',
#     'text': 'текст поста2'
# })
print(posts['next_from'])

#with open('data.json', 'w', encoding='utf-8') as f:
#    json.dump(posts, f, ensure_ascii=False, indent=4)