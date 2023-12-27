import pygame
import math 

pygame.init()

wid, high =1280, 720
win = pygame.display.set_mode((wid, high))
pygame.display.set_caption("Planet Simulation")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
silver = (192, 192, 192)
violet = (238, 130, 238)
red = (255, 0, 0)
purple = (128, 0, 128)
red_gold = (255, 215, 0)
light_blue = (173, 216, 230)
deep_blue = (0, 0, 205)
ice_blue = (176, 224, 230)
# Font
font = pygame.font.SysFont('comicsans', 30, True)
# Planet class
class Planet:
    AU = 149.6e6 * 1000 # km to m
    G = 6.67408e-11 # m^3 kg^-1 s^-2
    scale =  50 / AU # 1 pixel = 250 km
    timestep = 24 * 3600 # 1 day in seconds
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.dist_from_sun = 0

        self.x_vel = 0
        self.y_vel = 0


    def draw(self, win):
        x = self.x * self.scale + wid / 2
        y = self.y * self.scale + high / 2
        if len(self.orbit)>2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.scale + wid / 2
                y = y * self.scale + high / 2
                updated_points.append((x,y))
            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if not self.sun:
            distance = font.render(f"{round(self.dist_from_sun/Planet.AU )}AU", 1, white)

            win.blit(distance, (x-distance.get_width()/2, y-distance.get_height()/2))
       
    def attraction(self, other):
        other_x = other.x 
        other_y = other.y 
        dist_x = other_x - self.x
        dist_y = other_y - self.y
        distance = math.sqrt(dist_x**2 + dist_y**2)
        if other.sun:
            self.dist_from_sun = distance
        force = self.G * self.mass * other.mass / (distance**2)
        theta = math.atan2(dist_y, dist_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    def update_pos(self,planets):
        total_force_x =  0
        total_force_y = 0
        for planet in planets:
            if planet == self:
                continue
            force_x, force_y = self.attraction(planet)
            total_force_x += force_x
            total_force_y += force_y
        self.x_vel += total_force_x / self.mass * self.timestep
        self.y_vel += total_force_y / self.mass * self.timestep

        self.x += self.x_vel * self.timestep
        self.y += self.y_vel * self.timestep

        self.orbit.append((self.x, self.y))

def zooming(zoom):
    # allow for zooming in and out
    pass

#event loop
def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 50, yellow , 1.989*10**30)
    sun.sun = True
    mercury = Planet(0.387 * Planet.AU, 0, 8, silver, 3.285*10**23)
    mercury.y_vel = -47362
    venus = Planet(0.723 * Planet.AU, 0, 14, violet, 4.867*10**24)
    venus.y_vel = -35.02 * 1000
    earth = Planet(-1 * Planet.AU, 0, 16, blue, 5.972*10**24)
    earth.y_vel = 29783
    mars = Planet(-1.524 * Planet.AU, 0, 12, red, 6.39*10**23)
    mars.y_vel = 24100

    jupiter = Planet(5.203 * Planet.AU, 0, 30,purple , 1.898*10**27)
    jupiter.y_vel = -13070
    saturn = Planet(9.537 * Planet.AU, 0, 28, red_gold, 5.683*10**26)
    saturn.y_vel = -9690
    uranus = Planet(19.191 * Planet.AU, 0, 24, light_blue, 8.681*10**25)
    uranus.y_vel = -6810
    neptune = Planet(30.069 * Planet.AU, 0, 22, deep_blue, 1.024*10**26)
    neptune.y_vel = -5430
    pluto = Planet(39.482 * Planet.AU, 0, 10, ice_blue, 1.309*10**22)
    pluto.y_vel = -4740


    planets = [sun, earth, mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto]
    while run:
        clock.tick(60)
        win.fill(black)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(win)
            pygame.display.update()

    pygame.quit()
       
main()