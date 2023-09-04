import json
import os
from dotenv import load_dotenv
import requests
import time


def getMostRecentMatchID():
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=1"
    r = requests.get(url, headers={"X-Riot-Token": riotApiKey}).json()
    return r[0]


def timeLastPlayed():
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{matchId}"
    r = requests.get(url, headers={"X-Riot-Token": riotApiKey}).json()
    gameDate = r['info']['game_datetime'] / 1000
    now = time.time()
    diffHours = (now - gameDate) / 3600
    return "{:.1f}".format(diffHours)


def sendMsg():
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    data = {
        'object_type': 'text',
        'text': f"SISTER'S TFT PLAY DETECTED 🚨🚨🚨🚨 LAST PLAYED : {timeLastPlayed} HOURS AGO!!!"
                f"CHECK HER MOST RECENT PLAY AND BUST HER ASS!!"
                f"https://tft.op.gg/summoners/na/s0ju",
        'link': {
            'web_url': 'https://tft.op.gg/summoners/na/s0ju',
            'mobile_web_url': 'https://tft.op.gg/summoners/na/s0ju'
        },
        'button_title': 'BUST HER ASS!!!'
    }

    data = {'template_object': json.dumps(data)}
    requests.post(url, headers={"Authorization" : f"Bearer ${kakaoToken}"}, data=data)
    requests.post(url, headers={"Authorization": f"Bearer ${kakaoToken}"}, data=data)
    response = requests.post(url, headers={"Authorization" : f"Bearer ${kakaoToken}"}, data=data)
    print(response.json())

def getKakaoToken():
    # url = "https://kauth.kakao.com/oauth/token?scope=friends,talk_message"
    #
    # data = {
    #     "grant_type": "refresh_code",
    #     "client_id": os.getenv('KAKAO_API_KEY'),
    #     "redirect_uri": "http://localhost:5000",
    #     "code": 'BnZhGfKwvmtGEvd7kSlN1OeyWM2P3Sm0vHfmNnMRkTd5lRnN51tmpiMFEZBcgg86fjP72gopyV8AAAGKXnOuHg'
    # }
    # response = requests.post(url, data=data)
    #
    # tokens = response.json()
    #
    # print(tokens)

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv('KAKAO_API_KEY'),
        "refresh_token": refreshToken
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    # save in kakao_code.json
    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)

if __name__ == '__main__':
    load_dotenv()
    riotApiKey = os.getenv('RIOT_TOKEN')
    puuid = os.getenv('PUUID')
    matchId = getMostRecentMatchID()
    timeLastPlayed = timeLastPlayed()
    kakaoToken = os.getenv('KAKAO_TOKEN')
    refreshToken = os.getenv('KAKAO_REFRESH_TOKEN')

    # hoursAgo = timeLastPlayed()

    sendMsg()