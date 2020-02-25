import numpy as np
import cv2
import SimpleITK as sitk
from scipy import ndimage

from volume_file_handlers import copy_and_add_volume, read_volume


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


def move_moving_image_to_fixed(numpy_moving_image, numpy_fixed_image):
    # numpy_moving_image = (numpy_moving_image * 10).astype(np.dtype('int16'))
    sitk_fixed_image = sitk.GetImageFromArray(numpy_fixed_image)
    sitk_moving_image = sitk.GetImageFromArray(numpy_moving_image)

    elastix_image_filter = sitk.SimpleElastix()

    # Read Input
    elastix_image_filter.SetFixedImage(sitk_fixed_image)
    elastix_image_filter.SetMovingImage(sitk_moving_image)

    # elastix_image_filter.SetParameterMap(elastix_image_filter.GetDefaultParameterMap('rigid'))  # nonrigid
    elastix_image_filter.SetParameterMap(sitk.ReadParameterFile(params_path))

    # Perform registration
    elastix_image_filter.LogToConsoleOn()
    elastix_image_filter.SetOutputDirectory(output_folder)
    elastix_image_filter.Execute()

    # Write result image
    res_image = elastix_image_filter.GetResultImage()

    return sitk.GetArrayFromImage(res_image)


project_folder = r"C:\Workspace\Reg3d"
output_folder = r"{}\Result\\".format(project_folder)
data_folder = r"{}\Data\\".format(project_folder)
#
# moving_volume_path = r"{}\067---tomo.hdf5".format(data_folder)
# # moving_volume_path = r"{}\simulation_other_place.hdf5".format(data_folder)
# fixed_volume_path = r"{}\simulation.hdf5".format(data_folder)
# # fixed_volume_path = r"{}\064---512x512x512.hdf5".format(data_folder)

fixed_volume_path = r"{}\067---tomo.hdf5".format(data_folder)
moving_volume_path = r"{}\067_as_tomo.hdf5".format(data_folder)

params_path = r"CT_TO_CBCT_Par0058trans.txt"  # r"Parameters.Par0008.affine.txt"


fixed_image = read_volume(fixed_volume_path)
moving_image = read_volume(moving_volume_path)


moving_image_rotated = ndimage.rotate(moving_image, 10)

res_image_array = move_moving_image_to_fixed(moving_image, fixed_image)

output_path = r"{}\new_vol.hdf5".format(output_folder)
copy_and_add_volume(fixed_volume_path, output_path, res_image_array)

all_slicer_images = {
    'fixed': fixed_image,
    'moving': moving_image,
    'moving_rotated': moving_image_rotated,
    'moving_result': res_image_array
}

run_slicer_functionality(all_slicer_images, int(fixed_image.shape[1] / 2))


