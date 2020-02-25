from scipy import ndimage

from volume_file_handlers import copy_and_add_volume, read_volume


project_folder = r"C:\Workspace\Reg3d"
output_folder = r"{}\Result".format(project_folder)
data_folder = r"{}\Data".format(project_folder)

orig_vol_file = r"{}\067---454x512x512.hdf5".format(data_folder)
res_vol_file = r"{}\shift_and_rotate_067---454x512x512.hdf5".format(output_folder)


orig_vol = read_volume(orig_vol_file)

shifted_transform = ndimage.shift(orig_vol, -50)
shifted_rotated_transform = ndimage.rotate(shifted_transform, 15)
# shifted_rotated_transform = ndimage.affine_transform(shifted_rotated_transform, M)

copy_and_add_volume(orig_vol_file, res_vol_file, shifted_rotated_transform)
