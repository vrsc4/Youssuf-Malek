import pygame
import numpy as np


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 9.81  
AIR_DENSITY = 1.225  


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class FreefallSimulator:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Freefall Physics Simulator")
        self.clock = pygame.time.Clock()
        
        
        self.reset_simulation()
        self.font = pygame.font.Font(None, 32)
        
    def reset_simulation(self):
        self.mass = 80.0  
        self.position = 0  
        self.velocity = 0
        self.time = 0
        self.acceleration = 0
        self.parachute_deployed = False
        self.drag_coefficient = 0.5  
        self.cross_section = 0.5  
        
    def calculate_forces(self):
        
        weight = self.mass * GRAVITY
        
        
        if self.parachute_deployed:
            self.drag_coefficient = 1.75
            self.cross_section = 40.0  
        else:
            self.drag_coefficient = 0.5  
            self.cross_section = 0.5  
        
        drag = 0.5 * AIR_DENSITY * self.drag_coefficient * self.cross_section * self.velocity**2
        
        return weight, drag
    
    def update_physics(self, dt):
        weight, drag = self.calculate_forces()
        
        
        net_force = weight - drag if self.velocity > 0 else weight
        
        
        self.velocity += (net_force / self.mass) * dt
        self.position += self.velocity * dt
        self.time += dt
        
        
        self.acceleration = net_force / self.mass
        
        
        if self.position >= SCREEN_HEIGHT * 0.8:  
            self.position = SCREEN_HEIGHT * 0.8
            self.velocity = 0
            self.acceleration = 0
    
    def draw(self):
        self.screen.fill(BLACK)
        
        
        weight, drag = self.calculate_forces()
        
        
        ground_y = int(SCREEN_HEIGHT * 0.8)
        pygame.draw.line(self.screen, GREEN, (0, ground_y), (SCREEN_WIDTH, ground_y), 2)
        
        
        jumper_y = int(self.position)
        if self.parachute_deployed:
            
            pygame.draw.arc(self.screen, WHITE, 
                          (SCREEN_WIDTH//2 - 40, jumper_y - 40, 80, 80),
                          0, np.pi, 3)
        
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH//2, jumper_y), 10)
        
        
        info_texts = [
            f"Height: {(ground_y - jumper_y)/10:.1f} m",
            f"Velocity: {self.velocity:.1f} m/s",
            f"Acceleration: {self.acceleration:.1f} m/s²",
            f"Time: {self.time:.1f} s",
            f"Mass: {self.mass:.1f} kg",
            f"Parachute: {'OPEN' if self.parachute_deployed else 'CLOSED'}"
        ]
        
        for i, text in enumerate(info_texts):
            surface = self.font.render(text, True, WHITE)
            self.screen.blit(surface, (10, 10 + i * 30))
        
        
        arrow_scale = 0.1
        arrow_head_size = 10
        
        
        start_pos = (SCREEN_WIDTH - 100, jumper_y)
        end_pos = (SCREEN_WIDTH - 100, jumper_y + weight * arrow_scale)
        pygame.draw.line(self.screen, RED, start_pos, end_pos, 3)
        
        if weight > 0:
            left_point = (end_pos[0] - arrow_head_size//2, end_pos[1] - arrow_head_size)
            right_point = (end_pos[0] + arrow_head_size//2, end_pos[1] - arrow_head_size)
            pygame.draw.polygon(self.screen, RED, [end_pos, left_point, right_point])
        
        
        if self.velocity > 0:
            start_pos = (SCREEN_WIDTH - 100, jumper_y)
            end_pos = (SCREEN_WIDTH - 100, jumper_y - drag * arrow_scale)
            pygame.draw.line(self.screen, BLUE, start_pos, end_pos, 3)
            
            if drag > 0:
                left_point = (end_pos[0] - arrow_head_size//2, end_pos[1] + arrow_head_size)
                right_point = (end_pos[0] + arrow_head_size//2, end_pos[1] + arrow_head_size)
                pygame.draw.polygon(self.screen, BLUE, [end_pos, left_point, right_point])
        
        
        weight_text = self.font.render(f"{weight:.0f}N", True, RED)
        self.screen.blit(weight_text, (SCREEN_WIDTH - 150, jumper_y + 10))
        
        if self.velocity > 0:
            drag_text = self.font.render(f"{drag:.0f}N", True, BLUE)
            self.screen.blit(drag_text, (SCREEN_WIDTH - 150, jumper_y - 30))
        
        pygame.display.flip()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.parachute_deployed = not self.parachute_deployed
                elif event.key == pygame.K_r:
                    self.reset_simulation()
                elif event.key == pygame.K_UP:
                    self.mass += 10
                elif event.key == pygame.K_DOWN:
                    self.mass = max(50, self.mass - 10)
        return True
    
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_input()
            self.update_physics(dt)
            self.draw()

if __name__ == "__main__":
    simulator = FreefallSimulator()
    simulator.run()
