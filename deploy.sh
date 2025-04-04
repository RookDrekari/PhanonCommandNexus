#!/bin/bash

cd /home/rook/PCN

git pull origin main

cd pcn

hugo
sudo chown -R rook:www-data /home/rook/PCN/pcn/public
sudo chmod -R 755 /home/rook/PCN/pcn/public
sudo systemctl restart nginx

echo "Deployment complete!"
