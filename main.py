import os
import logging
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from discord.ui import View
import discord
from gtts import gTTS
import io
import asyncio
import ffmpeg
import tempfile


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('BotX')

class DropDown(View):
    @discord.ui.select(
        placeholder="Choose an option",
        options=[
            discord.SelectOption(label="Example Chats", value="prompts"),
            discord.SelectOption(label='Voice Commands',value="voice_com"),
            discord.SelectOption(label="Developer Info", value="dev")
        ]
    )
    async def select_callback(self, interaction, select):
        if select.values[0] == "prompts":
            help_prompt = '''To ask a question or use a command, please start your message with !!. For example:
• `!!Tell me a joke` - Request a joke from me.
• `!!Write a Python program` - To write any code
• `!!How to use Discord?` - Ask any question
'''
            await interaction.response.send_message(help_prompt)
        elif select.values[0] == 'dev':
            dev_prompt = '''BotX is developed by Haseeb Asif.
You can find more about me here:
• [LinkedIn](https://www.linkedin.com/in/haseeb-asif-4400212a0?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
• [GitHub](https://github.com/HaseebAsif7)
'''
            await interaction.response.send_message(dev_prompt)
        elif select.values[0]=="voice_com":
            voice_prompt=''' By default, responses are provided in text. To switch to voice mode, please use the `!!voice` command. Use !!quit to make Bot leave the call'''
            await interaction.response.send_message(voice_prompt)
            

async def get_response(query):
    if query and query not in ('voice', 'help'):
        llm = ChatGroq(
            temperature=0.5,
            model="mixtral-8x7b-32768",
            api_key=os.getenv('GROQ_API_KEY')
        )

        prompt_template = PromptTemplate(
            input_variables=["user_query"],
            template="""
            You are a friendly and helpful chatbot integrated into a Discord server. Your goal is to provide positive, concise, and relevant responses to user queries. Keep in mind that users are seeking quick and clear answers, so respond in a way that is engaging and easy to understand.

            Here is the user's query:
            {user_query}

            Provide a helpful and positive response, considering the nature of a Discord community and don't use emojis!!.
            """
        )
        chain = prompt_template | llm
        response = chain.invoke({'user_query': query})
        return response.content
    else:
        return "Invalid query or command."

# Load secret keys from dotenv file
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

# Define intents
intents = Intents.default()
intents.message_content = True  # Enable message content intent

Command_template = '!!'

# Create bot instance
bot = commands.Bot(command_prefix=Command_template, intents=intents, help_command=None)

@bot.event
async def on_ready():
    global voice
    voice=0 # default (text)
    
    await bot.change_presence(activity=discord.Game(name='Listening to !!help'))
    logger.info(f'Logged in as {bot.user}')
    logger.info(f'State: {bot.is_ready()}')

@bot.event
async def on_message(message):
    global voice
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Handle logout command (For Developer only)
    if message.content.startswith(Command_template + 'logout') and message.author.id==int(os.getenv('user_id')):
        try:
            await message.channel.send('Logging Out')
            await bot.close()
            logger.info('Logged Out')
        except Exception as e:
            logger.error(f'Error handling logout: {e}')
        return

    # Handle bot mentions
    if bot.user.mentioned_in(message):
        await message.channel.send(f'Hello {message.author.mention}! How can I assist you today? Use !!help for assistance')
        logger.info(f'{message.author} mentioned {bot.user}')
        return

    # Handle commands with the command template
    if message.content.startswith(Command_template): 
        query = message.content[len(Command_template):]   # Remove command template and strip extra spaces
        if query == 'help':
            view = DropDown()
            await message.channel.send('Choose an option from the dropdown:', view=view)
            logger.info(f'{message.author} asked for help')
            return
        
        if query == 'voice':
            if voice == 0:
                voice = 1
                logger.info(f'voice :{voice}')
                await message.channel.send("Voice Enabled")
            else:
                voice = 0
                logger.info(f'voice :{voice}')
                await message.channel.send("Voice Disabled")
            return

        if query != 'voice' and query !='quit':  
            response = await get_response(query)
            
            if voice == 0:  # Response in text
                await message.channel.send(response)
                logger.info(f'{message.author} asked: {query}')
            
            elif voice == 1:  # Response in voice
                if message.author.voice:  # If the user is in a voice channel
                    voice_channel = message.author.voice.channel
                    await speak_text(response, voice_channel)  # Ensure this is an async function call
                else:
                    await message.channel.send('You must be in a voice channel to hear the response!')

            return
        
        if query == 'quit':
            vc = discord.utils.get(bot.voice_clients, guild=message.guild)
            if vc and vc.is_connected():
                await vc.disconnect()
                await message.channel.send('Disconnected from voice channel.')
            else:
                await message.channel.send('Bot is not connected to any voice channel.')
            

    await bot.process_commands(message)


async def speak_text(response, voice_channel):
    tts = gTTS(text=response, lang='en')
    
    # Create a temporary file to store the initial audio data
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_input:
        tts.write_to_fp(temp_input)
        temp_input_path = temp_input.name
    
    # Define a path for the converted audio file
    temp_output_path = tempfile.mktemp(suffix='.wav')
    
    # Convert the audio file to WAV format using ffmpeg
    ffmpeg.input(temp_input_path).output(temp_output_path, format='wav').run()
    
    # Remove the initial temporary file
    os.remove(temp_input_path)
    
    # Connect to the voice channel
    vc = await voice_channel.connect()
    
    # Play the converted audio file
    logger.info('Speaking in Voice Channel')
    vc.play(discord.FFmpegPCMAudio(temp_output_path))

    
    while vc.is_playing():
        await asyncio.sleep(1)


    logger.info('Done Speaking')
    await vc.disconnect()

    
    os.remove(temp_output_path)


def main():
    bot.run(discord_token)

if __name__ == '__main__':
    main()
