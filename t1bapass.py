import vk_api

vk_session = vk_api.VkApi("+375447022103", "6626816")
vk_session.auth()
vk = vk_session.get_api()
posts = vk.newsfeed.get(count=3)