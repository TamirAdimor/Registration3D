import h5py


def copy_and_add_volume(orig_volume_path, dest_volume_path, volume):
    with h5py.File(dest_volume_path, "w") as dest_file:
        dset = dest_file.create_dataset("volume", data=volume)
        with h5py.File(orig_volume_path, 'r') as orig_file:
            orig_dset = orig_file['volume']
            for key in orig_dset.attrs.keys():
                dset.attrs[key] = orig_dset.attrs[key]


def read_volume(volume_path):
    with h5py.File(volume_path, 'r') as f:
        dset = f['volume']
        return dset[()]