
# install npm
sudo apt install npm

# go into a new folder then init the folder with npm
npm init

# install showdown, '-g' is the global option to install
npm install showdown -g

# run showdown
showdown makehtml -i INPUT.md -o OUTPUT.html