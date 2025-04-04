#!/bin/bash

cd /home/rook/PCN/pcn || exit 1

# Reset and pull to avoid conflicts in public/
git reset --hard origin/main || exit 1
GIT_SSH_COMMAND="ssh -i /home/rook/.ssh/pcn_deploy_key" git pull origin main || exit 1

# Rebuild site
hugo || exit 1
sudo chown -R rook:www-data /home/rook/PCN/pcn/public || exit 1
sudo chmod -R 755 /home/rook/PCN/pcn/public || exit 1
sudo systemctl restart nginx || exit 1

echo "Deployment complete!"