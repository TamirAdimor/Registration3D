import cv2


def run_slicer_functionality(dict_volumes_by_windows, start_depth):
    depth = start_depth
    show_volumes_slice_by_depth(dict_volumes_by_windows, start_depth)

    while True:
        k = cv2.waitKeyEx(0)
        if k == 2424832:  # Left
            depth += 10
        elif k == 2490368:  # UP
            depth += 100
        elif k == 2555904:  # Right
            depth -= 10
        elif k == 2621440:  # Down
            depth -= 100
        elif k == 27:  # escape key
            break
        else:  # other key
            continue
        show_volumes_slice_by_depth(dict_volumes_by_windows, depth)


def cut_volume(volume, d):
    return volume[d:-d, d:-d, d:-d]


def show_volumes_slice_by_depth(dict_volumes_by_windows, depth):
    for name, vol in dict_volumes_by_windows.items():
        show_volume_slice_by_depth(vol, 'Slice of {}'.format(name), depth)


def show_volume_slice_by_depth(volume, name, depth):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    volume_slice = apical_slice_from_volume(volume, depth)
    cv2.imshow(name, volume_slice)


def apical_slice_from_volume(volume, depth):
    depth = min(volume.shape[1]-1, depth)
    depth = max(0, depth)
    return volume[:, depth, :]
