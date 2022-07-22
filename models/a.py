import dill
import pandas as pd
import matplotlib.pyplot as plt
with open("natural_evolution.dill" ,"rb") as f:
    fi = dill.load(f)

df = pd.DataFrame.from_dict(fi['scores'], orient="index")
fig = df.plot(title="NaturalEvolution",figsize=(7,4)).get_figure()
plt.tight_layout()
fig.savefig('../../natural_evolution_30_generations.png', facecolor=(1, 1, 1))
print(df)
