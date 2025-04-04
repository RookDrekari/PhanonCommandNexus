#!/bin/bash

cd /home/rook/PCN/pcn || exit 1

git pull origin main || exit 1

hugo || exit 1
sudo chown -R rook:www-data /home/rook/PCN/pcn/public || exit 1
sudo chmod -R 755 /home/rook/PCN/pcn/public || exit 1
sudo systemctl restart nginx || exit 1

echo "Deployment complete!"