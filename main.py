import json
import requests
import urllib.parse
import time
import datetime
import random
import os
from cache import cache


max_api_wait_time = 3
max_time = 10
version = "1.0"

apis = [
    r"https://iv.datura.network/",
    r"https://invidious.private.coffee/",
    r"https://invidious.protokolla.fi/",
    r"https://invidious.perennialte.ch/",
    r"https://yt.cdaut.de/",
    r"https://invidious.materialio.us/",
    r"https://yewtu.be/",
    r"https://invidious.fdn.fr/",
    r"https://invidious.qwik.space/",
    r"https://invidious.privacyredirect.com/",
    r"https://invidious.drgns.space/",
    r"https://vid.puffyan.us",
    r"https://invidious.jing.rocks/",
    r"https://invidious.nerdvpn.de/",
    r"https://vid.puffyan.us/",
    r"https://inv.riverside.rocks/",
    r"https://invidio.xamh.de/",
    r"https://y.com.sb/",
    r"https://invidious.sethforprivacy.com/",
    r"https://invidious.tiekoetter.com/",
    r"https://inv.bp.projectsegfau.lt/",
    r"https://inv.vern.cc/",
    r"https://iteroni.com/",
    r"https://inv.privacy.com.de/",
    r"https://invidious.rhyshl.live/",
    r"https://inv.nadeko.net/",
    r"https://invidious.weblibre.org/",
    r"https://invidious.namazso.eu/",
    r"https://invidious.jing.rocks",
]

apichannels = []
apicomments = []
[[apichannels.append(i),apicomments.append(i)] for i in apis]
class APItimeoutError(Exception):
    pass

def is_json(json_str):
    result = False
    try:
        json.loads(json_str)
        result = True
    except json.JSONDecodeError as jde:
        pass
    return result

def apirequest(url):
    global apis
    global max_time
    starttime = time.time()
    for api in apis:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apis.append(api)
                apis.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apis.append(api)
            apis.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

def apichannelrequest(url):
    global apichannels
    global max_time
    starttime = time.time()
    for api in apichannels:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apichannels.append(api)
                apichannels.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apichannels.append(api)
            apichannels.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

def apicommentsrequest(url):
    global apicomments
    global max_time
    starttime = time.time()
    for api in apicomments:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apicomments.append(api)
                apicomments.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apicomments.append(api)
            apicomments.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")


def get_info(request):
    global version
    return json.dumps([version,os.environ.get('RENDER_EXTERNAL_URL'),str(request.scope["headers"]),str(request.scope['router'])[39:-2]])
    
def get_data(videoid):
    global logs
    t = json.loads(apirequest(r"api/v1/videos/"+ urllib.parse.quote(videoid)))
    return [{"id":i["videoId"],"title":i["title"],"authorId":i["authorId"],"author":i["author"],"viewCountText":i["viewCountText"]} for i in t["recommendedVideos"]],list(reversed([i["url"] for i in t["formatStreams"]]))[:2],t["descriptionHtml"].replace("\n","<br>"),t["title"],t["authorId"],t["author"],t["authorThumbnails"][-1]["url"]

def get_search(q,page):
    global logs
    t = json.loads(apirequest(fr"api/v1/search?q={urllib.parse.quote(q)}&page={page}&hl=jp"))
    def load_search(i):
        if i["type"] == "video":
            return {"title":i["title"],"id":i["videoId"],"authorId":i["authorId"],"author":i["author"],"viewCountText":i["viewCountText"],"length":str(datetime.timedelta(seconds=i["lengthSeconds"])),"published":i["publishedText"],"type":"video"}
        elif i["type"] == "playlist":
            return {"title":i["title"],"id":i["playlistId"],"thumbnail":i["videos"][0]["videoId"],"viewCountText":i["viewCountText"],"type":"playlist"}
        else:
            if i["authorThumbnails"][-1]["url"].startswith("https"):
                return {"author":i["author"],"id":i["authorId"],"thumbnail":i["authorThumbnails"][-1]["url"],"type":"channel"}
            else:
                return {"author":i["author"],"id":i["authorId"],"thumbnail":r"https://"+i["authorThumbnails"][-1]["url"],"type":"channel"}
    return [load_search(i) for i in t]

def get_channel(channelid):
    global apichannels
    t = json.loads(apichannelrequest(r"api/v1/channels/"+ urllib.parse.quote(channelid)))
    if t["latestVideos"] == []:
        print("APIがチャンネルを返しませんでした")
        apichannels.append(apichannels[0])
        apichannels.remove(apichannels[0])
        raise APItimeoutError("APIがチャンネルを返しませんでした")
    return [[{"title":i["title"],"id":i["videoId"],"authorId":t["authorId"],"author":t["author"],"viewCountText":i["viewCountText"],"published":i["publishedText"],"type":"video"} for i in t["latestVideos"]],{"channelname":t["author"],"channelicon":t["authorThumbnails"][-1]["url"],"channelprofile":t["descriptionHtml"]}]

def get_playlist(listid,page):
    t = json.loads(apirequest(r"/api/v1/playlists/"+ urllib.parse.quote(listid)+"?page="+urllib.parse.quote(page)))["videos"]
    return [{"title":i["title"],"id":i["videoId"],"authorId":i["authorId"],"author":i["author"],"type":"video"} for i in t]

def get_comments(videoid):
    t = json.loads(apicommentsrequest(r"api/v1/comments/"+ urllib.parse.quote(videoid)+"?hl=jp"))["comments"]
    return [{"author":i["author"],"authoricon":i["authorThumbnails"][-1]["url"],"authorid":i["authorId"],"body":i["contentHtml"].replace("\n","<br>")} for i in t]

def get_replies(videoid,key):
    t = json.loads(apicommentsrequest(fr"api/v1/comments/{videoid}?hmac_key={key}&hl=jp&format=html"))["contentHtml"]



def check_cokie(cookie):
    if cookie == "True":
        return True
    return True


from fastapi import FastAPI, Depends
from fastapi import Response,Cookie,Request
from fastapi.responses import HTMLResponse,PlainTextResponse
from fastapi.responses import RedirectResponse as redirect
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Union


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/css", StaticFiles(directory="./css"), name="static")
app.add_middleware(GZipMiddleware, minimum_size=1000)

from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory='templates').TemplateResponse


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return template("heddohon.html", {"request": request})
  
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return template("home.html", {"request": request})

@app.get('/watch', response_class=HTMLResponse)
def video(v: str, request: Request):
    videoid = v
    t = get_data(videoid)
    return template('video.html', {
        "request": request,
        "videoid": videoid,
        "videourls": t[1],
        "res": t[0],
        "description": t[2],
        "videotitle": t[3],
        "authorid": t[4],
        "authoricon": t[6],
        "author": t[5],
    })

@app.get("/search", response_class=HTMLResponse)
def search(q: str, request: Request, page: Union[int, None] = 1):
    return template("search.html", {
        "request": request,
        "results": get_search(q, page),
        "word": q,
        "next": f"/search?q={q}&page={page + 1}"
    })

@app.get("/hashtag/{tag}")
def search_by_tag(tag: str):
    return RedirectResponse(f"/search?q={tag}")

@app.get("/channel/{channelid}", response_class=HTMLResponse)
def channel(channelid: str, request: Request):
    t = get_channel(channelid)
    return template("channel.html", {
        "request": request,
        "results": t[0],
        "channelname": t[1]["channelname"],
        "channelicon": t[1]["channelicon"],
        "channelprofile": t[1]["channelprofile"]
    })

@app.get("/answer", response_class=HTMLResponse)
def set_cokie(q: str):
    if len(q) > 10:
        return "ランダム"
    return "文章"
  

@app.get("/snowball", response_class=HTMLResponse)
def home(request: Request):
    return template("snowball.html", {"request": request})

@app.get("/playlist", response_class=HTMLResponse)
def playlist(list: str, request: Request, page: Union[int, None] = 1):
    return template("search.html", {
        "request": request,
        "results": get_playlist(list, str(page)),
        "word": "",
        "next": f"/playlist?list={list}"
    })

@app.get("/suggest")
def suggest(keyword: str):
    return [i[0] for i in json.loads(requests.get(
        f"http://www.google.com/complete/search?client=youtube&hl=ja&ds=yt&q={urllib.parse.quote(keyword)}").text[19:-1])[1]]

@app.get("/comments")
def comments(request: Request, v: str):
    return template("comments.html", {"request": request, "comments": get_comments(v)})

@app.get("/thumbnail")
def thumbnail(v: str):
    return Response(content=requests.get(f"https://img.youtube.com/vi/{v}/0.jpg").content, media_type="image/jpeg")

@app.get("/load_instance")
def home():
    global url
    url = requests.get('https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()
    
    
@app.exception_handler(500)
def page(request: Request, __):
    return template("APIwait.html", {"request": request}, status_code=500)

@app.exception_handler(APItimeoutError)
def APIwait(request: Request, exception: APItimeoutError):
    return template("APIwait.html", {"request": request}, status_code=500)