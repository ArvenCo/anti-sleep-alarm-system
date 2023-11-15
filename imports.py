from flask import Flask, Blueprint, session
from flask_socketio import SocketIO, emit
import numpy as np
import cv2 as cv
import base64, math
import mediapipe as mp
