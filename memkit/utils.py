def world_to_screen(position, matrix, windows_width, windows_height):
    """
    position[0] = x
    position[1] = y
    position[2] = z
    """
    clipCoords_x = position[0] * matrix[0] + position[1] * matrix[4] + position[2] * matrix[8] + matrix[12]
    clipCoords_y = position[0] * matrix[1] + position[1] * matrix[5] + position[2] * matrix[9] + matrix[13]
    clipCoords_z = position[0] * matrix[2] + position[1] * matrix[6] + position[2] * matrix[10] + matrix[14]
    clipCoords_w = position[0] * matrix[3] + position[1] * matrix[7] + position[2] * matrix[11] + matrix[15]

    if clipCoords_w < 0.1:
        return None
    
    NDC_x = clipCoords_x / clipCoords_w
    NDC_y = clipCoords_y / clipCoords_w
    NDC_z = clipCoords_z / clipCoords_w

    screen_x = (windows_width / 2 * NDC_x) + (NDC_x + windows_width / 2)
    screen_y = -(windows_height / 2 * NDC_y) + (NDC_y + windows_height / 2)
    return {
        'x': screen_x,
        'y': screen_y
    }
