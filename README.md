# Telegram Message Bot - v0.3.4

This repository contains a Telegram bot script that allows you to send messages and images to a chat at specified
intervals using the Telegram Bot API. The bot is built using Python and utilizes the Aiogram library.

## Getting Started

### Prerequisites

- Python 3.x
- Aiogram 3.x
- fnmatch
- PIL, Image, ImageFont, ImageDraw
- sqlite3
- requests
- schedule

### Installation

1. Clone this repository to your local machine:

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. For ubuntu install font (opcional):

    ```bash
    apt install ttf-mscorefonts-installer
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a file named `conf.py` in the same directory as the bot script and set the required configuration variables:

    ```python
    # conf.py
    start_times = ['09:00', '12:00', '15:00']  # Add the times you want the bot to send messages
    db_path = 'my_database.db'  # Set the path to your SQLite database
    bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace this with your Telegram bot token or create .env file
    ```

Replace `YOUR_TELEGRAM_BOT_TOKEN` with your Telegram bot token.

### First run

  ```bash
  #Create dir img, logs and Create empty DB
  python ai_mess_bot.py --generate
  
  #Add admin chat ID respectively
  python ai_mess_bot.py --createadmin 123456789,NameAdmin
  
  ```

## Functionality

### Sending Messages and Images

The bot can send both text messages and images. It retrieves messages and image paths from a SQLite database and sends
them to the specified chat ID at the times specified in `start_times`.

To add a new message to the bot, you can use the command `/create` and then follow the prompts to save the message to
the database.

To add an image to a specific message, you can use the command `/upload` and follow the prompts to upload the image and
associate it with the desired message ID.

### Managing Messages

The bot provides several commands to manage messages:

- `/status`: Check the status of sent and unsent messages.
- `/get`: Retrieve information about a specific message, including associated images (if any).
- `/create`: Add new message in DB and return saved ID.
- `/upload`: Add new IMG for ID message.
- `/search`: Search message search by keyword return list ID messages.
- `/status`: Return status sending.
- `/control`: Change admin list
- Callback queries: The bot provides inline keyboard buttons for message management, such as removing a message,
  removing associated images, and replacing the message.

### Schedule and Sending

The bot uses the `schedule` library to schedule sending messages at the specified times in `start_times`. The `run()`
function sets up the schedule, and the bot continuously checks for pending tasks using `schedule.run_pending()`.

## Running the Bot

To run the bot, simply execute the script:

```bash
python ai_mess_bot.py --run
python mess_task.py
```

The bot will start polling for updates and send messages at the specified times.

## Note

Make sure you have properly set up the Telegram bot and obtained the bot token from the BotFather before running the
script. Also, ensure that the SQLite database file is available and accessible to the script.

## Contributions

Contributions to the project are welcome. Feel free to open issues or submit pull requests for any improvements or bug
fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
