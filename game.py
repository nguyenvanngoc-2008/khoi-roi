import os
import time
import random
import msvcrt

WIDTH = 10
HEIGHT = 20
BORDER = "#"
trang = " "
gia_toc = 0.9  
LEVEL_UP_SCORE = 200   

SHAPES = [  
    [[1, 1, 1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1],
     [1, 1]], 
    [[0, 1, 1],
     [1, 1, 0]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]]
]
SHAPE_CHARS = ["I", "J", "L", "O", "S", "T", "Z"]

class Blocks:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index
        self.shape = SHAPES[index]
        self.xoay1 = 0

    def xoay(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def tao(khoa_vt={}):
    grid = [[trang for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) in khoa_vt:
                grid[y][x] = khoa_vt[(x, y)]
    return grid

def kiem_tra(block, grid):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                try:
                    if block.x + x < 0 or block.x + x >= WIDTH or block.y + y >= HEIGHT:
                        return False
                    if grid[block.y + y][block.x + x] != trang:
                        return False
                except IndexError:
                    return False 
    return True

def clear_rows(grid, locked):
    row_cls = [i for i, row in enumerate(grid) if trang not in row]
    if not row_cls:
        return 0, locked
    row_cls.sort()
    new_locked = {}
    for (x, y), color in locked.items():
        if y in row_cls:
            continue
        shift = sum(1 for cls_y in row_cls if cls_y > y)
        new_locked[(x, y + shift)] = color

    return len(row_cls), new_locked


def draw_grid(grid, score, level, next):
    os.system('cls')
    print("--- Khối Rơi ---")
    print(f"Điểm: {score} | Cấp độ: {level}")
    print("Điều khiển: A(Trái) D(Phải) S(Xuống) W(Xoay) Q(Thoát)")
    print(BORDER * (WIDTH * 2 + 5) + "   --- Tiếp theo ---")

    for y in range(HEIGHT):
        line = BORDER + " "
        for x in range(WIDTH):
            line += grid[y][x] + " "
        line += BORDER
        if y < 5:
            ngoc = "   "
            if y - 1 >= 0 and y - 1 < len(next.shape):
                for cell in next.shape[y-1]:
                    ngoc += SHAPE_CHARS[next.index] + " " if cell else "  "
            line += ngoc

        print(line)

    print(BORDER * (WIDTH * 2 + 3))


def game_loop():
    khoa_vt = {}
    cur = Blocks(WIDTH // 2 - 1, 0, random.randint(0, len(SHAPES) - 1))
    next = Blocks(WIDTH // 2 - 1, 0, random.randint(0, len(SHAPES) - 1))
    game_over = False
    score = 0
    level = 1
    vt_roi = 0.8
    last_time = time.time()
    draw = True 
    while not game_over:
        grid = tao(khoa_vt)
        if msvcrt.kbhit():
            key = msvcrt.getch().lower()
            original_x, original_y = cur.x, cur.y
            
            if key == b'a': # Trái
                cur.x -= 1
            elif key == b'd': # Phải
                cur.x += 1
            elif key == b's': # Xuống
                cur.y += 1
            elif key == b'w': # Xoay
                cur.xoay()
            elif key == b'q': # Thoát
                game_over = True

            if not kiem_tra(cur, grid):
                cur.x, cur.y = original_x, original_y
                if key == b'w': 
                    cur.xoay(); cur.xoay(); cur.xoay()
            else:
                draw = True
        if time.time() - last_time > vt_roi:
            last_time = time.time()
            cur.y += 1
            if not kiem_tra(cur, grid):
                cur.y -= 1
                for y, row in enumerate(cur.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            khoa_vt[(cur.x + x, cur.y + y)] = SHAPE_CHARS[cur.index]
                gwlp = tao(khoa_vt)
                rows_cls, khoa_vt = clear_rows(gwlp, khoa_vt)
                if rows_cls > 0:
                    score += rows_cls * 100 * rows_cls
                    if score >= level * LEVEL_UP_SCORE:
                        level += 1
                        vt_roi *= gia_toc
                
                cur = next
                next = Blocks(WIDTH // 2 - 1, 0, random.randint(0, len(SHAPES) - 1))
                if not kiem_tra(cur, tao(khoa_vt)):
                    game_over = True
            draw = True
        if draw:
            ng = tao(khoa_vt)
            for y, row in enumerate(cur.shape):
                for x, cell in enumerate(row):
                    if cell and cur.y + y >= 0:
                        ng[cur.y + y][cur.x + x] = SHAPE_CHARS[cur.index]
            draw_grid(ng, score, level, next)
            draw = False
        time.sleep(0.01)


    os.system('cls')
    print("--- GAME OVER ---")
    print(f"Điểm của bạn: {score}")

if __name__ == "__main__":
    print("Nhấn phím bất kỳ để bắt đầu...")
    msvcrt.getch()
    game_loop()

