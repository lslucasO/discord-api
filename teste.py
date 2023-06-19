content = []

with open("database/Tarefas/tarefas.txt", "r") as arquivo:
    for item in arquivo:
        content.append(item)
        
f = open("database/Tarefas/tarefas.txt", "r")
    
print(len(content))
print(f.read())