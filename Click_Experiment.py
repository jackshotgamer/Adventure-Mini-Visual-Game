import sys
import sqlite3
import queue
import mouse
from random import randrange
clicks = queue.Queue()
con = sqlite3.connect('Click.sqlite')
con.execute("""create table if not exists `Clicks`(x int, y int)""")
con.commit()
mode = input('Is this input or map: ').lower().strip()

if mode == 'input':
    class A:
        def write(self, x):
            with open('somefile.txt', 'a') as f:
                f.write(str(x))

        def flush(self): pass


    def func():
        clicks.put((abs(mouse.get_position()[0]), abs(mouse.get_position()[1] - 1080)))


    sys.stdout = A()
    mouse.on_click(func)
    while True:
        x, y = clicks.get(block=True)
        con.execute("""insert into Clicks values (?,?)""", (x, y))
        con.commit()
elif mode == 'map':
    import arcade


    class AndScene(arcade.View):
        def __init__(self):
            super().__init__()
            self.shapelist = arcade.ShapeElementList()
            cursor = con.cursor()
            cursor.execute('select * from Clicks')
            for x_, y_ in cursor:
                self.shapelist.append(arcade.create_ellipse(x_, y_, 20, 20, (255, 0, 0, 15)))

        def on_draw(self):
            arcade.start_render()
            self.shapelist.draw()


    window = arcade.Window(800, 600, 'Heat map', fullscreen=True)
    window.show_view(AndScene())
    arcade.run()
if mode == 'secret':
    cursor = con.cursor()
    cursor.execute('select * from Clicks')
    times = 0
    length = 1
    do = True
    cursor2 = cursor
    for item in cursor2.fetchall():
        length += 1
    xlist = []
    ylist = []
    from numpy import mean
    import time
    import random

    cursor.execute('select * from Clicks')
    for x, y in cursor:
        times += 1
        if not times % 50:
            time.sleep(0.1)
            _ = round((times / length) * 100) + random.randint(-1, 1)
            _2 = _ if _ < 100 else 100
            if _2 >= 100:
                print('100%')
                do = False
            if do:
                print(f'{_2}%')
        xlist.append(x)
        ylist.append(y)
    if times > 0:
        time.sleep(4)
        for x in range(1, 97):
            if random.randint(0, 9) == 1:
                print(f'Results are {x}% ready')
            elif random.randint(0, 18) == 1:
                print('Assessing...')
            elif random.randint(0, 25) == 1:
                print('Calculating...')
            time.sleep(0.2)
        time.sleep(1)
        print(f'Results are 99% ready')
        time.sleep(2)
        print('Results ready.')
        time.sleep(2)
        password = input('Please enter password: ')
        time.sleep(1)
        print('Authorising... ')
        time.sleep(2)
        if password.lower().strip() != 'hm#':
            print('Incorrect Password')
            time.sleep(2)
            print('Authorities have been alerted, do not resist.')
            time.sleep(1)
            sys.exit(911)
        print('Account Authorised to see Project HeatMap')
        time.sleep(2)
        print('Results:')
        time.sleep(1)
        print(f'Mean of all x values: {mean(xlist)}')
        time.sleep(1)
        print(f'Mean of all y values: {mean(ylist)}')
        time.sleep(1)
        print('You are restricted from repeating these values to anyone else.\n- Project HeatMap')
        time.sleep(1)
        show_map = input('(y/n) do you wish to see more of Project HeatMap?\n')
        time.sleep(1)
        if show_map.lower().strip() == 'n':
            print('Very well.')
            time.sleep(1)
            sys.exit()
        elif show_map.lower().strip() == 'y':
            print('Loading...')
            for x in range(1, 97):
                if random.randint(0, 9) == 1:
                    print(f'Loading: {x}%')
                elif random.randint(0, 18) == 1:
                    print('Preparing...')
                elif random.randint(0, 25) == 1:
                    print('Formatting...')
                time.sleep(0.2)
            time.sleep(3)
            print('Showing you Project HeatMap')
            time.sleep(2)
            import arcade


            class AndScene(arcade.View):
                def __init__(self):
                    super().__init__()
                    self.shapelist = arcade.ShapeElementList()
                    cursor_ = con.cursor()
                    cursor_.execute('select * from Clicks')
                    for x_, y_ in cursor_:
                        self.shapelist.append(arcade.create_ellipse(x_, y_, 20, 20, (255, 0, 0, 15)))

                def on_draw(self):
                    arcade.start_render()
                    self.shapelist.draw()


            window = arcade.Window(800, 600, 'Heat map', fullscreen=True)
            window.show_view(AndScene())
            arcade.run()
    else:
        print('Results are empty.')
