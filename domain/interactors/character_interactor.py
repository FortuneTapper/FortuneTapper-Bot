from typing import List
from lxml import etree
from playwright.async_api import async_playwright
from adapter.gateways.character_repository.caching_character_repository import CachingCharacterRepository
from domain.entities import Character, Attributes, Skills, Skill, Defenses, Resources, Resource, Action, ActionCost, ActionType, Actions
from domain.interactors import exceptions


class CharacterInteractor():
    def __init__(self, repository: CachingCharacterRepository, demiplane_url: str):
        self.repository = repository
        self.demiplane_url = demiplane_url

    async def import_character(self, url, user_id, guild_id) -> Character:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url)
                await page.wait_for_selector("#\:r9\:")

                html_content = await page.content()

                page.click("#tabs-container > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-item.grid-block.sheet-tab-container.css-10p3pq5 > div.MuiGrid-root.MuiGrid-container.MuiGrid-item.tabs.css-k82uk1 > div > div:nth-child(2) > h3")
                equipement_content = await page.content()

                page.click("#tabs-container > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-item.grid-block.sheet-tab-container.css-10p3pq5 > div.MuiGrid-root.MuiGrid-container.MuiGrid-item.tabs.css-k82uk1 > div > div:nth-child(3) > h3")
                details_content = await page.content()

                await browser.close()
            
            tree = etree.HTML(html_content)
            tree_details = etree.HTML(details_content)

            character = Character(
                character_id= url.split('/')[-1],
                avatar=tree.xpath("//img[contains(@class, 'avatar__image')]/@src")[0],
                name=tree.xpath("//div[contains(@class, 'character-name')]//div[contains(@class, 'text-block__text')]/text()")[0].strip(),
                attributes=Attributes(
                    strength=int(tree.xpath("//div[contains(@class, 'attribute-box-strength')]//div[contains(@class, 'attribute-value') and contains(@class, 'text-block__text')]/text()")[0].strip()),
                    speed=int(tree.xpath("//div[contains(@class, 'attribute-box-speed')]//div[contains(@class, 'attribute-value') and contains(@class, 'text-block__text')]/text()")[0].strip()),
                    intellect=int(tree.xpath("//div[contains(@class, 'attribute-box-intellect')]//div[contains(@class, 'attribute-value') and contains(@class, 'text-block__text')]/text()")[0].strip()),
                    willpower=int(tree.xpath("//div[contains(@class, 'attribute-box-willpower')]//div[contains(@class, 'attribute-value') and contains(@class, 'text-block__text')]/text()")[0].strip()),
                    awareness=int(tree.xpath("//div[contains(@class, 'attribute-box-awareness')]//div[contains(@class, 'attribute-value') and contains(@class, 'text-block__text')]/text()")[0].strip()),
                    presence=int(tree.xpath("//div[contains(@class, 'attribute-box-presence')]//div[contains(@class, 'attribute-value') and contains(@class, 'text-block__text')]/text()")[0].strip())
                ),
                defenses=Defenses(
                    physical=int(tree.xpath("//div[contains(@class, 'defense-box-physical')]//div[contains(@class, 'defense-value') and contains(@class, 'text-block__text')]/text()")[0].strip()),
                    cognitive=int(tree.xpath("//div[contains(@class, 'defense-box-cognitive')]//div[contains(@class, 'defense-value') and contains(@class, 'text-block__text')]/text()")[0].strip()),
                    spiritual=int(tree.xpath("//div[contains(@class, 'defense-box-spiritual')]//div[contains(@class, 'defense-value') and contains(@class, 'text-block__text')]/text()")[0].strip()),
                    deflect=int(tree.xpath("//div[contains(@class, 'deflect-value')]/text()")[0].strip())
                ),
                resources=Resources(
                    health = Resource(
                        max = int(tree.xpath("//div[contains(@class, 'max-hit-point-indicator')]/text()")[0].strip()[1:]),
                        current =int(tree.xpath("//div[contains(@class, 'max-hit-point-indicator')]/text()")[0].strip()[1:])
                    ),
                    focus = Resource(
                        max = int(tree.xpath("//div[contains(@class, 'resource-box-focus')]//div[contains(@class, 'resource-max') and contains(@class, 'text-block__text')]/text()")[0].strip()[1:]),
                        current = int(tree.xpath("//div[contains(@class, 'resource-box-focus')]//div[contains(@class, 'resource-max') and contains(@class, 'text-block__text')]/text()")[0].strip()[1:])
                    ),
                    investiture = Resource(
                        max = int(tree.xpath("//div[contains(@class, 'resource-box-investiture')]//div[contains(@class, 'resource-max') and contains(@class, 'text-block__text')]/text()")[0].strip()[1:]),
                        current =int(tree.xpath("//div[contains(@class, 'resource-box-investiture')]//div[contains(@class, 'resource-max') and contains(@class, 'text-block__text')]/text()")[0].strip()[1:])
                    ),
                    movement=int(tree.xpath("//div[contains(@class, 'statistic-box--movement')]//div[contains(@class, 'statistic-value') and contains(@class, 'text-block__text')]/text()")[0].strip().split(' ')[0]),
                    recovery_die=int(tree.xpath("//div[contains(@class, 'statistic-box--recovery-die')]//div[contains(@class, 'statistic-value') and contains(@class, 'text-block__text')]/text()")[0].strip()[1:]),
                    senses_range=int(tree.xpath("//div[contains(@class, 'statistic-box--senses-range')]//div[contains(@class, 'statistic-value') and contains(@class, 'text-block__text')]/text()")[0].strip().split(' ')[0])
                ),
                skills = Skills(
                    athletics=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-athletics')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-athletics')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    agility=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-agility')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-agility')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    heavy_weapons=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-heavy-weapons')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-heavy-weapons')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    light_weapons=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-light-weapons')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-light-weapons')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    stealth=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-stealth')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-stealth')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    thievery=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-thievery')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-thievery')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    crafting=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-crafting')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-crafting')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    deduction=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-deduction')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-deduction')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    discipline=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-discipline')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-discipline')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    intimidation=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-intimidation')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-intimidation')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    lore=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-lore')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-lore')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    medicine=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-medicine')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-medicine')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    deception=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-deception')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-deception')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    insight=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-insight')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-insight')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    leadership=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-leadership')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-leadership')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    perception=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-perception')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-perception')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    persuasion=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-persuasion')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-persuasion')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    ),
                    survival=Skill(
                        proficiency=int(len(tree.xpath("//div[contains(@class, 'skill-row-survival')]//div[contains(@class, 'css-7ni74h')]")) / 2),
                        modifier=int(tree.xpath("//div[contains(@class, 'skill-row-survival')]//div[contains(@class, 'skill-modifier')]/text()")[0].strip())
                    )
                ),
                expertises = tree.xpath("//div[contains(@class, 'expertises-box')]//div[contains(@class, 'text-block__text')]/text()")[0].strip().split(', '),
                ancestry = tree.xpath("//div[contains(@class, 'header-name-subtitle-ancestry')]/text()")[0].strip(),
                paths=[],
                actions = Actions(
                    basic = [
                        Action(
                            name=action.xpath(".//div[contains(@class, 'stacked-title__title')]/text()")[0].strip(),
                            description=(
                                ' '.join(traits[0].strip().replace('\n', '').split())
                                if (traits := action.xpath(".//div[contains(@class, 'column--traits')]/text()")) else None
                            ),
                            cost=ActionCost(action.xpath(".//div[contains(@class, 'icon-font')]/div/text()")[0].strip()),
                            type=ActionType.BASIC,
                            dice=(
                                dice[0].strip()
                                if (dice := action.xpath(".//div[contains(@class, 'dice-action-button')]//div[contains(@class, 'simple-action-button-top-label')]/text()")) else None
                            ),
                            focus=(
                                int(focus[0].strip())
                                if (focus := action.xpath(".//div[contains(@class, 'focus-resource-action-button')]//div[contains(@class, 'simple-action-button-top-label')]/text()")) else 0
                            )
                        )
                        for action in tree.xpath("//div[contains(@class, 'sheet-box-component--basic-actions')]//div[contains(@class, 'builder-table-row')]")
                    ]
                ),
                equipament=[],
                goals=[]
            )
        except:
            raise exceptions.CharacterImportError()

        self.repository.save(user_id, guild_id, character)

        return character


    async def update_character(self, user_id, guild_id) -> Character:
        character = self.repository.get(user_id, guild_id)
                
        if character:
            return await self.import_character(f'{self.demiplane_url}{character.character_id}', str(user_id), str(guild_id))
        else:
            raise ReferenceError("No character recovored")
        
    def get_character(self, user_id, guild_id) -> Character:
        character = self.repository.get(user_id, guild_id)

        if not character:
            raise exceptions.CharacterImportError()
        
        return character

    def get_character_list(self, user_id, guild_id) -> List[Character]:
        return self.repository.get_all(user_id, guild_id)

    def select_character(self, user_id, guild_id, character_id) -> Character:
        character = self.repository.set_primary(user_id, guild_id, character_id)
        if not character:
            raise exceptions.CharacterImportError()
        
        return character
        

