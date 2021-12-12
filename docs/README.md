# install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# install pyenv
brew install pyenv

# you need install the target version first
pyenv install 3.8.12

# then sets a shell-specific Python version
pyenv shell 3.8.12

# use this python version to create virtualenv
python -m venv venv

--

# activate venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt

--

# setup & start db
# setu & start django
# seed data?
