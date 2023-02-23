"""
Copyright (c) 2023 plun1331

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from enum import Enum
from .datatypes import Short, Varint, UnsignedByte


class NextState(Enum):
    STATUS = Varint(1)
    LOGIN = Varint(2)


class Animation(Enum):
    SWING_MAIN_ARM = UnsignedByte(0)
    TAKE_DAMAGE = UnsignedByte(1)
    LEAVE_BED = UnsignedByte(2)
    SWING_OFFHAND = UnsignedByte(3)
    CRITICAL_EFFECT = UnsignedByte(4)
    MAGIC_CRITICAL_EFFECT = UnsignedByte(5)


class StatCategory(Enum):
    MINED = Varint(0)
    CRAFTED = Varint(1)
    USED = Varint(2)
    BROKEN = Varint(3)
    PICKED_UP = Varint(4)
    DROPPED = Varint(5)
    KILLED = Varint(6)
    KILLED_BY = Varint(7)
    CUSTOM = Varint(8)


class StatID(Enum):
    LEAVE_GAME = Varint(0)
    PLAY_ONE_MINUTE = Varint(1)
    TIME_SINCE_DEATH = Varint(2)
    TIME_SINCE_REST = Varint(3)
    SNEAK_TIME = Varint(4)
    WALK_ONE_CM = Varint(5)
    CROUCH_ONE_CM = Varint(6)
    SPRINT_ONE_CM = Varint(7)
    WALK_ON_WATER_ONE_CM = Varint(8)
    FALL_ONE_CM = Varint(9)
    CLIMB_ONE_CM = Varint(10)
    FLY_ONE_CM = Varint(11)
    WALK_UNDER_WATER_ONE_CM = Varint(12)
    MINECART_ONE_CM = Varint(13)
    BOAT_ONE_CM = Varint(14)
    PIG_ONE_CM = Varint(15)
    HORSE_ONE_CM = Varint(16)
    AVIATE_ONE_CM = Varint(17)
    SWIM_ONE_CM = Varint(18)
    STRIDER_ONE_CM = Varint(19)
    JUMP = Varint(20)
    DROP = Varint(21)
    DAMAGE_DEALT = Varint(22)
    DAMAGE_DEALT_ABSORBED = Varint(23)
    DAMAGE_DEALT_RESISTED = Varint(24)
    DAMAGE_TAKEN = Varint(25)
    DAMAGE_BLOCKED_BY_SHIELD = Varint(26)
    DAMAGE_ABSORBED = Varint(27)
    DAMAGE_RESISTED = Varint(28)
    DEATHS = Varint(29)
    MOB_KILLS = Varint(30)
    ANIMALS_BRED = Varint(31)
    PLAYER_KILLS = Varint(32)
    FISH_CAUGHT = Varint(33)
    TALKED_TO_VILLAGER = Varint(34)
    TRADED_WITH_VILLAGER = Varint(35)
    EAT_CAKE_SLICE = Varint(36)
    FILL_CAULDRON = Varint(37)
    USE_CAULDRON = Varint(38)
    CLEAN_ARMOR = Varint(39)
    CLEAN_BANNER = Varint(40)
    CLEAN_SHULKER_BOX = Varint(41)
    INTERACT_WITH_BREWINGSTAND = Varint(42)
    INTERACT_WITH_BEACON = Varint(43)
    INSPECT_DROPPER = Varint(44)
    INSPECT_HOPPER = Varint(45)
    INSPECT_DISPENSER = Varint(46)
    PLAY_NOTEBLOCK = Varint(47)
    TUNE_NOTEBLOCK = Varint(48)
    POT_FLOWER = Varint(49)
    TRIGGER_TRAPPED_CHEST = Varint(50)
    OPEN_ENDERCHEST = Varint(51)
    ENCHANT_ITEM = Varint(52)
    PLAY_RECORD = Varint(53)
    INTERACT_WITH_FURNACE = Varint(54)
    INTERACT_WITH_CRAFTING_TABLE = Varint(55)
    OPEN_CHEST = Varint(56)
    SLEEP_IN_BED = Varint(57)
    OPEN_SHULKER_BOX = Varint(58)
    OPEN_BARREL = Varint(59)
    INTERACT_WITH_BLAST_FURNACE = Varint(60)
    INTERACT_WITH_SMOKER = Varint(61)
    INTERACT_WITH_LECTERN = Varint(62)
    INTERACT_WITH_CAMPFIRE = Varint(63)
    INTERACT_WITH_CARTOGRAPHY_TABLE = Varint(64)
    INTERACT_WITH_LOOM = Varint(65)
    INTERACT_WITH_STONECUTTER = Varint(66)
    BELL_RING = Varint(67)
    RAID_TRIGGER = Varint(68)
    RAID_WIN = Varint(69)
    INTERACT_WITH_ANVIL = Varint(70)
    INTERACT_WITH_GRINDSTONE = Varint(71)
    TARGET_HIT = Varint(72)
    INTERACT_WITH_SMITHING_TABLE = Varint(73)


class BossBarColor(Enum):
    PINK = Varint(0)
    BLUE = Varint(1)
    RED = Varint(2)
    GREEN = Varint(3)
    YELLOW = Varint(4)
    PURPLE = Varint(5)
    WHITE = Varint(6)


class BossBarDivision(Enum):
    NO_DIVISION = Varint(0)
    SIX_NOTCHES = Varint(1)
    TEN_NOTCHES = Varint(2)
    TWELVE_NOTCHES = Varint(3)
    TWENTY_NOTCHES = Varint(4)


class CommandParser(Enum):
    BOOL = Varint(0)
    FLOAT = Varint(1)
    DOUBLE = Varint(2)
    INTEGER = Varint(3)
    LONG = Varint(4)
    STRING = Varint(5)
    ENTITY = Varint(6)
    GAME_PROFILE = Varint(7)
    BLOCK_POS = Varint(8)
    COLUMN_POS = Varint(9)
    VEC3 = Varint(10)
    VEC2 = Varint(11)
    BLOCK_STATE = Varint(12)
    BLOCK_PREDICATE = Varint(13)
    ITEM_STACK = Varint(14)
    ITEM_PREDICATE = Varint(15)
    COLOR = Varint(16)
    COMPONENT = Varint(17)
    MESSAGE = Varint(18)
    NBT = Varint(19)
    NBT_TAG = Varint(20)
    NBT_PATH = Varint(21)
    OBJECTIVE = Varint(22)
    OBJECTIVE_CRITERIA = Varint(23)
    OPERATION = Varint(24)
    PARTICLE = Varint(25)
    ANGLE = Varint(26)
    ROTATION = Varint(27)
    SCOREBOARD_SLOT = Varint(28)
    SCORE_HOLDER = Varint(29)
    SWIZZLE = Varint(30)
    TEAM = Varint(31)
    ITEM_SLOT = Varint(32)
    RESOURCE_LOCATION = Varint(33)
    FUNCTION = Varint(34)
    ENTITY_ANCHOR = Varint(35)
    INT_RANGE = Varint(36)
    FLOAT_RANGE = Varint(37)
    DIMENSION = Varint(38)
    GAMEMODE = Varint(39)
    TIME = Varint(40)
    RESOURCE_OR_TAG = Varint(41)
    RESOURCE_OR_TAG_KEY = Varint(42)
    TEMPLATE_MIRROR = Varint(45)
    TEMPLATE_ROTATION = Varint(46)
    UUID = Varint(47)


class BrigadierStringParser(Enum):
    SINGLE_WORD = Varint(0)
    QUOTABLE_PHRASE = Varint(1)
    GREEDY_PHRASE = Varint(2)


class FurnaceWindowProperty(Enum):
    FIRE_ICON = Short(0)
    MAX_BURN_TIME = Short(1)
    PROGRESS_ARROW = Short(2)
    MAX_PROGRESS_ARROW = Short(3)


class EnchantmentTableWindowProperty(Enum):
    LEVEL_REQUIREMENT_1 = Short(0)
    LEVEL_REQUIREMENT_2 = Short(1)
    LEVEL_REQUIREMENT_3 = Short(2)
    ENCHANTMENT_SEED = Short(3)
    ENCHANTMENT_ID_1 = Short(4)
    ENCHANTMENT_ID_2 = Short(5)
    ENCHANTMENT_ID_3 = Short(6)
    ENCHANTMENT_LEVEL_1 = Short(7)
    ENCHANTMENT_LEVEL_2 = Short(8)
    ENCHANTMENT_LEVEL_3 = Short(9)


class BeaconWindowProperty(Enum):
    POWER_LEVEL = Short(0)
    PRIMARY_EFFECT = Short(1)
    SECONDARY_EFFECT = Short(2)


class AnvilWindowProperty(Enum):
    REPAIR_COST = Short(0)


class BrewingStandWindowProperty(Enum):
    BREW_TIME = Short(0)
    FUEL_TIME = Short(1)


class StonecutterWindowProperty(Enum):
    RECIPE = Short(0)


class LoomWindowProperty(Enum):
    PATTERN = Short(0)


class LecternWindowProperty(Enum):
    PAGE = Short(0)


class Enchant(Enum):
    PROTECTION = Varint(0)
    FIRE_PROTECTION = Varint(1)
    FEATHER_FALLING = Varint(2)
    BLAST_PROTECTION = Varint(3)
    PROJECTILE_PROTECTION = Varint(4)
    RESPIRATION = Varint(5)
    AQUA_AFFINITY = Varint(6)
    THORNS = Varint(7)
    DEPTH_STRIDER = Varint(8)
    FROST_WALKER = Varint(9)
    BINDING_CURSE = Varint(10)
    SOUL_SPEED = Varint(11)
    SHARPNESS = Varint(12)
    SMITE = Varint(13)
    BANE_OF_ARTHROPODS = Varint(14)
    KNOCKBACK = Varint(15)
    FIRE_ASPECT = Varint(16)
    LOOTING = Varint(17)
    SWEEPING = Varint(18)
    EFFICIENCY = Varint(19)
    SILK_TOUCH = Varint(20)
    UNBREAKING = Varint(21)
    FORTUNE = Varint(22)
    POWER = Varint(23)
    PUNCH = Varint(24)
    FLAME = Varint(25)
    INFINITY = Varint(26)
    LUCK_OF_THE_SEA = Varint(27)
    LURE = Varint(28)
    LOYALTY = Varint(29)
    IMPALING = Varint(30)
    RIPTIDE = Varint(31)
    CHANNELING = Varint(32)
    MULTISHOT = Varint(33)
    QUICK_CHARGE = Varint(34)
    PIERCING = Varint(35)
    MENDING = Varint(36)
    VANISHING_CURSE = Varint(37)


class ChatSuggestionAction(Enum):
    ADD = Varint(0)
    REMOVE = Varint(1)
    SET = Varint(2)
