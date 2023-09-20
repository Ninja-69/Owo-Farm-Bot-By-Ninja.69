import re, os, asyncio, random, string, keep_alive, discord
from discord.ext import commands, tasks

version = 'v1.0'

user_token = os.environ['user_token']
spam_id = os.environ['spam_id']
catch_id = os.environ['catch_id']
bot_owner = os.environ['bot_owner']
pride_buddy_channel_id = os.environ['pride_buddy_channel_id']
logs_id = False
captcha_ping = False

if os.environ['logs_id']:
    logs_id = os.environ['logs_id']

if os.environ['captcha_ping']:
    captcha_ping = os.environ['captcha_ping']

sh_interval = False

with open('data/pokemon', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/legendary', 'r') as file:
    legendary_list = file.read()
with open('data/mythical', 'r') as file:
    mythical_list = file.read()
with open('data/level', 'r') as file:
    to_level = file.readline()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

poketwo = 716390085896962058
client = commands.Bot(command_prefix='[{ñ*]}¨ñ¨ÇÇÇ¨¨ÇÇÇ¨¨ÇÇÇ¨ñ¨')
stopped = False
captcha_done = True

intervals = [40.2]


def solve(message):
    if not stopped:
        hint = []
        for i in range(15, len(message) - 1):
            if message[i] != '\\':
                hint.append(message[i])
        hint_string = ''
        for i in hint:
            hint_string += i
        hint_replaced = hint_string.replace('_', '.')
        solution = re.findall('^' + hint_replaced + '$', pokemon_list,
                              re.MULTILINE)
        return solution


@tasks.loop(seconds=random.choice(intervals))
async def spam():
    # for i in intervals:
    #   if i < 1.9:
    #     print("→ You can't put less than 1.9s! Your interval was changed temporally to 2s.")
    #     intervals = [2]
    channel = client.get_channel(int(spam_id))
    if not stopped:
      await channel.send("vfiewojògeirjgoiohiewhpvoiweroijgoijrgpreo")


@spam.before_loop
async def before_spam():
    await client.wait_until_ready()


spam.start()


@client.event
async def on_ready():
    print(f'Logged into account: {client.user.name}')


@client.event
async def on_message(message):
    global stopped
    global captcha_done
    channel = client.get_channel(int(catch_id))
    if logs_id:
        logs_channel = client.get_channel(int(logs_id))
    if message.channel.id == int(catch_id):
        if message.author.id == poketwo:
            if not stopped:
                if message.embeds:
                    embed_title = message.embeds[0].title
                    if 'wild pokémon has appeared!' in embed_title:
                        spam.cancel()
                        await asyncio.sleep(30)
                        await channel.send('<@716390085896962058> h')
                    elif "Congratulations" in embed_title:
                        embed_content = message.embeds[0].description
                        if 'now level' in embed_content:
                            split = embed_content.split(' ')
                            a = embed_content.count(' ')
                            level = int(split[a].replace('!', ''))
                            if level == 100:
                                await channel.send(f".s {to_level}")
                                with open('data/level', 'r') as fi:
                                    data = fi.read().splitlines(True)
                                with open('data/level', 'w') as fo:
                                    fo.writelines(data[1:])
                    elif "Pride Buddy?" in embed_title:
                      spam.cancel()
                      stopped = True
                      print(f'--> Pride Buddy "{embed_title.replace(" as Pride Buddy?", "").replace("Set ", "")}" is waiting!')
                      channel = client.get_channel(int(pride_buddy_channel_id))
                      await channel.send(f'<@{bot_owner}>, A Pride Buddy is waiting for you!')
                      await asyncio.sleep(15)
                      spam.start()
                      stopped = False 
              
                else:
                    content = message.content
                    if 'The pokémon is ' in content:
                        if not len(solve(content)):
                            print('Pokemon not found.')
                        else:
                            for i in solve(content):
                                await asyncio.sleep(1.8)
                                await channel.send(
                                    f'<@716390085896962058> c {i}')
                        check = random.randint(1, 60)
                        if check == 1:
                            await asyncio.sleep(900)
                            spam.start()
                        else:
                            await asyncio.sleep(1)
                            spam.start()

                    elif 'Congratulations' in content:
                        global shiny
                        global legendary
                        global num_pokemon
                        global mythical
                        num_pokemon += 1
                        split = content.split(' ')
                        pokemon = split[7].replace('!', '')
                        if 'seem unusual...' in content:
                            shiny += 1

                            print('ㅤㅤㅤㅤ')
                            print(
                                '-----------------------------------------------'
                            )
                            print(f'    ⭐ A SHINY Pokémon was caught! ⭐')
                            print('ㅤㅤㅤㅤ')
                            print(f'    → Total Pokémon Caught: {num_pokemon}')
                            print(f'    → Mythical Pokémon Caught: {mythical}')
                            print(
                                f'    → Legendary Pokémon Caught: {legendary}')
                            print(f'    → Shiny Pokémon Caught: {shiny}')
                            print(
                                '-----------------------------------------------'
                            )
                            print('ㅤㅤㅤㅤ')

                            if logs_id:
                                await logs_channel.send(
                                    f'```⭐ A SHINY Pokémon was caught! ⭐```\n→ Total Pokémon Caught: {num_pokemon}\n→ Mythical Pokémon Caught: {mythical}\n→ Legendary Pokémon Caught: {legendary}\n→ Shiny Pokémon Caught: {shiny}'
                                )

                        elif re.findall('^' + pokemon + '$', legendary_list,
                                        re.MULTILINE):
                            legendary += 1

                            print('ㅤㅤㅤㅤ')
                            print(
                                '-----------------------------------------------'
                            )
                            print(f'     💎 A LEGENDARY Pokémon was caught! 💎')
                            print('ㅤㅤㅤㅤ')
                            print(
                                f'     → Total Pokémon Caught: {num_pokemon}')
                            print(
                                f'     → Mythical Pokémon Caught: {mythical}')
                            print(
                                f'     → Legendary Pokémon Caught: {legendary}'
                            )
                            print(f'     → Shiny Pokémon Caught: {shiny}')
                            print(
                                '-----------------------------------------------'
                            )
                            print('ㅤㅤㅤㅤ')

                            if logs_id:
                                await logs_channel.send(
                                    f'```💎 A LEGENDARY Pokémon was caught! 💎```\n→ Total Pokémon Caught: {num_pokemon}\n→ Mythical Pokémon Caught: {mythical}\n→ Legendary Pokémon Caught: {legendary}\n→ Shiny Pokémon Caught: {shiny}'
                                )

                        elif re.findall('^' + pokemon + '$', mythical_list,
                                        re.MULTILINE):
                            mythical += 1

                            print('ㅤㅤㅤㅤ')
                            print(
                                '-----------------------------------------------'
                            )
                            print(f'     💥 A MYTHICAL Pokémon was caught! 💥')
                            print('ㅤㅤㅤㅤ')
                            print(
                                f'     → Total Pokémon Caught: {num_pokemon}')
                            print(
                                f'     → Mythical Pokémon Caught: {mythical}')
                            print(
                                f'     → Legendary Pokémon Caught: {legendary}'
                            )
                            print(f'     → Shiny Pokémon Caught: {shiny}')
                            print(
                                '-----------------------------------------------'
                            )
                            print('ㅤㅤㅤㅤ')

                            if logs_id:
                                await logs_channel.send(
                                    f'```💥 A MYTHICAL Pokémon was caught! 💥```\n→ Total Pokémon Caught: {num_pokemon}\n→ Mythical Pokémon Caught: {mythical}\n→ Legendary Pokémon Caught: {legendary}\n→ Shiny Pokémon Caught: {shiny}'
                                )

                        else:
                            print('ㅤㅤㅤㅤ')
                            print(
                                '-----------------------------------------------'
                            )
                            print(f'     A new Pokémon was caught!')
                            print('ㅤㅤㅤㅤ')
                            print(
                                f'     → Total Pokémon Caught: {num_pokemon}')
                            print(
                                f'     → Mythical Pokémon Caught: {mythical}')
                            print(
                                f'     → Legendary Pokémon Caught: {legendary}'
                            )
                            print(f'     → Shiny Pokémon Caught: {shiny}')
                            print(
                                '-----------------------------------------------'
                            )
                            print('ㅤㅤㅤㅤ')

                            if logs_id:
                                await logs_channel.send(
                                    f'```A new Pokémon was caught!```\n→ Total Pokémon Caught: {num_pokemon}\n→ Mythical Pokémon Caught: {mythical}\n→ Legendary Pokémon Caught: {legendary}\n→ Shiny Pokémon Caught: {shiny}'
                                )

                    elif 'human' in content:
                        spam.cancel()
                        await logs_channel.send(
                            f"```Oops! Captcha detected!```\nYour autocatcher was paused because a pending captcha. Check your catch channel and use the command '%captcha_done' to confirm the autocatcher can continue."
                        )
                        if captcha_ping:
                            await logs_channel.send(
                                f'Captcha Ping: <@{captcha_ping}>')

                        print(
                            "Captcha detected! Please use '%captcha_done' in discord to reactivate the autocatcher!"
                        )
                        spam.cancel()
                        stopped = True
                        captcha_done = False
    if not message.author.bot:
        await client.process_commands(message)

print()
print(
    f'Pokétwo Autocatcher {version}\nA free  Pokétwo autocatcher Made by Ninja.69 \nEvent Log:'
)
keep_alive.keep_alive()
client.run(f"{user_token}")