from pathlib import Path

import converter.moxfield as moxfield


p = Path(__file__).parent / "want.csv"
s = moxfield.Moxfield(p)
s.save(Path(__file__).parent / "moxfield.csv")
