content = []

with open("database/Tarefas/tarefas.txt", "r") as arquivo:
    for item in arquivo:
        content.append(item)
        
print(len(content))