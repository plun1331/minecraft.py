#  Copyright (c) 2023, plun1331
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from enum import Enum as _Enum
from typing import Any

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from .datatypes import Byte, Int, String, UnsignedByte, Varint


class Enum(_Enum):
    """The base Enum class. All enums should inherit from this class."""

    def __bytes__(self):
        return bytes(self.value)

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    @classmethod
    def from_value(cls, value: Any) -> Self:
        """
        Converts a value into an enum member.

        :param value: The value to convert.

        :return: The enum member.

        :raises ValueError: The value is not a valid enum member.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")


class NextState(Enum):
    """The next state of the connection."""

    STATUS = Varint(1)
    LOGIN = Varint(2)


class State(Enum):
    HANDSHAKE = Varint(0)
    STATUS = Varint(1)
    LOGIN = Varint(2)
    PLAY = Varint(3)


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


class GameEvents(Enum):
    NO_RESPAWN_BLOCK_AVAILABLE = UnsignedByte(0)
    END_RAINING = UnsignedByte(1)
    BEGIN_RAINING = UnsignedByte(2)
    CHANGE_GAMEMODE = UnsignedByte(3)
    WIN_GAME = UnsignedByte(4)
    DEMO_EVENT = UnsignedByte(5)
    ARROW_HIT_PLAYER = UnsignedByte(6)
    RAIN_STRENGTH = UnsignedByte(7)
    THUNDER_STRENGTH = UnsignedByte(8)
    PUFFERFISH_STING = UnsignedByte(9)
    ELDER_GUARDIAN_MOB_APPEARANCE = UnsignedByte(10)
    ENABLE_RESPAWN_SCREEN = UnsignedByte(11)


class WorldEvents(Enum):
    DISPENSER_DISPENSES = Int(1000)
    DISPENSER_FAILS_TO_DISPENSE = Int(1001)
    DISPENSER_SHOOTS = Int(1002)
    ENDER_EYE_LAUNCHED = Int(1003)
    FIREWORK_SHOT = Int(1004)
    IRON_DOOR_OPENED = Int(1005)
    WOODEN_DOOR_OPENED = Int(1006)
    WOODEN_TRAPDOOR_OPENED = Int(1007)
    FENCE_GATE_OPENED = Int(1008)
    FIRE_EXTINGUISHED = Int(1009)
    PLAY_RECORD = Int(1010)
    IRON_DOOR_CLOSED = Int(1011)
    WOODEN_DOOR_CLOSED = Int(1012)
    WOODEN_TRAPDOOR_CLOSED = Int(1013)
    FENCE_GATE_CLOSED = Int(1014)
    GHAST_WARN = Int(1015)
    GHAST_SHOOTS = Int(1016)
    ENDERDRAGON_SHOOTS = Int(1017)
    BLAZE_SHOOTS = Int(1018)
    ZOMBIE_ATTACKS_WOOD_DOOR = Int(1019)
    ZOMBIE_ATTACKS_IRON_DOOR = Int(1020)
    ZOMBIE_BREAKS_WOOD_DOOR = Int(1021)
    WITHER_BREAKS_BLOCK = Int(1022)
    WITHER_SPAWNED = Int(1023)
    WITHER_SHOOTS = Int(1024)
    BAT_TAKES_OFF = Int(1025)
    ZOMBIE_INFECTS = Int(1026)
    ZOMBIE_VILLAGER_CONVERTED = Int(1027)
    ENDERDRAGON_DEATH = Int(1028)
    ANVIL_DESTROYED = Int(1029)
    ANVIL_USED = Int(1030)
    ANVIL_LANDED = Int(1031)
    PORTAL_TRAVEL = Int(1032)
    CHORUS_FLOWER_GROWN = Int(1033)
    CHORUS_FLOWER_DIED = Int(1034)
    BREWING_STAND_BREWED = Int(1035)
    IRON_TRAPDOOR_OPENED = Int(1036)
    IRON_TRAPDOOR_CLOSED = Int(1037)
    END_PORTAL_CREATED_IN_OVERWORLD = Int(1038)
    PHANTOM_BITES = Int(1039)
    ZOMBIE_CONVERTS_TO_DROWNED = Int(1040)
    HUSK_CONVERTS_TO_ZOMBIE_BY_DROWNING = Int(1041)
    GRINDSTONE_USED = Int(1042)
    BOOK_PAGE_TURNED = Int(1043)
    COMPOSTER_COMPOSTS = Int(1500)
    LAVA_CONVERTS_BLOCK = Int(1501)
    REDSTONE_TORCH_BURNS_OUT = Int(1502)
    ENDER_EYE_PLACED = Int(1503)
    SPAWNS_10_SMOKE_PARTICLES = Int(2000)
    BLOCK_BREAK = Int(2001)
    SPLASH_POTION = Int(2002)
    EYE_OF_ENDER_ENTITY_BREAK_ANIMATION = Int(2003)
    MOB_SPAWN_PARTICLE_EFFECT = Int(2004)
    BONEMEAL_PARTICLES = Int(2005)
    DRAGON_BREATH = Int(2006)
    INSTANT_SPLASH_POTION = Int(2007)
    ENDERDRAGON_DESTROYS_BLOCK = Int(2008)
    WET_SPONGE_VAPORIZES_IN_NETHER = Int(2009)
    END_GATEWAY_SPAWN = Int(3000)
    ENDERDRAGON_GROWL = Int(3001)
    ELECTRIC_SPARK = Int(3002)
    COPPER_APPLY_WAX = Int(3003)
    COPPER_REMOVE_WAX = Int(3004)
    COPPER_SCRAPE_OXIDATION = Int(3005)


class MapIconType(Enum):
    WHITE_ARROW = Varint(0)
    GREEN_ARROW = Varint(1)
    RED_ARROW = Varint(2)
    BLUE_ARROW = Varint(3)
    WHITE_CROSS = Varint(4)
    RED_POINTER = Varint(5)
    WHITE_CIRCLE = Varint(6)
    SMALL_WHITE_CIRCLE = Varint(7)
    MANSION = Varint(8)
    TEMPLE = Varint(9)
    WHITE_BANNER = Varint(10)
    ORANGE_BANNER = Varint(11)
    MAGENTA_BANNER = Varint(12)
    LIGHT_BLUE_BANNER = Varint(13)
    YELLOW_BANNER = Varint(14)
    LIME_BANNER = Varint(15)
    PINK_BANNER = Varint(16)
    GRAY_BANNER = Varint(17)
    LIGHT_GRAY_BANNER = Varint(18)
    CYAN_BANNER = Varint(19)
    PURPLE_BANNER = Varint(20)
    BLUE_BANNER = Varint(21)
    BROWN_BANNER = Varint(22)
    GREEN_BANNER = Varint(23)
    RED_BANNER = Varint(24)
    BLACK_BANNER = Varint(25)
    TREASURE_MARKER = Varint(26)


class Hand(Enum):
    MAIN_HAND = Varint(0)
    OFF_HAND = Varint(1)


class FilterType(Enum):
    PASS_THROUGH = Varint(0)
    FULLY_FILTERED = Varint(1)
    PARTIALLY_FILTERED = Varint(2)


class PlayerInfoUpdateActionBits(Enum):
    ADD_PLAYER = 0x01
    INITIALIZE_CHAT = 0x02
    UPDATE_GAMEMODE = 0x04
    UPDATE_LISTED = 0x08
    UPDATE_LATENCY = 0x16
    UPDATE_DISPLAY_NAME = 0x32


class FeetEyes(Enum):
    FEET = Varint(0)
    EYES = Varint(1)


class RecipeBookActionType(Enum):
    INIT = Varint(0)
    ADD = Varint(1)
    REMOVE = Varint(2)


class ChatColor(Enum):
    BLACK = Varint(0)
    DARK_BLUE = Varint(1)
    DARK_GREEN = Varint(2)
    DARK_AQUA = Varint(3)
    DARK_RED = Varint(4)
    DARK_PURPLE = Varint(5)
    GOLD = Varint(6)
    GRAY = Varint(7)
    DARK_GRAY = Varint(8)
    BLUE = Varint(9)
    GREEN = Varint(10)
    AQUA = Varint(11)
    RED = Varint(12)
    LIGHT_PURPLE = Varint(13)
    YELLOW = Varint(14)
    WHITE = Varint(15)
    OBFUSCATED = Varint(16)
    BOLD = Varint(17)
    STRIKETHROUGH = Varint(18)
    UNDERLINE = Varint(19)
    ITALIC = Varint(20)
    RESET = Varint(21)


class ScoreboardPosition(Enum):
    LIST = Byte(0)
    SIDEBAR = Byte(1)
    BELOW_NAME = Byte(2)
    TEAM_SPECIFIC_BLACK = Byte(3)
    TEAM_SPECIFIC_DARK_BLUE = Byte(4)
    TEAM_SPECIFIC_DARK_GREEN = Byte(5)
    TEAM_SPECIFIC_DARK_AQUA = Byte(6)
    TEAM_SPECIFIC_DARK_RED = Byte(7)
    TEAM_SPECIFIC_PURPLE = Byte(8)
    TEAM_SPECIFIC_GOLD = Byte(9)
    TEAM_SPECIFIC_GRAY = Byte(10)
    TEAM_SPECIFIC_DARK_GRAY = Byte(11)
    TEAM_SPECIFIC_BLUE = Byte(12)
    TEAM_SPECIFIC_GREEN = Byte(13)
    TEAM_SPECIFIC_AQUA = Byte(14)
    TEAM_SPECIFIC_RED = Byte(15)
    TEAM_SPECIFIC_LIGHT_PURPLE = Byte(16)
    TEAM_SPECIFIC_YELLOW = Byte(17)
    TEAM_SPECIFIC_WHITE = Byte(18)


class EquipmentSlot(Enum):
    MAINHAND = Byte(0)
    OFFHAND = Byte(1)
    BOOTS = Byte(2)
    LEGGINGS = Byte(3)
    CHESTPLATE = Byte(4)
    HELMET = Byte(5)


class UpdateObjectiveModes(Enum):
    CREATE = Byte(0)
    REMOVE = Byte(1)
    UPDATE = Byte(2)


class UpdateObjectiveType(Enum):
    INTEGER = Varint(0)
    HEARTS = Varint(1)


class UpdateTeamModes(Enum):
    CREATE = Byte(0)
    REMOVE = Byte(1)
    UPDATE = Byte(2)
    ADD_ENTITIES = Byte(3)
    REMOVE_ENTITIES = Byte(4)


class NameTagVisibility(Enum):
    ALWAYS = String("always")
    HIDE_FOR_OTHER_TEAMS = String("hideForOtherTeams")
    HIDE_FOR_OWN_TEAM = String("hideForOwnTeam")
    NEVER = String("never")


class CollisionRule(Enum):
    ALWAYS = String("always")
    PUSH_OTHER_TEAMS = String("pushOtherTeams")
    PUSH_OWN_TEAM = String("pushOwnTeam")
    NEVER = String("never")


class UpdateScoreAction(Enum):
    CREATE_OR_UPDATE = Varint(0)
    REMOVE = Varint(1)


class AdvancementFrameType(Enum):
    TASK = Varint(0)
    CHALLENGE = Varint(1)
    GOAL = Varint(2)


class ClientCommandAction(Enum):
    PERFORM_RESPAWN = Varint(0)
    REQUEST_STATS = Varint(1)


class ChatMode(Enum):
    ENABLED = Varint(0)
    COMMANDS_ONLY = Varint(1)
    HIDDEN = Varint(2)


class MainHand(Enum):
    LEFT = Varint(0)
    RIGHT = Varint(1)


class InteractionType(Enum):
    INTERACT = Varint(0)
    ATTACK = Varint(1)
    INTERACT_AT = Varint(2)


class PlayerActionStatus(Enum):
    STARTED_DIGGING = Varint(0)
    CANCELLED_DIGGING = Varint(1)
    FINISHED_DIGGING = Varint(2)
    DROP_ITEM_STACK = Varint(3)
    DROP_ITEM = Varint(4)
    SHOOT_ARROW = Varint(5)
    SWAP_ITEM_IN_HAND = Varint(6)


class BlockFace(Enum):
    BOTTOM = Byte(0)
    TOP = Byte(1)
    NORTH = Byte(2)
    SOUTH = Byte(3)
    WEST = Byte(4)
    EAST = Byte(5)


class PlayerCommandAction(Enum):
    START_SNEAKING = Varint(0)
    STOP_SNEAKING = Varint(1)
    LEAVE_BED = Varint(2)
    START_SPRINTING = Varint(3)
    STOP_SPRINTING = Varint(4)
    START_JUMP_WITH_HORSE = Varint(5)
    STOP_JUMP_WITH_HORSE = Varint(6)
    OPEN_HORSE_INVENTORY = Varint(7)
    START_FLYING_WITH_ELYTRA = Varint(8)


class RecipeBookID(Enum):
    CRAFTING = Varint(0)
    FURNACE = Varint(1)
    BLAST_FURNACE = Varint(2)
    SMOKER = Varint(3)


class ResourcePackStatus(Enum):
    SUCCESSFULLY_LOADED = Varint(0)
    DECLINED = Varint(1)
    FAILED_DOWNLOAD = Varint(2)
    ACCEPTED = Varint(3)


class SeenAdvancementsAction(Enum):
    OPENED_TAB = Varint(0)
    CLOSED_SCREEN = Varint(1)


class CommandBlockMode(Enum):
    SEQUENCE = Varint(0)
    AUTO = Varint(1)
    REDSTONE = Varint(2)


class ProgramStructureBlockAction(Enum):
    UPDATE_DATA = Varint(0)
    SAVE_STRUCTURE = Varint(1)
    LOAD_STRUCTURE = Varint(2)
    DETECT_SIZE = Varint(3)


class ProgramStructureBlockMode(Enum):
    SAVE = Varint(0)
    LOAD = Varint(1)
    CORNER = Varint(2)
    DATA = Varint(3)


class ProgramStructureBlockMirror(Enum):
    NONE = Varint(0)
    LEFT_RIGHT = Varint(1)
    FRONT_BACK = Varint(2)


class ProgramStructureBlockRotation(Enum):
    NONE = Varint(0)
    CLOCKWISE_90 = Varint(1)
    CLOCKWISE_180 = Varint(2)
    COUNTERCLOCKWISE_90 = Varint(3)
