from flask import Flask, render_template, request
import requests

app = Flask(__name__)

RAWG_API_KEY = "3279047c8302417a94fc4cda09efe1c2"

def search_games(query):
    url = f"https://api.rawg.io/api/games?search={query}&key={RAWG_API_KEY}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return []
    data = resp.json()
    return data.get("results", [])

def get_game_details(game_id):
    url = f"https://api.rawg.io/api/games/{game_id}?key={RAWG_API_KEY}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return {}
    return resp.json()

def make_download_links(game_name):
    name = game_name.replace(" ", "+")
    fitgirl = f"https://fitgirl-repacks.site/?s={name}"
    dodi = f"https://dodi-repacks.site/?s={name}"
    return fitgirl, dodi

@app.route('/', methods=['GET', 'POST'])
def index():
    games = []
    details = None
    fitgirl_link = dodi_link = ""
    selected_idx = None
    if request.method == 'POST':
        query = request.form.get('query', '')
        games = search_games(query)
        selected_idx = request.form.get('selected_idx')
        if selected_idx and selected_idx.isdigit():
            idx = int(selected_idx)
            if 0 <= idx < len(games):
                details = get_game_details(games[idx]['id'])
                fitgirl_link, dodi_link = make_download_links(details.get("name", ""))
    return render_template(
        'game_info.html',
        games=games,
        details=details,
        fitgirl_link=fitgirl_link,
        dodi_link=dodi_link,
        selected_idx=selected_idx
    )

if __name__ == "__main__":
    app.run(debug=True)