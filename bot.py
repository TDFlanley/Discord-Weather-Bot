import discord
from discord.ext import commands
import requests
import asyncio
intents = discord.Intents.default()  # Create a default intents object
intents.typing = True  # Disable typing event
intents.presences = True  # Disable presence-related events
intents.message_content = True #enable message content

bot = commands.Bot(command_prefix='!', intents=intents)  # Pass the intents parameter

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def hello(ctx):
     print("Hello command executed")  # Add this line
     await ctx.send("Hello!")
@bot.command()
async def weather(ctx):
    await ctx.send("Please enter a Zip code for weather information.")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        zip_code_message = await bot.wait_for("message", check=check, timeout=30)
        zip_code = zip_code_message.content

        weather_data = get_weather_data(zip_code)

        if weather_data:
            location = weather_data["name"]
            description = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]

            response = f"Weather in {location}: {description}. Temperature: {temperature}°F -"
            if temperature > 90:
                response += " It's fucking hot!"
            elif temperature < 90 and temperature > 70:
                response += " It's fucking perfect!"
            elif temperature > 69.0 and temperature < 70.0:
                response += "Nice"
            else:
                response += " It's fucking chilly!"
            await ctx.send(response)
        else:
            await ctx.send("Unable to fetch weather information for the specified ZIP code.")
    except asyncio.TimeoutError:
        await ctx.send("No ZIP code entered. Weather command cancelled.")


def get_weather_data(zip_code):
    api_key = "30700dc5de76810bf643a034e64f707b"
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={api_key}&units=imperial"

    try:
        response = requests.get(url)
        data = response.json()
        return data
    except requests.RequestException:
        return None 



@bot.command()
async def tvo(ctx):
    temecula_data = get_weather_data("Temecula")
    ontario_data = get_weather_data("Ontario")

    if temecula_data and ontario_data:
        temecula_temp = temecula_data["main"]["temp"]
        ontario_temp = ontario_data["main"]["temp"]

        response = f"Weather in Temecula: {temecula_temp}°F - "
        response += f"\nWeather in Ontario: {ontario_temp}°F - "
        if temecula_temp < ontario_temp and temecula_temp > 45 and temecula_temp < 90:
            response += "\nTemecula wins: It might be borning here, but at least the weather is nice"
        elif temecula_temp > ontario_temp and temecula_temp > 90:
            response += "\nWe all lose, Temecula is burning"
        elif ontario_temp > temecula_temp and ontario_temp > 90:
            response += "\nI don't want to talk bad about Ontario, but, do you smell burning hair?"
        elif ontario_temp < temecula_temp and ontario_temp > 45 and ontario_temp < 90:
            response += "\nAnd people say there is no nice time of year in Ontario"
        else:
            response += "\n Sweet baby Jesus it's cold outside"
        await ctx.send(response)
    else:
        await ctx.send("Unable to fetch weather information.")

def get_weather_data(city):
    api_key = "30700dc5de76810bf643a034e64f707b"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},US&appid={api_key}&units=imperial"

    try:
        response = requests.get(url)
        data = response.json()
        return data
    except requests.RequestException:
        return None


# Run the bot
bot.run("MTEyNDA4MTU4NzE3MzE5NjA3MQ.G63BoA.wUVGJvslYcWenNn4MhyG3oyIPQXu55Yywr6m74")

