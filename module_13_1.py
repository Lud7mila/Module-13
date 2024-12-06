# "Асинхронные силачи"

import asyncio
import time

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    delay = 1/power
    for ind in range(1, 6):
        print(f'Силач {name} поднял {ind} шар' )
        await asyncio.sleep(delay)
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    print("Старт")
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))
    await task1
    await task2
    await task3
    print("Финиш")


start = time.time()
asyncio.run(start_tournament())
end = time.time()
print(end - start)
