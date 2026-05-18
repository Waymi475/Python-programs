import os, time, random, sys
import select

class CubeGame:
    def __init__(self):
        self.w = 50
        self.h = 10
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_started = False
        
        # Прыжок кубика (увеличенная высота)
        self.jumping = False
        self.jump_height = 0
        self.jump_max = 6  # Было 4, теперь 6 (выше прыжок)
        
        # Препятствия
        self.obstacle_x = self.w
        self.obstacle_type = 'cactus'
        
        # Скорость
        self.speed = 2
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def jump(self):
        """Мгновенный прыжок"""
        if not self.jumping and self.game_started and not self.game_over:
            self.jumping = True
            self.jump_height = 0
    
    def update_jump(self):
        """Обновление прыжка"""
        if self.jumping:
            if self.jump_height < self.jump_max:
                self.jump_height += 1
            else:
                self.jumping = False
        else:
            if self.jump_height > 0:
                self.jump_height -= 1
    
    def update_obstacles(self):
        """Обновление препятствий"""
        if not self.game_started or self.game_over:
            return
        
        # Движение препятствия
        self.obstacle_x -= self.speed
        
        # Создание нового препятствия
        if self.obstacle_x < -5:
            self.obstacle_x = self.w
            self.score += 10
            
            # Выбираем тип препятствия
            if self.score > 150:
                self.obstacle_type = random.choice(['cactus', 'bird'])
            else:
                self.obstacle_type = 'cactus'
            
            # Увеличиваем скорость
            self.speed = 2 + self.score // 300
            if self.speed > 6:
                self.speed = 6
    
    def check_collision(self):
        """Проверка столкновения (исправлено)"""
        if not self.game_started or self.game_over:
            return
        
        # Позиция кубика (x=5 и x=6)
        # Проверяем пересечение с препятствием
        cube_left = 5
        cube_right = 7  # Кубик занимает x=5 и x=6
        
        obs_left = self.obstacle_x
        obs_right = self.obstacle_x + 1  # Препятствие шириной 1 символ
        
        # Проверка наложения по горизонтали
        if cube_right >= obs_left and cube_left <= obs_right:
            # Если это птица и кубик достаточно высоко - не умираем
            if self.obstacle_type == 'bird' and self.jump_height >= 4:
                return  # Пролетел над птицей
            
            # Если кубик достаточно высоко - перепрыгивает кактус
            if self.jump_height >= 5:
                return  # Перепрыгнул
            
            # Столкновение
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
    
    def draw(self):
        """Отрисовка игры"""
        self.clear()
        
        # Верхняя граница
        print('┌' + '─' * self.w + '┐')
        
        # Игровое поле
        for y in range(self.h):
            line = '│'
            for x in range(self.w):
                # Земля
                if y == self.h - 2:
                    line += '█'
                # Кубик (на земле или в воздухе)
                elif y == self.h - 3 - self.jump_height and x == 5:
                    line += '■'
                elif y == self.h - 3 - self.jump_height and x == 6:
                    line += '■'
                # Препятствие
                elif x == self.obstacle_x:
                    if y == self.h - 3:
                        if self.obstacle_type == 'cactus':
                            line += '▲'
                        else:
                            line += '°'
                    elif y == self.h - 4 and self.obstacle_type == 'bird':
                        line += '─'
                    else:
                        line += ' '
                else:
                    line += ' '
            line += '│'
            print(line)
        
        # Нижняя граница
        print('└' + '─' * self.w + '┘')
        
        # Информация
        print(f"  СЧЕТ: {self.score}  |  РЕКОРД: {self.high_score}  |  СКОРОСТЬ: {self.speed}")
        
        # Подсказка по прыжку
        jump_indicator = "ВЫСОКИЙ ПРЫЖОК" if self.jump_max == 6 else "НОРМАЛЬНЫЙ"
        print(f"  {jump_indicator}  |  ПРОБЕЛ - ПРЫЖОК")
        
        # Меню
        if not self.game_started:
            print("\n" + "═" * self.w)
            print("■ PYTHON DASH ■".center(self.w))
            print("".center(self.w))
            print("  НАЖМИТЕ 'S' ДЛЯ СТАРТА  ".center(self.w))
            print("  ПРОБЕЛ - ПРЫЖОК  ".center(self.w))
            print("═" * self.w)
        elif self.game_over:
            print("\n" + "═" * self.w)
            print("💀 GAME OVER 💀".center(self.w))
            print(f"  СЧЕТ: {self.score}  ".center(self.w))
            print("".center(self.w))
            print("  'R' - НОВАЯ ИГРА  ".center(self.w))
            print("  'Q' - ВЫХОД  ".center(self.w))
            print("═" * self.w)
    
    def run(self):
        """Главный игровой цикл"""
        print("ЗАГРУЗКА...")
        time.sleep(1)
        
        # Скрываем курсор
        print('\033[?25l', end='')
        
        # Настройка неблокирующего ввода
        if os.name != 'nt':
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty_settings = termios.tcgetattr(fd)
            tty_settings[3] = tty_settings[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, tty_settings)
        
        try:
            while True:
                start_time = time.time()
                
                # Проверка ввода
                if select.select([sys.stdin], [], [], 0)[0]:
                    ch = sys.stdin.read(1)
                    
                    if ch == 's' and not self.game_started:
                        self.game_started = True
                        self.game_over = False
                        self.score = 0
                        self.obstacle_x = self.w
                        self.speed = 2
                        self.jumping = False
                        self.jump_height = 0
                    elif ch == ' ' and self.game_started and not self.game_over:
                        self.jump()
                    elif ch == 'r' and self.game_over:
                        self.game_started = True
                        self.game_over = False
                        self.score = 0
                        self.obstacle_x = self.w
                        self.speed = 2
                        self.jumping = False
                        self.jump_height = 0
                    elif ch == 'q':
                        break
                
                # Обновление игры
                if self.game_started and not self.game_over:
                    self.update_jump()
                    self.update_obstacles()
                    self.check_collision()
                
                # Отрисовка
                self.draw()
                
                # Задержка для FPS
                elapsed = time.time() - start_time
                frame_delay = 1.0 / 30
                if elapsed < frame_delay:
                    time.sleep(frame_delay - elapsed)
                
        except KeyboardInterrupt:
            pass
        finally:
            if os.name != 'nt':
                termios.tcsetattr(fd, termios.TCSANOW, old_settings)
            print('\033[?25h', end='')
            print("\nСпасибо за игру!")

# ОЧЕНЬ МЕДЛЕННАЯ ВЕРСИЯ С ВЫСОКИМ ПРЫЖКОМ
class SlowHighJump:
    def __init__(self):
        self.w = 50
        self.h = 10
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_started = False
        
        self.jumping = False
        self.jump_height = 0
        self.jump_max = 7  # Очень высокий прыжок
        
        self.obstacle_x = self.w
        self.speed = 1  # Очень медленно
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw(self):
        self.clear()
        
        print("═" * self.w)
        print("■ SLOW MODE ■".center(self.w))
        print("═" * self.w)
        
        for y in range(self.h):
            line = ""
            for x in range(self.w):
                if y == self.h - 1:
                    line += "█"
                elif y == self.h - 2 - self.jump_height and x == 5:
                    line += "■"
                elif y == self.h - 2 - self.jump_height and x == 6:
                    line += "■"
                elif x == self.obstacle_x and y == self.h - 2:
                    line += "▲"
                else:
                    line += " "
            print(line)
        
        print("═" * self.w)
        print(f"СЧЕТ: {self.score}     РЕКОРД: {self.high_score}")
        print(f"ВЫСОТА ПРЫЖКА: {self.jump_max}")
        
        if not self.game_started:
            print("\nS - СТАРТ | ПРОБЕЛ - ПРЫЖОК")
        elif self.game_over:
            print(f"\nGAME OVER! СЧЕТ: {self.score}")
            print("R - НОВАЯ ИГРА | Q - ВЫХОД")
    
    def run(self):
        if os.name != 'nt':
            import termios
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, new)
        
        try:
            while True:
                if select.select([sys.stdin], [], [], 0)[0]:
                    ch = sys.stdin.read(1)
                    
                    if ch == 's' and not self.game_started:
                        self.game_started = True
                        self.score = 0
                        self.game_over = False
                        self.obstacle_x = self.w
                        self.speed = 1
                    elif ch == ' ' and self.game_started and not self.game_over and not self.jumping:
                        self.jumping = True
                        self.jump_height = 0
                    elif ch == 'r' and self.game_over:
                        self.game_started = True
                        self.game_over = False
                        self.score = 0
                        self.obstacle_x = self.w
                        self.speed = 1
                        self.jumping = False
                        self.jump_height = 0
                    elif ch == 'q':
                        break
                
                if self.game_started and not self.game_over:
                    # Прыжок
                    if self.jumping:
                        if self.jump_height < self.jump_max:
                            self.jump_height += 1
                        else:
                            self.jumping = False
                    else:
                        if self.jump_height > 0:
                            self.jump_height -= 1
                    
                    # Препятствие
                    self.obstacle_x -= self.speed
                    if self.obstacle_x < 0:
                        self.obstacle_x = self.w
                        self.score += 10
                        if self.score % 300 == 0 and self.score > 0:
                            self.speed += 0.3
                            if self.speed > 3.5:
                                self.speed = 3.5
                    
                    # Столкновение (исправлено)
                    if self.obstacle_x <= 8 and self.obstacle_x >= 4:
                        if self.jump_height < 5:  # Нужно прыгнуть выше 5
                            self.game_over = True
                            if self.score > self.high_score:
                                self.high_score = self.score
                
                self.draw()
                time.sleep(0.07)
                
        except:
            pass
        finally:
            if os.name != 'nt':
                termios.tcsetattr(fd, termios.TCSANOW, old)
            print("\nИгра завершена!")

if __name__ == "__main__":
    print("ВЫБЕРИТЕ ВЕРСИЮ:")
    print("1. Высокий прыжок (исправлено столкновение)")
    print("2. Очень высокий + медленный")
    
    choice = input("\n👉 ВАШ ВЫБОР: ")
    
    if choice == '1':
        game = CubeGame()
        game.run()
    else:
        game = SlowHighJump()
        game.run()