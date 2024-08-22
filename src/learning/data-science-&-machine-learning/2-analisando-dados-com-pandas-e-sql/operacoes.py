import pandas as pd

df = pd.df = pd.DataFrame(
    {
        "col1": [1, 2, 3, 4],
        "col2": [444, 555, 666, 444],
        "col3": ["abc", "def", "ghi", "xyz"],
    }
)

df
df.head()

df.info()
df.memory_usage()

df["col2"].unique()

df["col2"].nunique()


def comp(x):
    return x**2


df["col1_calc"] = df["col1"].apply(comp)
res = df["col1"].apply(lambda x: x * 5)
res

df
df["col1"].sum()
df["col1"].mean()
df["col1"].product()
df["col1"].std()
df["col1"].max()
df["col1"].sum()

df["col1"].idxmax()

df[df["col2"] == 444]

df[df["col2"] == 444]["col1"].sum()

df.sort_values(by="col2")

data = {
    "A": ["foo", "foo", "foo", "bar", "bar", "bar"],
    "B": ["one", "one", "two", "two", "one", "one"],
    "C": ["x", "y", "x", "y", "x", "y"],
    "D": [1, 3, 2, 5, 4, 1],
}

df = pd.DataFrame(data)

dict_map = {"one": "1", "two": "2"}

df['E']  = df["B"].map(dict_map)
df


df.pivot_table(index="A", columns="B", values="D")