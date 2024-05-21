from flask import Flask, redirect, request, url_for, session, jsonify
import requests
import json
import os
from vision import detectBadStuff


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Replace with your Instagram App ID and App Secret
INSTAGRAM_APP_ID = '295626456945238'
INSTAGRAM_APP_SECRET = os.environ['instagramsecret']
REDIRECT_URI = 'https://70ac8810-32fb-46bb-9acf-734a23db8ee8-00-25khz7k18zzv.spock.replit.dev/callback'  # Note the https

@app.route('/')
def home():
    auth_url = f'https://api.instagram.com/oauth/authorize?client_id={INSTAGRAM_APP_ID}&redirect_uri={REDIRECT_URI}&scope=user_profile,user_media&response_type=code'
    return f'<a href="{auth_url}">Login with Instagram</a>'

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Error: No code received'

    token_url = 'https://api.instagram.com/oauth/access_token'
    token_data = {
        'client_id': INSTAGRAM_APP_ID,
        'client_secret': INSTAGRAM_APP_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    try:
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        token_json = token_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching access token: {e}")
        return f"Error fetching access token: {e}"

    access_token = token_json.get('access_token')
    user_id = token_json.get('user_id')

    if not access_token or not user_id:
        return 'Error: No access token or user ID received'

    session['access_token'] = access_token
    session['user_id'] = user_id

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    user_id = session.get('user_id')

    if not access_token or not user_id:
        return 'Error: User not logged in'

    user_info_url = f'https://graph.instagram.com/{user_id}?fields=id,username,account_type,media_count&access_token={access_token}'

    try:
        user_info_response = requests.get(user_info_url)
        user_info_response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        user_info = user_info_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info: {e}")
        return f"Error fetching user info: {e}"

    media_url = f'https://graph.instagram.com/{user_id}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,children&access_token={access_token}'

    try:
        media_response = requests.get(media_url)
        media_response.raise_for_status()
        media = media_response.json()['data']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching media: {e}")
        return f"Error fetching media: {e}"

    media_html = []
    for item in media:
        if item['media_type'] == 'CAROUSEL_ALBUM' and 'children' in item:
            child_media_html = []
            children_url = f'https://graph.instagram.com/{item["id"]}/children?fields=id,media_type,media_url,thumbnail_url&access_token={access_token}'
            try:
                children_response = requests.get(children_url)
                children_response.raise_for_status()
                children = children_response.json()['data']
                for child in children:
                    child_media_url = child['media_url'] if child['media_type'] == 'IMAGE' else child['thumbnail_url']
                    child_media_html.append(f'<div><img src="{child_media_url}" style="width: 150px; height: auto; margin-right: 10px;"><p id="scan-{child["id"]}">Scanning image...</p></div>')
            except requests.exceptions.RequestException as e:
                print(f"Error fetching children media: {e}")
                return f"Error fetching children media: {e}"
            child_media_html_str = ''.join(child_media_html)
            media_html.append(f'<div style="display: flex; flex-direction: row;">{child_media_html_str}</div>')
        else:
            media_url = item['media_url'] if item['media_type'] == 'IMAGE' else item['thumbnail_url']
            media_html.append(f'<div><img src="{media_url}" style="width: 150px; height: auto;"><p id="scan-{item["id"]}">Scanning image...</p></div>')

        caption = item.get('caption', '')
        permalink = item.get('permalink', '')
        media_html.append(f'<p>{caption}</p>')
        media_html.append(f'<p><a href="{permalink}">View on Instagram</a></p>')

    media_list = ''.join(media_html)

    print(f"User Info: {json.dumps(user_info, indent=2)}")
    return f'''
        <h1>Logged in as {user_info["username"]}</h1>
        <p>Account Type: {user_info["account_type"]}</p>
        <p>Media Count: {user_info["media_count"]}</p>
        <div>{media_list}</div>
        <script src="/static/scan_images.js"></script>
    '''

@app.route('/scan_image', methods=['POST'])
def scan_image():
    data = request.get_json()
    image_url = data.get('image_url')
    # Call your vision.py function here
    result = detectBadStuff(image_url)  # Make sure to import the function at the top
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
