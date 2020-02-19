import SimpleITK as sitk

from volume_file_handlers import copy_and_add_volume, read_volume

# fixed_volume_path = str(sys.argv[1])
# moving_volume_path = str(sys.argv[2])
# output_path = str(sys.argv[3])

moving_volume_path = r"C:\LocalZ\Data\Human\US-CCF\US-CCF-067\plan\2018-09-04-123358.153000--CT-454x512x512-AXIAL-interval-0.8.hdf5"
fixed_volume_path = r"C:\LocalZ\Data\Human\US-CCF\US-CCF-064\plan\2018-08-14-150822.541000--CT-512x512x512-AXIAL-interval-0.8.hdf5"
params_path = r"Parameters.Par0008.affine.txt"
# params_path = r"Parameters.Par0008.elastic.txt"

output_path = r"C:\test_output\new_vol.hdf5"


sitk_fixed_image = sitk.GetImageFromArray(read_volume(fixed_volume_path))
sitk_moving_image = sitk.GetImageFromArray(read_volume(moving_volume_path))
# sitk_moving_image = sitk_fixed_image

# copy_and_add_volume(fixed_volume_path, output_path, fixed_volume_path)

# Instantiate SimpleElastix
elastixImageFilter = sitk.SimpleElastix()


# Read Input
elastixImageFilter.SetFixedImage(sitk_fixed_image)
elastixImageFilter.SetMovingImage(sitk_moving_image)

# elastixImageFilter.SetParameterMap(elastixImageFilter.GetDefaultParameterMap('rigid'))  # nonrigid
elastixImageFilter.SetParameterMap(sitk.ReadParameterFile(params_path))

# Perform registration
elastixImageFilter.LogToConsoleOn()
elastixImageFilter.Execute()

# Write result image
res_image = elastixImageFilter.GetResultImage()

res_image_array = sitk.GetArrayFromImage(res_image)

copy_and_add_volume(fixed_volume_path, output_path, res_image_array)
# elastixImageFilter.WriteImage(res_image, output)


