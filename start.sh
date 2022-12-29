echo "Cloning Repo...."
git clone https://github.com/konichiwa55115/youtube-bot /LazyDeveloper
cd /LazyDeveloper
mkdir playlists
pip3 install -r requirements.txt
echo "Starting Bot...."
python3 bot.py
