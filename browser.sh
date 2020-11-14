#!/bin/bash

install()
{
        python3 -m venv venv
        source ./venv/bin/activate
        pip3 install -r ./requirements.txt
}

test()
{
        pytest .
}

run()
{
	    python3 -m textbrowser
}

help()
{
        echo "                                           "
        echo " Example of usage:"
        echo "    ./browser.sh install"
        echo " ------------------------------------------"
        echo "                                           "
        echo " Available commands:"
        echo " install - instals virtual env + deps"
        echo " test    - runs tests"
        echo " run     - runs textbrowser"
        echo " help    - prints help"
        echo "                                           "
}

COMMANDS_PATT="install|test|run|help"
if [[ "$1" =~ ^($COMMANDS_PATT)$ ]]
then
        $1
else
        help
fi