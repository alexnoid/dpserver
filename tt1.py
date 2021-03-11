# import sqlite3
# import contextlib
# import string
#
#
# def execute_statement(statement):
#     with contextlib.closing(sqlite3.connect('DB/data.db')) as conn: # auto-closes
#         with conn: # auto-commits
#             with contextlib.closing(conn.cursor()) as cursor: # auto-closes
#                 cursor.execute(statement)
#                 values = cursor.fetchall()
#                 return values
#
# log = "оааоао"
# pas = "ytbptcnty"
# string.Template('hanning${num}.pdf').substitute(locals()))
# query = f"select * from users"
# print(execute_statement(query))
import vk_api


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def main():
    """ Пример обработки капчи """

    login, password = '+375447022103', '6626816'
    vk_session = vk_api.VkApi(
        login, password,
        captcha_handler=captcha_handler  # функция для обработки капчи
    )

    try:
        vk_session.auth()
        vk = vk_session.get_api()
        print(vk.newsfeed.get(count=3))
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return


if __name__ == '__main__':
    main()