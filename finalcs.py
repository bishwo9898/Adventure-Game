from graphics import *
import random

def load_map_file(filename):
    file = open(filename, "r")
    map_data = []
    line = file.readline()
    while line != "":
        line = line.strip()
        row = line.split(" ")
        map_data.append(row)
        line = file.readline()
    file.close()
    return map_data

def find_player_start(map_data):
    row = 0
    col = 0
    while row < len(map_data):
        col = 0
        while col < len(map_data[0]):
            if map_data[row][col] == "U":
                return row, col
            col = col + 1
        row = row + 1

def wall_nearby(map_data, row, col, pr, pc):
    if map_data[row][col] != "W":
        return False
    if row == pr - 1 and col == pc:
        return True
    if row == pr + 1 and col == pc:
        return True
    if row == pr and col == pc - 1:
        return True
    if row == pr and col == pc + 1:
        return True
    return False


def draw_everything(win, map_data, pr, pc, gold, has_sword):
    win.setBackground("gray")

    row = 0
    while row < len(map_data):
        col = 0
        while col < len(map_data[0]):
            x1 = col * 35
            y1 = row * 35
            x2 = x1 + 35
            y2 = y1 + 35
            tile = Rectangle(Point(x1, y1), Point(x2, y2))
            if row == pr and col == pc:
                tile.setFill("green")
            elif wall_nearby(map_data, row, col, pr, pc):
                tile.setFill("gray")
            else:
                tile.setFill("white")
            tile.draw(win)
            col = col + 1
        row = row + 1

    hud_bg = Rectangle(Point(620, 70), Point(750, 160))
    hud_bg.setFill("gray")
    hud_bg.setOutline("gray")
    hud_bg.draw(win)

    gold_text = Text(Point(685, 90), "Gold: " + str(gold))
    weapon_name = "Sword" if has_sword else "Sling"
    weapon_text = Text(Point(685, 120), "Weapon: " + weapon_name)
    gold_text.setSize(12)
    weapon_text.setSize(12)
    gold_text.draw(win)
    weapon_text.draw(win)

def draw_arrow_buttons(win):
    buttons = {}

    up = Rectangle(Point(650, 400), Point(690, 440))
    down = Rectangle(Point(650, 480), Point(690, 520))
    left = Rectangle(Point(610, 440), Point(650, 480))
    right = Rectangle(Point(690, 440), Point(730, 480))

    up.setFill("lightblue")
    down.setFill("lightblue")
    left.setFill("lightblue")
    right.setFill("lightblue")

    up.draw(win)
    down.draw(win)
    left.draw(win)
    right.draw(win)

    Text(up.getCenter(), "↑").draw(win)
    Text(down.getCenter(), "↓").draw(win)
    Text(left.getCenter(), "←").draw(win)
    Text(right.getCenter(), "→").draw(win)

    buttons["Up"] = up
    buttons["Down"] = down
    buttons["Left"] = left
    buttons["Right"] = right

    return buttons

def which_button(buttons, point):
    if not point:
        return ""
    if point.getX() < 610 or point.getX() > 730 or point.getY() < 400 or point.getY() > 520:
        return ""
    if 650 <= point.getX() <= 690:
        if 400 <= point.getY() <= 440:
            return "Up"
        if 480 <= point.getY() <= 520:
            return "Down"
    if 610 <= point.getX() <= 650 and 440 <= point.getY() <= 480:
        return "Left"
    if 690 <= point.getX() <= 730 and 440 <= point.getY() <= 480:
        return "Right"
    return ""

def try_move(map_data, row, col, direction):
    new_row = row
    new_col = col
    if direction == "Up":
        new_row = row - 1
    if direction == "Down":
        new_row = row + 1
    if direction == "Left":
        new_col = col - 1
    if direction == "Right":
        new_col = col + 1
    if map_data[new_row][new_col] != "W":
        return new_row, new_col
    return row, col

def show_popup(message):
    win = GraphWin("Information", 300, 100)
    text = Text(Point(150, 40), message)
    text.setSize(12)
    text.draw(win)
    note = Text(Point(150, 75), "(click to keep going)")
    note.setSize(8)
    note.setTextColor("gray")
    note.draw(win)
    win.getMouse()
    win.close()

def end_screen(win, message, color):
    txt = Text(Point(380, 280), message)
    txt.setSize(36)
    txt.setTextColor(color)
    txt.draw(win)

def game_intro():
    win = GraphWin("Adventure Begins", 765, 565)
    win.setBackground("black")

    lines = [
        "You wake up for your 8 am class, but this morning, everything feels scary.",
        "You find yourself lost on campus. This feels like a dream, but very real at the same time...",
        "",
        "You wake up in a cold, damp, dark area. You're lying on the ground in a pool of blood and vomit.",
        "It appears to be your own. Wow! What a wild night last night was.",
        "You remember so little, but your head pounds and you wish you were home in bed",
        "(or even in Dave's 170 class - anywhere but here). ",
        "You remember so little, but your head pounds and you wish you were home in bed.",
        "You stagger to your feet and bump up against a slimy wall. Ewwwwww!",
        "Your pockets are empty. Even your trusty dagger is gone. This so sucks.",
        "You spot a sling and some rocks on the ground and take them. It's time to get out of here."
    ]

    y = 50
    for i in range(len(lines)):
        line = Text(Point(380, y), lines[i])
        line.setTextColor("white")
        line.setSize(15)
        line.draw(win)
        y = y + 25

    click_note = Text(Point(380, 540), "(Click anywhere to begin your escape...)")
    click_note.setSize(10)
    click_note.setTextColor("gray")
    click_note.draw(win)
    win.getMouse()
    win.close()

def check_tile(tile, has_sword, gold):
    alive = True
    won = False
    chance = random.randint(1, 100)
    if tile == "G":
        show_popup("You found gold! +50")
        gold = gold + 50
    if tile == "S":
        show_popup("You found a sword! You feel powerful.")
        has_sword = True
    if tile == "P":
        show_popup("You fell in a pit and died.")
        alive = False
    if tile == "E":
        show_popup("You made it to the exit!")
        won = True
    if tile == "K":
        if has_sword:
            if chance <= 99:
                show_popup("You fought a kobold and won!")
            else:
                show_popup("You fought a kobold and died!")
                alive = False
        else:
            if chance <= 75:
                show_popup("You fought a kobold and won!")
            else:
                show_popup("You fought a kobold and died!")
                alive = False
    if tile == "O":
        if has_sword:
            if chance <= 90:
                show_popup("You fought an ogre and won!")
            else:
                show_popup("You fought an ogre and died!")
                alive = False
        else:
            if chance <= 20:
                show_popup("You fought an ogre and won!")
            else:
                show_popup("You fought an ogre and died!")
                alive = False
    if tile == "D":
        if has_sword:
            if chance <= 10:
                show_popup("You fought a dragon and survived! You are insane!")
            else:
                show_popup("You got fried by the dragon! ")
                alive = False
        else:
            if chance <= 1:
                show_popup("You fought a dragon and survived!")
            else:
                show_popup("You got roasted by the dragon!")
                alive = False
    return alive, won, has_sword, gold

def run_level(filename):
    map_data = load_map_file(filename)
    pr, pc = find_player_start(map_data)
    has_sword = False
    gold = 0
    alive = True
    won = False

    win = GraphWin("Adventure", 765, 565)
    buttons = draw_arrow_buttons(win)
    draw_everything(win, map_data, pr, pc, gold, has_sword)

    playing = True
    while playing:
        if alive == True and won == False:
            click = win.getMouse()
            direction = which_button(buttons, click)
            if direction != "":
                move_result = try_move(map_data, pr, pc, direction)
                new_r = move_result[0]
                new_c = move_result[1]
                tile_result = check_tile(map_data[new_r][new_c], has_sword, gold)
                alive = tile_result[0]
                won = tile_result[1]
                has_sword = tile_result[2]
                gold = tile_result[3]
                if map_data[new_r][new_c] != "W" and alive:
                    pr = new_r
                    pc = new_c
                    map_data[pr][pc] = "-"
                draw_everything(win, map_data, pr, pc, gold, has_sword)
        else:
            playing = False

    return win, won, alive

def main():
    game_intro() 

    lvl1 = run_level("map01.txt")
    win = lvl1[0]
    success = lvl1[1]
    alive = lvl1[2]


    if success == True:
        show_popup("You found a ladder! Let's jump to the next level!")
        win.close()
        lvl2 = run_level("map02.txt")
        win = lvl2[0]
        success = lvl2[1]

    if success == True:
        end_screen(win, "Yay! You Escaped! :D", "green")
    else:
        end_screen(win, "Game Over :(", "red")

    win.getMouse()
    win.close()

main()
