import os, time, math, random
from enum import Enum

class AnimationType(Enum):
    WAVES = "Волны"
    CUBE = "3D Куб"
    PARTICLES = "Частицы"
    SIN = "Синусоида"
    SPIRAL = "Спираль"
    EXPLOSION = "Взрыв"
    MATRIX = "Матрица"
    FIRE = "Огонь"
    BOUNCE = "Мяч"
    STARS = "Звезды"
    HEART = "Пульсирующее сердце"
    SNAKE = "Змейка"
    RAINBOW = "Радуга"

class Generator:
    def __init__(self, w=60, h=25):
        self.w, self.h = w, h
        self.chars = " .:;+=xX$&@"
        self.frame = 0
        
    def get_char(self, b):
        return self.chars[int(max(0, min(0.99, b)) * (len(self.chars)-1))]
    
    def clear(self):
        print('\033[2J\033[H', end='')
    
    def waves(self):
        buf = [[' ']*self.w for _ in range(self.h)]
        for y in range(self.h):
            for x in range(self.w):
                v = (math.sin(x*0.15+self.frame*0.1) + math.cos(y*0.1+self.frame*0.12) + math.sin((x+y)*0.08+self.frame*0.15))/3
                buf[y][x] = self.get_char((v+1)/2)
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def cube(self):
        buf = [[' ']*self.w for _ in range(self.h)]
        cx, cy = self.w//2, self.h//2
        sz = min(self.w, self.h)//4
        ax, ay = self.frame*0.05, self.frame*0.07
        verts = [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]
        edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        proj = []
        for v in verts:
            y = v[1]*math.cos(ax)-v[2]*math.sin(ax)
            z = v[1]*math.sin(ax)+v[2]*math.cos(ax)
            x2 = v[0]*math.cos(ay)+z*math.sin(ay)
            z2 = -v[0]*math.sin(ay)+z*math.cos(ay)
            s = 1.5/(z2+2.5)
            proj.append((int(cx+x2*sz*s), int(cy-y*sz*s)))
        for e in edges:
            x1,y1 = proj[e[0]]
            x2,y2 = proj[e[1]]
            dx,dy = abs(x2-x1), abs(y2-y1)
            sx = 1 if x1<x2 else -1
            sy = 1 if y1<y2 else -1
            err = dx-dy
            while True:
                if 0<=x1<self.w and 0<=y1<self.h: buf[y1][x1] = '#'
                if x1==x2 and y1==y2: break
                e2 = err*2
                if e2 > -dy: err -= dy; x1 += sx
                if e2 < dx: err += dx; y1 += sy
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def particles(self):
        if not hasattr(self, 'ps'):
            self.ps = []
            for _ in range(40):
                self.ps.append([random.uniform(0,self.w), random.uniform(0,self.h),
                               random.uniform(-1,1), random.uniform(-1,1), 1.0])
        buf = [[' ']*self.w for _ in range(self.h)]
        for p in self.ps:
            p[0] += p[2]; p[1] += p[3]; p[4] -= 0.01
            if p[4]<=0 or p[0]<0 or p[0]>=self.w or p[1]<0 or p[1]>=self.h:
                p[0]=random.uniform(0,self.w); p[1]=random.uniform(0,self.h)
                p[2]=random.uniform(-1,1); p[3]=random.uniform(-1,1); p[4]=1.0
            x,y = int(p[0]), int(p[1])
            if 0<=x<self.w and 0<=y<self.h: buf[y][x] = self.get_char(p[4])
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def sin_wave(self):
        buf = [[' ']*self.w for _ in range(self.h)]
        for x in range(self.w):
            y = self.h//2 + int(math.sin(x*0.2+self.frame*0.2)*10)
            if 0<=y<self.h: buf[y][x] = '@'
            y2 = self.h//3 + int(math.sin(x*0.3+self.frame*0.25)*6)
            if 0<=y2<self.h: buf[y2][x] = '#'
            y3 = self.h*2//3 + int(math.cos(x*0.25+self.frame*0.15)*8)
            if 0<=y3<self.h: buf[y3][x] = '+'
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def spiral(self):
        buf = [[' ']*self.w for _ in range(self.h)]
        cx, cy = self.w//2, self.h//2
        mr = min(self.w, self.h)//2
        for i in range(200):
            t = i/50
            r = (t%1)*mr
            a = 4*2*math.pi*(t%1)-self.frame*0.1
            x,y = int(cx+r*math.cos(a)), int(cy+r*math.sin(a))
            if 0<=x<self.w and 0<=y<self.h: buf[y][x] = self.get_char(1-r/mr)
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def explosion(self):
        buf = [[' ']*self.w for _ in range(self.h)]
        cx, cy = self.w//2, self.h//2
        r = (self.frame%30)*2
        for y in range(self.h):
            for x in range(self.w):
                d = math.sqrt((x-cx)**2+(y-cy)**2)
                if abs(d-r)<2: buf[y][x] = '@'
        for _ in range(30):
            a = random.uniform(0,2*math.pi)
            rr = r+random.uniform(-5,10)
            x,y = int(cx+rr*math.cos(a)), int(cy+rr*math.sin(a))
            if 0<=x<self.w and 0<=y<self.h: buf[y][x] = random.choice('*+#@')
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def matrix(self):
        if not hasattr(self, 'drops'):
            self.drops = []
            for _ in range(self.w//4):
                self.drops.append([random.randint(0,self.w), random.randint(0,self.h),
                                  random.uniform(1,4), random.randint(5,15)])
        buf = [[' ']*self.w for _ in range(self.h)]
        for d in self.drops:
            d[1] += d[2]
            if d[1] > self.h+d[3]: d[1] = -d[3]; d[0] = random.randint(0,self.w)
            for i in range(d[3]):
                y = int(d[1]-i)
                if 0<=y<self.h and 0<=d[0]<self.w:
                    buf[y][d[0]] = '@' if i==0 else self.get_char(1-i/d[3])
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def fire(self):
        if not hasattr(self, 'fb'):
            self.fb = [[0]*self.w for _ in range(self.h)]
        for x in range(self.w): self.fb[self.h-1][x] = random.randint(200,255)
        for y in range(self.h-2,-1,-1):
            for x in range(self.w):
                l = self.fb[y+1][x-1] if x>0 else 0
                c = self.fb[y+1][x]
                r = self.fb[y+1][x+1] if x<self.w-1 else 0
                self.fb[y][x] = max(0, (l+c+r)//3 - random.randint(0,5))
        buf = [[' ']*self.w for _ in range(self.h)]
        for y in range(self.h):
            for x in range(self.w):
                b = self.fb[y][x]/255
                buf[y][x] = '@' if b>0.8 else '#' if b>0.6 else '+' if b>0.4 else '.' if b>0.2 else ' '
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def bounce(self):
        if not hasattr(self, 'ball'):
            self.ball = [self.w//2, self.h//2, random.uniform(1,3), random.uniform(1,3)]
        buf = [[' ']*self.w for _ in range(self.h)]
        b = self.ball
        b[0] += b[2]; b[1] += b[3]
        if b[0]<=0 or b[0]>=self.w-1: b[2] = -b[2]; b[0] = max(0, min(self.w-1, b[0]))
        if b[1]<=0 or b[1]>=self.h-1: b[3] = -b[3]; b[1] = max(0, min(self.h-1, b[1]))
        r = 3
        for y in range(max(0,int(b[1]-r)), min(self.h,int(b[1]+r+1))):
            for x in range(max(0,int(b[0]-r)), min(self.w,int(b[0]+r+1))):
                d = math.sqrt((x-b[0])**2+(y-b[1])**2)
                if d<=r: buf[y][x] = '@' if d<r*0.7 else 'O' if d<r*0.9 else 'o'
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def stars(self):
        if not hasattr(self, 'stars_list'):
            self.stars_list = []
            for _ in range(80):
                self.stars_list.append([random.randint(0,self.w-1), random.randint(0,self.h-1),
                                       random.uniform(0.3,1), random.uniform(0.02,0.1)])
        buf = [[' ']*self.w for _ in range(self.h)]
        for s in self.stars_list:
            b = s[2] + math.sin(self.frame*s[3])*0.3
            b = max(0.1, min(1, b))
            if b>0.8: c='*'
            elif b>0.6: c='.'
            else: c=' '
            if 0<=s[0]<self.w and 0<=s[1]<self.h: buf[s[1]][s[0]] = c
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def heart(self):
        """Пульсирующее сердце"""
        buf = [[' ']*self.w for _ in range(self.h)]
        cx, cy = self.w//2, self.h//2
        pulse = abs(math.sin(self.frame*0.1)) * 2
        scale = 0.8 + pulse * 0.3
        
        for y in range(self.h):
            for x in range(self.w):
                nx = (x - cx) / (self.w/4)
                ny = (y - cy) / (self.h/4)
                # Формула сердца: (x^2 + (9/4)y^2 + |x|*y - 1) <= 0
                heart_eq = (nx*nx + (9/4)*ny*ny + abs(nx)*ny - 1) * scale
                if heart_eq <= 0:
                    brightness = 0.5 + pulse * 0.5 - abs(heart_eq)
                    brightness = max(0.2, min(0.9, brightness))
                    buf[y][x] = self.get_char(brightness)
                elif abs(heart_eq) < 0.3:
                    buf[y][x] = '.'
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def snake(self):
        """Змейка, ползущая по экрану"""
        if not hasattr(self, 'snake'):
            self.snake = []
            self.snake_dir = 0
            for i in range(8):
                self.snake.append([self.w//4 - i, self.h//2])
        buf = [[' ']*self.w for _ in range(self.h)]
        
        # Движение змейки
        if self.frame % 5 == 0:
            head = self.snake[0]
            dirs = [(1,0), (0,1), (-1,0), (0,-1)]
            # Простое движение вправо с периодической сменой направления
            if self.frame % 60 < 30:
                dx, dy = 1, 0
            else:
                dx, dy = 0, 1
            
            new_head = [head[0] + dx, head[1] + dy]
            # Проверка границ
            if new_head[0] < 0 or new_head[0] >= self.w or new_head[1] < 0 or new_head[1] >= self.h:
                new_head = [head[0] - dx, head[1] - dy]
            
            self.snake.insert(0, new_head)
            self.snake.pop()
        
        # Рисуем змейку
        for i, seg in enumerate(self.snake):
            x, y = seg[0], seg[1]
            if 0 <= x < self.w and 0 <= y < self.h:
                if i == 0:
                    buf[y][x] = '@'  # Голова
                else:
                    buf[y][x] = 'o'  # Тело
        
        # Рисуем еду
        if not hasattr(self, 'food'):
            self.food = [random.randint(0, self.w-1), random.randint(0, self.h-1)]
        
        fx, fy = self.food
        if 0 <= fx < self.w and 0 <= fy < self.h:
            buf[fy][fx] = '*'
        
        # Проверка съедания
        if self.snake[0][0] == fx and self.snake[0][1] == fy:
            self.food = [random.randint(0, self.w-1), random.randint(0, self.h-1)]
            self.snake.append(self.snake[-1])  # Растем
        
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)
    
    def rainbow(self):
        """Радужные волны"""
        buf = [[' ']*self.w for _ in range(self.h)]
        colors = ['@', '#', '&', '%', '+', '=', '-', ':', '.']
        
        for y in range(self.h):
            for x in range(self.w):
                # Создаем радужный паттерн
                r_val = (math.sin(x*0.1 + self.frame*0.1) + 1) / 2
                g_val = (math.sin(y*0.1 + self.frame*0.12) + 1) / 2
                b_val = (math.sin((x+y)*0.1 + self.frame*0.08) + 1) / 2
                
                # Комбинируем каналы
                brightness = (r_val + g_val + b_val) / 3
                color_idx = int((r_val - g_val) * len(colors))
                color_idx = abs(color_idx) % len(colors)
                
                buf[y][x] = colors[color_idx] if brightness > 0.3 else ' '
        
        self.frame += 1
        return '\n'.join(''.join(r) for r in buf)

def main():
    try:
        import shutil
        w, h = shutil.get_terminal_size()
        w, h = min(w-5, 70), min(h-5, 25)
    except:
        w, h = 60, 25
    
    g = Generator(w, h)
    anims = [g.waves, g.cube, g.particles, g.sin_wave, g.spiral, 
             g.explosion, g.matrix, g.fire, g.bounce, g.stars,
             g.heart, g.snake, g.rainbow]
    
    while True:
        print('\033[2J\033[H')
        print("="*w)
        print("КОНСОЛЬНЫЙ ВИДЕОГЕНЕРАТОР".center(w))
        print("="*w)
        print("\nВыберите анимацию:")
        for i, a in enumerate(AnimationType, 1):
            print(f"{i:2}. {a.value}")
        print(f"{len(anims)+1:2}. Выход")
        
        try:
            c = int(input("\n👉 Ваш выбор: "))
            if c == len(anims)+1:
                print("\n👋 До свидания!")
                break
            if 1 <= c <= len(anims):
                print(f"\nДлительность в секундах (0=бесконечно): ", end='')
                dur = input().strip()
                dur = None if dur in ['0',''] else float(dur)
                
                print(f"\n▶️ {AnimationType(list(AnimationType)[c-1]).value}")
                print("⏹️ Ctrl+C для остановки")
                time.sleep(1.5)
                
                start = time.time()
                fr = 0
                try:
                    while True:
                        t = time.time()
                        print('\033[2J\033[H', end='')
                        print(anims[c-1]())
                        elapsed = time.time()-t
                        time.sleep(max(0, 1/15 - elapsed))
                        fr += 1
                        if dur and time.time()-start > dur: break
                except KeyboardInterrupt:
                    pass
                print(f"\n✅ Кадров: {fr}")
                input("\nНажмите Enter...")
        except:
            pass

if __name__ == "__main__":
    main()