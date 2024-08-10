# BotX - Advanced Discord Chatbot

**BotX** is a sophisticated Discord chatbot designed to enhance your server interactions with dynamic responses and advanced voice capabilities. Developed using the `discord.py` library, BotX features integration with the Mistral AI model and Google Text-to-Speech (gTTS), with voice responses processed through FFmpeg.

## Key Features

- **Dynamic Responses**: BotX utilizes the advanced Mistral AI model via the Groq API to generate precise, relevant, and engaging responses to user queries. Whether you're seeking factual information, need assistance with a task, or just want some fun, BotX's intelligent processing ensures that you receive well-crafted answers that fit the context of your inquiry.

- **Enhanced Voice Interaction**: One of BotX's standout features is its ability to transform text responses into natural, human-like speech. Using Google Text-to-Speech (gTTS), BotX converts written replies into audio, which is then processed through FFmpeg to ensure compatibility with Discord's voice channels. This feature allows the bot to join voice channels and speak directly to users, providing a more immersive and interactive experience. The audio is carefully converted to a format that Discord can handle, ensuring clear and high-quality sound.

- **Interactive Help Menu**: BotX offers a user-friendly help system through an interactive dropdown menu. By using the `!!help` command, users can access a well-organized menu that provides information on various topics such as command usage, voice mode toggles, and developer details. This feature simplifies navigation and makes it easy for users to find the information they need quickly.

- **24/7 Availability**: BotX is hosted on Pylexnodes, a reliable cloud platform, ensuring that it remains active and operational around the clock. This means that the bot is always available to assist with queries, provide entertainment, or manage server interactions, regardless of the time of day. The robust hosting setup guarantees minimal downtime and consistent performance.

## Setup and Installation

To get BotX up and running, follow these steps:

### Prerequisites

- **Python 3.8 or higher**
- **FFmpeg**: Make sure FFmpeg is installed and accessible in your system's PATH.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Haseebasif7/BotX-Discord-.git
   cd BotX
   ```
2. **Create a Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies**
    ```
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables**

   Create a .env file in the root directory of the project and add the following variables:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   GROQ_API_KEY=your_groq_api_key
   user_id=your_discord_user_id

   ```
5. **Run the Bot**
    ```
   python bot.py
   ```
## Usage

### Commands

- **`!!help`** - Displays the interactive help menu.
- **`!!voice`** - Toggles between text and voice mode.
- **`!!logout`** - Logs out the bot (Developer only).
- **`!!<query>`** - Ask the bot a question or request information.

### Voice Interaction

Ensure you are in a voice channel to receive responses in voice mode.

## Contributing

Contributions to BotX are welcome! If you have suggestions, bug reports, or improvements, please open an issue or submit a pull request.

## Acknowledgements

- **discord.py**: For the Discord API wrapper.
- **gTTS**: For text-to-speech conversion.
- **FFmpeg**: For audio processing.
- **Groq API**: For AI-based responses.

