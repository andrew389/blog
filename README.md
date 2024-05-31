# Blog Application

## Overview

Welcome to our blogging platform! Our application provides a seamless experience for users to create, manage, and engage with content through a combination of a Django web application, a Telegram bot, and website integration.

## Features

### User Experience

- **Seamless Registration:** Easily sign up and become a member of our blogging community.
- **Effortless Access:** Log in and out with ease, ensuring privacy and security.
- **Password Recovery:** Never lose access to your account with our password recovery feature.
- **Personalized Profiles:** Customize your profile with your name, email, and avatar.

### Content Management

- **Creative Expression:** Create, read, update, and delete articles to foster dynamic discussions.

### Telegram Bot Integration

- **User Engagement:** Receive a warm welcome and guidance with commands like "/start" and "/help".
- **Stay Updated:** Instantly access the latest blog articles with the "/latest" command.
- **Interactive Features:** Subscribe to receive notifications in Telegram for new articles.

### Website Integration

- **Timely Updates:** Explore the latest news posts, ensuring you're always up-to-date with fresh content.

## Technical Deployment

### Seamless Setup
Before you begin, make sure you have the following programs installed on your computer:

```bash
docker --version
```

If after running this command, you were shown the docker version, then go to the next step, else follow these steps:

- Docker: [Docker Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)
1. **Clone Repository:** Simply copy the GitHub repository to your local machine to get started.
   ```bash
   git clone https://github.com/andrew389/blog.git
    ```
2. **Navigate to Directory:** Move into the project directory within your terminal or command prompt.

    ```bash
    cd blog
    ```

3. **Launch with Docker:** Execute the following command to deploy the application using Docker, ensuring a consistent and reliable environment.

    ```bash
    docker-compose up --build -d
    ```


4. **Graceful Shutdown:** When it's time to close up shop, use the following commands to stop and remove Docker containers and images, maintaining a tidy development environment.

    ```bash
    docker stop $(docker ps -q)
    docker rm $(docker ps -a -q)
    docker rmi $(docker images -q)
    ```