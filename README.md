# Blog Application

## User Experience

- **Seamless Registration:** Users can easily sign up to become members of your blogging community, opening doors to a world of content.
- **Effortless Access:** Once registered, users can log in and out with ease, ensuring their privacy and security.
- **Never Lose Access:** Password recovery ensures that users can always regain access to their accounts, even if they forget their passwords.
- **Personalized Profiles:** Users can personalize their profiles by editing details like their name, email, and avatar, making their presence on the platform uniquely theirs.

## Content Management

- **Creative Expression:** Users have the power to create, read, update, and delete their articles, fostering a dynamic and evolving space for ideas and discussions.

# Telegram Bot Integration

## User Engagement

- **Warm Welcome:** The "/start" command welcomes users to the Telegram bot, setting a friendly tone from the start.
- **Guidance at Hand:** The "/help" command provides users with a handy list of available commands and their descriptions, ensuring they can make the most of the bot's features.
- **Stay Updated:** Users can use the "/latest" command to instantly access the newest blog article, keeping them informed and engaged.

## Interactive Features

- **Instant Notifications:** Subscribing to blog updates enables users to receive timely notifications in Telegram whenever a new article is published, keeping them in the loop and eager to explore fresh content.

# Website Integration

## Timely Updates

- **Current Content:** Users can explore the latest news posts, ensuring they're always up-to-date with the freshest content available, all within a day of publication.

# Technical Deployment

## Seamless Setup

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