# FortuneTapper-Bot

FortuneTapper is a Discord Bot designed to allow playing Cosmere RPG games through Discord.

## 🚀 Features

- Character import
- Dice rolling
- Skill tests and attack actions

## 🛠️ Installation

#### 0. Prerequisites

Before installing and running the project, make sure you have the following components set up:

- Python 3.9 or higher: Required to run the bot.
- Redis Cache: An instance of Redis for caching.
- JSON-compatible Database: A database that supports JSON column types, such as PostgreSQL (version 9.4 or higher).
- Discord Token: Needed to connect the bot to your Discord server (you can follow the [official tutorial](https://discord.com/developers/docs/quick-start/getting-started))

#### 1. Clone the repository
```
git clone https://github.com/FortuneTapper/FortuneTapper-Bot.git
```

#### 2. [Optional] Set up the virtual environment
```
python -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies
```
pip install -r requirements.txt
```

#### 4. Configure environment variables
Create a `.env` file and add the following:
```
DISCORD_TOKEN=your_discord_token
REDIS_URL=url_to_access_redis_cache
DATABASE_URL=any_db_that_supports_json_data
```



## 🧑‍💻 Usage

### Running the Bot

1. **Start the bot**:
```
python bot.py
```

2. **Available Commands**:
## Available Commands

- **`/import <URL>`**: Imports a character from a Demiplane public URL.  
  Example: `/import https://demiplane.com/character/12345`

- **`/update`**: Updates the currently selected character from the Demiplane sheet.

- **`/character`**: Displays a summary of the currently selected character.

- **`/sheet`**: Shows the full character sheet of the selected character.

- **`/list`**: Lists all characters imported by the user.

- **`/select <character_id>`**: Selects a character from the list of available ones.  
  Example: `/select abc123`

- **`/roll <dice>`**: Rolls a generic dice expression (e.g., `1d20`, `2d6`).  
  Example: `/roll 1d20`

- **`/tap <stat> [advantage] [plot_die] [plot_advantage]`**: Performs a skill check using a specified stat. Supports advantage/disadvantage and plot die.  
  Example: `/tap Athletics Advantage True Advantage`

- **`/attack <damage_dice> [weapon_type] [advantage] [damage_advantage] [plot_die] [plot_advantage] [plot_die_damage] [weapon_name]`**: Rolls for an attack, including damage, advantage, and optional plot dice.  
  Example: `/attack 2d8 Light Weapon Advantage None False None False "Shardblade"`



## 📚 Contribution

Before contributing, please read the [wiki](https://github.com/FortuneTapper/FortuneTapper-Bot/wiki) and follow the development guidelines.

1. Fork the project.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push your branch (`git push origin feature/new-feature`).
5. Open a Pull Request.