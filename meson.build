project('textbrowser', 'c')

ncurses = dependency('ncurses', version: '>=5.7')
curl = dependency('libcurl', version: '>=8.5')

executable('textbrowser', 'src/main.c', dependencies: [ncurses, curl])