import h5py

TOMO_location = r"C:\Workspace\Reg3d\Data\067---tomo.hdf5"
start_location = [150, 250, 400]


def get_voxels_indexes(index, tomo_volume_shape):
    offset_before = int(tomo_volume_shape[index] / 2)
    offset_after = tomo_volume_shape[index] - offset_before
    start = start_location[index] - offset_before
    end = start_location[index] + offset_after
    return start, end


def cat_volume_as_tomo(orig_volume_path, dest_volume_path):
    with h5py.File(orig_volume_path, 'r') as orig_file:
        with h5py.File(TOMO_location, 'r') as tomo_file:
            tomo_dset = tomo_file['volume']
            tomo_volume_shape = tomo_dset[()].shape
            orig_volume = orig_file['volume'][()]
            x_s, x_e = get_voxels_indexes(0, tomo_volume_shape)
            y_s, y_e = get_voxels_indexes(1, tomo_volume_shape)
            z_s, z_e = get_voxels_indexes(2, tomo_volume_shape)
            cropped_volume = orig_volume[x_s: x_e, y_s: y_e, z_s: z_e]

            with h5py.File(dest_volume_path, "w") as dest_file:
                dset = dest_file.create_dataset("volume", data=cropped_volume)
                for key in tomo_dset.attrs.keys():
                    dset.attrs[key] = tomo_dset.attrs[key]


project_folder = r"C:\Workspace\Reg3d"
output_folder = r"{}\Result".format(project_folder)
data_folder = r"{}\Data".format(project_folder)

orig_vol_file = r"{}\067---454x512x512.hdf5".format(data_folder)
res_vol_file = r"{}\067_as_tomo.hdf5".format(output_folder)
cat_volume_as_tomo(orig_vol_file, res_vol_file)
