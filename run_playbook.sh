#!/bin/bash

export DO_API_KEY='apikeytyid8tg8g90sd8acv80vc8b'
export DO_SSH_KEY='sshkey8s:8a:8f:8g'
export DOMAIN='testdomain.com'
export A_RECORD='12345678'
export EMAIL='test@test.com'

ansible-playbook jitsi-provision.yml
