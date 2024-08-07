#!/bin/bash

echo 'Choose a username:'
read NEW_USER

# Create a new user and append it to the sudo group
# without removing the user from other groups
adduser $NEW_USER
usermod -aG sudo $NEW_USER

# Create the .ssh directory for the new user
mkdir /home/$NEW_USER/.ssh

# Change permissions of the new .ssh directory
# From right to left:
# 0 - no permissions to other users of the system
# 0 - no permissions to members of the group the directory belongs to
# 7 - give reading/writing/executing permissions to the owner of the file
chmod 700 /home/$NEW_USER/.ssh

# Add the authorized keys from root to the new user
sudo cp /root/.ssh/authorized_keys /home/$NEW_USER/.ssh/authorized_keys

# Change ownership of the new .ssh directory so it
# belongs to the NEW_USER group and th the NEW_USER user
sudo chown -R $NEW_USER:$NEW_USER /home/$NEW_USER/.ssh

# Change permissions of the authorized_keys file
# From right to left:
# 0 - no permissions to other users of the system
# 0 - no permissions to members of the group the file belongs to
# 6 - give reading/writing permissions to the owner of the file
sudo chmod 600 /home/$NEW_USER/.ssh/authorized_keys

# Final message
echo ''
echo 'Your new user named' '"'$NEW_USER'"' 'was created.'
echo 'Logout and use the command "ssh NEW_USER@SERVER_IP" to access using it.'
echo ''
