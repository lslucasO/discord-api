content = []
check_list = []

with open("database/Tarefas/tarefas.txt", "r") as arquivo:
    for item in arquivo:

        content.append(item[2:-1])
    
print(content)