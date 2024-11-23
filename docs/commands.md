# 📜 Commands Documentation

This document provides an overview of all available commands in **FortuneTapper-Bot**, including their descriptions, parameters, and examples.

---

## 🎲 Tap Commands

### **`/roll`**
- **Description:** Performs a generic dice roll.
- **Parameters:**
  - `dice` (string): Dice expression in the format `XdY`, e.g., `1d20`, `2d6+3`.
- **Example:**
  ```
  /roll 1d20
  ```

---

### **`/tap`**
- **Description:** Performs a skill test roll.
- **Parameters:**
  - `stat` (choice): The skill to use for the test. Options include:
    - Athletics, Agility, Heavy Weapons, Light Weapons, Stealth, Thievery, Crafting, Deduction, Discipline, Intimidation, Lore, Medicine, Deception, Insight, Leadership, Perception, Persuasion, Survival.
  - `advantage` (choice): Whether to roll with advantage or disadvantage. Options:
    - Advantage, Disadvantage, None.
  - `plot_die` (boolean): Whether to include a plot die in the roll.
  - `plot_advantage` (choice): Whether the plot die roll should have advantage, disadvantage, or none. Options:
    - Advantage, Disadvantage, None.
- **Example:**
  ```
  /tap stat:Athletics advantage:Advantage plot_die:true plot_advantage:Disadvantage
  ```

---

### **`/attack`**
- **Description:** Performs an attack roll.
- **Parameters:**
  - `damage_dice` (string): Dice expression for damage, e.g., `2d8+4`.
  - `weapon_type` (choice): Type of weapon used. Options:
    - Heavy Weapon, Light Weapon, Unarmed.
  - `advantage` (choice): Whether to roll the attack with advantage or disadvantage. Options:
    - Advantage, Disadvantage, None.
  - `damage_advantage` (choice): Whether to roll damage with advantage or disadvantage. Options:
    - Advantage, Disadvantage, None.
  - `plot_die` (boolean): Whether to include a plot die for the attack.
  - `plot_advantage` (choice): Whether the plot die roll should have advantage, disadvantage, or none. Options:
    - Advantage, Disadvantage, None.
  - `plot_die_damage` (boolean): Whether to apply the plot die to the damage roll.
  - `weapon_name` (string): Name of the weapon used.
- **Example:**
  ```
  /attack damage_dice:1d12 weapon_type:Heavy Weapon advantage:None plot_die:true plot_advantage:Advantage
  ```

---

## 👤 Character Commands

### **`/import`**
- **Description:** Imports a character from a Demiplane URL.
- **Parameters:**
  - `url` (string): URL of the Demiplane character sheet.
- **Example:**
  ```
  /import https://demiplane.com/sheet/character/12345
  ```

---

### **`/update`**
- **Description:** Updates the current active character from its Demiplane sheet.
- **Parameters:** None.
- **Example:**
  ```
  /update
  ```

---

### **`/character`**
- **Description:** Displays a summary of the currently active character.
- **Parameters:** None.
- **Example:**
  ```
  /character
  ```

---

### **`/sheet`**
- **Description:** Displays the complete character sheet for the active character.
- **Parameters:** None.
- **Example:**
  ```
  /sheet
  ```

---

### **`/list`**
- **Description:** Lists all imported characters for the current user in the server.
- **Parameters:** None.
- **Example:**
  ```
  /list
  ```

---

### **`/select`**
- **Description:** Selects a character from the user's imported characters list as the active one.
- **Parameters:**
  - `character_id` (string): The ID of the character to select.
- **Example:**
  ```
  /select character_id:12345
  ```

---

## 🔧 Notes
- All commands are slash commands (`/command`) and must be used in Discord chat.
- Ensure your bot has the required permissions to read and send messages in the channel.
- For help, use `/help` or refer to the bot documentation.
