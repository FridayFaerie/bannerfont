from fontTools.ttLib import TTFont
from fontTools.subset import Options, Subsetter
from fontTools.merge import Merger

symbols_path = "Font.ttf"
latin_path = "Monocraft.ttf"
latin_subset_path = "Monocraft-Subset.ttf"
output_path = "Combined.ttf"
symbols = TTFont(symbols_path)

# Build a subset of the latin font
latin = TTFont(latin_path)
options = Options()
subsetter = Subsetter(options=options)
subsetter.populate(unicodes=range(0, 128))
subsetter.subset(latin)
latin.save(latin_subset_path)

# Merge the symbol font and Latin subset.
# The fonts need matching units per em.
merged = Merger().merge([latin_subset_path, symbols_path])


for name in ["COLR","CPAL"]:#,"SVG ","sbix"]:
    merged[name] = symbols[name]

merged.save(output_path)
