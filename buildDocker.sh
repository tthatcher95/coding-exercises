docker build -t nutrienimage .
echo "Building Image"

docker kill nutrienapp
echo "Killing Docker Image"

docker rm nutrienapp
echo "Removing Docker Image"

echo "Running 'nutrien' Image"
docker run -d --name nutrienapp -p 80:80 nutrienimage
echo '-------------------------------'
echo '--- http://127.0.0.1/docs -----\a'
echo '-------------------------------'
echo "CTRL Click above URL to go to running API"
