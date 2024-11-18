import json
import requests
import urllib.parse
import time
import datetime
import random
import os
from cache import cache

max_api_wait_time = 4
max_time = 10
version = "1.0"

videoapis = [
  r"https://invidious.qwik.space",   
  r"https://yt.drgnz.club",   
  r"https://invidious.privacyredirect.com",   
  r"https://invidious.jing.rocks",   
  r"https://iv.datura.network",   
  r"https://invidious.private.coffee",   
  r"https://invidious.materialio.us",   
  r"https://invidious.fdn.fr",   
  r"https://vid.puffyan.us",   
  r"https://iteroni.com",   
  r"https://invidious.private.coffee",   
  r"https://youtube.privacyplz.org",   
  r"https://invidious.fdn.fr",   
  r"https://youtube.mosesmang.com",   
  r"https://inv.nadeko.net",   
  r"https://invidious.nerdvpn.de",   
  r"https://iv.datura.network",   
  r"https://invidious.perennialte.ch"
];

apis = [
r"https://invidious.jing.rocks/",
r"https://invidious.nerdvpn.de/",
r"https://inv.nadeko.net/",
r"https://invidious.jing.rocks/",
r"https://inv.vern.cc/",
r"https://inv.zzls.xyz/",
r"https://invi.susurrando.com/",
r"https://invidious.epicsite.xyz/",
r"https://invidious.esmailelbob.xyz/",
r"https://invidious.garudalinux.org/",
r"https://invidious.kavin.rocks/",
r"https://invidious.lidarshield.cloud/",
r"https://invidious.lunar.icu/",
r"https://yt-us.discard.no/",
r"https://invidious.nerdvpn.de/",
r"https://invidious.privacydev.net/",
r"https://invidious.sethforprivacy.com/",
r"https://invidious.slipfox.xyz/",
r"https://yt-no.discard.no/",
r"https://invidious.snopyta.org/",
r"https://invidious.tiekoetter.com/",
r"https://invidious.vpsburti.com/",
r"https://invidious.weblibre.org/",
r"https://invidious.pufe.org/",
r"https://iv.ggtyler.dev/",
r"https://iv.melmac.space/",
r"https://vid.puffyan.us/",
r"https://watch.thekitty.zone/",
r"https://yewtu.be/",
r"https://youtube.moe.ngo/",
r"https://yt.31337.one/",
r"https://yt.funami.tech/",
r"https://yt.oelrichsgarcia.de/",
r"https://yt.wkwkwk.fun/",
r"https://youtube.076.ne.jp/",
r"https://invidious.projectsegfau.lt/",
r"https://invidious.fdn.fr/",
r"https://i.oyster.men/",
r"https://invidious.domain.glass/",
r"https://inv.skrep.eu/",
r"https://clips.im.allmendenetz.de/",
r"https://ytb.trom.tf/",
r"https://invidious.pcgamingfreaks.at/",
r"https://youtube.notrack.ch/",
r"https://iv.ok0.org/",
r"https://youtube.vpn-home-net.de/",
r"http://144.126.251.186/",
r"https://invidious.citizen4.eu/",
r"https://yt.sebaorrego.net/",
r"https://invidious.pesso.al/",
r"https://invidious.manasiwibi.com/",
r"https://toob.unternet.org/",
r"https://youtube.mosesmang.com/",
r"https://invidious.varishangout.net/",
r"https://invidio.xamh.de/",
r"https://yt.tesaguri.club/",
r"https://video.francevpn.fr/",
r"https://inv.in.projectsegfau.lt/",
r"https://invid.nevaforget.de/",
r"https://tube.foss.wtf/",
r"https://invidious.777.tf/",
r"https://inv.tux.pizza/",
r"https://youtube.076.ne.jp",
r"https://invidious.osi.kr/",
r"https://inv.riverside.rocks/",
r"https://inv.bp.mutahar.rocks/",
r"https://invidious.namazso.eu/",
r"https://tube.cthd.icu/",
r"https://invidious.snopyta.org/",
r"https://yewtu.be/",
r"https://invidious.privacy.gd/",
r"https://invidious.lunar.icu/",
r"https://vid.puffyan.us/",
r"https://invidious.weblibre.org/",
r"https://invidious.esmailelbob.xyz/",
r"https://invidio.xamh.de/",
r"https://invidious.kavin.rocks/",
r"https://invidious-us.kavin.rocks/",
r"https://invidious.mutahar.rocks/",
r"https://invidious.zee.li/",
r"https://tube.connect.cafe/",
r"https://invidious.zapashcanon.fr/",
r"https://invidious.poast.org/",
r"https://ytb.trom.tf/",
r"https://invidious.froth.zone/",
r"https://invidious.domain.glass/",
r"https://invidious.sp-codes.de/",
r"http://144.126.251.186/",
r"https://yt.512mb.org/",
r"https://invidious.fdn.fr/",
r"https://invidious.pcgamingfreaks.at/",
r"https://tube.meowz.moe/",
r"https://clips.im.allmendenetz.de/",
r"https://inv.skrep.eu/",
r"https://invidious.frbin.com/",
r"https://dev.invidio.us/",
r"https://invidious.site/",
r"https://invidious.sethforprivacy.com/",
r"https://invidious.stemy.me/",
r"https://betamax.cybre.club/",
r"https://invidious.com/",
r"https://invidious.snopyta.org/",
r"https://yewtu.be/",
r"https://invidious.kavin.rocks/",
r"https://vid.puffyan.us/",
r"https://inv.riverside.rocks/",
r"https://invidious.not.futbol/",
r"https://youtube.076.ne.jp/",
r"https://yt.artemislena.eu",
r"https://invidious.esmailelbob.xyz/",
r"https://invidious.projectsegfau.lt/",
r"https://invidious.dhusch.de/",
r"https://inv.odyssey346.dev/"
]

waapis = [
  r"https://ludicrous-wonderful-temple.glitch.me/",   
  r"https://yt.drgnz.club",   
  r"https://invidious.privacyredirect.com",   
  r"https://invidious.jing.rocks",   
  r"https://iv.datura.network",   
  r"https://invidious.private.coffee",   
  r"https://invidious.materialio.us",   
  r"https://invidious.fdn.fr",   
  r"https://vid.puffyan.us",   
  r"https://iteroni.com",   
  r"https://invidious.private.coffee",   
  r"https://youtube.privacyplz.org",   
  r"https://invidious.fdn.fr",   
  r"https://youtube.mosesmang.com",   
  r"https://inv.nadeko.net",   
  r"https://invidious.nerdvpn.de",   
  r"https://iv.datura.network",   
  r"https://invidious.perennialte.ch"
];

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
    
def videoapirequest(url, headers=None):
    global apis
    global max_time
    starttime = time.time()

    for api in apis:
        if time.time() - starttime >= max_time - 1:
            break
        try:
            res = requests.get(api + url,timeout=max_api_wait_time)

            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apis.append(api)
                apis.remove(api)
        except Exception as e:
            print(f"タイムアウト:{api}, エラー: {e}")
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
    t = json.loads(apirequest_video(r"api/v1/videos/" + urllib.parse.quote(videoid)))

    # 関連動画を解析してリストにする
    related_videos = [
        {
            "id": i["videoId"],
            "title": i["title"],
            "authorId": i["authorId"],
            "author": i["author"],
            "viewCount": i["viewCount"]  # 再生回数を追加（デフォルトは0）
        }
        for i in t["recommendedVideos"]
    ]
    return (
        related_videos,
        list(reversed([i["url"] for i in t["formatStreams"]]))[:2],  # 逆順で2つのストリームURLを取得
        t["descriptionHtml"].replace("\n", "<br>"),
        t["title"],
        t["authorId"],
        t["author"],
        t["authorThumbnails"][-1]["url"],
        t["viewCount"] 
    )    
    
def getting_data(videoid):
    url = f"https://ludicrous-wonderful-temple.glitch.me/api/login/{urllib.parse.quote(videoid)}"
    response = requests.get(url)
    if response.status_code == 200:
        t = response.json()
        print(t)
        recommended_videos = [{
            "id": t["videoId"],
            "title": t["videoTitle"],
            "authorId": t["channelId"],
            "author": t["channelName"],
            "viewCountText": f"{t['videoViews']} views"
        }]
        stream_url = t["stream_url"]
        description = t["videoDes"].replace("\n", "<br>")
        title = t["videoTitle"]
        authorId = t["channelId"]
        author = t["channelName"]
        author_icon = t["channelImage"] 
        return recommended_videos, stream_url, description, title, authorId, author, author_icon
  
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
app.mount("/static", StaticFiles(directory="static"), name="static")
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
    return template('watch.html', {
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
    
@app.get('/video', response_class=HTMLResponse)
def video(v: str, request: Request):
    videoid = v
    t = getting_data(videoid)
    print(t)
    print(t[1])
    return template('watchwa.html', {
        "request": request,
        "videoid": videoid,
        "res": t[0],
        "videourls": t[1],
        "description": t[2],
        "videotitle": t[3],
        "authorid": t[4],
        "authoricon": t[6],
        "author": t[5],
        "streamUrl": t[1],
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

@app.get("/app", response_class=HTMLResponse)
def home(request: Request):
    return template("app.html", {"request": request})
    
@app.get("/snowball", response_class=HTMLResponse)
def home(request: Request):
    return template("snowball.html", {"request": request})
  
@app.get("/2048", response_class=HTMLResponse)
def home(request: Request):
    return template("2048.html", {"request": request})
  
@app.get("/heddohon", response_class=HTMLResponse)
def home(request: Request):
    return template("more.html", {"request": request})
  
@app.get("/uranai", response_class=HTMLResponse)
def home(request: Request):
    return template("uranai.html", {"request": request})
  
@app.get("/tool", response_class=HTMLResponse)
def home(request: Request):
    return template("tool.html", {"request": request})
  
@app.get("/craft", response_class=HTMLResponse)
def home(request: Request):
    return template("craft.html", {"request": request})
  
@app.get("/drive", response_class=HTMLResponse)
def home(request: Request):
    return template("drive.html", {"request": request})
  
@app.get("/send", response_class=HTMLResponse)
def home(request: Request):
    return template("send.html", {"request": request})
  
@app.get("/tubeurl", response_class=HTMLResponse)
def home(request: Request):
    return template("tubeurl.html", {"request": request})
  
@app.get("/fileview", response_class=HTMLResponse)
def home(request: Request):
    return template("fileview.html", {"request": request})
  
@app.get("/sonota", response_class=HTMLResponse)
def home(request: Request):
    return template("sonota.html", {"request": request})
  
@app.get("/android", response_class=HTMLResponse)
def home(request: Request):
    return template("android.html", {"request": request})
    
@app.exception_handler(500)
def page(request: Request, __):
    return template("APIwait.html", {"request": request}, status_code=500)

@app.exception_handler(APItimeoutError)
def APIwait(request: Request, exception: APItimeoutError):
    return template("APIwait.html", {"request": request}, status_code=500)