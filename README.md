<h1 align="center">Welcome to Slack Commands 👋</h1>

## ✨ Overview

Within this repository it will demostrate how to slack commands solution

## Features

- ✨ `/motivate` Get quote of the day
- ✨ `/aws-get-resources` List resources against given region and service within AWS

## Locally

- 🚀 Prerequisites
    1. Docker
    2. AWS SAM
    3. Slack
    4. Ngrok

- 🚀 Commands
    1. `export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock`
    2. `sam build -t infrastructure/sam/template.yaml --use-container`
    3. `sam local start-api`

## Coming Soon
- ❗️ Infrastructure support in Terraform

## Author

👤 **Jazz**