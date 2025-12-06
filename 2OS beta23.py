import pygame
import sys
import os
import datetime
import random
import math
import webbrowser
import requests
import json
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Screen setup
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("OS Simulator - Enhanced")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 120, 215)
LIGHT_BLUE = (100, 180, 255)
GRAY = (240, 240, 240)
DARK_GRAY = (50, 50, 50)
MAC_BLUE = (0, 122, 255)
MAC_GRAY = (240, 240, 240)
MAC_DARK_GRAY = (30, 30, 30)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Fonts
try:
    title_font = pygame.font.SysFont("segoeui", 48, bold=True)
    large_font = pygame.font.SysFont("segoeui", 36)
    medium_font = pygame.font.SysFont("segoeui", 24)
    small_font = pygame.font.SysFont("segoeui", 18)
    mac_title_font = pygame.font.SysFont("sfnsdisplay", 48, bold=True)
    mac_large_font = pygame.font.SysFont("sfnsdisplay", 36)
    mac_medium_font = pygame.font.SysFont("sfnsdisplay", 24)
    mac_small_font = pygame.font.SysFont("sfnsdisplay", 18)
    persian_font = pygame.font.SysFont("tahoma", 18)
except:
    # Fallback fonts if specified fonts are not available
    title_font = pygame.font.SysFont(None, 48, bold=True)
    large_font = pygame.font.SysFont(None, 36)
    medium_font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 18)
    mac_title_font = pygame.font.SysFont(None, 48, bold=True)
    mac_large_font = pygame.font.SysFont(None, 36)
    mac_medium_font = pygame.font.SysFont(None, 24)
    mac_small_font = pygame.font.SysFont(None, 18)
    persian_font = pygame.font.SysFont(None, 18)

# OS States
BOOT_SCREEN = 0
WINDOWS_11 = 1
MACOS = 2

current_os = BOOT_SCREEN
current_app = None
windows_start_open = False
mac_dock_open = False
windows_apps = []
mac_apps = []
active_windows = []
context_menu = None
background_image = None
background_color = BLUE
current_language = "english"  # "english" or "farsi"

# Clock
clock = pygame.time.Clock()

# Load images
def load_image(name, scale=1):
    try:
        # Check if file exists
        if not os.path.exists(f"assets/{name}"):
            raise FileNotFoundError(f"Image assets/{name} not found")
            
        image = pygame.image.load(f"assets/{name}")
        if scale != 1:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except Exception as e:
        print(f"Error loading image {name}: {e}")
        # Create a placeholder if image not found
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        pygame.draw.rect(surf, color, (0, 0, 50, 50), border_radius=8)
        return surf

# Create assets directory if it doesn't exist
if not os.path.exists("assets"):
    os.makedirs("assets")

# Icons
icons = {
    "windows": load_image("windows_icon.png"),
    "mac": load_image("mac_icon.png"),
    "browser": load_image("browser_icon.png"),
    "settings": load_image("settings_icon.png"),
    "terminal": load_image("terminal_icon.png"),
    "music": load_image("music_icon.png"),
    "calculator": load_image("calculator_icon.png"),
    "notes": load_image("notes_icon.png"),
    "calendar": load_image("calendar_icon.png"),
    "store": load_image("store_icon.png"),
    "game": load_image("game_icon.png"),
    "camera": load_image("camera_icon.png"),
    "gallery": load_image("gallery_icon.png"),
    "facebook": load_image("facebook_icon.png"),
    "instagram": load_image("instagram_icon.png"),
    "twitter": load_image("twitter_icon.png"),
    "telegram": load_image("telegram_icon.png"),
    "whatsapp": load_image("whatsapp_icon.png"),
    "power": load_image("power_icon.png"),
    "weather": load_image("weather_icon.png"),
    "mail": load_image("mail_icon.png"),
    "maps": load_image("maps_icon.png"),
    "files": load_image("files_icon.png"),
    "video": load_image("video_icon.png"),
}

# Create enhanced icons if images not available
for key in icons:
    if icons[key].get_size() == (50, 50):
        # This is a placeholder, create a proper icon
        icons[key] = pygame.Surface((64, 64), pygame.SRCALPHA)
        if key == "windows":
            pygame.draw.rect(icons[key], BLUE, (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (12, 12, 40, 40), border_radius=8)
        elif key == "mac":
            pygame.draw.rect(icons[key], MAC_BLUE, (0, 0, 64, 64), border_radius=32)
            pygame.draw.rect(icons[key], WHITE, (16, 16, 32, 32), border_radius=16)
        elif key == "browser":
            pygame.draw.rect(icons[key], (0, 150, 255), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (8, 8, 48, 30), border_radius=6)
            pygame.draw.rect(icons[key], (0, 150, 255), (12, 12, 40, 22), border_radius=4)
        elif key == "settings":
            pygame.draw.circle(icons[key], (100, 100, 100), (32, 32), 32)
            pygame.draw.circle(icons[key], WHITE, (32, 32), 24)
            pygame.draw.circle(icons[key], (100, 100, 100), (32, 32), 16)
            pygame.draw.circle(icons[key], WHITE, (32, 32), 8)
        elif key == "terminal":
            pygame.draw.rect(icons[key], (0, 200, 0), (0, 0, 64, 64), border_radius=12)
            for i in range(5):
                pygame.draw.rect(icons[key], WHITE, (12, 16 + i*8, 40, 4), border_radius=2)
        elif key == "music":
            pygame.draw.rect(icons[key], (200, 0, 100), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (12, 12, 40, 40), border_radius=8)
            for i in range(3):
                pygame.draw.rect(icons[key], (200, 0, 100), (16 + i*10, 20, 6, 24), border_radius=2)
        elif key == "calculator":
            pygame.draw.rect(icons[key], (255, 165, 0), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (8, 8, 48, 48), border_radius=8)
            for i in range(4):
                for j in range(4):
                    pygame.draw.rect(icons[key], (255, 165, 0), (16 + j*10, 16 + i*10, 6, 6), border_radius=2)
        elif key == "notes":
            pygame.draw.rect(icons[key], (255, 255, 0), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (8, 8, 48, 48), border_radius=8)
            for i in range(4):
                pygame.draw.rect(icons[key], (255, 255, 0), (16, 20 + i*8, 32, 4), border_radius=2)
        elif key == "calendar":
            pygame.draw.rect(icons[key], (255, 0, 0), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (8, 8, 48, 48), border_radius=8)
            pygame.draw.rect(icons[key], (255, 0, 0), (8, 8, 48, 12), border_radius=8)
            for i in range(3):
                for j in range(4):
                    pygame.draw.rect(icons[key], (255, 0, 0), (16 + j*10, 28 + i*10, 6, 6), border_radius=2)
        elif key == "store":
            pygame.draw.rect(icons[key], (0, 200, 200), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (12, 12, 40, 40), border_radius=8)
            pygame.draw.rect(icons[key], (0, 200, 200), (20, 20, 24, 24), border_radius=6)
        elif key == "game":
            pygame.draw.rect(icons[key], (150, 0, 200), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (12, 12, 40, 40), border_radius=8)
            pygame.draw.circle(icons[key], (150, 0, 200), (32, 32), 12)
        elif key == "camera":
            pygame.draw.rect(icons[key], (0, 150, 150), (0, 0, 64, 64), border_radius=12)
            pygame.draw.circle(icons[key], WHITE, (32, 32), 20)
            pygame.draw.circle(icons[key], (0, 150, 150), (32, 32), 12)
            pygame.draw.circle(icons[key], WHITE, (32, 32), 6)
        elif key == "gallery":
            pygame.draw.rect(icons[key], (200, 100, 0), (0, 0, 64, 64), border_radius=12)
            for i in range(2):
                for j in range(2):
                    pygame.draw.rect(icons[key], WHITE, (12 + j*20, 12 + i*20, 16, 16), border_radius=4)
        elif key == "facebook":
            pygame.draw.rect(icons[key], (59, 89, 152), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (20, 16, 24, 32), border_radius=4)
            pygame.draw.circle(icons[key], WHITE, (32, 20), 6)
        elif key == "instagram":
            pygame.draw.rect(icons[key], (225, 48, 108), (0, 0, 64, 64), border_radius=12)
            pygame.draw.circle(icons[key], WHITE, (32, 32), 16)
            pygame.draw.circle(icons[key], (225, 48, 108), (32, 32), 12)
            pygame.draw.circle(icons[key], WHITE, (40, 24), 4)
        elif key == "twitter":
            pygame.draw.rect(icons[key], (29, 161, 242), (0, 0, 64, 64), border_radius=12)
            # Draw bird shape
            points = [(20, 32), (28, 24), (32, 28), (36, 24), (44, 32), (36, 36), (32, 32), (28, 36)]
            pygame.draw.polygon(icons[key], WHITE, points)
        elif key == "telegram":
            pygame.draw.rect(icons[key], (0, 136, 204), (0, 0, 64, 64), border_radius=12)
            # Draw paper plane
            pygame.draw.polygon(icons[key], WHITE, [(16, 32), (48, 16), (32, 48), (24, 40)])
        elif key == "whatsapp":
            pygame.draw.rect(icons[key], (37, 211, 102), (0, 0, 64, 64), border_radius=12)
            pygame.draw.circle(icons[key], WHITE, (32, 32), 20)
            pygame.draw.circle(icons[key], (37, 211, 102), (32, 32), 16)
            # Draw phone and message
            pygame.draw.rect(icons[key], WHITE, (24, 28, 16, 8), border_radius=2)
        elif key == "power":
            pygame.draw.rect(icons[key], (255, 50, 50), (0, 0, 64, 64), border_radius=12)
            pygame.draw.circle(icons[key], WHITE, (32, 32), 20)
            pygame.draw.rect(icons[key], WHITE, (30, 16, 4, 16))
        elif key == "weather":
            pygame.draw.rect(icons[key], (0, 180, 255), (0, 0, 64, 64), border_radius=12)
            pygame.draw.circle(icons[key], WHITE, (32, 32), 20)
            for i in range(8):
                angle = math.radians(i * 45)
                x = 32 + 28 * math.cos(angle)
                y = 32 + 28 * math.sin(angle)
                pygame.draw.circle(icons[key], WHITE, (int(x), int(y)), 6)
        elif key == "mail":
            pygame.draw.rect(icons[key], (200, 0, 0), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (12, 20, 40, 24), border_radius=4)
            pygame.draw.polygon(icons[key], WHITE, [(12, 20), (32, 32), (52, 20)])
        elif key == "maps":
            pygame.draw.rect(icons[key], (0, 150, 0), (0, 0, 64, 64), border_radius=12)
            pygame.draw.rect(icons[key], WHITE, (12, 12, 40, 40), border_radius=8)
            pygame.draw.circle(icons[key], (0, 150, 0), (32, 32), 8)
            for i in range(4):
                angle = math.radians(i * 90)
                x = 32 + 20 * math.cos(angle)
                y = 32 + 20 * math.sin(angle)
                pygame.draw.circle(icons[key], (0, 150, 0), (int(x), int(y)), 4)
        elif key == "files":
            pygame.draw.rect(icons[key], (100, 100, 200), (0, 0, 64, 64), border_radius=12)
            for i in range(3):
                pygame.draw.rect(icons[key], WHITE, (12, 12 + i*16, 40, 12), border_radius=4)
        elif key == "video":
            pygame.draw.rect(icons[key], (180, 0, 100), (0, 0, 64, 64), border_radius=12)
            pygame.draw.polygon(icons[key], WHITE, [(24, 20), (24, 44), (44, 32)])

# Background images
backgrounds = {
    "windows": load_image("windows_bg.jpg", max(WIDTH/1920, HEIGHT/1080)),
    "mac": load_image("mac_bg.jpg", max(WIDTH/1920, HEIGHT/1080)),
    "boot": load_image("boot_bg.jpg", max(WIDTH/1920, HEIGHT/1080)),
}

# Create window class
class Window:
    def __init__(self, title, x, y, width, height, content_func, closable=True, minimizable=True, maximizable=True):
        self.title = title
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content_func = content_func
        self.closable = closable
        self.minimizable = minimizable
        self.maximizable = maximizable
        self.minimized = False
        self.maximized = False
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.resizing = False
        self.active = True
        self.z_index = 0
        
    def draw(self, surface):
        if self.minimized:
            return
            
        if self.maximized:
            x, y, width, height = 0, 0, WIDTH, HEIGHT
        else:
            x, y, width, height = self.x, self.y, self.width, self.height
            
        # Draw window
        if current_os == WINDOWS_11:
            # Windows 11 style window with modern design
            pygame.draw.rect(surface, WHITE, (x, y, width, height), border_radius=10)
            pygame.draw.rect(surface, LIGHT_BLUE, (x, y, width, 40), border_radius=10)
            pygame.draw.rect(surface, BLUE, (x, y, width, 40), 2, border_radius=10)
            
            # Title with shadow effect
            title_text = medium_font.render(self.title, True, WHITE)
            surface.blit(title_text, (x + 15, y + 10))
            
            # Modern window buttons
            close_color = (232, 17, 35) if self.is_close_hovered() else (200, 200, 200)
            pygame.draw.rect(surface, close_color, (x + width - 40, y + 10, 20, 20), border_radius=10)
            close_x = medium_font.render("×", True, WHITE)
            surface.blit(close_x, (x + width - 35, y + 5))
            
            if self.maximizable:
                max_color = LIGHT_BLUE if self.is_maximize_hovered() else (200, 200, 200)
                pygame.draw.rect(surface, max_color, (x + width - 70, y + 10, 20, 20), border_radius=10)
                max_symbol = medium_font.render("□", True, WHITE)
                surface.blit(max_symbol, (x + width - 65, y + 5))
                
            if self.minimizable:
                min_color = LIGHT_BLUE if self.is_minimize_hovered() else (200, 200, 200)
                pygame.draw.rect(surface, min_color, (x + width - 100, y + 10, 20, 20), border_radius=10)
                min_symbol = medium_font.render("−", True, WHITE)
                surface.blit(min_symbol, (x + width - 95, y + 5))
        else:
            # macOS style window with modern design
            pygame.draw.rect(surface, MAC_GRAY, (x, y, width, height), border_radius=12)
            pygame.draw.rect(surface, MAC_DARK_GRAY, (x, y, width, height), 2, border_radius=12)
            
            # Title bar with gradient effect
            for i in range(40):
                color_val = 50 + i * 5
                pygame.draw.rect(surface, (color_val, color_val, color_val), (x, y + i, width, 1))
            
            # Title
            title_text = mac_medium_font.render(self.title, True, WHITE)
            surface.blit(title_text, (x + 50, y + 10))
            
            # Modern window buttons
            close_color = (255, 95, 87) if self.is_close_hovered() else (200, 200, 200)
            pygame.draw.circle(surface, close_color, (x + 20, y + 20), 8)
            
            if self.minimizable:
                min_color = (255, 189, 46) if self.is_minimize_hovered() else (200, 200, 200)
                pygame.draw.circle(surface, min_color, (x + 40, y + 20), 8)
                
            if self.maximizable:
                max_color = (40, 201, 64) if self.is_maximize_hovered() else (200, 200, 200)
                pygame.draw.circle(surface, max_color, (x + 60, y + 20), 8)
        
        # Draw content with subtle border
        content_rect = pygame.Rect(x + 5, y + 45, width - 10, height - 50)
        pygame.draw.rect(surface, WHITE, content_rect, border_radius=8)
        self.content_func(surface, content_rect)
        
    def is_close_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if current_os == WINDOWS_11:
            if self.maximized:
                return WIDTH - 50 <= mouse_x <= WIDTH - 30 and 10 <= mouse_y <= 30
            else:
                return self.x + self.width - 40 <= mouse_x <= self.x + self.width - 20 and self.y + 10 <= mouse_y <= self.y + 30
        else:
            if self.maximized:
                return 20 <= mouse_x <= 36 and 12 <= mouse_y <= 28
            else:
                return self.x + 12 <= mouse_x <= self.x + 28 and self.y + 12 <= mouse_y <= self.y + 28
                
    def is_minimize_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if current_os == WINDOWS_11:
            if self.maximized:
                return WIDTH - 100 <= mouse_x <= WIDTH - 80 and 10 <= mouse_y <= 30
            else:
                return self.x + self.width - 100 <= mouse_x <= self.x + self.width - 80 and self.y + 10 <= mouse_y <= self.y + 30
        else:
            if self.maximized:
                return 40 <= mouse_x <= 56 and 12 <= mouse_y <= 28
            else:
                return self.x + 32 <= mouse_x <= self.x + 48 and self.y + 12 <= mouse_y <= self.y + 28
                
    def is_maximize_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if current_os == WINDOWS_11:
            if self.maximized:
                return WIDTH - 70 <= mouse_x <= WIDTH - 50 and 10 <= mouse_y <= 30
            else:
                return self.x + self.width - 70 <= mouse_x <= self.x + self.width - 50 and self.y + 10 <= mouse_y <= self.y + 30
        else:
            if self.maximized:
                return 60 <= mouse_x <= 76 and 12 <= mouse_y <= 28
            else:
                return self.x + 52 <= mouse_x <= self.x + 68 and self.y + 12 <= mouse_y <= self.y + 28
    
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if self.is_close_hovered():
                return "close"
                
            if self.minimizable and self.is_minimize_hovered():
                self.minimized = True
                return "minimize"
                
            if self.maximizable and self.is_maximize_hovered():
                self.maximized = not self.maximized
                return "maximize"
                
            # Check if clicking on title bar for dragging
            title_rect = pygame.Rect(self.x, self.y, self.width, 40)
            if title_rect.collidepoint(mouse_x, mouse_y) and not self.maximized:
                self.dragging = True
                self.drag_offset_x = mouse_x - self.x
                self.drag_offset_y = mouse_y - self.y
                # Bring to front
                global active_windows
                if self in active_windows:
                    active_windows.remove(self)
                    active_windows.append(self)
                
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == MOUSEMOTION and self.dragging:
            self.x = pygame.mouse.get_pos()[0] - self.drag_offset_x
            self.y = pygame.mouse.get_pos()[1] - self.drag_offset_y
            
        return None

class ContextMenu:
    def __init__(self, x, y, options):
        self.x = x
        self.y = y
        self.options = options
        self.width = 200
        self.height = len(options) * 30
        self.visible = True
        
    def draw(self, surface):
        if not self.visible:
            return
            
        # Draw menu background with shadow
        pygame.draw.rect(surface, (240, 240, 240), (self.x, self.y, self.width, self.height), border_radius=8)
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height), 1, border_radius=8)
        
        # Draw options
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(self.x, self.y + i*30, self.width, 30)
            
            # Highlight if hovered
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if option_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(surface, LIGHT_BLUE, option_rect, border_radius=8)
            
            option_text = small_font.render(option, True, DARK_GRAY)
            surface.blit(option_text, (self.x + 10, self.y + i*30 + 5))
    
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check if click is inside menu
            menu_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if menu_rect.collidepoint(mouse_x, mouse_y):
                # Find which option was clicked
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.x, self.y + i*30, self.width, 30)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        return option
                return None
            else:
                # Click outside menu - close it
                self.visible = False
                return "close"
        return None

# Enhanced app content functions
def browser_content(surface, rect):
    # Modern browser design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Address bar with modern design
    pygame.draw.rect(surface, (245, 245, 245), (rect.x, rect.y, rect.width, 50), border_radius=8)
    pygame.draw.rect(surface, (220, 220, 220), (rect.x, rect.y, rect.width, 50), 1, border_radius=8)
    
    # Navigation buttons
    nav_buttons = ["←", "→", "⟳", "⌂"]
    for i, btn in enumerate(nav_buttons):
        btn_rect = pygame.Rect(rect.x + 10 + i*40, rect.y + 10, 30, 30)
        pygame.draw.rect(surface, LIGHT_BLUE, btn_rect, border_radius=6)
        btn_text = small_font.render(btn, True, WHITE)
        surface.blit(btn_text, (rect.x + 20 + i*40, rect.y + 15))
    
    # Address bar
    address_rect = pygame.Rect(rect.x + 180, rect.y + 10, rect.width - 260, 30)
    pygame.draw.rect(surface, WHITE, address_rect, border_radius=6)
    pygame.draw.rect(surface, (200, 200, 200), address_rect, 1, border_radius=6)
    
    address_text = small_font.render("https://www.example.com", True, DARK_GRAY)
    surface.blit(address_text, (rect.x + 190, rect.y + 15))
    
    # Content area with sample website
    content_rect = pygame.Rect(rect.x + 10, rect.y + 60, rect.width - 20, rect.height - 70)
    pygame.draw.rect(surface, (250, 250, 250), content_rect, border_radius=8)
    
    # Website header
    pygame.draw.rect(surface, BLUE, (rect.x + 10, rect.y + 60, rect.width - 20, 60), border_radius=8)
    header_text = medium_font.render("Example Website", True, WHITE)
    surface.blit(header_text, (rect.x + rect.width//2 - header_text.get_width()//2, rect.y + 80))
    
    # Sample content
    content_lines = [
        "Welcome to the Enhanced Browser!",
        "This is a modern web browsing experience.",
        "",
        "Features:",
        "• Fast browsing",
        "• Secure connections",
        "• Modern design",
        "",
        "Try navigating with the buttons above!"
    ]
    
    for i, line in enumerate(content_lines):
        line_text = small_font.render(line, True, DARK_GRAY)
        surface.blit(line_text, (rect.x + 30, rect.y + 140 + i*25))

def settings_content(surface, rect):
    # Modern settings design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Settings categories sidebar
    sidebar_rect = pygame.Rect(rect.x, rect.y, 200, rect.height)
    pygame.draw.rect(surface, (245, 245, 245), sidebar_rect, border_radius=8)
    pygame.draw.rect(surface, (220, 220, 220), sidebar_rect, 1, border_radius=8)
    
    # Settings title
    title_text = medium_font.render("Settings", True, DARK_GRAY)
    surface.blit(title_text, (rect.x + 220, rect.y + 20))
    
    # Settings categories
    categories = ["System", "Display", "Sound", "Network", "Apps", "Privacy", "Personalization"]
    for i, category in enumerate(categories):
        cat_rect = pygame.Rect(rect.x + 10, rect.y + 20 + i*40, 180, 35)
        
        # Highlight selected category
        if i == 0:  # System is selected by default
            pygame.draw.rect(surface, LIGHT_BLUE, cat_rect, border_radius=6)
        
        cat_text = small_font.render(category, True, DARK_GRAY)
        surface.blit(cat_text, (rect.x + 20, rect.y + 25 + i*40))
    
    # Settings content
    content_rect = pygame.Rect(rect.x + 210, rect.y + 60, rect.width - 220, rect.height - 70)
    pygame.draw.rect(surface, (250, 250, 250), content_rect, border_radius=8)
    
    # System settings
    sys_settings = [
        ("OS Version", "OS Simulator v2.0"),
        ("Processor", "Simulated CPU"),
        ("Memory", "16 GB"),
        ("Storage", "1 TB SSD"),
        ("Graphics", "Simulated GPU")
    ]
    
    for i, (setting, value) in enumerate(sys_settings):
        setting_text = small_font.render(setting, True, DARK_GRAY)
        value_text = small_font.render(value, True, BLUE)
        surface.blit(setting_text, (rect.x + 230, rect.y + 80 + i*30))
        surface.blit(value_text, (rect.x + 400, rect.y + 80 + i*30))

def terminal_content(surface, rect):
    # Modern terminal design
    pygame.draw.rect(surface, (20, 20, 30), rect, border_radius=8)
    
    # Terminal header
    pygame.draw.rect(surface, (40, 40, 50), (rect.x, rect.y, rect.width, 30), border_radius=8)
    header_text = small_font.render("Terminal", True, WHITE)
    surface.blit(header_text, (rect.x + 10, rect.y + 5))
    
    # Terminal content
    lines = [
        "user@os-simulator:~$ welcome",
        "Welcome to Enhanced OS Simulator Terminal",
        "",
        "user@os-simulator:~$ help",
        "Available commands: help, about, clear, date, sysinfo",
        "",
        "user@os-simulator:~$ date",
        datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M:%S"),
        "",
        "user@os-simulator:~$ sysinfo",
        "OS: OS Simulator v2.0",
        "CPU: Simulated Processor @ 3.2GHz",
        "Memory: 16GB RAM",
        "Storage: 1TB SSD",
        "",
        "user@os-simulator:~$ _"
    ]
    
    for i, line in enumerate(lines):
        line_text = small_font.render(line, True, WHITE)
        surface.blit(line_text, (rect.x + 10, rect.y + 40 + i*20))

def music_content(surface, rect):
    # Modern music player design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Player header
    pygame.draw.rect(surface, (30, 30, 40), (rect.x, rect.y, rect.width, 50), border_radius=8)
    header_text = medium_font.render("Music Player", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 10))
    
    # Album art with modern design
    album_rect = pygame.Rect(rect.x + rect.width//2 - 100, rect.y + 70, 200, 200)
    pygame.draw.rect(surface, (50, 50, 70), album_rect, border_radius=12)
    
    # Vinyl record effect
    pygame.draw.circle(surface, (30, 30, 30), (rect.x + rect.width//2, rect.y + 170), 80)
    pygame.draw.circle(surface, (200, 200, 200), (rect.x + rect.width//2, rect.y + 170), 30)
    pygame.draw.circle(surface, (30, 30, 30), (rect.x + rect.width//2, rect.y + 170), 10)
    
    # Song info
    song_text = medium_font.render("Now Playing: Enhanced Experience", True, DARK_GRAY)
    surface.blit(song_text, (rect.x + rect.width//2 - song_text.get_width()//2, rect.y + 290))
    
    artist_text = small_font.render("Artist: Hessam Edien", True, DARK_GRAY)
    surface.blit(artist_text, (rect.x + rect.width//2 - artist_text.get_width()//2, rect.y + 320))
    
    # Progress bar with modern design
    pygame.draw.rect(surface, (220, 220, 220), (rect.x + 50, rect.y + 350, rect.width - 100, 8), border_radius=4)
    pygame.draw.rect(surface, BLUE, (rect.x + 50, rect.y + 350, (rect.width - 100) * 0.7, 8), border_radius=4)
    
    # Time indicators
    time_current = small_font.render("2:15", True, DARK_GRAY)
    time_total = small_font.render("3:20", True, DARK_GRAY)
    surface.blit(time_current, (rect.x + 50, rect.y + 365))
    surface.blit(time_total, (rect.x + rect.width - 80, rect.y + 365))
    
    # Modern player controls
    controls = ["⏮", "⏸", "⏭"]
    for i, control in enumerate(controls):
        control_rect = pygame.Rect(rect.x + rect.width//2 - 90 + i*60, rect.y + 390, 50, 40)
        pygame.draw.rect(surface, BLUE, control_rect, border_radius=8)
        control_text = medium_font.render(control, True, WHITE)
        surface.blit(control_text, (rect.x + rect.width//2 - 75 + i*60, rect.y + 395))

def calculator_content(surface, rect):
    # Modern calculator design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Display with modern design
    display_rect = pygame.Rect(rect.x + 20, rect.y + 20, rect.width - 40, 70)
    pygame.draw.rect(surface, (30, 30, 40), display_rect, border_radius=8)
    
    display_text = medium_font.render("0", True, WHITE)
    surface.blit(display_text, (rect.x + rect.width - 40 - display_text.get_width(), rect.y + 45))
    
    # Modern calculator buttons
    buttons = [
        "C", "±", "%", "÷",
        "7", "8", "9", "×",
        "4", "5", "6", "−",
        "1", "2", "3", "+",
        "0", ".", "="
    ]
    
    for i, button in enumerate(buttons):
        if button == "0":
            # Make zero button wider
            btn_x = rect.x + 20
            btn_y = rect.y + 330
            btn_width = 130
        else:
            row = i // 4
            col = i % 4
            btn_x = rect.x + 20 + col * 70
            btn_y = rect.y + 110 + row * 55
            btn_width = 60
        
        btn_height = 45
        
        # Different colors for different button types
        if button in ["C", "±", "%"]:
            btn_color = (180, 180, 180)
        elif button in ["÷", "×", "−", "+", "="]:
            btn_color = (255, 159, 10)
        else:
            btn_color = (50, 50, 60)
        
        pygame.draw.rect(surface, btn_color, (btn_x, btn_y, btn_width, btn_height), border_radius=8)
        btn_text = medium_font.render(button, True, WHITE)
        surface.blit(btn_text, (btn_x + btn_width//2 - btn_text.get_width()//2, btn_y + btn_height//2 - btn_text.get_height()//2))

def notes_content(surface, rect):
    # Modern notes design
    pygame.draw.rect(surface, (255, 255, 240), rect, border_radius=8)
    
    # Notes header
    pygame.draw.rect(surface, (200, 200, 180), (rect.x, rect.y, rect.width, 50), border_radius=8)
    header_text = medium_font.render("Notes", True, DARK_GRAY)
    surface.blit(header_text, (rect.x + 20, rect.y + 10))
    
    # Sample note content with modern formatting
    note_content = [
        "Welcome to Enhanced Notes!",
        "",
        "This is a modern note-taking application with",
        "a clean and intuitive interface.",
        "",
        "Features:",
        "• Rich text formatting",
        "• Multiple notebooks",
        "• Cloud synchronization",
        "• Search functionality",
        "",
        "Created by Hessam Edien",
        "OS Simulator v2.0"
    ]
    
    for i, line in enumerate(note_content):
        line_text = small_font.render(line, True, DARK_GRAY)
        surface.blit(line_text, (rect.x + 20, rect.y + 70 + i*25))
    
    # Decorative elements
    pygame.draw.rect(surface, (255, 230, 200), (rect.x + rect.width - 100, rect.y + 70, 80, 10), border_radius=5)
    pygame.draw.rect(surface, (200, 230, 255), (rect.x + rect.width - 100, rect.y + 90, 80, 10), border_radius=5)
    pygame.draw.rect(surface, (230, 255, 200), (rect.x + rect.width - 100, rect.y + 110, 80, 10), border_radius=5)

def calendar_content(surface, rect):
    # Modern calendar design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Calendar header
    pygame.draw.rect(surface, BLUE, (rect.x, rect.y, rect.width, 60), border_radius=8)
    
    now = datetime.datetime.now()
    month_year = now.strftime("%B %Y")
    month_text = medium_font.render(month_year, True, WHITE)
    surface.blit(month_text, (rect.x + rect.width//2 - month_text.get_width()//2, rect.y + 15))
    
    # Navigation arrows
    pygame.draw.polygon(surface, WHITE, [(rect.x + 20, rect.y + 30), (rect.x + 40, rect.y + 20), (rect.x + 40, rect.y + 40)])
    pygame.draw.polygon(surface, WHITE, [(rect.x + rect.width - 20, rect.y + 30), (rect.x + rect.width - 40, rect.y + 20), (rect.x + rect.width - 40, rect.y + 40)])
    
    # Days of week
    days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    for i, day in enumerate(days):
        day_text = small_font.render(day, True, DARK_GRAY)
        surface.blit(day_text, (rect.x + 20 + i*70, rect.y + 70))
    
    # Calendar grid with modern design
    for week in range(6):
        for day in range(7):
            day_rect = pygame.Rect(rect.x + 20 + day*70, rect.y + 100 + week*50, 60, 40)
            
            # Highlight current day
            if week == 2 and day == now.weekday():
                pygame.draw.rect(surface, LIGHT_BLUE, day_rect, border_radius=8)
            else:
                pygame.draw.rect(surface, (245, 245, 245), day_rect, border_radius=8)
            
            pygame.draw.rect(surface, (220, 220, 220), day_rect, 1, border_radius=8)
            
            # Day numbers
            day_num = week * 7 + day + 1 - now.replace(day=1).weekday()
            if 1 <= day_num <= 31:
                day_color = DARK_GRAY if week == 2 and day == now.weekday() else DARK_GRAY
                day_text = small_font.render(str(day_num), True, day_color)
                surface.blit(day_text, (rect.x + 45 + day*70, rect.y + 115 + week*50))

def store_content(surface, rect):
    # Modern app store design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Store header
    pygame.draw.rect(surface, (30, 30, 40), (rect.x, rect.y, rect.width, 60), border_radius=8)
    header_text = medium_font.render("App Store", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 15))
    
    # Search bar
    search_rect = pygame.Rect(rect.x + 200, rect.y + 15, rect.width - 250, 30)
    pygame.draw.rect(surface, (50, 50, 60), search_rect, border_radius=6)
    search_text = small_font.render("Search apps...", True, (150, 150, 150))
    surface.blit(search_text, (rect.x + 210, rect.y + 20))
    
    # Categories
    categories = ["Featured", "Games", "Productivity", "Utilities", "Entertainment", "Social"]
    for i, category in enumerate(categories):
        cat_rect = pygame.Rect(rect.x + 20, rect.y + 80 + i*40, 150, 30)
        pygame.draw.rect(surface, LIGHT_BLUE if i == 0 else (240, 240, 240), cat_rect, border_radius=6)
        cat_text = small_font.render(category, True, DARK_GRAY)
        surface.blit(cat_text, (rect.x + 30, rect.y + 85 + i*40))
    
    # Featured apps
    featured_title = medium_font.render("Featured Apps", True, DARK_GRAY)
    surface.blit(featured_title, (rect.x + 200, rect.y + 80))
    
    featured_apps = ["Browser", "Music", "Calculator", "Notes", "Calendar", "Terminal"]
    for i, app in enumerate(featured_apps):
        app_rect = pygame.Rect(rect.x + 200 + (i%3)*140, rect.y + 120 + (i//3)*160, 120, 140)
        pygame.draw.rect(surface, (245, 245, 245), app_rect, border_radius=8)
        pygame.draw.rect(surface, (220, 220, 220), app_rect, 1, border_radius=8)
        
        # App icon
        screen.blit(icons[app.lower()], (rect.x + 200 + (i%3)*140 + 35, rect.y + 120 + (i//3)*160 + 20))
        
        # App name
        app_text = small_font.render(app, True, DARK_GRAY)
        surface.blit(app_text, (rect.x + 200 + (i%3)*140 + 60 - app_text.get_width()//2, rect.y + 120 + (i//3)*160 + 90))
        
        # Get button
        get_rect = pygame.Rect(rect.x + 200 + (i%3)*140 + 30, rect.y + 120 + (i//3)*160 + 110, 60, 25)
        pygame.draw.rect(surface, BLUE, get_rect, border_radius=6)
        get_text = small_font.render("GET", True, WHITE)
        surface.blit(get_text, (rect.x + 200 + (i%3)*140 + 45, rect.y + 120 + (i//3)*160 + 115))

def game_content(surface, rect):
    # Modern game design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Game header
    pygame.draw.rect(surface, (40, 40, 50), (rect.x, rect.y, rect.width, 50), border_radius=8)
    header_text = medium_font.render("Space Adventure", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 10))
    
    # Game area
    game_rect = pygame.Rect(rect.x + 20, rect.y + 70, rect.width - 40, 300)
    pygame.draw.rect(surface, (20, 20, 30), game_rect, border_radius=8)
    
    # Stars (background)
    for _ in range(50):
        x = random.randint(game_rect.x, game_rect.x + game_rect.width)
        y = random.randint(game_rect.y, game_rect.y + game_rect.height)
        pygame.draw.circle(surface, WHITE, (x, y), 1)
    
    # Player spaceship
    ship_points = [
        (game_rect.x + 50, game_rect.y + game_rect.height - 30),
        (game_rect.x + 30, game_rect.y + game_rect.height - 10),
        (game_rect.x + 70, game_rect.y + game_rect.height - 10)
    ]
    pygame.draw.polygon(surface, GREEN, ship_points)
    
    # Enemies
    for i in range(3):
        enemy_x = game_rect.x + 200 + i*100
        enemy_y = game_rect.y + 50 + i*30
        pygame.draw.rect(surface, RED, (enemy_x, enemy_y, 30, 30), border_radius=6)
    
    # Score
    score_text = medium_font.render("Score: 1250", True, WHITE)
    surface.blit(score_text, (game_rect.x + 10, game_rect.y + 10))
    
    # Instructions
    instructions = [
        "Controls:",
        "← → : Move",
        "SPACE : Shoot",
        "ESC : Pause"
    ]
    
    for i, line in enumerate(instructions):
        line_text = small_font.render(line, True, WHITE)
        surface.blit(line_text, (game_rect.x + game_rect.width - 150, game_rect.y + 20 + i*25))

def camera_content(surface, rect):
    # Modern camera design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Camera header
    pygame.draw.rect(surface, (30, 30, 40), (rect.x, rect.y, rect.width, 50), border_radius=8)
    header_text = medium_font.render("Camera", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 10))
    
    # Viewfinder
    viewfinder_rect = pygame.Rect(rect.x + 20, rect.y + 70, rect.width - 40, 250)
    pygame.draw.rect(surface, (20, 20, 30), viewfinder_rect, border_radius=8)
    
    # Camera lens effect
    pygame.draw.circle(surface, (50, 50, 70), (rect.x + rect.width//2, rect.y + 195), 80)
    pygame.draw.circle(surface, (30, 30, 50), (rect.x + rect.width//2, rect.y + 195), 60)
    pygame.draw.circle(surface, (70, 70, 90), (rect.x + rect.width//2, rect.y + 195), 40)
    pygame.draw.circle(surface, (100, 100, 120), (rect.x + rect.width//2, rect.y + 195), 20)
    
    # Shutter button
    shutter_rect = pygame.Rect(rect.x + rect.width//2 - 30, rect.y + 340, 60, 60)
    pygame.draw.circle(surface, RED, (rect.x + rect.width//2, rect.y + 370), 30)
    pygame.draw.circle(surface, (200, 50, 50), (rect.x + rect.width//2, rect.y + 370), 20)
    
    # Camera modes
    modes = ["Photo", "Video", "Portrait", "Panorama"]
    for i, mode in enumerate(modes):
        mode_rect = pygame.Rect(rect.x + 20 + i*100, rect.y + 410, 80, 30)
        pygame.draw.rect(surface, LIGHT_BLUE if i == 0 else (240, 240, 240), mode_rect, border_radius=6)
        mode_text = small_font.render(mode, True, DARK_GRAY)
        surface.blit(mode_text, (rect.x + 40 + i*100 - mode_text.get_width()//2, rect.y + 415))

def gallery_content(surface, rect):
    # Modern gallery design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Gallery header
    pygame.draw.rect(surface, (30, 30, 40), (rect.x, rect.y, rect.width, 50), border_radius=8)
    header_text = medium_font.render("Gallery", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 10))
    
    # Photo grid
    for i in range(9):
        row = i // 3
        col = i % 3
        photo_rect = pygame.Rect(rect.x + 20 + col*140, rect.y + 70 + row*140, 120, 120)
        
        # Different colored photos
        colors = [
            (255, 200, 200), (200, 255, 200), (200, 200, 255),
            (255, 255, 200), (255, 200, 255), (200, 255, 255),
            (230, 230, 250), (250, 230, 230), (230, 250, 230)
        ]
        
        pygame.draw.rect(surface, colors[i], photo_rect, border_radius=8)
        pygame.draw.rect(surface, (200, 200, 200), photo_rect, 1, border_radius=8)
        
        # Photo label
        photo_text = small_font.render(f"Photo {i+1}", True, DARK_GRAY)
        surface.blit(photo_text, (rect.x + 20 + col*140 + 60 - photo_text.get_width()//2, rect.y + 70 + row*140 + 50))

def social_media_content(surface, rect, platform):
    # Modern social media design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Platform-specific colors
    platform_colors = {
        "Facebook": (59, 89, 152),
        "Instagram": (225, 48, 108),
        "Twitter": (29, 161, 242),
        "Telegram": (0, 136, 204),
        "WhatsApp": (37, 211, 102)
    }
    
    # Header with platform color
    header_color = platform_colors.get(platform, (30, 30, 40))
    pygame.draw.rect(surface, header_color, (rect.x, rect.y, rect.width, 60), border_radius=8)
    
    header_text = medium_font.render(platform, True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 15))
    
    # User profile
    profile_rect = pygame.Rect(rect.x + 20, rect.y + 80, 50, 50)
    pygame.draw.circle(surface, (200, 200, 200), (rect.x + 45, rect.y + 105), 25)
    
    user_text = small_font.render("Hessam Edien", True, DARK_GRAY)
    surface.blit(user_text, (rect.x + 80, rect.y + 90))
    
    status_text = small_font.render("Online", True, GREEN)
    surface.blit(status_text, (rect.x + 80, rect.y + 110))
    
    # Post input
    post_rect = pygame.Rect(rect.x + 20, rect.y + 140, rect.width - 40, 40)
    pygame.draw.rect(surface, (245, 245, 245), post_rect, border_radius=6)
    pygame.draw.rect(surface, (220, 220, 220), post_rect, 1, border_radius=6)
    
    post_text = small_font.render("What's on your mind?", True, (150, 150, 150))
    surface.blit(post_text, (rect.x + 30, rect.y + 150))
    
    # Sample posts
    posts = [
        {
            "user": "OS Simulator",
            "content": f"Welcome to {platform}! This is a modern social media experience.",
            "time": "2 hrs ago",
            "likes": 42,
            "comments": 7
        },
        {
            "user": "Hessam Edien",
            "content": "Just exploring the enhanced OS Simulator. Amazing work!",
            "time": "5 hrs ago",
            "likes": 28,
            "comments": 3
        }
    ]
    
    for i, post in enumerate(posts):
        post_y = rect.y + 200 + i*120
        
        # Post background
        post_bg = pygame.Rect(rect.x + 20, post_y, rect.width - 40, 100)
        pygame.draw.rect(surface, (250, 250, 250), post_bg, border_radius=8)
        pygame.draw.rect(surface, (230, 230, 230), post_bg, 1, border_radius=8)
        
        # User info
        user_text = small_font.render(post["user"], True, DARK_GRAY)
        surface.blit(user_text, (rect.x + 30, post_y + 10))
        
        time_text = small_font.render(post["time"], True, (150, 150, 150))
        surface.blit(time_text, (rect.x + 30, post_y + 30))
        
        # Post content
        content_text = small_font.render(post["content"], True, DARK_GRAY)
        surface.blit(content_text, (rect.x + 30, post_y + 50))
        
        # Engagement
        likes_text = small_font.render(f"♥ {post['likes']}", True, RED)
        comments_text = small_font.render(f"💬 {post['comments']}", True, BLUE)
        surface.blit(likes_text, (rect.x + 30, post_y + 75))
        surface.blit(comments_text, (rect.x + 100, post_y + 75))

def facebook_content(surface, rect):
    social_media_content(surface, rect, "Facebook")

def instagram_content(surface, rect):
    social_media_content(surface, rect, "Instagram")

def twitter_content(surface, rect):
    social_media_content(surface, rect, "Twitter")

def telegram_content(surface, rect):
    social_media_content(surface, rect, "Telegram")

def whatsapp_content(surface, rect):
    social_media_content(surface, rect, "WhatsApp")

def weather_content(surface, rect):
    # Modern weather app design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Header with gradient
    for i in range(60):
        color_val = 100 + i * 2
        pygame.draw.rect(surface, (color_val, color_val, 255), (rect.x, rect.y + i, rect.width, 1))
    
    header_text = medium_font.render("Weather", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 15))
    
    # Current weather
    current_rect = pygame.Rect(rect.x + 20, rect.y + 80, rect.width - 40, 120)
    pygame.draw.rect(surface, (200, 230, 255), current_rect, border_radius=8)
    
    # Temperature
    temp_text = large_font.render("22°C", True, DARK_GRAY)
    surface.blit(temp_text, (rect.x + 40, rect.y + 100))
    
    # Weather condition
    condition_text = medium_font.render("Sunny", True, DARK_GRAY)
    surface.blit(condition_text, (rect.x + 40, rect.y + 140))
    
    # Location
    location_text = small_font.render("Tehran, Iran", True, DARK_GRAY)
    surface.blit(location_text, (rect.x + 40, rect.y + 170))
    
    # Weather icon (sun)
    pygame.draw.circle(surface, (255, 200, 0), (rect.x + rect.width - 80, rect.y + 140), 40)
    
    # Forecast
    forecast_title = medium_font.render("5-Day Forecast", True, DARK_GRAY)
    surface.blit(forecast_title, (rect.x + 20, rect.y + 220))
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    temps = ["24°", "23°", "25°", "22°", "21°"]
    
    for i, (day, temp) in enumerate(zip(days, temps)):
        day_rect = pygame.Rect(rect.x + 20 + i*100, rect.y + 260, 80, 80)
        pygame.draw.rect(surface, (240, 245, 255), day_rect, border_radius=8)
        
        day_text = small_font.render(day, True, DARK_GRAY)
        surface.blit(day_text, (rect.x + 40 + i*100 - day_text.get_width()//2, rect.y + 270))
        
        temp_text = small_font.render(temp, True, DARK_GRAY)
        surface.blit(temp_text, (rect.x + 40 + i*100 - temp_text.get_width()//2, rect.y + 300))
        
        # Simple weather icon
        pygame.draw.circle(surface, (255, 200, 0), (rect.x + 40 + i*100, rect.y + 320), 10)

def mail_content(surface, rect):
    # Modern email app design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Header
    pygame.draw.rect(surface, (200, 50, 50), (rect.x, rect.y, rect.width, 60), border_radius=8)
    header_text = medium_font.render("Mail", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 15))
    
    # Compose button
    compose_rect = pygame.Rect(rect.x + rect.width - 120, rect.y + 15, 100, 30)
    pygame.draw.rect(surface, WHITE, compose_rect, border_radius=6)
    compose_text = small_font.render("Compose", True, (200, 50, 50))
    surface.blit(compose_text, (rect.x + rect.width - 110, rect.y + 20))
    
    # Folders
    folders = ["Inbox", "Sent", "Drafts", "Spam"]
    for i, folder in enumerate(folders):
        folder_rect = pygame.Rect(rect.x + 20, rect.y + 80 + i*40, 150, 30)
        pygame.draw.rect(surface, LIGHT_BLUE if i == 0 else (240, 240, 240), folder_rect, border_radius=6)
        folder_text = small_font.render(folder, True, DARK_GRAY)
        surface.blit(folder_text, (rect.x + 30, rect.y + 85 + i*40))
    
    # Emails
    emails = [
        {"sender": "OS Simulator Team", "subject": "Welcome to Enhanced OS", "preview": "Thank you for using our enhanced operating system...", "time": "10:30 AM"},
        {"sender": "Hessam Edien", "subject": "App Updates", "preview": "I've added several new features to the applications...", "time": "9:15 AM"},
        {"sender": "Support Team", "subject": "Your Feedback", "preview": "We appreciate your feedback on our simulator...", "time": "Yesterday"}
    ]
    
    for i, email in enumerate(emails):
        email_rect = pygame.Rect(rect.x + 190, rect.y + 80 + i*100, rect.width - 210, 90)
        pygame.draw.rect(surface, (250, 250, 250) if i != 0 else (230, 240, 255), email_rect, border_radius=8)
        pygame.draw.rect(surface, (220, 220, 220), email_rect, 1, border_radius=8)
        
        sender_text = small_font.render(email["sender"], True, DARK_GRAY)
        surface.blit(sender_text, (rect.x + 210, rect.y + 90 + i*100))
        
        subject_text = small_font.render(email["subject"], True, DARK_GRAY)
        surface.blit(subject_text, (rect.x + 210, rect.y + 110 + i*100))
        
        preview_text = small_font.render(email["preview"], True, (150, 150, 150))
        surface.blit(preview_text, (rect.x + 210, rect.y + 130 + i*100))
        
        time_text = small_font.render(email["time"], True, (150, 150, 150))
        surface.blit(time_text, (rect.x + rect.width - 80, rect.y + 90 + i*100))

def maps_content(surface, rect):
    # Modern maps app design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Header
    pygame.draw.rect(surface, (50, 150, 50), (rect.x, rect.y, rect.width, 60), border_radius=8)
    header_text = medium_font.render("Maps", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 15))
    
    # Search bar
    search_rect = pygame.Rect(rect.x + 20, rect.y + 80, rect.width - 40, 40)
    pygame.draw.rect(surface, (240, 240, 240), search_rect, border_radius=6)
    pygame.draw.rect(surface, (220, 220, 220), search_rect, 1, border_radius=6)
    
    search_text = small_font.render("Search for places or addresses", True, (150, 150, 150))
    surface.blit(search_text, (rect.x + 30, rect.y + 90))
    
    # Map area
    map_rect = pygame.Rect(rect.x + 20, rect.y + 140, rect.width - 40, rect.height - 160)
    pygame.draw.rect(surface, (200, 230, 200), map_rect, border_radius=8)
    
    # Streets
    for i in range(5):
        street_y = map_rect.y + 40 + i*60
        pygame.draw.rect(surface, (100, 100, 100), (map_rect.x, street_y, map_rect.width, 4))
    
    for i in range(6):
        street_x = map_rect.x + 40 + i*80
        pygame.draw.rect(surface, (100, 100, 100), (street_x, map_rect.y, 4, map_rect.height))
    
    # Landmarks
    landmarks = [
        {"x": map_rect.x + 100, "y": map_rect.y + 80, "name": "OS Tower", "color": BLUE},
        {"x": map_rect.x + 300, "y": map_rect.y + 120, "name": "Simulator Park", "color": GREEN},
        {"x": map_rect.x + 200, "y": map_rect.y + 200, "name": "App Plaza", "color": RED},
        {"x": map_rect.x + 400, "y": map_rect.y + 180, "name": "Code Center", "color": PURPLE}
    ]
    
    for landmark in landmarks:
        pygame.draw.circle(surface, landmark["color"], (landmark["x"], landmark["y"]), 10)
        name_text = small_font.render(landmark["name"], True, DARK_GRAY)
        surface.blit(name_text, (landmark["x"] - name_text.get_width()//2, landmark["y"] + 15))
    
    # Current location
    pygame.draw.circle(surface, BLUE, (map_rect.x + 150, map_rect.y + 150), 8)
    pygame.draw.circle(surface, (100, 100, 255), (map_rect.x + 150, map_rect.y + 150), 15, 2)

def files_content(surface, rect):
    # Modern file manager design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Header
    pygame.draw.rect(surface, (100, 100, 200), (rect.x, rect.y, rect.width, 60), border_radius=8)
    header_text = medium_font.render("Files", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 15))
    
    # Navigation buttons
    nav_buttons = ["←", "→", "↑", "⟳"]
    for i, btn in enumerate(nav_buttons):
        btn_rect = pygame.Rect(rect.x + 120 + i*40, rect.y + 15, 30, 30)
        pygame.draw.rect(surface, (150, 150, 220), btn_rect, border_radius=6)
        btn_text = small_font.render(btn, True, WHITE)
        surface.blit(btn_text, (rect.x + 130 + i*40, rect.y + 20))
    
    # Address bar
    address_rect = pygame.Rect(rect.x + 280, rect.y + 15, rect.width - 380, 30)
    pygame.draw.rect(surface, (80, 80, 160), address_rect, border_radius=6)
    address_text = small_font.render("/Home/Documents", True, WHITE)
    surface.blit(address_text, (rect.x + 290, rect.y + 20))
    
    # Search bar
    search_rect = pygame.Rect(rect.x + rect.width - 90, rect.y + 15, 70, 30)
    pygame.draw.rect(surface, (150, 150, 220), search_rect, border_radius=6)
    search_text = small_font.render("🔍", True, WHITE)
    surface.blit(search_text, (rect.x + rect.width - 75, rect.y + 20))
    
    # Sidebar with locations
    sidebar_rect = pygame.Rect(rect.x, rect.y + 70, 200, rect.height - 80)
    pygame.draw.rect(surface, (245, 245, 245), sidebar_rect, border_radius=8)
    
    locations = ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos"]
    for i, location in enumerate(locations):
        loc_rect = pygame.Rect(rect.x + 10, rect.y + 80 + i*40, 180, 30)
        pygame.draw.rect(surface, LIGHT_BLUE if i == 1 else (240, 240, 240), loc_rect, border_radius=6)
        loc_text = small_font.render(location, True, DARK_GRAY)
        surface.blit(loc_text, (rect.x + 20, rect.y + 85 + i*40))
    
    # File area
    file_rect = pygame.Rect(rect.x + 210, rect.y + 70, rect.width - 220, rect.height - 80)
    pygame.draw.rect(surface, (250, 250, 250), file_rect, border_radius=8)
    
    # Files and folders
    items = [
        {"name": "Projects", "type": "folder", "size": "", "modified": "Yesterday"},
        {"name": "Resume.pdf", "type": "file", "size": "245 KB", "modified": "Today"},
        {"name": "Photos", "type": "folder", "size": "", "modified": "2 days ago"},
        {"name": "Notes.txt", "type": "file", "size": "12 KB", "modified": "Today"},
        {"name": "Music", "type": "folder", "size": "", "modified": "1 week ago"},
        {"name": "Report.docx", "type": "file", "size": "1.2 MB", "modified": "Yesterday"}
    ]
    
    for i, item in enumerate(items):
        item_rect = pygame.Rect(rect.x + 220, rect.y + 80 + i*50, rect.width - 240, 40)
        pygame.draw.rect(surface, (255, 255, 255), item_rect, border_radius=6)
        pygame.draw.rect(surface, (230, 230, 230), item_rect, 1, border_radius=6)
        
        # Icon
        icon_color = (100, 150, 255) if item["type"] == "folder" else (150, 150, 150)
        pygame.draw.rect(surface, icon_color, (rect.x + 230, rect.y + 85 + i*50, 30, 30), border_radius=6)
        
        # Name
        name_text = small_font.render(item["name"], True, DARK_GRAY)
        surface.blit(name_text, (rect.x + 270, rect.y + 85 + i*50))
        
        # Details
        details_text = small_font.render(f"{item['size']} • {item['modified']}", True, (150, 150, 150))
        surface.blit(details_text, (rect.x + 270, rect.y + 105 + i*50))

def video_content(surface, rect):
    # Modern video player design
    pygame.draw.rect(surface, WHITE, rect, border_radius=8)
    
    # Header
    pygame.draw.rect(surface, (180, 0, 100), (rect.x, rect.y, rect.width, 60), border_radius=8)
    header_text = medium_font.render("Video Player", True, WHITE)
    surface.blit(header_text, (rect.x + 20, rect.y + 15))
    
    # Video area
    video_rect = pygame.Rect(rect.x + 20, rect.y + 80, rect.width - 40, 250)
    pygame.draw.rect(surface, (20, 20, 30), video_rect, border_radius=8)
    
    # Play button
    play_rect = pygame.Rect(rect.x + rect.width//2 - 30, rect.y + 170, 60, 60)
    pygame.draw.circle(surface, (180, 0, 100), (rect.x + rect.width//2, rect.y + 200), 30)
    pygame.draw.polygon(surface, WHITE, [(rect.x + rect.width//2 - 10, rect.y + 190), 
                                       (rect.x + rect.width//2 - 10, rect.y + 210),
                                       (rect.x + rect.width//2 + 15, rect.y + 200)])
    
    # Video info
    info_rect = pygame.Rect(rect.x + 20, rect.y + 350, rect.width - 40, 80)
    pygame.draw.rect(surface, (245, 245, 245), info_rect, border_radius=8)
    
    title_text = medium_font.render("OS Simulator Demo", True, DARK_GRAY)
    surface.blit(title_text, (rect.x + 30, rect.y + 360))
    
    desc_text = small_font.render("A demonstration of the enhanced OS Simulator features", True, (150, 150, 150))
    surface.blit(desc_text, (rect.x + 30, rect.y + 390))
    
    duration_text = small_font.render("Duration: 5:30", True, (150, 150, 150))
    surface.blit(duration_text, (rect.x + rect.width - 100, rect.y + 360))
    
    # Controls
    controls = ["⏮", "⏪", "⏸", "⏩", "⏭"]
    for i, control in enumerate(controls):
        control_rect = pygame.Rect(rect.x + rect.width//2 - 120 + i*50, rect.y + 450, 40, 40)
        pygame.draw.rect(surface, (180, 0, 100), control_rect, border_radius=6)
        control_text = small_font.render(control, True, WHITE)
        surface.blit(control_text, (rect.x + rect.width//2 - 110 + i*50, rect.y + 455))

# Initialize apps
windows_apps = [
    {"name": "Browser", "icon": "browser", "func": browser_content},
    {"name": "Settings", "icon": "settings", "func": settings_content},
    {"name": "Terminal", "icon": "terminal", "func": terminal_content},
    {"name": "Music", "icon": "music", "func": music_content},
    {"name": "Calculator", "icon": "calculator", "func": calculator_content},
    {"name": "Notes", "icon": "notes", "func": notes_content},
    {"name": "Calendar", "icon": "calendar", "func": calendar_content},
    {"name": "Store", "icon": "store", "func": store_content},
    {"name": "Game", "icon": "game", "func": game_content},
    {"name": "Camera", "icon": "camera", "func": camera_content},
    {"name": "Gallery", "icon": "gallery", "func": gallery_content},
    {"name": "Facebook", "icon": "facebook", "func": facebook_content},
    {"name": "Instagram", "icon": "instagram", "func": instagram_content},
    {"name": "Twitter", "icon": "twitter", "func": twitter_content},
    {"name": "Telegram", "icon": "telegram", "func": telegram_content},
    {"name": "WhatsApp", "icon": "whatsapp", "func": whatsapp_content},
    {"name": "Weather", "icon": "weather", "func": weather_content},
    {"name": "Mail", "icon": "mail", "func": mail_content},
    {"name": "Maps", "icon": "maps", "func": maps_content},
    {"name": "Files", "icon": "files", "func": files_content},
    {"name": "Video", "icon": "video", "func": video_content},
]

mac_apps = [
    {"name": "Browser", "icon": "browser", "func": browser_content},
    {"name": "Settings", "icon": "settings", "func": settings_content},
    {"name": "Terminal", "icon": "terminal", "func": terminal_content},
    {"name": "Music", "icon": "music", "func": music_content},
    {"name": "Calculator", "icon": "calculator", "func": calculator_content},
    {"name": "Notes", "icon": "notes", "func": notes_content},
    {"name": "Calendar", "icon": "calendar", "func": calendar_content},
    {"name": "Store", "icon": "store", "func": store_content},
    {"name": "Game", "icon": "game", "func": game_content},
    {"name": "Camera", "icon": "camera", "func": camera_content},
    {"name": "Gallery", "icon": "gallery", "func": gallery_content},
    {"name": "Facebook", "icon": "facebook", "func": facebook_content},
    {"name": "Instagram", "icon": "instagram", "func": instagram_content},
    {"name": "Twitter", "icon": "twitter", "func": twitter_content},
    {"name": "Telegram", "icon": "telegram", "func": telegram_content},
    {"name": "WhatsApp", "icon": "whatsapp", "func": whatsapp_content},
    {"name": "Weather", "icon": "weather", "func": weather_content},
    {"name": "Mail", "icon": "mail", "func": mail_content},
    {"name": "Maps", "icon": "maps", "func": maps_content},
    {"name": "Files", "icon": "files", "func": files_content},
    {"name": "Video", "icon": "video", "func": video_content},
]

# Boot screen
def draw_boot_screen():
    screen.fill(BLACK)
    
    # Animated boot loader
    boot_text = title_font.render("OS Simulator v2.0", True, WHITE)
    screen.blit(boot_text, (WIDTH//2 - boot_text.get_width()//2, HEIGHT//4))
    
    # Loading animation
    loading_width = 400
    loading_height = 20
    loading_x = WIDTH//2 - loading_width//2
    loading_y = HEIGHT//2 - loading_height//2
    
    pygame.draw.rect(screen, DARK_GRAY, (loading_x, loading_y, loading_width, loading_height), border_radius=10)
    
    # Animated progress bar
    progress = (pygame.time.get_ticks() // 50) % loading_width
    pygame.draw.rect(screen, BLUE, (loading_x, loading_y, progress, loading_height), border_radius=10)
    
    # Boot options
    options = [
        "Windows 11",
        "macOS",
        "Help (F1)",
        "Power Off"
    ]
    
    for i, option in enumerate(options):
        option_text = large_font.render(f"{i+1}. {option}", True, WHITE)
        screen.blit(option_text, (WIDTH//2 - 150, HEIGHT//2 + 60 + i*60))
    
    # Instructions
    instructions = small_font.render("Press 1-4 to select an option or use mouse to click", True, WHITE)
    screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT - 50))
    
    # Create clickable areas
    windows_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 60, 300, 50)
    mac_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 120, 300, 50)
    help_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 180, 300, 50)
    power_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 240, 300, 50)
    
    return windows_rect, mac_rect, help_rect, power_rect

# Windows 11 desktop
def draw_windows_desktop():
    # Background with parallax effect
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        # Create a gradient background
        for y in range(HEIGHT):
            color_val = 50 + (y * 150 // HEIGHT)
            pygame.draw.line(screen, (color_val, color_val, color_val + 50), (0, y), (WIDTH, y))
    
    # Modern taskbar with transparency
    taskbar_height = 50
    taskbar_surface = pygame.Surface((WIDTH, taskbar_height), pygame.SRCALPHA)
    taskbar_surface.fill((30, 30, 30, 200))
    screen.blit(taskbar_surface, (0, HEIGHT - taskbar_height))
    
    # Start button with modern design
    start_rect = pygame.Rect(10, HEIGHT - taskbar_height + 5, 120, 40)
    pygame.draw.rect(screen, BLUE, start_rect, border_radius=8)
    start_text = medium_font.render("Start", True, WHITE)
    screen.blit(start_text, (20, HEIGHT - taskbar_height + 15))
    
    # System tray with modern icons
    time_text = small_font.render(datetime.datetime.now().strftime("%H:%M"), True, WHITE)
    screen.blit(time_text, (WIDTH - 60, HEIGHT - taskbar_height + 15))
    
    # App icons on taskbar with hover effect
    for i, app in enumerate(windows_apps[:8]):
        icon_rect = pygame.Rect(140 + i*50, HEIGHT - taskbar_height + 5, 40, 40)
        
        # Hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if icon_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, (80, 80, 80, 150), icon_rect, border_radius=8)
        
        screen.blit(pygame.transform.scale(icons[app["icon"]], (30, 30)), (140 + i*50 + 5, HEIGHT - taskbar_height + 10))
    
    # Desktop icons with modern design
    for i, app in enumerate(windows_apps[:12]):
        icon_rect = pygame.Rect(50 + (i%4)*120, 100 + (i//4)*120, 80, 100)
        
        # Icon background with hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if icon_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, (255, 255, 255, 100), icon_rect, border_radius=8)
        
        # App icon
        screen.blit(pygame.transform.scale(icons[app["icon"]], (50, 50)), (50 + (i%4)*120 + 15, 100 + (i//4)*120 + 10))
        
        # App name with shadow
        app_text = small_font.render(app["name"], True, WHITE)
        text_shadow = small_font.render(app["name"], True, (0, 0, 0, 150))
        screen.blit(text_shadow, (50 + (i%4)*120 + 40 - app_text.get_width()//2 + 1, 100 + (i//4)*120 + 65 + 1))
        screen.blit(app_text, (50 + (i%4)*120 + 40 - app_text.get_width()//2, 100 + (i//4)*120 + 65))
    
    # Start menu
    if windows_start_open:
        draw_windows_start_menu()
    
    return start_rect

def draw_windows_start_menu():
    menu_width = 500
    menu_height = 600
    menu_x = 0
    menu_y = HEIGHT - 50 - menu_height
    
    # Menu background with blur effect (simulated)
    menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
    menu_surface.fill((30, 30, 30, 230))
    screen.blit(menu_surface, (menu_x, menu_y))
    
    # Search bar
    search_rect = pygame.Rect(menu_x + 20, menu_y + 20, menu_width - 40, 50)
    pygame.draw.rect(screen, (50, 50, 50), search_rect, border_radius=10)
    search_text = small_font.render("Type here to search", True, (150, 150, 150))
    screen.blit(search_text, (menu_x + 40, menu_y + 35))
    
    # Pinned apps section
    pinned_text = medium_font.render("Pinned", True, WHITE)
    screen.blit(pinned_text, (menu_x + 20, menu_y + 90))
    
    for i, app in enumerate(windows_apps[:12]):
        row = i // 4
        col = i % 4
        app_rect = pygame.Rect(menu_x + 20 + col*110, menu_y + 130 + row*100, 100, 90)
        
        # App icon background
        pygame.draw.rect(screen, (60, 60, 60), app_rect, border_radius=8)
        
        # App icon
        screen.blit(pygame.transform.scale(icons[app["icon"]], (50, 50)), (menu_x + 20 + col*110 + 25, menu_y + 130 + row*100 + 10))
        
        # App name
        app_name = small_font.render(app["name"], True, WHITE)
        screen.blit(app_name, (menu_x + 20 + col*110 + 50 - app_name.get_width()//2, menu_y + 130 + row*100 + 65))
    
    # Recommended section
    recommended_text = medium_font.render("Recommended", True, WHITE)
    screen.blit(recommended_text, (menu_x + 20, menu_y + 400))
    
    # Power options
    power_rect = pygame.Rect(menu_x + menu_width - 120, menu_y + menu_height - 60, 100, 40)
    pygame.draw.rect(screen, (200, 0, 0), power_rect, border_radius=8)
    power_text = small_font.render("Power", True, WHITE)
    screen.blit(power_text, (menu_x + menu_width - 70 - power_text.get_width()//2, menu_y + menu_height - 50))
    
    return power_rect

# macOS desktop
def draw_mac_desktop():
    # Background with modern design
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        # Create a macOS-style gradient
        for y in range(HEIGHT):
            color_val = 100 + (y * 100 // HEIGHT)
            pygame.draw.line(screen, (color_val, color_val, color_val + 100), (0, y), (WIDTH, y))
    
    # Menu bar with modern design
    menu_height = 30
    menu_surface = pygame.Surface((WIDTH, menu_height), pygame.SRCALPHA)
    menu_surface.fill((50, 50, 50, 220))
    screen.blit(menu_surface, (0, 0))
    
    # Apple menu
    apple_text = mac_small_font.render("", True, WHITE)
    screen.blit(apple_text, (15, 5))
    
    # Menu items
    menus = ["Finder", "File", "Edit", "View", "Go", "Window", "Help"]
    x_offset = 50
    for menu in menus:
        menu_text = mac_small_font.render(menu, True, WHITE)
        screen.blit(menu_text, (x_offset, 5))
        x_offset += menu_text.get_width() + 20
    
    # System info with modern design
    time_text = mac_small_font.render(datetime.datetime.now().strftime("%H:%M"), True, WHITE)
    screen.blit(time_text, (WIDTH - 50, 5))
    
    # Dock with modern design
    dock_height = 80
    dock_surface = pygame.Surface((WIDTH, dock_height), pygame.SRCALPHA)
    dock_surface.fill((50, 50, 50, 180))
    screen.blit(dock_surface, (0, HEIGHT - dock_height))
    
    # App icons in dock with reflection effect
    for i, app in enumerate(mac_apps[:10]):
        icon_size = 60
        icon_x = WIDTH//2 - 250 + i*60
        icon_y = HEIGHT - dock_height + 10
        
        # Icon background with hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.Rect(icon_x, icon_y, icon_size, icon_size).collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, (255, 255, 255, 100), (icon_x, icon_y, icon_size, icon_size), border_radius=12)
        
        # App icon
        screen.blit(pygame.transform.scale(icons[app["icon"]], (icon_size-10, icon_size-10)), (icon_x+5, icon_y+5))
    
    # Desktop icons with modern design
    for i, app in enumerate(mac_apps[:8]):
        icon_rect = pygame.Rect(50 + (i%4)*120, 100, 80, 100)
        
        # Icon background with hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if icon_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, (255, 255, 255, 100), icon_rect, border_radius=10)
        
        # App icon
        screen.blit(pygame.transform.scale(icons[app["icon"]], (50, 50)), (50 + (i%4)*120 + 15, 100 + 10))
        
        # App name
        app_text = mac_small_font.render(app["name"], True, WHITE)
        screen.blit(app_text, (50 + (i%4)*120 + 40 - app_text.get_width()//2, 100 + 60))
    
    # If dock is open, show more apps
    if mac_dock_open:
        draw_mac_dock_expanded()

def draw_mac_dock_expanded():
    expanded_height = 250
    dock_surface = pygame.Surface((WIDTH, expanded_height), pygame.SRCALPHA)
    dock_surface.fill((50, 50, 50, 220))
    screen.blit(dock_surface, (0, HEIGHT - expanded_height))
    
    # Show all apps in expanded dock
    for i, app in enumerate(mac_apps):
        row = i // 8
        col = i % 8
        icon_x = WIDTH//2 - 280 + col*70
        icon_y = HEIGHT - expanded_height + 20 + row*80
        
        # App icon
        screen.blit(pygame.transform.scale(icons[app["icon"]], (50, 50)), (icon_x+10, icon_y+10))
        
        # App name
        app_text = mac_small_font.render(app["name"], True, WHITE)
        screen.blit(app_text, (icon_x + 35 - app_text.get_width()//2, icon_y + 65))

# Help screen
def draw_help_screen():
    help_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    help_surface.fill((0, 0, 0, 220))
    
    title_text = title_font.render("OS Simulator v2.0 - Help", True, WHITE)
    help_surface.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
    
    # Help content with modern layout
    help_sections = [
        {
            "title": "CONTROLS",
            "items": [
                "ESC: Exit application or go back",
                "F1: Show/hide this help screen",
                "Mouse: Interact with OS elements",
                "Right-click: Context menu",
                "F11: Toggle fullscreen",
                "F2: Toggle language (English/Farsi)"
            ]
        },
        {
            "title": "WINDOWS 11",
            "items": [
                "Click Start button to open Start Menu",
                "Click desktop icons to open applications",
                "Use window controls to minimize/maximize/close",
                "Right-click for context menus",
                "Taskbar shows running applications"
            ]
        },
        {
            "title": "macOS",
            "items": [
                "Click dock icons to open applications",
                "Menu bar at top provides system options",
                "Use colored window buttons to manage windows",
                "Right-click for context menus",
                "Dock shows frequently used apps"
            ]
        },
        {
            "title": "APPLICATIONS",
            "items": [
                "Browser: Modern web browsing experience",
                "Settings: System configuration options",
                "Terminal: Command line interface",
                "Music: Audio player with modern UI",
                "Calculator: Scientific calculator",
                "Notes: Note-taking application",
                "Calendar: Monthly calendar view",
                "Store: App discovery and installation",
                "Game: Space adventure game",
                "Camera: Camera simulation",
                "Gallery: Image gallery",
                "Social Media: Facebook, Instagram, etc.",
                "Weather: Weather forecast",
                "Mail: Email client",
                "Maps: Interactive maps",
                "Files: File manager",
                "Video: Media player"
            ]
        }
    ]
    
    y_offset = 120
    for section in help_sections:
        # Section title
        section_title = medium_font.render(section["title"], True, LIGHT_BLUE)
        help_surface.blit(section_title, (WIDTH//2 - 350, y_offset))
        y_offset += 40
        
        # Section items
        for item in section["items"]:
            item_text = small_font.render(item, True, WHITE)
            help_surface.blit(item_text, (WIDTH//2 - 340, y_offset))
            y_offset += 25
        
        y_offset += 20
    
    # Footer
    footer_text = small_font.render("Press any key to close this help screen", True, WHITE)
    help_surface.blit(footer_text, (WIDTH//2 - footer_text.get_width()//2, HEIGHT - 50))
    
    screen.blit(help_surface, (0, 0))

# Power options screen
def draw_power_options():
    power_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    power_surface.fill((0, 0, 0, 220))
    
    title_text = title_font.render("Power Options", True, WHITE)
    power_surface.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
    
    options = [
        ("Shutdown", (255, 50, 50)),
        ("Restart", (50, 150, 255)),
        ("Sleep", (255, 200, 50)),
        ("Log Out", (150, 150, 150)),
        ("Cancel", (100, 100, 100))
    ]
    
    option_rects = []
    for i, (option, color) in enumerate(options):
        option_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + i*70, 200, 50)
        pygame.draw.rect(power_surface, color, option_rect, border_radius=10)
        
        option_text = medium_font.render(option, True, WHITE)
        power_surface.blit(option_text, (WIDTH//2 - option_text.get_width()//2, HEIGHT//2 + i*70 + 15))
        
        option_rects.append(option_rect)
    
    screen.blit(power_surface, (0, 0))
    return option_rects

# Loading screens
def draw_windows_loading(progress):
    screen.fill(BLACK)
    
    # Windows logo with modern design
    logo_size = 150
    logo_x = WIDTH//2 - logo_size//2
    logo_y = HEIGHT//2 - logo_size//2 - 50
    
    # Modern Windows logo
    pygame.draw.rect(screen, BLUE, (logo_x, logo_y, logo_size, logo_size), border_radius=20)
    
    # Logo segments
    segment_size = logo_size // 2 - 10
    pygame.draw.rect(screen, WHITE, (logo_x + 10, logo_y + 10, segment_size, segment_size), border_radius=8)
    pygame.draw.rect(screen, WHITE, (logo_x + logo_size - segment_size - 10, logo_y + 10, segment_size, segment_size), border_radius=8)
    pygame.draw.rect(screen, WHITE, (logo_x + 10, logo_y + logo_size - segment_size - 10, segment_size, segment_size), border_radius=8)
    pygame.draw.rect(screen, WHITE, (logo_x + logo_size - segment_size - 10, logo_y + logo_size - segment_size - 10, segment_size, segment_size), border_radius=8)
    
    # Loading text
    loading_text = medium_font.render("Loading Windows 11...", True, WHITE)
    screen.blit(loading_text, (WIDTH//2 - loading_text.get_width()//2, HEIGHT//2 + 50))
    
    # Modern loading bar
    bar_width = 400
    bar_height = 20
    bar_x = WIDTH//2 - bar_width//2
    bar_y = HEIGHT//2 + 100
    
    pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=10)
    pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width * progress / 100, bar_height), border_radius=10)
    
    # Percentage with modern design
    percent_text = medium_font.render(f"{int(progress)}%", True, WHITE)
    screen.blit(percent_text, (WIDTH//2 - percent_text.get_width()//2, bar_y + 25))

def draw_mac_loading(progress):
    screen.fill(BLACK)
    
    # Apple logo with modern design
    logo_size = 150
    logo_x = WIDTH//2 - logo_size//2
    logo_y = HEIGHT//2 - logo_size//2 - 50
    
    # Modern Apple logo
    pygame.draw.rect(screen, MAC_BLUE, (logo_x, logo_y, logo_size, logo_size), border_radius=75)
    
    # Logo details
    pygame.draw.rect(surface, (200, 200, 255), (logo_x + 30, logo_y + 30, logo_size - 60, logo_size - 60), border_radius=40)
    pygame.draw.rect(surface, (150, 150, 255), (logo_x + 50, logo_y + 50, logo_size - 100, logo_size - 100), border_radius=30)
    
    # Loading text
    loading_text = mac_medium_font.render("Loading macOS...", True, WHITE)
    screen.blit(loading_text, (WIDTH//2 - loading_text.get_width()//2, HEIGHT//2 + 50))
    
    # Modern progress indicator (spinning)
    center_x, center_y = WIDTH//2, HEIGHT//2 + 100
    radius = 40
    
    # Draw spinning circle with modern design
    for i in range(0, int(progress * 3.6), 10):
        rad_angle = math.radians(i)
        x = center_x + radius * math.cos(rad_angle)
        y = center_y + radius * math.sin(rad_angle)
        pygame.draw.circle(screen, MAC_BLUE, (int(x), int(y)), 8)
    
    # Inner circle
    pygame.draw.circle(screen, (50, 50, 100), (center_x, center_y), radius - 20)
    
    # Percentage
    percent_text = mac_medium_font.render(f"{int(progress)}%", True, WHITE)
    screen.blit(percent_text, (WIDTH//2 - percent_text.get_width()//2, center_y + 60))

# Main game loop
running = True
show_help = False
show_power_options = False
loading = False
loading_progress = 0
loading_os = None
power_option_rects = []

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if show_help:
                    show_help = False
                elif show_power_options:
                    show_power_options = False
                elif current_os == BOOT_SCREEN:
                    running = False
                else:
                    # Show power options or go back to boot screen
                    show_power_options = True
                    
            elif event.key == K_F1:
                show_help = not show_help
                
            elif event.key == K_F2:
                # Toggle language
                current_language = "farsi" if current_language == "english" else "english"
                
            elif event.key == K_F11:
                # Toggle fullscreen
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    
            elif event.key == K_1 and current_os == BOOT_SCREEN:
                loading = True
                loading_os = WINDOWS_11
                loading_progress = 0
                
            elif event.key == K_2 and current_os == BOOT_SCREEN:
                loading = True
                loading_os = MACOS
                loading_progress = 0
                
            elif event.key == K_3 and current_os == BOOT_SCREEN:
                show_help = True
                
            elif event.key == K_4 and current_os == BOOT_SCREEN:
                running = False
                
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if event.button == 3:  # Right click
                # Create context menu
                if current_os != BOOT_SCREEN:
                    options = ["New Folder", "Refresh", "Properties", "Personalize"]
                    context_menu = ContextMenu(mouse_x, mouse_y, options)
            
            if show_help:
                # Any click closes help
                show_help = False
                
            elif show_power_options:
                for i, rect in enumerate(power_option_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        if i == 0:  # Shutdown
                            running = False
                        elif i == 1:  # Restart
                            current_os = BOOT_SCREEN
                            active_windows = []
                            show_power_options = False
                        elif i == 2:  # Sleep
                            # Simulate sleep (just hide windows)
                            active_windows = []
                            show_power_options = False
                        elif i == 3:  # Log Out
                            current_os = BOOT_SCREEN
                            active_windows = []
                            show_power_options = False
                        elif i == 4:  # Cancel
                            show_power_options = False
                            
            elif context_menu and context_menu.visible:
                result = context_menu.handle_event(event)
                if result:
                    context_menu = None
                    
            elif current_os == BOOT_SCREEN:
                windows_rect, mac_rect, help_rect, power_rect = draw_boot_screen()
                if windows_rect.collidepoint(mouse_x, mouse_y):
                    loading = True
                    loading_os = WINDOWS_11
                    loading_progress = 0
                elif mac_rect.collidepoint(mouse_x, mouse_y):
                    loading = True
                    loading_os = MACOS
                    loading_progress = 0
                elif help_rect.collidepoint(mouse_x, mouse_y):
                    show_help = True
                elif power_rect.collidepoint(mouse_x, mouse_y):
                    running = False
                    
            elif current_os == WINDOWS_11:
                start_rect = draw_windows_desktop()
                if start_rect.collidepoint(mouse_x, mouse_y):
                    windows_start_open = not windows_start_open
                    
                # Check for desktop app icon clicks
                for i, app in enumerate(windows_apps[:12]):
                    icon_rect = pygame.Rect(50 + (i%4)*120, 100 + (i//4)*120, 80, 100)
                    if icon_rect.collidepoint(mouse_x, mouse_y):
                        new_window = Window(app["name"], 100 + (len(active_windows) * 30), 100 + (len(active_windows) * 30), 
                                          600, 500, app["func"])
                        active_windows.append(new_window)
                        
                # Check for taskbar app clicks
                for i, app in enumerate(windows_apps[:8]):
                    icon_rect = pygame.Rect(140 + i*50, HEIGHT - 50 + 5, 40, 40)
                    if icon_rect.collidepoint(mouse_x, mouse_y):
                        new_window = Window(app["name"], 100 + (len(active_windows) * 30), 100 + (len(active_windows) * 30), 
                                          600, 500, app["func"])
                        active_windows.append(new_window)
                        
                # Check for power option in start menu
                if windows_start_open:
                    power_rect = draw_windows_start_menu()
                    if power_rect.collidepoint(mouse_x, mouse_y):
                        show_power_options = True
                        windows_start_open = False
                        
            elif current_os == MACOS:
                # Check for dock app clicks
                for i, app in enumerate(mac_apps[:10]):
                    icon_size = 60
                    icon_x = WIDTH//2 - 250 + i*60
                    icon_y = HEIGHT - 80 + 10
                    
                    icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
                    if icon_rect.collidepoint(mouse_x, mouse_y):
                        new_window = Window(app["name"], 100 + (len(active_windows) * 30), 100 + (len(active_windows) * 30), 
                                          600, 500, app["func"])
                        active_windows.append(new_window)
                        
                # Check for desktop icon clicks
                for i, app in enumerate(mac_apps[:8]):
                    icon_rect = pygame.Rect(50 + i*120, 100, 80, 100)
                    if icon_rect.collidepoint(mouse_x, mouse_y):
                        new_window = Window(app["name"], 100 + (len(active_windows) * 30), 100 + (len(active_windows) * 30), 
                                          600, 500, app["func"])
                        active_windows.append(new_window)
                        
                # Check for Apple menu click
                apple_rect = pygame.Rect(10, 0, 30, 30)
                if apple_rect.collidepoint(mouse_x, mouse_y):
                    show_power_options = True
            
            # Handle window events
            for window in active_windows[:]:
                result = window.handle_event(event)
                if result == "close":
                    active_windows.remove(window)
    
    # Draw current screen
    if loading:
        if loading_os == WINDOWS_11:
            draw_windows_loading(loading_progress)
        else:
            draw_mac_loading(loading_progress)
        
        # Update loading progress
        loading_progress += 0.5
        if loading_progress >= 100:
            loading = False
            current_os = loading_os
            loading_os = None
            # Set background image
            if current_os == WINDOWS_11:
                background_image = backgrounds["windows"]
                background_color = BLUE
            else:
                background_image = backgrounds["mac"]
                background_color = MAC_BLUE
            
    elif show_help:
        draw_help_screen()
        
    elif show_power_options:
        power_option_rects = draw_power_options()
        
    elif current_os == BOOT_SCREEN:
        draw_boot_screen()
        
    elif current_os == WINDOWS_11:
        draw_windows_desktop()
        
        # Draw active windows
        for window in active_windows:
            window.draw(screen)
            
    elif current_os == MACOS:
        draw_mac_desktop()
        
        # Draw active windows
        for window in active_windows:
            window.draw(screen)
    
    # Draw context menu if active
    if context_menu and context_menu.visible:
        context_menu.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()