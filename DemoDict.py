colors = {"apple":"red", "banana":"yellow"}
print(len(colors))

colors["kiwi"] = "green"
print(colors["apple"])

for item in colors.items():
    print(item)
