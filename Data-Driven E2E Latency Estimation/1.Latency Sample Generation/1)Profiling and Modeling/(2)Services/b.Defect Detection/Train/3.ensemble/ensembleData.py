import pandas as pd

waferattributescnn4 = pd.read_csv("./wafercnnAttribute4.csv")
waferattributessvm = pd.read_csv("./wafersvmAttribute.csv")
waferattributes4 = pd.concat([waferattributescnn4, waferattributessvm], axis=1)
waferattributes4.to_csv("waferAttribute4.csv")

waferattributescnn0 = pd.read_csv("./wafercnnAttribute0.csv")
waferattributes0 = pd.concat([waferattributescnn0, waferattributessvm], axis=1)

waferattributes0.to_csv("waferAttribute0.csv")