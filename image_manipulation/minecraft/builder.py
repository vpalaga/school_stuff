import math
import pickle
from os.path import isfile, join
from PIL import Image, ImageDraw
from generator import ImageLoader
from typing import Dict

class Build:
    FOLDER = "outputs"
    MC_FOLDER = r"C:\Users\vit\AppData\Roaming\.minecraft\saves\New World (5)\datapacks\pixelpack\data\yourpack\functions\builds"

    BLOCK_NAME_MAP = {
        # _side / _top / _front / _back stripped — use base block name
        "ancient_debris_side": "ancient_debris",
        "basalt_side": "basalt",
        "barrel_side": "barrel",
        "beehive_front": "beehive",
        "beehive_front_honey": "beehive",
        "bee_nest_front": "bee_nest",
        "bee_nest_front_honey": "bee_nest",
        "bee_nest_side": "bee_nest",
        "birch_log": "birch_log",  # fine
        "blast_furnace_front": "blast_furnace",
        "bone_block_side": "bone_block",
        "cactus_side": "cactus",
        "cartography_table_side1": "cartography_table",
        "cartography_table_side3": "cartography_table",
        "chiseled_quartz_block_top": "chiseled_quartz_block",
        "chiseled_tuff_bricks_top": "chiseled_tuff_bricks",
        "chiseled_tuff_top": "chiseled_tuff",
        "composter_side": "composter",
        "crafting_table_front": "crafting_table",
        "crafting_table_side": "crafting_table",
        "crafter_bottom": "crafter",
        "crimson_nylium_side": "crimson_nylium",
        "dispenser_front": "dispenser",
        "dried_kelp_side": "dried_kelp_block",
        "dropper_front": "dropper",
        "fletching_table_front": "fletching_table",
        "fletching_table_side": "fletching_table",
        "furnace_front": "furnace",
        "furnace_side": "furnace",
        "hay_block_side": "hay_block",
        "hopper_outside": "hopper",
        "jukebox_side": "jukebox",
        "lodestone_side": "lodestone",
        "loom_front": "loom",
        "loom_side": "loom",
        "melon_side": "melon",
        "muddy_mangrove_roots_side": "muddy_mangrove_roots",
        "mushroom_block_inside": "mushroom_stem",  # pore-only texture = mushroom_stem
        "mycelium_side": "mycelium",
        "observer_back": "observer",
        "observer_front": "observer",
        "observer_side": "observer",
        "ochre_froglight_side": "ochre_froglight",
        "pearlescent_froglight_side": "pearlescent_froglight",
        "piston_top": "piston",
        "piston_top_sticky": "sticky_piston",
        "podzol_side": "podzol",
        "polished_basalt_side": "polished_basalt",
        "pumpkin_side": "pumpkin",
        "quartz_block_side": "quartz_block",
        "reinforced_deepslate_side": "reinforced_deepslate",
        "respawn_anchor_side0": "respawn_anchor",
        "sculk_catalyst_side": "sculk_catalyst",
        "smithing_table_front": "smithing_table",
        "smoker_front": "smoker",
        "smoker_side": "smoker",
        "suspicious_gravel_0": "suspicious_gravel",
        "suspicious_sand_0": "suspicious_sand",
        "target_side": "target",
        "tnt_side": "tnt",
        "verdant_froglight_side": "verdant_froglight",
        "warped_nylium_side": "warped_nylium",
        "blackstone_top": "blackstone",
        "deepslate_top": "deepslate",
        "jack_o_lantern": "jack_o_lantern",  # fine
    }
    def __init__(self, name:str, blockSize:int=16):
        self.name = name
        self.path = join(Build.FOLDER, name + ".png")
        self.blockSize = blockSize

        if not isfile(self.path): # file validation
            raise FileNotFoundError(f"{self.path} not valid")

        self.image = Image.open(self.path)
        self.imageRaw = ImageLoader.load(self.path)
        self.fitsBlocks:tuple[int,int] = self._calcBlocks()
        self.blocksUsed = set()

        self.blockMap:dict[tuple[int,int], str] = pickle.load(open(self.path + ".pkl", "rb"))
        self._filterBlocks()
        print(f"blocks total: {len(self.blockMap)}")
    def _filterBlocks(self)->None:
        newMap = {}
        for pos, block in self.blockMap.items():
            blockRaw = block.split(".")[0]
            blockId = Build.BLOCK_NAME_MAP.get(blockRaw, blockRaw)  # use map, fallback to raw
            newMap[pos] = blockId
            self.blocksUsed.add(blockId)

        self.blockMap = newMap
        print("filtered unusable blocks")
    def _calcBlocks(self)->tuple[int,int]:
        h, w, ch = self.imageRaw.shape

        blockW:int = math.floor(w / self.blockSize)
        blockH:int = math.floor(h / self.blockSize)

        return blockW, blockH
    def show(self)->None:
        self.image.show()

    def splitIntoChunks(self, n:int=16)->None:
        h, w, ch = self.imageRaw.shape

        gapPixels = n * self.blockSize
        draw = ImageDraw.Draw(self.image)

        for x in range(self.fitsBlocks[0]):
            xPos = x * gapPixels
            draw.line((xPos, 0, xPos, h), fill="red", width=2)

        for y in range(self.fitsBlocks[1]):
            yPos = y * gapPixels
            draw.line((0, yPos, w, yPos), fill="red", width=2)

    def printMaterials(self)->None:
        materials: Dict[str, int] = {}

        for block in self.blockMap.values():
            try :
                materials[block] += 1
            except KeyError:
                materials[block] = 1

        materials = dict(sorted(materials.items(), key=lambda item: item[1], reverse=True))

        for block, amt in materials.items():
            print(f"{block:.<35}: {amt:<5}: {amt//64:<3} *64+ {amt%64}")
    def generateCommand(self, z: int = 0) -> None:
        name = self.name.split(".")[0]

        commands = [
            f"setblock {x} {z} {y} minecraft:{block}\nsetblock {x} {z-1} {y} minecraft:stone"
            for (x, y), block in self.blockMap.items()
        ]

        chunk_size = 1000
        chunks = [commands[i:i + chunk_size] for i in range(0, len(commands), chunk_size)]

        # Write chunk files
        for i, chunk in enumerate(chunks):
            path = join(Build.MC_FOLDER, f"{name}_{i + 1}.mcfunction")
            with open(path, "w") as f:
                f.write("\n".join(chunk))

        # Write main file that calls all chunks
        main = "\n".join(f"function yourpack:builds/{name}_{i + 1}" for i in range(len(chunks)))
        with open(join(Build.MC_FOLDER, f"{name}.mcfunction"), "w") as f:
            f.write(main)
    def generateSingleBlockCommand(self)->None:
        name = self.name.split(".")[0]
        for x, block in enumerate(self.blocksUsed):
            main = f"setblock {x} 0 0 minecraft:{block}\nsetblock {x} -1 0 minecraft:stone\n"
            with open(join(Build.MC_FOLDER, f"blocks_{name}_{x}.mcfunction"), "w") as f:
                f.write(main)

        # gen main command file
        commands = [f"function yourpack:builds/blocks_{name}_{n}" for n in range(len(self.blocksUsed))]
        with open(join(Build.MC_FOLDER, f"blocks_{name}.mcfunction"), "w") as f:
            f.write("\n".join(commands))

if __name__ == "__main__":
    b = Build("32")
    b.splitIntoChunks(n=16)
    b.printMaterials()
    b.generateSingleBlockCommand()
    print(b.blocksUsed)
    b.generateCommand()
