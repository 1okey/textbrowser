#include <stdio.h>
#include <ncurses.h>

int main() {
    WINDOW* wnd = initscr();            // Start ncurses mode
    printw("> Where you want to go:\n");
    refresh();
    char buf[80];
    getstr(buf);
    printw("you entered: %s\n Press ESC to escape", buf);
    refresh();
    while (getch() != 27) {
        printw("Press ESC to escape", buf);
        refresh();
    }
    endwin();
    return 0;
}