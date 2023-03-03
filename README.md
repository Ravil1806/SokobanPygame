# SokobanPygame
Sokoban(сокобан — кладовщик) — компьютерная игра-головоломка, где игроку необходимо расставить ящики(в проекте бутылки) по обозначенным местам лабиринта. Игра Sokoban была создана в 1981 году Хироюки Имабаяси.

# Описание проекта
Проект включает в себя 5 уровней, сложность которых увеличивается по мере прохождения. Игроку необходимо передвинуть все "пятилитровки" на нужные места. Все уровни и дизайн игры были разработаны лично мной.

# Особенности проекта
Все уровни записаны в текстовых файлах, которые загружаются, и по ним генерируется уровень. Обозначения символов в текстовых файлах:

| Обозначение| Символ|
| -----------|:-----:|
| Стена      | #     |
| Игрок      | @     |
| Бутылка    | $     |
| Цель	     | &     |
| Пол        | .     |

А вот пример уровня:
```
####################
#&.##..#....#......#
#..#...........#.$.#
#..#.....#..##.##..#
#.....##....#......#
#....##........#.$.#
##.####.###.#..##..#
##&@#&.............#
##.####.###.#......#
#....##........#.$.#
#.....##.....#.##..#
#..#.....#..##.....#
#..#........#..#.$.#
#&.##..#.......##..#
####################
```

Используется база данных для фиксирования пройденного уровня, например, если пройти первый уровень и закрыть игру, то при новом открытии можно будет начать сразу со второго уровня или заново, начиная с первого. В главное меню можно выйти в любое время, главное случайно не нажать во время прохождения уровня, иначе придётся проходить уровень заново. Кстати для этого есть кнопка "Рестарт" в случае ошибки.
Во время игры идёт музыка, а также есть звуки передвижения персонажа и толкания бутылки.

# Дальнейшее развитие
 * Визуальная составляющая
 * Звуковая составляющая
 * Больше уровней
 * Список лучших игроков
 * ОТКАТ ХОДА
 * и т.д.

# Скриношоты игры
Главное меню
!["Main menu"](data/screenshoots_for_readme/main_menu.png?raw=true "Main menu")
Первый уровень
!["First level"](data/screenshoots_for_readme/first_lvl.png?raw=true "First level")
