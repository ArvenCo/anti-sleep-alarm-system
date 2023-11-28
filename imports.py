from flask import Flask, Blueprint, session
from flask_socketio import SocketIO, emit, join_room
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import cv2 as cv
import base64, math
import mediapipe as mp
from multiprocessing import Process, Manager, Queue
from datetime import datetime