# Docker Image Activity Maintainer

This Python script helps maintain Docker Hub images by automatically updating them to prevent inactivity deletion. Docker Hub's retention policy removes inactive images that haven't been pushed or pulled for 6 months.

## Features

- Fetches all public repositories for a specified Docker Hub user
- Checks image tags' last updated timestamps
- Automatically pulls, re-tags, and pushes images that are approaching the inactivity threshold
- Handles pagination for repositories and tags using Docker Hub API v2
- Processes multiple repositories and their tags

## How It Works

The script:

1. Authenticates with Docker Hub using provided credentials
2. Retrieves all public repositories for the user
3. For each repository:
   - Fetches all tags
   - Checks the last updated timestamp for each tag
   - If a tag is older than the threshold (180 days), the script:
     - Pulls the image
     - Re-tags it
     - Pushes it back to Docker Hub

## Prerequisites

- Python 3.6 or higher
- Docker CLI installed and configured
- Docker Hub account with access token
- Required Python packages:
  - requests

## Configuration

The script requires the following configuration:

- Docker Hub username
- Docker Hub access token
- Threshold period (default: 180 days)

## Environment Variables

Copy the example environment file and fill in your values:

```bash
cp .env.example .env

```
