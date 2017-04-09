#!/bin/bash

echo -n "Encrypt Inventory ... "
ansible-vault encrypt ../hosts --vault-password-file=../../pass
echo -n "Encrypt keys ... "
ansible-vault encrypt ../keys/* --vault-password-file=../../pass
echo -n "Encrypt group_vars ... "
ansible-vault encrypt ../group_vars/* --vault-password-file=../../pass
echo -n "Encrypt role vars ... "
ansible-vault encrypt ../roles/*/vars/* --vault-password-file=../../pass
