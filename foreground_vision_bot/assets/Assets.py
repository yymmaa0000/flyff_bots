from pathlib import Path

import cv2 as cv

mob_aibatt_small_path = str(Path(__file__).parent / "names" / "Aibatt_Small.png")
mob_pukepuke_small_path = str(Path(__file__).parent / "names" / "Pukepuke_Small.png")

# mob_type_wind_path = str(Path(__file__).parent / "mob_types" / "wind.png")
# mob_type_fire_path = str(Path(__file__).parent / "mob_types" / "fire.png")
# mob_type_soil_path = str(Path(__file__).parent / "mob_types" / "soil.png")
# mob_type_water_path = str(Path(__file__).parent / "mob_types" / "water.png")
# mob_type_electricity_path = str(Path(__file__).parent / "mob_types" / "electricity.png")

mob_type_wind_path = str(Path(__file__).parent / "mob_types" / "wind_weak.png")
mob_type_fire_path = str(Path(__file__).parent / "mob_types" / "fire_weak.png")
mob_type_soil_path = str(Path(__file__).parent / "mob_types" / "soil_weak.png")
mob_type_water_path = str(Path(__file__).parent / "mob_types" / "water_weak.png")
mob_type_electricity_path = str(Path(__file__).parent / "mob_types" / "electricity_weak.png")

mob_life_bar_path = str(Path(__file__).parent / "general" / "mob_life_bar.png")
user_target_bar_path = str(Path(__file__).parent / "general" / "user_target_bar.png")
inventory_perin_converter_path = str(Path(__file__).parent / "general" / "inventory_perin_converter.png")
inventory_icons_path = str(Path(__file__).parent / "general" / "inventory_icons.png")


class MobType:
    WIND = cv.imread(mob_type_wind_path, cv.IMREAD_GRAYSCALE)
    FIRE = cv.imread(mob_type_fire_path, cv.IMREAD_GRAYSCALE)
    SOIL = cv.imread(mob_type_soil_path, cv.IMREAD_GRAYSCALE)
    WATER = cv.imread(mob_type_water_path, cv.IMREAD_GRAYSCALE)
    ELECTRICITY = cv.imread(mob_type_electricity_path, cv.IMREAD_GRAYSCALE)


class MobInfo:
    AIBATT = {
        "name": "aibatt",
        "element": "wind",
        "map_name": "Flaris",
        "height_offset": 20,
        "name_img": cv.imread(mob_aibatt_small_path, cv.IMREAD_GRAYSCALE),
        "element_img": MobType.WIND,
    }
    PUKEPUKE = {
        "name": "pukepuke",
        "element": "fire",
        "map_name": "Flaris",
        "height_offset": 40,
        "name_img": cv.imread(mob_pukepuke_small_path, cv.IMREAD_GRAYSCALE),
        "element_img": MobType.FIRE,
    }

    @staticmethod
    def get_all_mobs():
        """
        Get a list of all mobs registered. Using a approach of getting all 
        attributes of the class, and filtering the internal class attributes.

        :return: list of all mobs
        """
        return [
            getattr(MobInfo, attr)
            for attr in dir(MobInfo)
            if not attr.startswith("__") and not callable(getattr(MobInfo, attr))
        ]


class GeneralAssets:
    MOB_LIFE_BAR = cv.imread(mob_life_bar_path, cv.IMREAD_GRAYSCALE)
    USER_TARGET_BAR = cv.imread(user_target_bar_path, cv.IMREAD_GRAYSCALE)
    INVENTORY_PERIN_CONVERTER = cv.imread(inventory_perin_converter_path, cv.IMREAD_GRAYSCALE)
    INVENTORY_ICONS = cv.imread(inventory_icons_path, cv.IMREAD_GRAYSCALE)
