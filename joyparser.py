# "Conda_env_3.7"
import requests as rq
from bs4 import BeautifulSoup as bs
import os, os.path
import time
import urllib.parse



def parser(page, from_page, until_page=-1, on_text_tags=False, on_info=False):

    data_text = {}
    text_tags = {}
    comments = {}
    post_info = {}
    images = {}

    while not from_page == until_page:
        print("scanning:", page + "/" + str(from_page))

        # функция если  проблемы с интеренетом
        def getpage(page, from_page):
            try:
                s = rq.Session()
                # getting url
                url = s.get(page + "/" + str(from_page))
                return url
            except Exception:
                print(
                    "упс, похоже что то произошло интернетом, пожалуста проверьте соединение и переподключитесь к впн")
                # sleep for a bit in case that helps
                input("для переподключения введите все что угодно:")
                # try again
                return getpage(page, from_page)

        soup = bs(getpage(page, from_page).content, "html.parser")

        # сам парсер

        def info(i, ty, file_tag, path):
            for ay in i.select(path):
                # creating dict with tags
                file_tag.setdefault(ty, []).append("{}".format(ay.text))
            return file_tag

        def infolist(i, ty, file_tag, atr, path):
            for ay in i.select(path):
                # creating dict with tags
                file_tag.setdefault(ty, []).append("{}".format(ay[atr]))
            return file_tag

        atr = ["a", "img"]  # "a" - большие изображения которые надо разворачивать + гифки
        # "img" - мелкие изображения которые слишком малы что бы разворачивать
        global key
        data = []

        datatext = {}
        dataimage = {}
        rating_DMY_hm_postlink = {}
        bestcommenttext_userinfo_avatar_pic = {}
        index = 0
        file_tag = {}
        # block selection
        for i in soup.select(".article"):
            # create post number as dict key
            for ay in i.select(".ufoot > div > .link_wr > a"):
                key = os.path.basename(ay["href"])

            for i2 in i.select(".post_content "):

                if on_text_tags:
                    # парс текста в посте если он имеется
                    for io in i2.select("div"):
                        if io.text:
                            datatext.setdefault(key, []).append("{}".format(io.text))
                    # tag web
                    # block selection

                    # теги
                    x = info(i, key, file_tag, ".post_top > .taglist > b > a")
                    file_tag = x
                if on_info:
                    # рейтинг поста
                    x = info(i, key, rating_DMY_hm_postlink, ".ufoot > div > .post_rating > span")
                    rating_DMY_hm_postlink = x
                    # дата  день год месяц точное время

                    x = info(i, key, rating_DMY_hm_postlink, ".ufoot > div > .date > span > span")
                    rating_DMY_hm_postlink = x

                    # ссылка на пост

                    # лучший коммент (если он есть) тексты + имя юзеров  и тд + прикрепленные пикчи и аватары
                    x = info(i, key, bestcommenttext_userinfo_avatar_pic, '.post_comment_list > div > div')
                    bestcommenttext_userinfo_avatar_pic = x

                    x = infolist(i, key, bestcommenttext_userinfo_avatar_pic, "src",
                                 '.post_comment_list > div > div > img')
                    bestcommenttext_userinfo_avatar_pic = x

                # print(i2)
                for i3 in i2.select(".image "):
                    # print(i3)
                    for i4 in i3.findAll(atr[index:]):

                        if i4.has_attr("href"):
                            # print(i4)
                            # decode urlencoded and add to list
                            dataimage.setdefault(key, []).append("{}".format(urllib.parse.unquote(i4["href"])))

                            break

                        else:
                            # print(i2)
                            if i4.has_attr("src"):
                                # decode urlencoded and add to list
                                dataimage.setdefault(key, []).append("{}".format(urllib.parse.unquote(i4["src"])))

                            break

                    # дает некоторую информацию о посте

        from_page -= 1
        # counter

        # извлекаем ссылки на пикчи (номер_поста:[картанка1, картинка2])
        images.update(dataimage)
        # извлекаем текст
        data_text.update(datatext)
        # создаем дикт с ключами номера поста  это теги файлов
        text_tags.update(file_tag)
        # лучшие коменты и тд
        comments.update(bestcommenttext_userinfo_avatar_pic)
        # пачка информации о посте
        post_info.update(rating_DMY_hm_postlink)
        print("posts scanned:", len(images.values()))
        # не трогать блэт. сайт может забанить если запросов больше чем определенное значение
        # бан на какой то промежуток по ip вероятнее всего и может еще и по headers(это переменная request)
        # фиксится библиотекой stem не я вам этого не говорил, и это не хорошо
        # возможно proxifier вместе с tor browser прокатит
        time.sleep(1)
    return images, data_text, text_tags, comments, post_info




# Saving the objects:





# пример применения функции инфо - сортировка по рейтингу
def sort_by_rating(linksbase, info, rating):
    sorted_links = {}
    print("sorting by rating...")
    for me in linksbase:
        if float(info[me][0]) >= rating:
            sorted_links.setdefault(me, linksbase[me])
    lk = sorted_links
    return lk




# def duplicate(x):
#   print(len(list(dict.fromkeys(x))))
#   return list(dict.fromkeys(x))
def get_rdy(images):
    """it's just convert to list"""
    ln = []
    for link in images.values():
        ln.extend(link)
    return ln



def download_images(images,download_path, warn_on = True):
    def downloader(links,d_path):
        print("download starting...\nначинаю загрузку...")

        # это данные которые передаются при запросе к link
        # таким образом я обманываю сайт

        request = ({
            'Host': 'img10.reactor.cc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'image/webp,*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://joyreactor.cc/',
            'Connection': 'keep-alive',

            'Cache-Control': 'max-age=0',
            'Pragma': 'no-cache'
        })

        counter = int(len(links))

        # функция если у вас проблемы с интеренетом
        def getimage(Im_link, request, path_FileBaseName):
            try:
                time.sleep(1)  # don't touch it coz ping need to not overload website or get frecking ban
                # не трогать задержка нужна что бы не перегружать вэбсайт и не получить ебаный бан от сайта
                with open(path_FileBaseName, 'wb') as f:  # открываем файл
                    f.write(rq.get(Im_link, headers=request).content)
                    # делаем запрос на получение файла

            except Exception:
                print(
                    "упс, похоже что то произошло интернетом, пожалуста проверьте соединение и "
                    "переподключитесь к впн")
                # sleep for a bit in case that helps
                input("для переподключения введите все что угодно:")
                # try again
                return getimage(Im_link, request, path_FileBaseName)

        for Im_link in links:  # итерация хуяция

            print("files left:", counter)
            counter = counter - 1

            path_FileBaseName = d_path + os.sep + os.path.basename(Im_link)
            # проверяем существует ли файл в диооектории

            if not os.path.exists(path_FileBaseName):

                getimage(Im_link, request, path_FileBaseName)
            else:
                print("Файл (" + os.path.basename(Im_link) + ") уже существует в директории (" + d_path + ")")
    if warn_on:
        if len(images) == 0:
            print("files does not found")
        else:
            print("\n\nDownload", len(images), "files?\n\n")
            x = input("Proceed ([y]/n)?\n\n")
            if x.lower() == "y":
                downloader(images,download_path)

    else:
        print("files found:", len(images))
        downloader(images)








# создаем сохранение переменной

#with open(urllib.parse.unquote(os.path.basename(page)) +
#          "_pic" + "(" + str(from_page_pickle) + "-" + str(till_page) + ")" + ".pkl", 'wb') as f:
#    pickle.dump(linksbase, f)
#with open(urllib.parse.unquote(os.path.basename(page)) +
#          "_info" + "(" + str(from_page_pickle) + "-" + str(till_page) + ")" + ".pkl", 'wb') as f:
#    pickle.dump(inf, f)

__version__ = "0.3"
__author__ = "ExE https://github.com/ExecutorExe"