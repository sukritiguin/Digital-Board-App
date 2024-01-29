import tkinter as tk
from tkinter import ttk, colorchooser, simpledialog, messagebox, Menu
from PIL import Image, ImageTk, ImageGrab
import math
from tkinter.simpledialog import askstring
import tkinter.filedialog as filedialog
from ttkbootstrap import Style
from tkinter import PhotoImage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import img2pdf
import io
import pyperclip
import base64
import json