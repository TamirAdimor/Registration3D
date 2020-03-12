import cv2


class Slicer:
    def __init__(self, dict_volumes_by_windows, start_depth):
        self.dict_volumes_by_windows = dict_volumes_by_windows
        self.start_depth = start_depth
        self.depth = self.start_depth
        self.point = (-1, -1, -1)

    def show(self):
        self.show_volumes_slice_by_depth()
    
        while True:
            k = cv2.waitKeyEx(0)
            if k == 2424832:  # Left
                self.depth += 2
            elif k == 2490368:  # UP
                self.depth += 20
            elif k == 2555904:  # Right
                self.depth -= 2
            elif k == 2621440:  # Down
                self.depth -= 20
            elif k == 27:  # escape key
                break
            else:  # other key
                continue
            self.show_volumes_slice_by_depth()

    @staticmethod
    def cut_volume(volume, d):
        return volume[d:-d, d:-d, d:-d]

    def show_volumes_slice_by_depth(self):
        index = 0
        for name, vol in self.dict_volumes_by_windows.items():
            self.show_volume_slice_by_depth(vol, 'Slice of {}'.format(name), self.depth, index)
            index += 1

    def show_volume_slice_by_depth(self, volume, name, depth, index):
        def on_click(code, x, y, *args):
            if code != 1:
                return
    
            self.point = (x, depth, y)
            print("code: {}, coordinates: ({}, {})".format(code, x, y))
            self.show_volumes_slice_by_depth()
    
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, 600, 600)
        cv2.moveWindow(name, index * 650, 100)
        cv2.setMouseCallback(name, on_click)
        volume_slice = self.apical_slice_from_volume(volume, depth)
        volume_slice = volume_slice + (-1 * volume_slice.min())
        volume_slice = volume_slice / volume_slice.max()
        if self.point[0] >= 0 and self.depth == self.point[1]:
            point_x = self.point[0]
            point_y = self.point[2]
            cv2.line(volume_slice, (point_x, point_y), (point_x, point_y), (255, 0, 0))
        cv2.imshow(name, volume_slice)

    def apical_slice_from_volume(self, volume, depth):
        depth = min(volume.shape[1]-1, depth)
        depth = max(0, depth)
        return volume[:, depth, :]
