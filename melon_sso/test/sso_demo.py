from flask import Flask
from flask import render_template, request
import requests

app = Flask(__name__)

client_id = "xxxx"
client_secret = "xxxx"
redirect_uri = "xxxx/customer/gitee/redirect"
global access_token


@app.route('/')
def gitee_user():
    return render_template('home.html')


@app.route('/login')
def hello_world():
    return render_template('login.html')


@app.route('/customer/gitee/redirect')
def gitee_redirect():
    global access_token

    code = request.args.get('code')
    # github实现auth
    # token_url = "https://gitee.com/login/oauth/access_token?" \
    #             'client_id={}&client_secret={}&code={}'
    # token_url = token_url.format(client_id, client_secret, code)
    # # gitee实现auth
    token_url = "https://gitee.com/oauth/token?" \
                'grant_type=authorization_code&code={}&client_id={}&redirect_uri={}&client_secret={}'
    token_url = token_url.format(code, client_id, redirect_uri, client_secret)
    header = {
        "accept": "application/json"
    }
    res = requests.post(token_url, headers=header)
    if res.status_code == 200:
        res_dict = res.json()
        access_token = res_dict["access_token"]

    user_url = 'https://gitee.com/api/v5/user'
    access_token = 'token {}'.format(access_token)
    headers = {
        'accept': 'application/json',
        'Authorization': access_token
    }
    isLogin = 0
    res = requests.get(user_url, headers=headers)
    if res.status_code == 200:
        user_info = res.json()
        email = user_info.get('email', None)
        company_name = user_info.get('company', None)
        isLogin = 1
        return render_template('home.html', email=email, company_name=company_name, isLogin=isLogin)

    return None
