"""
3D viewport using OpenGL for rendering the tiger
"""
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QSurfaceFormat
from OpenGL.GL import *
from OpenGL.GLU import *
import math


class Viewport3D(QOpenGLWidget):
    """OpenGL widget for 3D rendering"""
    
    def __init__(self, game_manager):
        super().__init__()
        self.game_manager = game_manager
        
        # Camera settings
        self.camera_distance = 5.0
        self.camera_rotation_x = 30.0
        self.camera_rotation_y = 45.0
        
        # Mouse tracking
        self.last_mouse_pos = None
        self.setMouseTracking(True)
        
        # Tiger animation
        self.tiger_scale = 1.0
        self.tiger_scale_direction = 0.01
        self.tiger_rotation = 0.0
        self.tiger_color = [1.0, 0.6, 0.2]  # Orange tiger
        self.tiger_happy = False
        
        # Animation timer
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._animate)
        self.anim_timer.start(16)  # ~60 FPS
        
        # Setup OpenGL format
        fmt = QSurfaceFormat()
        fmt.setDepthBufferSize(24)
        fmt.setStencilBufferSize(8)
        fmt.setVersion(2, 1)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(fmt)
        
    def initializeGL(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Setup lighting
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        
        glClearColor(0.2, 0.3, 0.4, 1.0)  # Dark blue background
        
    def resizeGL(self, w, h):
        """Handle window resize"""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h if h != 0 else 1, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Setup camera
        cam_x = self.camera_distance * math.sin(math.radians(self.camera_rotation_y)) * math.cos(math.radians(self.camera_rotation_x))
        cam_y = self.camera_distance * math.sin(math.radians(self.camera_rotation_x))
        cam_z = self.camera_distance * math.cos(math.radians(self.camera_rotation_y)) * math.cos(math.radians(self.camera_rotation_x))
        
        gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)
        
        # Draw ground plane
        self._draw_ground()
        
        # Draw tiger (placeholder cube with stripes)
        self._draw_tiger()
        
    def _draw_ground(self):
        """Draw a simple ground plane"""
        glDisable(GL_LIGHTING)
        glBegin(GL_QUADS)
        glColor3f(0.3, 0.5, 0.3)  # Green ground
        glVertex3f(-5, -1, -5)
        glVertex3f(5, -1, -5)
        glVertex3f(5, -1, 5)
        glVertex3f(-5, -1, 5)
        glEnd()
        glEnable(GL_LIGHTING)
        
    def _draw_tiger(self):
        """Draw tiger placeholder (animated cube)"""
        glPushMatrix()
        
        # Apply rotation
        glRotatef(self.tiger_rotation, 0, 1, 0)
        
        # Apply breathing animation
        scale = self.tiger_scale
        glScalef(scale, scale, scale)
        
        # Set color based on mood
        glColor3fv(self.tiger_color)
        
        # Draw body (main cube)
        self._draw_cube(1.5, 1.0, 1.0)
        
        # Draw head
        glPushMatrix()
        glTranslatef(0.9, 0.2, 0)
        glColor3f(self.tiger_color[0], self.tiger_color[1], self.tiger_color[2])
        self._draw_cube(0.7, 0.7, 0.7)
        
        # Draw eyes
        glColor3f(0, 0, 0)
        glPushMatrix()
        glTranslatef(0.3, 0.15, 0.25)
        self._draw_sphere(0.08)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.3, 0.15, -0.25)
        self._draw_sphere(0.08)
        glPopMatrix()
        
        glPopMatrix()
        
        # Draw legs
        glColor3f(self.tiger_color[0] * 0.8, self.tiger_color[1] * 0.8, self.tiger_color[2] * 0.8)
        positions = [
            (0.5, -0.8, 0.4),
            (0.5, -0.8, -0.4),
            (-0.5, -0.8, 0.4),
            (-0.5, -0.8, -0.4)
        ]
        for pos in positions:
            glPushMatrix()
            glTranslatef(*pos)
            self._draw_cube(0.2, 0.4, 0.2)
            glPopMatrix()
        
        # Draw tail
        glPushMatrix()
        glTranslatef(-0.9, 0.2, 0)
        glRotatef(20 + math.sin(self.tiger_rotation * 0.1) * 10, 0, 0, 1)
        glColor3f(self.tiger_color[0], self.tiger_color[1], self.tiger_color[2])
        self._draw_cube(0.6, 0.15, 0.15)
        glPopMatrix()
        
        glPopMatrix()
        
    def _draw_cube(self, width, height, depth):
        """Draw a cube with given dimensions"""
        w, h, d = width / 2, height / 2, depth / 2
        
        glBegin(GL_QUADS)
        
        # Front
        glNormal3f(0, 0, 1)
        glVertex3f(-w, -h, d)
        glVertex3f(w, -h, d)
        glVertex3f(w, h, d)
        glVertex3f(-w, h, d)
        
        # Back
        glNormal3f(0, 0, -1)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(w, -h, -d)
        
        # Top
        glNormal3f(0, 1, 0)
        glVertex3f(-w, h, -d)
        glVertex3f(-w, h, d)
        glVertex3f(w, h, d)
        glVertex3f(w, h, -d)
        
        # Bottom
        glNormal3f(0, -1, 0)
        glVertex3f(-w, -h, -d)
        glVertex3f(w, -h, -d)
        glVertex3f(w, -h, d)
        glVertex3f(-w, -h, d)
        
        # Right
        glNormal3f(1, 0, 0)
        glVertex3f(w, -h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(w, h, d)
        glVertex3f(w, -h, d)
        
        # Left
        glNormal3f(-1, 0, 0)
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, -h, d)
        glVertex3f(-w, h, d)
        glVertex3f(-w, h, -d)
        
        glEnd()
        
    def _draw_sphere(self, radius):
        """Draw a simple sphere"""
        quadric = gluNewQuadric()
        gluSphere(quadric, radius, 16, 16)
        gluDeleteQuadric(quadric)
        
    def _animate(self):
        """Update animations"""
        # Breathing animation
        self.tiger_scale += self.tiger_scale_direction
        if self.tiger_scale > 1.05 or self.tiger_scale < 0.95:
            self.tiger_scale_direction *= -1
            
        # Rotation
        self.tiger_rotation += 0.5
        if self.tiger_rotation >= 360:
            self.tiger_rotation = 0
            
        self.update()
        
    def update_scene(self):
        """Update scene based on pet state"""
        pet = self.game_manager.pet
        
        # Change color based on mood
        if pet.mood < 30:
            self.tiger_color = [0.6, 0.6, 0.7]  # Gray when sad
        elif pet.hunger < 30:
            self.tiger_color = [0.8, 0.4, 0.2]  # Darker when hungry
        else:
            self.tiger_color = [1.0, 0.6, 0.2]  # Normal orange
            
    def mousePressEvent(self, event):
        """Handle mouse press for camera control"""
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            
    def mouseMoveEvent(self, event):
        """Handle mouse drag for camera rotation"""
        if self.last_mouse_pos is not None and event.buttons() & Qt.LeftButton:
            dx = event.pos().x() - self.last_mouse_pos.x()
            dy = event.pos().y() - self.last_mouse_pos.y()
            
            self.camera_rotation_y += dx * 0.5
            self.camera_rotation_x += dy * 0.5
            
            # Clamp vertical rotation
            self.camera_rotation_x = max(-89, min(89, self.camera_rotation_x))
            
            self.last_mouse_pos = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None
            
    def wheelEvent(self, event):
        """Handle mouse wheel for camera zoom"""
        delta = event.angleDelta().y()
        self.camera_distance -= delta * 0.01
        self.camera_distance = max(2.0, min(10.0, self.camera_distance))
        self.update()