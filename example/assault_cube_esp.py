from memkit import memory, utils
import cv2
import numpy as np

mem = memory('ac_client.exe')
module = mem.get_module('ac_client.exe')

entity_list = mem.read(module.base + 0x18AC04, 'u32')
num_of_player = mem.read(module.base + 0x18AC04 + 0x8, 'i32')

windows_width = mem.read(module.base + 0x191ED8, 'i32')
windows_height = mem.read(module.base + 0x191EDC, 'i32')


while True:
    image = 255 * np.zeros(shape=[
        windows_width, windows_height, 3
    ], dtype=np.uint8)

    for i in range(num_of_player):
        player = mem.read(entity_list + 0x4 * i, 'u32')
        if player == 0:
            continue

        health = mem.read(player + 0xEC, 'i32')
        if health <= 0:
            continue

        position_head = [
            mem.read(player + 0x4, 'f32'),
            mem.read(player + 0x8, 'f32'),
            mem.read(player + 0xC, 'f32'),
        ]
        position_bottom = [
            mem.read(player + 0x28, 'f32'),
            mem.read(player + 0x2C, 'f32'),
            mem.read(player + 0x30, 'f32'),
        ]

        view_matrix = []
        for i in range(16):
            view_matrix.append(mem.read(0x57DFD0 + 0x4 * i, 'f32'))

        screen_head = utils.world_to_screen(
            position_head, view_matrix, windows_width, windows_height
        )
        screen_bottom = utils.world_to_screen(
            position_bottom, view_matrix, windows_width, windows_height
        )

        if not screen_head and not screen_bottom:
            continue

        h = screen_bottom['y'] - screen_head['y']
        w = int(h * 0.25)
        cv2.rectangle(image, (
            int(screen_head['x']) - w, int(screen_head['y'])
        ),
            (
            int(screen_bottom['x']) + w, int(screen_bottom['y'])
        ), (0, 0, 255), 2)

        cv2.imshow('ESP', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()