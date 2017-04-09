#!/bin/bash

echo -n "Decrypt Inventory ... "
ansible-vault decrypt ../hosts --vault-password-file=../../pass
echo -n "Decrypt keys ... "
ansible-vault decrypt ../keys/* --vault-password-file=../../pass
echo -n "Decrypt group_vars ... "
ansible-vault decrypt ../group_vars/* --vault-password-file=../../pass
echo -n "Decrypt role vars ... "
ansible-vault decrypt ../roles/*/vars/* --vault-password-file=../../pass
