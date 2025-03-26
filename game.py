import imgui
import numpy as np
import random
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from assets.objects.objects import playerProps, spaceProps, jungleProps, riverProps, CreateStone, CreateKeyIcon, CreatePlayer, CreateJungleEnemy, CreateSpaceEnemy, CreateRiverEnemy

def random_nonoverlapping_position(existing_objs, new_radius, i, number_of_stones=8, max_attempts=1000):
    """Try up to max_attempts to find a position that doesn't overlap existing stones."""

    screen_left = -450
    screen_right = 450
    total_width = screen_right - screen_left
    interval_width = (total_width - 200) / number_of_stones

    for _ in range(max_attempts):
        # Pick one of the intervals at random
        # i = random.randint(0, number_of_stones - 1)
        x_start = screen_left + i * (interval_width + 30)
        x_end = x_start + interval_width - 10

        # Sample a random x within that interval
        y = random.uniform(x_start, x_end)
        # Sample y normally
        x = random.uniform(-300, 300)
        center = np.array([x, y, 0], dtype=np.float32)

        overlap = False
        for obj in existing_objs:
            if obj.properties['name'] == 'stone':
                dist = np.linalg.norm(center - obj.properties['position'])
                # Check if circles overlap
                if dist < (new_radius + obj.properties['radius']) or abs(obj.properties['position'][0] - center[0]) < 2*new_radius:
                    overlap = True
                    break

        if not overlap:
            return center

    return None 

def random_enemy_position(existing_objs, new_radius, max_attempts=1000):
    """
    Picks a random position within a given range and checks for overlap 
    with existing objects that have a 'radius' property.
    """
    for _ in range(max_attempts):
        x = random.uniform(-350, 350)
        y = random.uniform(-250, 250)
        center = np.array([x, y, 0], dtype=np.float32)

        overlap = False
        for obj in existing_objs:
            if 'radius' in obj.properties:
                dist = np.linalg.norm(center - obj.properties['position'])
                if dist < (new_radius + obj.properties['radius']):
                    overlap = True
                    break

        if not overlap:
            return center

    return None 

class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = -1
        self.camera = Camera(height, width)
        self.shaders = [Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])]
        self.objects = []
        self.maps = [self.create_jungle_map(), self.create_river_map(), self.create_space_map()]
        self.current_map = 0
        # self.player = Object(self.shaders[0], playerProps)
        self.player_on_rock = None
        self.jump_charge_time = 0.0
        self.health = 100
        self.lives = 3
        self.total_time = 0.0
        self.is_game_over = False
        self.is_game_won = False

        # Store hold times for W, A, S, D in a dictionary
        self.keyHoldTimes = {
            'W': 0.0,
            'A': 0.0,
            'S': 0.0,
            'D': 0.0
        }

    def CreateDoorObject(self, name: str, position: np.ndarray, radius: float=40.0):
        """Creates a simple rectangular or circular 'door' object."""
        # If you have a custom function to create geometry, use it here
        # For simplicity, let's re-use a circle from CreateStone
        
        verts, inds = CreateStone(radius=radius, color=[0.7, 0.2, 0.2])
        return Object(self.shaders[0], {
            'name': name,
            'vertices': np.array(verts, dtype=np.float32),
            'indices': np.array(inds, dtype=np.uint32),
            'position': position,
            'rotation_z': 0.0,
            'scale': np.array([1, 1, 1], dtype=np.float32),
            'speed': 0.0,               # Doors are stationary
            'radius': radius,           # For distance checks
            'attached_to_player': False # Not used, but included for consistency
        })

    def create_space_map(self):
        space = Object(self.shaders[0], spaceProps)
        player = Object(self.shaders[0], playerProps)
        player.properties['position'] = np.array([-420, -450, 0], dtype=np.float32)
        objs =  [space, player]
        stone_objs = []

        # Add bottom-left entry "door"
        entry_door = self.CreateDoorObject('entry_door', np.array([-450, -450, 0], dtype=np.float32), radius=30)
        objs.append(entry_door)
        # Add top-right exit "door"
        exit_door = self.CreateDoorObject('exit_door', np.array([450, 450, 0], dtype=np.float32), radius=40)
        objs.append(exit_door)

        # Create the sun stone
        sun_verts, sun_inds = CreateStone(radius=30, color=[1.0, 1.0, 0.0])
        sun_obj = Object(self.shaders[0], {
            'name': 'stone',
            'vertices': np.array(sun_verts, dtype=np.float32),
            'indices': np.array(sun_inds, dtype=np.uint32),
            'position': np.array([0, 0, 0], dtype=np.float32),
            'rotation_z': 0.0,
            'scale': np.array([1, 1, 1], dtype=np.float32),
            'speed': 0.0,  # Sun stone is stationary
            'radius': 30,
            'is_sun': True,
            'direction': np.array([0.0, 0.0, 0.0], dtype=np.float32),
        })
        stone_objs.append(sun_obj)

        # Add random non-overlapping stones
        for i in range(6):
            r = 28
            angle = random.uniform(0, 2 * np.pi)
            distance_from_sun = (i + 1) * 62
            pos = np.array([distance_from_sun * np.cos(angle), distance_from_sun * np.sin(angle), 0], dtype=np.float32)
            # if pos is None:
            #     # If we can't find a valid spot, just skip or place at a default
            #     continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'name': 'stone',
                'vertices': np.array(stone_verts, dtype=np.float32),
                'indices': np.array(stone_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([1, 1, 1], dtype=np.float32),
                'speed': random.uniform(0.5, 1.5),
                'radius': r,
                'is_sun': False,
                'direction': np.array([0.0, 0.0, 0.0], dtype=np.float32),
                'orbit_center': sun_obj.properties['position'],
                'orbit_radius': distance_from_sun,
                'orbit_angle': angle
            })
            stone_objs.append(stone_obj)

        # Pick exactly three random stones to hold keys
        non_sun_stones = [s for s in stone_objs if not s.properties['is_sun']]
        if len(non_sun_stones) >= 3:
            chosen_stones = random.sample(non_sun_stones, 3)
            for s in chosen_stones:
                key_verts, key_inds = CreateKeyIcon(
                    radius=10,  # small radius for the key
                    color=[1.0, 1.0, 0.0]
                )
                key_obj = Object(self.shaders[0], {
                    'name': 'key',
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True,  # custom flag to indicate it's a key
                    'attached_to_player': False,
                    'direction': s.properties['direction'].copy(),
                    'owner_stone': s,
                    'orbit_center': sun_obj.properties['position'],
                    'orbit_radius': s.properties['orbit_radius'],
                    'orbit_angle': s.properties['orbit_angle']
                })
                stone_objs.append(key_obj)

        # Enemies: reuse "CreatePlayer" geometry, then define each as an enemy
        enemy_objs = []
        for i in range(3):
            enemy_verts, enemy_inds = CreateSpaceEnemy()
            enemy_radius = 25
            pos = random_enemy_position(enemy_objs, enemy_radius)
            if pos is None:
                continue
            enemy_obj = Object(self.shaders[0], {
                'name': 'enemy',
                'vertices': np.array(enemy_verts, dtype=np.float32),
                'indices': np.array(enemy_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([30, 30, 1], dtype=np.float32),  # Similar to player
                'speed': random.uniform(40, 90),  # Random speed
                'radius': enemy_radius,
                # direction: random normalized direction
                'direction': np.array([
                    random.uniform(-1.0, 1.0),
                    random.uniform(-1.0, 1.0),
                    0.0
                ], dtype=np.float32),
            })
            enemy_objs.append(enemy_obj)

        objs.extend(stone_objs)
        objs.extend(enemy_objs)

        return objs

    def create_jungle_map(self):
        jungle = Object(self.shaders[0], jungleProps)
        player = Object(self.shaders[0], playerProps)
        player.properties['position'] = np.array([-420, -450, 0], dtype=np.float32)
        objs =  [jungle, player]
        stone_objs = []

        # Add bottom-left entry "door"
        entry_door = self.CreateDoorObject('entry_door', np.array([-450, -450, 0], dtype=np.float32), radius=30)
        objs.append(entry_door)
        # Add top-right exit "door"
        exit_door = self.CreateDoorObject('exit_door', np.array([450, 450, 0], dtype=np.float32), radius=40)
        objs.append(exit_door)

        # Add random non-overlapping stones
        for i in range(8):
            r = 40
            pos = random_nonoverlapping_position(objs, r, i)
            if pos is None:
                # If we can't find a valid spot, just skip or place at a default
                continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'name': 'stone',
                'vertices': np.array(stone_verts, dtype=np.float32),
                'indices': np.array(stone_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([1, 1, 1], dtype=np.float32),
                'speed': random.uniform(50, 120),
                'radius': r,
                'direction': np.array([
                    random.uniform(-1.0, 1.0),
                    random.uniform(-1.0, 1.0),
                    0.0
                ], dtype=np.float32),
                'carries_key': False,
                'key_obj': None
            })
            stone_objs.append(stone_obj)

        # Pick exactly three random stones to hold keys
        if len(stone_objs) >= 3:
            chosen_stones = random.sample(stone_objs, 3)
            for s in chosen_stones:
                key_verts, key_inds = CreateKeyIcon(
                    radius=10,  # small radius for the key
                    color=[1.0, 1.0, 0.0]
                )
                key_obj = Object(self.shaders[0], {
                    'name': 'key',
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True,  # custom flag to indicate it's a key
                    'attached_to_player': False,
                    'direction': s.properties['direction'].copy(),
                    'owner_stone': s
                })
                s.properties['carries_key'] = True
                s.properties['key_obj'] = key_obj
                stone_objs.append(key_obj)

        # Enemies: reuse "CreatePlayer" geometry, then define each as an enemy
        enemy_objs = []
        for i in range(3):
            enemy_verts, enemy_inds = CreateJungleEnemy()
            enemy_radius = 25
            pos = random_enemy_position(enemy_objs, enemy_radius)
            if pos is None:
                continue
            enemy_obj = Object(self.shaders[0], {
                'name': 'enemy',
                'vertices': np.array(enemy_verts, dtype=np.float32),
                'indices': np.array(enemy_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([30, 30, 1], dtype=np.float32),  # Similar to player
                'speed': random.uniform(40, 90),  # Random speed
                'radius': enemy_radius,
                # direction: random normalized direction
                'direction': np.array([
                    random.uniform(-1.0, 1.0),
                    random.uniform(-1.0, 1.0),
                    0.0
                ], dtype=np.float32),
            })
            enemy_objs.append(enemy_obj)

        objs.extend(stone_objs)
        objs.extend(enemy_objs)

        return objs

    def create_river_map(self):
        river = Object(self.shaders[0], riverProps)
        player = Object(self.shaders[0], playerProps)
        player.properties['position'] = np.array([-420, -450, 0], dtype=np.float32)
        objs =  [river, player]
        stone_objs = []

        # Add bottom-left entry "door"
        entry_door = self.CreateDoorObject('entry_door', np.array([-450, -450, 0], dtype=np.float32), radius=30)
        objs.append(entry_door)
        # Add top-right exit "door"
        exit_door = self.CreateDoorObject('exit_door', np.array([450, 450, 0], dtype=np.float32), radius=40)
        objs.append(exit_door)

        # Add random non-overlapping stones
        for i in range(8):
            r = 40
            pos = random_nonoverlapping_position(objs, r, i)
            if pos is None:
                # If we can't find a valid spot, just skip or place at a default
                continue

            stone_verts, stone_inds = CreateStone(radius=r, color=[0.7, 0.7, 0.7])
            stone_obj = Object(self.shaders[0], {
                'name': 'stone',
                'vertices': np.array(stone_verts, dtype=np.float32),
                'indices': np.array(stone_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([1, 1, 1], dtype=np.float32),
                'speed': random.uniform(50, 120),
                'radius': r
            })
            stone_objs.append(stone_obj)

        # Pick exactly three random stones to hold keys
        if len(stone_objs) >= 3:
            chosen_stones = random.sample(stone_objs, 3)
            for s in chosen_stones:
                key_verts, key_inds = CreateKeyIcon(
                    radius=10,  # small radius for the key
                    color=[1.0, 1.0, 0.0]
                )
                key_obj = Object(self.shaders[0], {
                    'name': 'key',
                    'vertices': np.array(key_verts, dtype=np.float32),
                    'indices': np.array(key_inds, dtype=np.uint32),
                    'position': s.properties['position'].copy() + np.array([0, 0, 1], dtype=np.float32),
                    'rotation_z': 0.0,
                    'scale': np.array([1, 1, 1], dtype=np.float32),
                    'speed': s.properties['speed'],
                    'has_key': True, # custom flag to indicate it's a key
                    'attached_to_player': False
                })
                stone_objs.append(key_obj)

        # Enemies: reuse "CreatePlayer" geometry, then define each as an enemy
        enemy_objs = []
        for i in range(3):
            enemy_verts, enemy_inds = CreateRiverEnemy()
            enemy_radius = 25
            pos = random_enemy_position(enemy_objs, enemy_radius)
            if pos is None:
                continue
            enemy_obj = Object(self.shaders[0], {
                'name': 'enemy',
                'vertices': np.array(enemy_verts, dtype=np.float32),
                'indices': np.array(enemy_inds, dtype=np.uint32),
                'position': pos,
                'rotation_z': 0.0,
                'scale': np.array([30, 30, 1], dtype=np.float32),  # Similar to player
                'speed': random.uniform(40, 90),  # Random speed
                'radius': enemy_radius,
                # direction: random normalized direction
                'direction': np.array([
                    random.uniform(-1.0, 1.0),
                    random.uniform(-1.0, 1.0),
                    0.0
                ], dtype=np.float32),
            })
            enemy_objs.append(enemy_obj)

        objs.extend(stone_objs)
        objs.extend(enemy_objs)

        return objs

    def InitScreen(self):
        # self.objects = self.maps[self.current_map]
        
        if self.screen == 0:
            self.current_map = 0
            self.objects = self.maps[0]
        if self.screen == 1:
            self.current_map = 1
            self.objects = self.maps[1]
        if self.screen == 2:
            self.current_map = 2
            self.objects = self.maps[2]

    def ProcessFrame(self, inputs, time):
        if self.screen == -1:
            self.screen = 0
            self.InitScreen()

        # Update hold times for WASD
        delta = time['deltaTime']
        for key in ['W', 'A', 'S', 'D']:
            if key in inputs:  # key is pressed
                self.keyHoldTimes[key] += delta
            else:
                self.keyHoldTimes[key] = 0.0

        self.total_time += delta

        if self.screen == 0:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
            # self.show_switch_map_button()
        if self.screen == 1:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
            # self.show_switch_map_button()
        if self.screen == 2:
            self.DrawText()
            self.UpdateScene(inputs, time)
            self.DrawScene()
            # self.show_switch_map_button()

    def DrawText(self):
        if self.screen == 0:
           pass
        if self.screen == 1:
           pass
        if self.screen == 2:
           pass

    def DrawHUD(self):
        # Position and size the HUD at the very top
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(self.width, 30)  # 30 px in height, adjust as needed

        # Begin a new ImGui window for the HUD
        imgui.begin("HUD", True,
                    flags=imgui.WINDOW_NO_TITLE_BAR | 
                          imgui.WINDOW_NO_RESIZE |
                          imgui.WINDOW_NO_MOVE |
                          imgui.WINDOW_NO_SCROLLBAR |
                          imgui.WINDOW_NO_SAVED_SETTINGS)

        # Health ratio for the bar
        health_ratio = max(0.0, min(1.0, self.health / 100.0))
        # Color transitions from red (low health) to green (full health)
        bar_color = (1.0 - health_ratio, health_ratio, 0.0, 1.0)


        imgui.same_line()
        imgui.text_unformatted(f"Time: {int(self.total_time)}s")

        # Draw heart icons for lives (using text hearts, but you could use textures if desired)

        imgui.same_line()
        imgui.text_unformatted(f"      Map: {self.screen + 1}")
        imgui.same_line()
        hearts_str = f"                 Lives: {self.lives}"
        imgui.text_unformatted(hearts_str)

        imgui.same_line()
        # Draw health bar
        imgui.text_unformatted("                Health: ")
        imgui.same_line()
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, *bar_color)
        imgui.progress_bar(health_ratio, size=(self.width * 0.3, 0), overlay="")
        imgui.pop_style_color()

        imgui.end()

    def UpdateScene(self, inputs, time):

        # If lives drop to zero, mark game over
        if self.lives <= 0:
            self.is_game_over = True
            return
                
        delta = time['deltaTime']
        player_speed = 100.0 

        # Check if health reached zero
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.health = 100
                # Respawn at the bottom-left "entry_door"
                spawn_door = next((o for o in self.objects if o.properties['name'] == 'entry_door'), None)
                if spawn_door:
                    player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
                    if player_obj:
                        player_obj.properties['position'] = spawn_door.properties['position'].copy()
            else:
                self.is_game_over = True
                return

        # Check for collisions between player and enemies
        player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
        if player_obj:
            for obj in self.objects:
                if obj.properties['name'] == 'enemy':
                    dist = np.linalg.norm(player_obj.properties['position'] - obj.properties['position'])
                    if dist < (player_obj.properties['radius'] + obj.properties['radius']):
                        self.health -= 10 * delta  # Reduce health over time when in contact

        # for obj in self.objects:
        #     # Assuming 'player' can be identified by a property check or simply check if it has 'velocity'
        #     if obj is not None and obj.properties['name'] == 'player':
        #         if 'W' in inputs:
        #             obj.properties['position'][1] += player_speed * delta
        #         if 'S' in inputs:
        #             obj.properties['position'][1] -= player_speed * delta
        #         if 'A' in inputs:
        #             obj.properties['position'][0] -= player_speed * delta
        #         if 'D' in inputs:
        #             obj.properties['position'][0] += player_speed * delta

        #         # Clamp the player's position to avoid going out of screen bounds
        #         x, y, z = obj.properties['position']
        #         x = max(-470.0, min(470.0, x))
        #         y = max(-450.0, min(440.0, y))
        #         obj.properties['position'] = np.array([x, y, z], dtype=np.float32)

        if self.screen == 0:

            player_speed = 100.0
            for obj in self.objects:
                # Assuming 'player' can be identified by a property check or simply check if it has 'velocity'
                if obj is not None and obj.properties['name'] == 'player':
                    if 'W' in inputs:
                        obj.properties['position'][1] += player_speed * delta
                    if 'S' in inputs:
                        obj.properties['position'][1] -= player_speed * delta
                    if 'A' in inputs:
                        obj.properties['position'][0] -= player_speed * delta
                    if 'D' in inputs:
                        obj.properties['position'][0] += player_speed * delta

                    # Clamp the player's position to avoid going out of screen bounds
                    x, y, z = obj.properties['position']
                    x = max(-470.0, min(470.0, x))
                    y = max(-450.0, min(440.0, y))
                    obj.properties['position'] = np.array([x, y, z], dtype=np.float32)

            # Move enemies randomly
            for obj in self.objects:
                if obj.properties['name'] == 'enemy':
                    delta = time['deltaTime']
                    # Move in the stored direction at 'speed'
                    direction = obj.properties['direction']
                    speed = obj.properties['speed']
                    obj.properties['position'] += direction * speed * delta

                    # If near some boundary, flip direction or randomize again
                    x, y, z = obj.properties['position']
                    if abs(y) > 460 or abs(x) > 360: 
                        obj.properties['direction'] = np.array([
                            random.uniform(-1.0, 1.0),
                            random.uniform(-1.0, 1.0),
                            0.0
                        ], dtype=np.float32)

            # Move stones randomly
            for obj in self.objects:
                delta = time['deltaTime']
                if obj.properties['name'] == 'stone':
                    direction = obj.properties['direction']
                    speed = obj.properties['speed']
                    obj.properties['position'] += direction * speed * delta

                    # If near some boundary, flip direction or randomize again
                    x, y, z = obj.properties['position']
                    if abs(y) > 460 or abs(x) > 360:
                        if obj.properties['carries_key']:
                            obj.properties['direction'] = np.array([
                                random.uniform(-1.0, 1.0),
                                random.uniform(-1.0, 1.0),
                                0.0
                            ], dtype=np.float32)
                            obj.properties['key_obj'].properties['direction'] = obj.properties['direction'].copy()
                        else:
                            obj.properties['direction'] = np.array([
                                random.uniform(-1.0, 1.0),
                                random.uniform(-1.0, 1.0),
                                0.0
                            ], dtype=np.float32)

                # If the object is a key, update its position to follow the owner stone
                if obj.properties['name'] == 'key':
                    obj.properties['position'] += obj.properties['direction'] * obj.properties['speed'] * delta

            jump_key = 'SPACE'  
            min_jump = 50.0
            max_jump = 300.0

            self.player_on_rock = None
            player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
            if player_obj:
                for rock in (o for o in self.objects if o.properties['name'] == 'stone'):
                    dist = np.linalg.norm(player_obj.properties['position'] - rock.properties['position'])
                    if dist < rock.properties['radius']:
                        self.player_on_rock = rock
                        break

            # If on rock, move player along with rock
            if self.player_on_rock is not None and player_obj:
                # The rock moves downward => replicate the same shift
                rock = self.player_on_rock
                player_obj.properties['position'] = rock.properties['position'].copy()
                
                # Check if there's a key on this same rock
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    dist_key_rock = np.linalg.norm(key_obj.properties['position'] - rock.properties['position'])
                    if dist_key_rock < rock.properties['radius']:
                        # Attach key to player
                        key_obj.properties['attached_to_player'] = True

            # If a key is attached to the player, sync its position
            if player_obj:
                x_pos = -40
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    if key_obj.properties.get('attached_to_player'):
                        x_pos += 20
                        key_obj.properties['position'] = player_obj.properties['position'] + np.array([x_pos, 7, 2], dtype=np.float32)

            # Accumulate jump charge if jump key is pressed
            if jump_key in inputs:
                self.jump_charge_time += delta
                self.jump_charge_time = min(self.jump_charge_time, 7.0)  # clamp max charge time
            # On jump key release, perform jump
            else:
                if self.jump_charge_time > 0.0:
                    # print(f"Jumping with charge time: {self.jump_charge_time}")
                    distance_factor = self.jump_charge_time * 200.0
                    jump_dist = max(min_jump, min(max_jump, distance_factor))
                    # Use last movement direction or a chosen direction
                    dx = 0.0
                    dy = 0.0
                    # if 'W' in inputs: dy += 1.0
                    # if 'S' in inputs: dy -= 1.0
                    # if 'A' in inputs: dx -= 1.0
                    # if 'D' in inputs: dx += 1.0
                    
                    # Use hold times to define direction
                    dy += self.keyHoldTimes['W']
                    dy -= self.keyHoldTimes['S']
                    dx += self.keyHoldTimes['D']
                    dx -= self.keyHoldTimes['A']
                    # Normalize direction
                    length = (dx**2 + dy**2)**0.5
                    # print(f"Jump direction: {dx}, {dy}")
                    if length > 0.0:
                        dx /= length
                        dy /= length
                    # Apply jump
                    # print(f"Jumping with distance: {jump_dist}")
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')
                    if player_obj:
                        player_obj.properties['position'][0] += dx * jump_dist
                        player_obj.properties['position'][1] += dy * jump_dist
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')

                self.jump_charge_time = 0.0

            # Door logic: if player is near exit_door and has 3 keys, move keys into door slots and switch map
            if player_obj:
                exit_door_obj = next((o for o in self.objects if o.properties['name'] == 'exit_door'), None)
                if exit_door_obj:
                    dist_door = np.linalg.norm(player_obj.properties['position'] - exit_door_obj.properties['position'])
                    if dist_door < exit_door_obj.properties['radius']:
                        # Count attached keys
                        attached_keys = [k for k in self.objects if k.properties.get('attached_to_player')]
                        if len(attached_keys) >= 3:
                            # Position the keys in the door's “slots”
                            slot_offset = -10
                            for k in attached_keys[:3]:
                                slot_offset += 10
                                k.properties['position'] = exit_door_obj.properties['position'] + np.array([slot_offset, 0, 5], dtype=np.float32)
                                k.properties['attached_to_player'] = False
                            # Switch map
                            self.switch_map()

        if self.screen == 1:

            player_speed = 100.0
            for obj in self.objects:
                # Assuming 'player' can be identified by a property check or simply check if it has 'velocity'
                if obj is not None and obj.properties['name'] == 'player':
                    if 'W' in inputs:
                        obj.properties['position'][1] += player_speed * delta
                    if 'S' in inputs:
                        obj.properties['position'][1] -= player_speed * delta
                    if 'A' in inputs:
                        obj.properties['position'][0] -= player_speed * delta
                    if 'D' in inputs:
                        obj.properties['position'][0] += player_speed * delta

                    # Clamp the player's position to avoid going out of screen bounds
                    x, y, z = obj.properties['position']
                    x = max(-470.0, min(470.0, x))
                    y = max(-450.0, min(440.0, y))
                    obj.properties['position'] = np.array([x, y, z], dtype=np.float32)

            # Move enemies randomly
            for obj in self.objects:
                if obj.properties['name'] == 'enemy':
                    delta = time['deltaTime']
                    # Move in the stored direction at 'speed'
                    direction = obj.properties['direction']
                    speed = obj.properties['speed']
                    obj.properties['position'] += direction * speed * delta

                    # If near some boundary, flip direction or randomize again
                    x, y, z = obj.properties['position']
                    if abs(x) > 330 or abs(y) > 400: 
                        obj.properties['direction'] = np.array([
                            random.uniform(-1.0, 1.0),
                            random.uniform(-1.0, 1.0),
                            0.0
                        ], dtype=np.float32)

        # Move stones top to bottom and vice versa
            for obj in self.objects:
                if obj.properties['name'] == 'stone' or obj.properties['name'] == 'key':
                    # Move from top to bottom (or vice versa)
                    # print(time)
                    obj.properties['position'][0] -= obj.properties['speed'] * time['deltaTime']
                    # Reset if out of bounds
                    if obj.properties['position'][0] < -300 or obj.properties['position'][0] > 300:
                        obj.properties['speed'] = -1 * obj.properties['speed']

            jump_key = 'SPACE'  
            min_jump = 50.0
            max_jump = 300.0

            self.player_on_rock = None
            player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
            if player_obj:
                for rock in (o for o in self.objects if o.properties['name'] == 'stone'):
                    dist = np.linalg.norm(player_obj.properties['position'] - rock.properties['position'])
                    if dist < rock.properties['radius']:
                        self.player_on_rock = rock
                        break

            if self.player_on_rock is None and player_obj is not None:
                x, y, _ = player_obj.properties['position']
                if -400 < x < 400 and -500 < y < 500:
                    self.health -= 20 * delta

            # If on rock, move player along with rock
            if self.player_on_rock is not None and player_obj:
                # The rock moves downward => replicate the same shift
                rock = self.player_on_rock
                player_obj.properties['position'][0] -= rock.properties['speed'] * delta
                
                # Check if there's a key on this same rock
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    dist_key_rock = np.linalg.norm(key_obj.properties['position'] - rock.properties['position'])
                    if dist_key_rock < rock.properties['radius']:
                        # Attach key to player
                        key_obj.properties['attached_to_player'] = True

            # If a key is attached to the player, sync its position
            if player_obj:
                x_pos = -40
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    if key_obj.properties.get('attached_to_player'):
                        x_pos += 20
                        key_obj.properties['position'] = player_obj.properties['position'] + np.array([x_pos, 7, 2], dtype=np.float32)

            # Accumulate jump charge if jump key is pressed
            if jump_key in inputs:
                self.jump_charge_time += delta
                self.jump_charge_time = min(self.jump_charge_time, 7.0)  # clamp max charge time
            # On jump key release, perform jump
            else:
                if self.jump_charge_time > 0.0:
                    # print(f"Jumping with charge time: {self.jump_charge_time}")
                    distance_factor = self.jump_charge_time * 200.0
                    jump_dist = max(min_jump, min(max_jump, distance_factor))
                    # Use last movement direction or a chosen direction
                    dx = 0.0
                    dy = 0.0
                    # if 'W' in inputs: dy += 1.0
                    # if 'S' in inputs: dy -= 1.0
                    # if 'A' in inputs: dx -= 1.0
                    # if 'D' in inputs: dx += 1.0
                    
                    # Use hold times to define direction
                    dy += self.keyHoldTimes['W']
                    dy -= self.keyHoldTimes['S']
                    dx += self.keyHoldTimes['D']
                    dx -= self.keyHoldTimes['A']
                    # Normalize direction
                    length = (dx**2 + dy**2)**0.5
                    # print(f"Jump direction: {dx}, {dy}")
                    if length > 0.0:
                        dx /= length
                        dy /= length
                    # Apply jump
                    # print(f"Jumping with distance: {jump_dist}")
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')
                    if player_obj:
                        player_obj.properties['position'][0] += dx * jump_dist
                        player_obj.properties['position'][1] += dy * jump_dist
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')

                self.jump_charge_time = 0.0

            # Door logic: if player is near exit_door and has 3 keys, move keys into door slots and switch map
            if player_obj:
                exit_door_obj = next((o for o in self.objects if o.properties['name'] == 'exit_door'), None)
                if exit_door_obj:
                    dist_door = np.linalg.norm(player_obj.properties['position'] - exit_door_obj.properties['position'])
                    if dist_door < exit_door_obj.properties['radius']:
                        # Count attached keys
                        attached_keys = [k for k in self.objects if k.properties.get('attached_to_player')]
                        if len(attached_keys) >= 3:
                            # Position the keys in the door's “slots”
                            slot_offset = -10
                            for k in attached_keys[:3]:
                                slot_offset += 10
                                k.properties['position'] = exit_door_obj.properties['position'] + np.array([slot_offset, 0, 5], dtype=np.float32)
                                k.properties['attached_to_player'] = False
                            # Switch map
                            self.switch_map()

        if self.screen == 2:

            player_speed = 40.0
            for obj in self.objects:
                # Assuming 'player' can be identified by a property check or simply check if it has 'velocity'
                if obj is not None and obj.properties['name'] == 'player':
                    if 'W' in inputs:
                        obj.properties['position'][1] += player_speed * delta
                    if 'S' in inputs:
                        obj.properties['position'][1] -= player_speed * delta
                    if 'A' in inputs:
                        obj.properties['position'][0] -= player_speed * delta
                    if 'D' in inputs:
                        obj.properties['position'][0] += player_speed * delta

                    # Clamp the player's position to avoid going out of screen bounds
                    x, y, z = obj.properties['position']
                    x = max(-470.0, min(470.0, x))
                    y = max(-450.0, min(440.0, y))
                    obj.properties['position'] = np.array([x, y, z], dtype=np.float32)

            # Move enemies randomly
            for obj in self.objects:
                if obj.properties['name'] == 'enemy':
                    delta = time['deltaTime']
                    # Move in the stored direction at 'speed'
                    direction = obj.properties['direction']
                    speed = obj.properties['speed']
                    obj.properties['position'] += direction * speed * delta

                    # If near some boundary, flip direction or randomize again
                    x, y, z = obj.properties['position']
                    if abs(y) > 460 or abs(x) > 360: 
                        obj.properties['direction'] = np.array([
                            random.uniform(-1.0, 1.0),
                            random.uniform(-1.0, 1.0),
                            0.0
                        ], dtype=np.float32)

            # Move stones in a circular orbit around the sun stone
            for obj in self.objects:
                delta = time['deltaTime']
                if obj.properties['name'] == 'stone' and not obj.properties['is_sun']:
                    obj.properties['orbit_angle'] += obj.properties['speed'] * delta
                    obj.properties['position'][0] = obj.properties['orbit_center'][0] + obj.properties['orbit_radius'] * np.cos(obj.properties['orbit_angle'])
                    obj.properties['position'][1] = obj.properties['orbit_center'][1] + obj.properties['orbit_radius'] * np.sin(obj.properties['orbit_angle'])

                # If the object is a key, update its position to follow the owner stone
                if obj.properties['name'] == 'key':
                    obj.properties['orbit_angle'] += obj.properties['speed'] * delta
                    obj.properties['position'][0] = obj.properties['orbit_center'][0] + obj.properties['orbit_radius'] * np.cos(obj.properties['orbit_angle'])
                    obj.properties['position'][1] = obj.properties['orbit_center'][1] + obj.properties['orbit_radius'] * np.sin(obj.properties['orbit_angle'])                   

            jump_key = 'SPACE'  
            min_jump = 50.0
            max_jump = 200.0

            self.player_on_rock = None
            player_obj = next((o for o in self.objects if o.properties['name'] == 'player'), None)
            if player_obj:
                for rock in (o for o in self.objects if o.properties['name'] == 'stone'):
                    dist = np.linalg.norm(player_obj.properties['position'] - rock.properties['position'])
                    if dist < rock.properties['radius'] and not rock.properties['is_sun']:
                        self.player_on_rock = rock
                        break
            
            if self.player_on_rock is None and player_obj is not None:
                x, y, _ = player_obj.properties['position']
                if -500 < y < 500 and -400 < x < 400:
                    self.health -= 5 * delta  # Reduce health over time when not on a stone

            if player_obj is not None:
                # Check if player is inside the sun stone
                for obj_stone in [o for o in self.objects if o.properties['name'] == 'stone']:
                    if obj_stone.properties['is_sun']:
                        stone_pos = obj_stone.properties['position']
                        stone_radius = obj_stone.properties['radius']
                        player_pos = player_obj.properties['position']
                        distance = np.linalg.norm(player_pos - stone_pos)
                        if distance < stone_radius:
                            self.health = 0  # Player loses all health if inside the sun stone

            # If on rock, move player along with rock
            if self.player_on_rock is not None and player_obj:
                rock = self.player_on_rock
                player_obj.properties['position'] = rock.properties['position']
                
                # Check if there's a key on this same rock
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    dist_key_rock = np.linalg.norm(key_obj.properties['position'] - rock.properties['position'])
                    if dist_key_rock < rock.properties['radius']:
                        # Attach key to player
                        key_obj.properties['attached_to_player'] = True

            # If a key is attached to the player, sync its position
            if player_obj:
                x_pos = -40
                for key_obj in (o for o in self.objects if o.properties['name'] == 'key'):
                    if key_obj.properties.get('attached_to_player'):
                        x_pos += 20
                        key_obj.properties['position'] = player_obj.properties['position'] + np.array([x_pos, 7, 2], dtype=np.float32)

            # Accumulate jump charge if jump key is pressed
            if jump_key in inputs:
                self.jump_charge_time += delta
                self.jump_charge_time = min(self.jump_charge_time, 7.0)  # clamp max charge time
            # On jump key release, perform jump
            else:
                if self.jump_charge_time > 0.0:
                    # print(f"Jumping with charge time: {self.jump_charge_time}")
                    distance_factor = self.jump_charge_time * 200.0
                    jump_dist = max(min_jump, min(max_jump, distance_factor))
                    # Use last movement direction or a chosen direction
                    dx = 0.0
                    dy = 0.0
                    # if 'W' in inputs: dy += 1.0
                    # if 'S' in inputs: dy -= 1.0
                    # if 'A' in inputs: dx -= 1.0
                    # if 'D' in inputs: dx += 1.0
                    
                    # Use hold times to define direction
                    dy += self.keyHoldTimes['W']
                    dy -= self.keyHoldTimes['S']
                    dx += self.keyHoldTimes['D']
                    dx -= self.keyHoldTimes['A']
                    # Normalize direction
                    length = (dx**2 + dy**2)**0.5
                    # print(f"Jump direction: {dx}, {dy}")
                    if length > 0.0:
                        dx /= length
                        dy /= length
                    # Apply jump
                    # print(f"Jumping with distance: {jump_dist}")
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')
                    if player_obj:
                        player_obj.properties['position'][0] += dx * jump_dist
                        player_obj.properties['position'][1] += dy * jump_dist
                    # print(f'self.player.properties["position"]: {player_obj.properties["position"]}')

                self.jump_charge_time = 0.0

            # Door logic: if player is near exit_door and has 3 keys, move keys into door slots and switch map
            if player_obj:
                exit_door_obj = next((o for o in self.objects if o.properties['name'] == 'exit_door'), None)
                if exit_door_obj:
                    dist_door = np.linalg.norm(player_obj.properties['position'] - exit_door_obj.properties['position'])
                    if dist_door < exit_door_obj.properties['radius']:
                        # Count attached keys
                        attached_keys = [k for k in self.objects if k.properties.get('attached_to_player')]
                        if len(attached_keys) >= 3:
                            # Position the keys in the door's “slots”
                            slot_offset = -10
                            for k in attached_keys[:3]:
                                slot_offset += 10
                                k.properties['position'] = exit_door_obj.properties['position'] + np.array([slot_offset, 0, 5], dtype=np.float32)
                                k.properties['attached_to_player'] = False
                            # Switch map
                            self.switch_map()

            
    def DrawScene(self):
        if self.screen in (0, 1, 2):
            for shader in self.shaders:
                self.camera.Update(shader)
 
            for obj in self.objects:
                obj.Draw()

            self.DrawHUD()
            
    def switch_map(self):
        self.current_map += 1
        self.screen += 1
        if self.current_map >= len(self.maps) or self.screen >= len(self.maps):
            # self.current_map = 0  # Loop back to the first map or handle game completion
            # self.screen = 0
            self.is_game_won = True
        else:
            self.InitScreen()
        
    def show_switch_map_button(self):
        imgui.begin("Switch Map", True)
        if imgui.button("Next Map"):
            self.switch_map()
        imgui.end()