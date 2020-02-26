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

    res_image_array = move_moving_image_to_fixed(moving_image, fixed_image, params_path, output_folder)

    copy_and_add_volume(fixed_volume_path, output_image_path, res_image_array)

    all_slicer_images = {
        'fixed': fixed_image,
        'moving': moving_image,
        'moving_result': res_image_array
    }

    run_slicer_functionality(all_slicer_images, int(fixed_image.shape[1] / 2))


def transform_moving_image(moving_image):
    moving_image_rotated = ndimage.rotate(moving_image, 10)
    return moving_image_rotated


def show_histogram(fixed_image, moving_image):
    plt.hist(moving_image.flatten().ravel(), 2000, [-2000, 2000])
    plt.title('Histogram for gray scale picture1')
    volume = (fixed_image * 100).astype('int16')
    plt.hist(volume.flatten().ravel(), 2000, [-1000, 1000])
    plt.title('Histogram for gray scale picture2')
    plt.show()


def main():
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
    # moving_volume_path = r"{}\067---tomo.hdf5".format(data_folder)
    # fixed_volume_path = r"{}\067_as_tomo.hdf5".format(data_folder)

    params_path = r"CT_TO_CBCT_Par0058trans.txt"  # r"Parameters.Par0008.affine.txt"
    register(fixed_volume_path, moving_volume_path, output_folder, params_path)


if __name__ == '__main__':
    main()
