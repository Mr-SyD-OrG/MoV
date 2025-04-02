if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Mr-SyD-OrG/Mov.git /TheMovieProviderBot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /TheMovieProviderBot
fi
cd /TheMovieProviderBot
pip3 install -r requirements.txt
echo "Starting TheMovieProviderBot...."
python3 -m mfinder
