#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ncurses.h>
#include <curl/curl.h>

// request history
static char ** history[100][100];
static int history_ptr = 0;
static int history_size = 100;

// response cache
// actual array of responses
// keys of pages that point to responses

typedef enum { InputOk = 0, InputInvalid = 1, InputUnsafe = 2 } InputError;

typedef struct {
    char* input;
    InputError error;
} InputResult;

typedef struct {
    char* content;
    uint32_t size;
    InputError error;
} RequestResult;

typedef enum { Noop = 0, Exit = 1, Help = 2, History = 3 } Command;

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

Command is_command(const char * input) {
    // trie is much more efficient here but for simplicity we use strcmp
    if (strcmp(input, ":help") == 0) {
        return Help;
    } else if (strcmp(input, ":exit") == 0) {
        return Exit;
    } else if (strcmp(input, ":history") == 0) {
        return History;
    }

    // clear or clean

    return Noop;
}

void handle_command(Command cmd) {
    switch (cmd) {
        case Help:
            print_help();
            break;
        case Exit:
            printw("Exiting the application\n");
            exit(0);
            break;
        case History:
            print_history();
            break;
        default:
            break;
    }
}


RequestResult request(const char * url) {
    CURL* conn = curl_easy_init();
    if (conn == NULL) {
        return (RequestResult){ .content = NULL, .size = 0, .error = 1 };
    }

    curl_easy_setopt(conn, CURLOPT_URL, url);
    CURLcode res = curl_easy_perform(conn);

    if (res != CURLE_OK) {
        curl_easy_cleanup(conn);
        return (RequestResult){ .content = NULL, .size = 0, .error = 1 };
    }

    char * buf = (char* ) malloc(4086 * sizeof(char));
    uint32_t actual_size = 0;
    curl_easy_recv(conn, buf, sizeof(buf), &actual_size);

    curl_socket_t sockfd;

    /* Extract the socket from the curl handle - we need it for waiting. */
    res = curl_easy_getinfo(conn, CURLINFO_ACTIVESOCKET, &sockfd);
    if (res != CURLE_OK) {
        curl_easy_cleanup(conn);
        return (RequestResult){ .content = NULL, .size = 0, .error = 1 };
    }
      /* read data */
    res = curl_easy_recv(conn, buf, sizeof(buf), &actual_size);

    curl_easy_cleanup(conn);

    return (RequestResult){ .content = buf, .size = actual_size, .error = 0 };
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
        printw("\n> Where you want to go: ");
        refresh();
        getstr(buf);

        Command cmd = is_command(buf);
        if (cmd != Noop) {
            handle_command(cmd);
            continue;
        }
        
        InputResult sanitized = sanitize_input(&buf);
        if (sanitized.error != InputOk) {
            printw("Dangerous input provided\n");
            continue;
        }

        InputResult validated = validate_input(sanitized.input);
        if (validated.error != InputOk) {
            printw("Invalid input provided\n");
            continue;
        }

        // cache lookup first and then attempt to request
        RequestResult response = request(validated.input);
        if (response.error != 0) {
            printw("Failed to fetch the page\n");
            continue;
        }

        printw("%s\n", buf);

        // check if history is full
        // have a deque structure for history
        if (history_ptr < history_size) {
            strcpy(history[history_ptr++], buf);
        }

    } while (true);
    
    endwin();
    return 0;
}