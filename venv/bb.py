from flask import Flask, render_template, request
import game_main

def restart():
    p = game_main.Cool()
    p.main


if __name__ == '__main__':
    restart()