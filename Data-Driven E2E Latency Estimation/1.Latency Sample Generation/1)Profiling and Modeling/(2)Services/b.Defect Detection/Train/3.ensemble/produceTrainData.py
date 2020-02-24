
if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    from PIL import Image
    # Convert data into pictures
    df = pd.read_pickle("./wafermap_withpattern.pkl")

    df_withlabel = df.reset_index()
    df_withlabel.info()
    print(df_withlabel[:2])
    inde=[]
    for index, row in df_withlabel.iterrows():
        usage = str(row['trianTestLabel'][0][0])
        if usage == 'Training':
            inde.append(row["index"])
    print(inde)
    df_withlabel=df_withlabel.loc[df_withlabel['index'].isin(inde)]
    df_withlabel.info()
    df_withlabel.to_pickle("wafermap_withpatterntrain.pkl")
