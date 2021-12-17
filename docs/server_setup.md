# Notes taken when setting up Digital Ocean in case there is need to reproduce

- Install `gaveged` to fix docker-compose hanging
	- https://stackoverflow.com/questions/59941911/docker-compose-up-hangs-forever-how-to-debug

For deploying, see https://medium.com/swlh/how-to-deploy-your-application-to-digital-ocean-using-github-actions-and-save-up-on-ci-cd-costs-74b7315facc2
- Create pawnguild user, ssh-keygen, put pub key in deploy keys
- Edit organization secret SSH_HOST to be correct
- Edit organization secret SSH_KEY to be correct (private key)
