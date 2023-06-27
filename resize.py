import os
from gimpfu import *


def resize_images(input_folder, output_folder, width, height):
    files = os.listdir(input_folder)

    for file_name in files:
        image = pdb.gimp_file_load(os.path.join(
            input_folder, file_name), file_name)

        if image.base_type == GRAY:
            layer = image.layers[0]
            pdb.gimp_image_convert_layer_to_rgb(image, layer)

        layer = image.layers[0]
        pdb.gimp_layer_scale(layer, width, height, True)

        new_image = pdb.gimp_image_new(100, 100, RGB)

        transparent_layer = pdb.gimp_layer_new(
            new_image, 100, 100, RGBA_IMAGE, "Transparent Layer", 100, NORMAL_MODE)
        pdb.gimp_image_add_layer(new_image, transparent_layer, 0)

        margin_size = (100 - width) // 2

        new_layer = pdb.gimp_layer_new(new_image, width + 2 * margin_size,
                                       height + 2 * margin_size, RGBA_IMAGE, "Resized Layer", 100, NORMAL_MODE)
        pdb.gimp_image_insert_layer(new_image, new_layer, None, 0)
        pdb.gimp_edit_copy(layer)
        floating_sel = pdb.gimp_edit_paste(new_layer, True)
        pdb.gimp_floating_sel_anchor(floating_sel)

        output_file = os.path.join(output_folder, file_name)
        pdb.gimp_file_save(new_image, new_layer, output_file, output_file)

        pdb.gimp_image_delete(image)
        pdb.gimp_image_delete(new_image)


register(
    "python_fu_resize_images",
    "Resize images in a folder to a specific size",
    "Resize images in a folder",
    "Bostra",
    "Bostra",
    "2023",
    "<Toolbox>/Python-Fu/Resize Images",
    "",
    [
        (PF_DIRNAME, "input_folder", "Input folder", ""),
        (PF_DIRNAME, "output_folder", "Output folder", ""),
        (PF_INT, "width", "Width", 75),
        (PF_INT, "height", "Height", 75)
    ],
    [],
    resize_images)

main()
