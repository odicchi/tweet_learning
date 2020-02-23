import json
import config
from requests_oauthlib import OAuth1Session
from time import sleep
import re
import emoji
from mongo_dao import MongoDAO

# 今回は使わない
# 絵文字を除去する
def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

# APIキー設定(別ファイルのconfig.pyで定義しています)
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

# 認証処理
twitter = OAuth1Session(CK, CS, AT, ATS)  

# タイムライン取得エンドポイント
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"  

# 取得アカウント
necopla_menber = ['@yukino__NECOPLA', '@yurinaNECOPLA', '@riku_NECOPLA', '@miiNECOPLA', '@kaori_NECOPLA', '@sakuraNECOPLA', '@miriNECOPLA', '@renaNECOPLA']

# パラメータの定義
params = {'q': '-filter:retweets',
          'max_id': 0, # 取得を開始するID
          'count': 200}

# arg1:DB Name
# arg2:Collection Name
mongo = MongoDAO("db", "necopla_tweets")
mongo.delete_many({})

regex_twitter_account = '@[0-9a-zA-Z_]+'

for menber in necopla_menber:
    print(menber)
    del params['max_id'] # 取得を開始するIDをクリア
    # 最新の200件を取得／2回目以降はparams['max_id']に設定したIDより古いツイートを取得
    for j in range(100):
        params['screen_name'] = menber
        res = twitter.get(url, params=params)
        if res.status_code == 200:
            # API残り回数
            limit = res.headers['x-rate-limit-remaining']
            print("API remain: " + limit)
            if limit == 1:
                sleep(60*15)
            
            n = 0
            tweets = json.loads(res.text)
            # 処理中のアカウントからツイートが取得出来なくなったらループを抜ける
            if len(tweets) == 0:
                break
            # ツイート単位で処理する
            for tweet in tweets:
                # ツイートデータを丸ごと登録
                if not "RT @" in tweet['text'][0:4]:
                    mongo.insert_one({'tweet':re.sub(regex_twitter_account, '',tweet['text'].split('http')[0]).strip()})
            
                if len(tweets) >= 1:
                    params['max_id'] = tweets[-1]['id']-1
