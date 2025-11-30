#include <stdio.h>
#include <string.h>
#include <ncurses.h>

static char ** history[100][100];
static int history_ptr = 0;
static int history_size = 100;

typedef enum { Ok = 0, Invalid = 1, Unsafe = 2 } InputErrorCode;

typedef struct {
    char* input;
    InputErrorCode error;
} InputResult;

typedef struct {
    char* content;
    InputErrorCode error;
} RequestResult;

void print_help() {
    printw("Textbrowser provides a most simple way to peek at websites\n\
        :help - print this help\n\
        :exit - to exit browser\n\
        :history - to exit browser");
    refresh();
}

void print_history() {
    for (int i = 0; i < history_ptr; i++) {
        printw("%d: %s\n", i + 1, history[i]);
    }
    refresh();
}

RequestResult request(const char * url) {
    return (RequestResult){ .content = NULL, .error = 0 };
}

InputResult validate_input(const char * input) {
    return (InputResult){ .input = input, 0 };
}

InputResult sanitize_input(const char * input) {
    return (InputResult){ .input = input, 0 };
}

int main() {
    WINDOW* wnd = initscr();            // Start ncurses mode
    
    char buf[80];

    do {
        refresh();
        printw("\n> Where you want to go: ");
        refresh();
        getstr(buf);

        if (strcmp(buf, ":help") == 0) {
            print_help();
            continue;
        }

        if (strcmp(buf, ":history") == 0) {
            print_history();
            continue;
        }
        
        InputResult sanitized = sanitize_input(&buf);
        if (sanitized.error) {
            printw("Dangerous input provided\n");
            continue;
        }

        InputResult validated = validate_input(sanitized.input);
        if (validated.error) {
            printw("Invalid input provided\n");
            continue;
        }

        printw("you entered: %s\n", buf);
        if (history_ptr < history_size) {
            strcpy(history[history_ptr++], buf);
        }

    } while (true);
    
    endwin();
    return 0;
}