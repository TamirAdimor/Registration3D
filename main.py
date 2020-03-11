from collections import OrderedDict

import SimpleITK as sitk
from matplotlib import pyplot as plt
from scipy import ndimage

from slicer import run_slicer_functionality
from volume_file_handlers import copy_and_add_volume, read_volume


def move_moving_image_to_fixed(numpy_moving_image, numpy_fixed_image, params_path, log_folder):
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
    elastix_image_filter.SetOutputDirectory(log_folder)
    elastix_image_filter.Execute()

    # Write result image
    res_image = elastix_image_filter.GetResultImage()

    return sitk.GetArrayFromImage(res_image)


def register(fixed_volume_path, moving_volume_path, output_folder, params_path):
    output_image_path = r"{}\new_vol.hdf5".format(output_folder)

    moving_image = read_volume(moving_volume_path)
    fixed_image = read_volume(fixed_volume_path)

    # moving_image = normalize_ct_volume(moving_image)
    # fixed_image = normalize_ct_volume(fixed_image)

    # show_histogram(fixed_image, moving_image)

    # run_slicer_functionality({'moving_image': moving_image, 'fixed_image': fixed_image}, int(moving_image.shape[1] / 2))
    # exit()

    # rotated_moving_image = rotate_and_save(moving_image)

    res_image_array = move_moving_image_to_fixed(moving_image, fixed_image, params_path, output_folder)

    copy_and_add_volume(fixed_volume_path, output_image_path, res_image_array)

    all_slicer_images = OrderedDict([
        # 'moving': moving_image,
        ('moving_rotated', moving_image),
        ('moving_result', res_image_array),
        ('fixed', fixed_image)
    ])

    run_slicer_functionality(all_slicer_images, int(fixed_image.shape[1] / 2))


def rotate_and_save(moving_image):
    print('rotating...')
    moving_image_rotated = transform_moving_image(moving_image)
    print('finished rotating')
    data_folder = r"..\\Data\\"
    origin_path = r"{}\064---512x512x512.hdf5".format(data_folder)
    transformed_path = r"{}\064---transformed.hdf5".format(data_folder)
    copy_and_add_volume(origin_path, transformed_path, moving_image_rotated)
    print('saved')
    return moving_image_rotated


def transform_moving_image(image):
    image = ndimage.shift(image, [-50, 0, 0])
    image = ndimage.rotate(image, 5, axes=(2, 0))
    image = ndimage.rotate(image, 10, axes=(1, 0))
    return image


def show_histogram(fixed_image, moving_image):
    plt.hist(moving_image.flatten().ravel(), 2000, [-2000, 2000])
    plt.title('Histogram for gray scale picture1')
    volume = (fixed_image * 100).astype('int16')
    plt.hist(volume.flatten().ravel(), 2000, [-1000, 1000])
    plt.title('Histogram for gray scale picture2')
    plt.show()


def normalize_cabt_volume(volume):

    volume[volume < 0] = 0
    volume[volume > 1] = 0
    # volume += volume.min()
    volume *= 255
    new_volume = volume.astype('uint8')
    return new_volume


def normalize_ct_volume(volume):
    new_volume = volume.astype('uint8')
    new_volume[volume < -950] = 0
    new_volume[(-950 <= volume) & (volume < -670)] = 30
    new_volume[(-670 <= volume) & (volume < -190)] = 60
    new_volume[(-190 <= volume) & (volume < -50)] = 80
    new_volume[-50 <= volume] = 200

    # # fixed_image = fixed_image.astype('float64')
    # cabt_min, cabt_max = fixed_image.min(), fixed_image.max()
    # ct_min, ct_max = moving_image.min(), moving_image.max()
    # moving_image -= ct_min
    # moving_image = moving_image / (ct_max - ct_min)
    # moving_image *= (cabt_max - cabt_min) / 2
    # moving_image += cabt_min + 0.4
    # moving_image = - (moving_image.max() - moving_image) / 2
    # # moving_image[moving_image >= 0] = 3
    # # moving_image[moving_image < 0] = -1
    # # fixed_image[fixed_image >= 0] = 3
    # # fixed_image[fixed_image < 0] = -1
    return new_volume


def main():
    project_folder = r"../"
    output_folder = r"{}\Result\\".format(project_folder)
    data_folder = r"{}\Data\\".format(project_folder)
    #
    # moving_volume_path = r"{}\067---tomo.hdf5".format(data_folder)
    # # moving_volume_path = r"{}\simulation_other_place.hdf5".format(data_folder)
    # fixed_volume_path = r"{}\simulation.hdf5".format(data_folder)
    # # fixed_volume_path = r"{}\064---512x512x512.hdf5".format(data_folder)

    fixed_volume_path = r"{}\064---512x512x512.hdf5".format(data_folder)
    moving_volume_path = r"{}\064---transformed.hdf5".format(data_folder)
    # fixed_volume_path = r"{}\067---tomo.hdf5".format(data_folder)
    # moving_volume_path = r"{}\067_as_tomo.hdf5".format(data_folder)
    # fixed_volume_path = r"{}\ccf-085\segmented_volume.hdf5".format(data_folder)
    # moving_volume_path = r"{}\ccf-085\original_volume.hdf5".format(data_folder)

    params_path = r"Parameters.Par0008.affine.txt"  # r"Parameters.Par0008.affine.txt"
    register(fixed_volume_path, moving_volume_path, output_folder, params_path)


if __name__ == '__main__':
    main()
