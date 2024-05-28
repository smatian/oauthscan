from flask import Blueprint, request, redirect, url_for, session, jsonify
import requests
import json
import os
from vision import detectBadStuff  # Adjust this import to your actual module

instagram_blueprint = Blueprint('instagram', __name__)

from flask import Blueprint, request, redirect, url_for, session, jsonify
import requests
import os

instagram_blueprint = Blueprint('instagram', __name__)

@instagram_blueprint.route('/')
def home():
    auth_url = f"https://api.instagram.com/oauth/authorize?client_id={os.getenv('INSTAGRAM_APP_ID')}&redirect_uri={os.getenv('REDIRECT_URI')}&scope=user_profile,user_media&response_type=code"
    return f'<a href="{auth_url}">Login with Instagram</a>'

@instagram_blueprint.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Error: No code received'
    
    token_data = {
        'client_id': os.getenv('INSTAGRAM_APP_ID'),
        'client_secret': os.getenv('INSTAGRAM_APP_SECRET'),
        'grant_type': 'authorization_code',
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'code': code
    }
    token_url = 'https://api.instagram.com/oauth/access_token'
    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        return f"Error fetching access token: {response.text}"
    
    token_json = response.json()
    access_token = token_json.get('access_token')
    user_id = token_json.get('user_id')
    if not access_token or not user_id:
        return 'Error: No access token or user ID received'
    
    session['access_token'] = access_token
    session['user_id'] = user_id
    return redirect(url_for('instagram.profile'))

@instagram_blueprint.route('/profile')
def profile():
    access_token = session.get('access_token')
    user_id = session.get('user_id')
    
    if not access_token or not user_id:
        return 'Error: User not logged in'
    
    user_info_url = f"https://graph.instagram.com/{user_id}?fields=id,username,account_type,media_count&access_token={access_token}"
    user_info_response = requests.get(user_info_url)
    if user_info_response.status_code != 200:
        return f"Error fetching user info: {user_info_response.text}"
    user_info = user_info_response.json()

    media_url = f"https://graph.instagram.com/{user_id}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,children&access_token={access_token}"
    media_response = requests.get(media_url)
    if media_response.status_code != 200:
        return f"Error fetching media: {media_response.text}"
    media = media_response.json().get('data', [])

    media_html = ''.join([f'<img src="{item["media_pk"]}" alt="{item.get("caption", "")}" style="width:150px;" id="img-{item["id"]}"><br><p id="result-{item["id"]}">Pending scan...</p>' for item in media])
    
    return f'''
        <h1>Logged in as {user_info["username"]}</h1>
        <p>Account Type: {user_info["account_type"]}</p>
        <p>Media Count: {user_info["media_count"]}</p>
        <div>{media_html}</div>
        <script src="/static/js/scan_images.js"></script>
    '''


@instagram_blueprint.route('/profile')
def profile():
    access_token = session.get('access_token')
    user_id = session.get('user_id')

    if not access_token or not user_id:
        return 'Error: User not logged in'

    user_info_url = f'https://graph.instagram.com/{user_id}?fields=id,username,account_type,media_count&access_token={access_token}'

    try:
        user_info_response = requests.get(user_info_url)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching user info: {e}"

    media_url = f'https://graph.instagram.com/{user_id}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,children&access_token={access_token}'
    
    try:
        media_response = requests.get(media_url)
        media_response.raise_for_status()
        media = media_response.json()['data']
    except requests.exceptions.RequestException as e:
        return f"Error fetching media: {e}"

    # Constructing HTML for media items without scanning
    media_html = ''
    for item in media:
        media_html += f'<div><img src="{item["media_url"]}" alt="{item.get("caption", "")}" style="width:150px;" id="image-{item["id"]}">'
        media_html += f'<p>Scan result: <span id="scan-result-{item["id"]}">Scanning...</span></p></div>'

    return f'''
        <h1>Logged in as {user_info["username"]}</h1>
        <p>Account Type: {user_info["account_type"]}</p>
        <p>Media Count: {user_info["media_count"]}</p>
        <div>{media_html}</div>
        <script src="/static/js/scan_images.js"></script>  <!-- Make sure this JS file is correctly linked and available -->
    '''




@instagram_blueprint.route('/scan_image', methods=['POST'])
def scan_image():
    data = request.get_json()
    image_url = data.get('image_url')
    result = detectBadStuff(image_url)  # Assuming this function returns some JSON or a result string
    return jsonify({'result': result})

