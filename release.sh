#!usr/bin/bash

# Create a directory with current date and time
now=$(date +"%Y_%m_%d__%H_%M_%S");
mkdir -p "releases/$now/"

# Copy files needed by themain HTML page
cp -f background.jpg "releases/$now/background.jpg"
cp -f ie10-viewport-bug-workaround.js "releases/$now/ie10-viewport-bug-workaround.js"
cp -f narrow-jumbotron.css "releases/$now/narrow-jumbotron.css"

# Compile JS using Google API Closure Compiler which also minifies JS code
python -B compile_js.py "releases/$now/script.min.js"

# Copy main HTML page
cp -f index.html "releases/$now/index.html"

# Update HTML page to use minified JS path
sed -i s/script.js/script.min.js/g "releases/$now/index.html"

# Zip entire release
cd releases
zip -r  "$now.zip" "$now/"