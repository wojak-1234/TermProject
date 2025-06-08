from flask import *
import requests
import urllib.parse
import base64
import json

app = Flask(__name__)
# 클라이언트 아이디 , 클라이언트 시크릿 , login 이후 redirect 할 주소 (/callback) 을 정의.
app.secret_key = 'verysecret'
clientid="b616a25fe7014a1aaaf6347b189247af"
clientsecret="26b61a4ffb9a49b295d3d5996e90a715"
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
# 기본 페이지
@app.route('/')
def realhome():
    return render_template('template.html')

# (로그인 한 후 홈 클릭했을 시 페이지 입니다.)
@app.route('/home')
def home():
    current_dn = session['display_name']
    current_piu = session['profile_image_url']
    return render_template('afterlogintemplate.html',
                           display_name=current_dn,
                           profile_image_url=current_piu)
# [메뉴 1]

# [메뉴 2]

# 매뉴 2 기본페이지
@app.route('/mood')
def mood():
    current_dn = session['display_name']
    current_piu = session['profile_image_url']
    return render_template('Html.html'       ,
       display_name=current_dn,
        profile_image_url=current_piu)

# 메뉴 2 버튼클릭시
@app.route('/submitmood',methods=['POST'])
def pickmood():
    selected_genre=''
    getrecommendationurl='https://api.spotify.com/v1/search'
    moodvalue = float(request.form.get('moodvalue'))
    header1 = {'Authorization': f"Bearer {session.get('access_token')}"}
    if moodvalue <= 0.333:
        search_term = 'calm morning songs'
    elif moodvalue <= 0.666:
        search_term = 'upbeat pop for noon'
    else:
        search_term = 'relaxing evening jazz'

    query_params = {
        'q': search_term,
        'type': 'track',
        'limit': 10,
        'market': 'KR'
    }
    current_dn = session['display_name']
    current_piu = session['profile_image_url']
    try:
        tracklist = requests.get(getrecommendationurl, headers=header1, params=query_params)
        tracklist.raise_for_status()
        raw_tracklist = tracklist.json()
        final_recommendation_data_string = json.dumps(raw_tracklist, ensure_ascii=False)
        print(final_recommendation_data_string)
        return render_template('aftermood.html', finalresponse=final_recommendation_data_string, display_name=current_dn, # display_name이라는 이름으로 display_name 변수 전달
        profile_image_url=current_piu)
    except requests.exceptions.RequestException as e:
        return f"API 호출 중 오류 발생 {e}"
    except json.JSONDecodeError as e:
        return f"Spotify 응답 JSON 파싱 오류 {e}"
    except Exception as e:
        return f"예상치 못한 오류: {e}"

# 로그인 관련 부분
@app.route('/login')
def login():
    query_params = {
        'client_id': clientid,
        'response_type': 'code',
        'redirect_uri': 'http://127.0.0.1:5000/callback', # 어느 창에서 실행했는지 무관하게 지정된 브라우저 탭으로 이동시킴.
        'scope': 'user-read-private user-read-email user-top-read'  # 스코프는 공백으로 구분합니다.
    }
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params) # 딕셔너리 값을 적합한 쿼리 형식으로 변환해줌
    return redirect(url) # 인증 시스템 url redirect

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1/'

# 콜백 라우트 (인증 후 리다이렉트되는 곳)
@app.route('/callback')
def callback():
    code = request.args.get('code')
    tokenurl = 'https://accounts.spotify.com/api/token'
    auth_str = f"{clientid}:{clientsecret}"
    encoded_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded' # 폼 데이터 전송 시 필수
    }

    # POST 요청 바디 (폼 데이터 형식)
    data = {
        'grant_type': 'authorization_code', # 인증 코드 플로우임을 명시
        'code': code, # Spotify로부터 받은 임시 인증 코드
        'redirect_uri': REDIRECT_URI # Spotify 대시보드에 등록된 URI와 일치해야 함
    }
    # 2. Spotify Token 엔드포인트에 POST 요청 보내기
    try:
        response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)

        response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생시키는 함수
        token_info = response.json()  # 응답을 JSON 형태로 파싱
    except requests.exceptions.RequestException as e:
        print(f"Error requesting access token: {e}")
        return "왜 안되노", 500

    # 3. 응답에서 Access Token 및 Refresh Token 추출 및 저장
    access_token = token_info.get('access_token')
    refresh_token = token_info.get('refresh_token')
    expires_in = token_info.get('expires_in')

    # 세션에 토큰 정보 저장
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['expires_in'] = expires_in

    #4.필요한 정보들 가져오기
    try:
        user_headers = {
            'Authorization': f'Bearer {access_token}'
        }
        # 'me' 엔드포인트에 요청 (사용자 ID 필요 없음)
        user_profile_response = requests.get(f"{SPOTIFY_API_BASE_URL}me", headers=user_headers)

        print("Status Code:", user_profile_response.status_code)
        print("Response Text:", user_profile_response.text)


        user_profile_response.raise_for_status()
        user_profile = user_profile_response.json()

        # 세션에 사용자 정보 저장
        session['display_name'] = user_profile.get('display_name', 'Spotify 사용자')
        images = user_profile.get('images', [])
        profile_image_url = images[0]['url'] if images else None
        session['profile_image_url'] = profile_image_url
        current_dn = session['display_name']
        current_piu = session['profile_image_url']
# 오류 처리방법
    except requests.exceptions.RequestException as e:
        print(f"Spotify 사용자 프로필 가져오기 오류: {e}")
        return "Logged in, but failed to fetch user profile. Please try again.", 500
# html 문서에 형식 보냄.
    return render_template(
        'afterlogintemplate.html',            # 렌더링할 HTML 파일 이름 (templates 폴더 안에 있어야 함)
        display_name=current_dn, # display_name이라는 이름으로 display_name 변수 전달
        profile_image_url=current_piu
    )
@app.route('/color')
def color():
    current_dn = session['display_name']
    current_piu = session['profile_image_url']
    query_parameter={'type':"tracks",
                     'time_range':'long_term',
    'limit':50 }
    access_token = session['access_token']
    user_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        top_track_response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=user_headers,
                                          params=query_parameter)

        print(f"Top Tracks API Status Code: {top_track_response.status_code}")
        print(f"Top Tracks API Response Text: {top_track_response.text}")

        top_track_response.raise_for_status()
        raw_toptrack = top_track_response.json()
        final_toptrack = json.dumps(raw_toptrack, ensure_ascii=False)
        print(final_toptrack)
        return render_template('colorpick.html', finalresponse=final_toptrack,
                                   display_name=current_dn,  # display_name이라는 이름으로 display_name 변수 전달
                                   profile_image_url=current_piu)
    except requests.exceptions.RequestException as e:
        return f"API 호출 중 오류 발생 {e}"
    except json.JSONDecodeError as e:
        return f"Spotify 응답 JSON 파싱 오류 {e}"
    except Exception as e:
        return f"예상치 못한 오류: {e}"

@app.route('/search')
def search_page():
    """
    곡 검색 및 분석 페이지를 렌더링합니다.
    """
    current_dn = session.get('display_name')
    current_piu = session.get('profile_image_url')

    if not current_dn:
        return redirect(url_for('login')) # 로그인되지 않았다면 로그인 페이지로 리다이렉트

    return render_template('search.html',
                           display_name=current_dn,
                           profile_image_url=current_piu)

# 프론트엔드 JavaScript에서 호출하는 API 엔드포인트
@app.route('/api/search', methods=['GET'])
def api_search_song_info_direct():
    song_query = request.args.get('q')

    if not song_query:
        return jsonify({"error": "검색어가 필요합니다."}), 400

    access_token = session.get('access_token')
    if not access_token:
        return jsonify({"error": "로그인이 필요합니다. (Access Token 없음)"}), 401

    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        search_params = {
            'q': song_query,
            'type': 'track',
            'limit': 1
        }
        search_response = requests.get(
            f"{SPOTIFY_API_BASE_URL}search",
            headers=headers,
            params=search_params
        )
        search_response.raise_for_status() # HTTP 오류 발생 시 예외
        search_results = search_response.json()

        tracks = search_results.get('tracks', {}).get('items', [])
        if not tracks:
            return jsonify({"error": "검색 결과가 없습니다."})

        first_track = tracks[0]
        track_name = first_track['name']
        artist_name = first_track['artists'][0]['name'] if first_track['artists'] else 'Unknown Artist'
        album_image_url = first_track['album']['images'][0]['url'] if first_track['album']['images'] else None
        popularity = first_track['popularity']

        result_data = {
            "track_name": track_name,
            "artist_name": artist_name,
            "album_image_url": album_image_url,
            "popularity": popularity,
        }

        return jsonify(result_data)

    except requests.exceptions.RequestException as e:
        print(f"Spotify API 호출 중 오류 발생: {e}")
        return jsonify({"error": f"Spotify API 통신 오류: {e}"}), 500
    except Exception as e:
        print(f"서버 처리 중 예상치 못한 오류: {e}")
        return jsonify({"error": f"서버 오류: {e}"}), 500
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('realhome'))
if __name__ == '__main__':
    app.run(debug=True)