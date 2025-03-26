import numpy as np

def CreateCircle(center, radius, colour, points = 10, offset = 0, semi = False):
    vertices = [center[0], center[1], center[2], colour[0], colour[1], colour[2]]
    indices = []

    if semi == True:
        for i in range(points+1):
            vertices += [
                center[0] + radius * np.cos(float(i * np.pi)/points),
                center[1] + radius * np.sin(float(i * np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]
    else:
        for i in range(points):
            vertices += [
                center[0] + radius * np.cos(float(i * 2* np.pi)/points),
                center[1] + radius * np.sin(float(i * 2* np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points-1 else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]

    return (vertices, indices)    

def CreatePlayer():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [220/255, 183/255, 139/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateSpaceEnemy():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [180/255, 224/255, 150/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateJungleEnemy():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [180/255, 224/255, 150/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateRiverEnemy():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [180/255, 224/255, 150/255], 50, 0)

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,1,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [1,0,0], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.9,0.9,0.9], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateBackground():
    grassColour = [0,1,0]
    waterColour = [0,0,1]

    vertices = [
        -500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        -400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        -400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]

    return vertices, indices

playerVerts, playerInds = CreatePlayer()
playerProps = {
    'name': 'player',

    'vertices' : np.array(playerVerts, dtype = np.float32),
    
    'indices' : np.array(playerInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'radius': 25
}

backgroundVerts, backgroundInds = CreateBackground()
backgroundProps = {
    'name': 'background',

    'vertices' : np.array(backgroundVerts, dtype = np.float32),
    
    'indices' : np.array(backgroundInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0]
}

def CreateSpaceBiome():
    spaceColour = [0.1,0.1,0.1]
    planetColour = [0.5,0.3,0.7]
    # Define vertices and indices for forest biome
    vertices = [
        500.0, 500.0, -0.9, planetColour[0], planetColour[1], planetColour[2],
        400.0, 500.0, -0.9, planetColour[0], planetColour[1], planetColour[2],
        400.0, -500.0, -0.9, planetColour[0], planetColour[1], planetColour[2],
        500.0, -500.0, -0.9, planetColour[0], planetColour[1], planetColour[2],

        -500.0, 500.0, -0.9, planetColour[0], planetColour[1], planetColour[2],
        -400.0, 500.0, -0.9, planetColour[0], planetColour[1], planetColour[2],
        -400.0, -500.0, -0.9, planetColour[0], planetColour[1], planetColour[2],
        -500.0, -500.0, -0.9, planetColour[0], planetColour[1], planetColour[2],

        400.0, 500.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2],
        -400.0, 500.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2],
        -400.0, -500.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2],
        400.0, -500.0, -0.9, spaceColour[0], spaceColour[1], spaceColour[2],
    ]
    indices = [
        # Define indices for trees, ground, etc.
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]
    return vertices, indices

def CreateJungleBiome():
    cliffColour = [0.5,0.5,0]
    grasslandColour = [0.5,1,0.5]
    # Define vertices and indices for desert biome
    vertices = [
        500.0, 500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2],
        400.0, 500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2],
        400.0, -500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2],
        500.0, -500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2],

        -500.0, 500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2],
        -400.0, 500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2],
        -400.0, -500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2],
        -500.0, -500.0, -0.9, cliffColour[0], cliffColour[1], cliffColour[2],

        400.0, 500.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2],
        -400.0, 500.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2],
        -400.0, -500.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2],
        400.0, -500.0, -0.9, grasslandColour[0], grasslandColour[1], grasslandColour[2],
    ]
    indices = [
        # Define indices for cacti, sand, etc.
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]
    return vertices, indices

def CreateRiverBiome():
    landColour = [0,1,0]
    riverColour = [0,0,1]
    # Define vertices and indices for river biome
    vertices = [
        500.0, 500.0, -0.9, landColour[0], landColour[1], landColour[2],
        400.0, 500.0, -0.9, landColour[0], landColour[1], landColour[2],
        400.0, -500.0, -0.9, landColour[0], landColour[1], landColour[2],
        500.0, -500.0, -0.9, landColour[0], landColour[1], landColour[2],

        -500.0, 500.0, -0.9, landColour[0], landColour[1], landColour[2],
        -400.0, 500.0, -0.9, landColour[0], landColour[1], landColour[2],
        -400.0, -500.0, -0.9, landColour[0], landColour[1], landColour[2],
        -500.0, -500.0, -0.9, landColour[0], landColour[1], landColour[2],

        400.0, 500.0, -0.9, riverColour[0], riverColour[1], riverColour[2],
        -400.0, 500.0, -0.9, riverColour[0], riverColour[1], riverColour[2],
        -400.0, -500.0, -0.9, riverColour[0], riverColour[1], riverColour[2],
        400.0, -500.0, -0.9, riverColour[0], riverColour[1], riverColour[2],
    ]
    indices = [
        # Define indices for water, rocks, etc.
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]
    return vertices, indices

def CreateStone(radius=15, color=[0.7, 0.7, 0.7], center=[0.0, 0.0, 0.0], points=20):
    
    # center = [np.random.uniform(-380, 380), np.random.uniform(-380, 380), 0]
    # Create a circular stone mesh using your existing CreateCircle function
    verts, inds = CreateCircle(center, radius, color, points)
    return verts, inds

def CreateKeyIcon(radius=5, color=[1.0, 1.0, 0.0], points=12):
    """
    Creates a small circular 'key' graphic.
    Reuse your CreateCircle function, or define your own small circle here.
    """
    verts, inds = CreateCircle([0.0, 0.0, 0.0], radius, color, points)
    return verts, inds

def CreateHeartIcon(radius=8, color=[1.0, 0.0, 0.0]):
    """
    Creates a simple heart shape using two circles plus a triangle-like shape.
    You can tweak points for a more detailed heart.
    """
    # Left circle
    left_circle_verts, left_circle_inds = CreateCircle([-0.5, 0.0, 1.0], radius, color, 16, 0)
    # Right circle (shift x by +0.5 so it joins the left circle)
    right_circle_verts, right_circle_inds = CreateCircle([0.5, 0.0, 1.0], radius, color, 16, len(left_circle_verts)//6)
    
    # Triangle portion (approx)
    triangle_verts = [
        0.0, -1.0*radius, 1.0, color[0], color[1], color[2],
        -1.0*radius, 0.0, 1.0, color[0], color[1], color[2],
        1.0*radius, 0.0, 1.0, color[0], color[1], color[2],
    ]
    triangle_inds = [0,1,2]
    # Adjust the triangle indices offset
    tri_offset = (len(left_circle_verts) + len(right_circle_verts)) // 6

    # Combine everything
    verts = left_circle_verts + right_circle_verts + triangle_verts
    inds = left_circle_inds + right_circle_inds + [
        triangle_inds[0] + tri_offset,
        triangle_inds[1] + tri_offset,
        triangle_inds[2] + tri_offset
    ]
    return verts, inds


# Example properties for biomes
spaceVerts, spaceInds = CreateSpaceBiome()
spaceProps = {
    'name': 'spacemap',
    'vertices': np.array(spaceVerts, dtype=np.float32),
    'indices': np.array(spaceInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
}

jungleVerts, jungleInds = CreateJungleBiome()
jungleProps = {
    'name': 'junglemap',
    'vertices': np.array(jungleVerts, dtype=np.float32),
    'indices': np.array(jungleInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
}

riverVerts, riverInds = CreateRiverBiome()
riverProps = {
    'name': 'rivermap',
    'vertices': np.array(riverVerts, dtype=np.float32),
    'indices': np.array(riverInds, dtype=np.uint32),
    'position': np.array([0, 0, 0], dtype=np.float32),
    'rotation_z': 0.0,
    'scale': np.array([1, 1, 1], dtype=np.float32),
}