from PIL import Image


def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:

    # Check if image size is dividable by tile size
    if image_size[0] % tile_size[0] != 0 or image_size[1] % tile_size[1] != 0:
        return False

    # For checking if ordering is valid

    # Check if number of tiles is correct
    if len(ordering) != (image_size[0] // tile_size[0]) * (image_size[1] // tile_size[1]):
        return False

    # Check if any tile is repeated
    elif len(ordering) != len(set(ordering)):
        return False

    # Check if any tile is out of range
    elif any([tile < 0 or tile >= len(ordering) for tile in ordering]):
        return False

    return True


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:

    # Open image
    image = Image.open(image_path)

    # Check if input is valid
    if not valid_input(image.size, tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

    # Create new image
    new_image = Image.new(image.mode, image.size)

    # Coordinates for first paste
    paste_index_x = 0
    paste_index_y = 0

    # Iterate over tiles
    for tile_index in ordering:

        # Calculate coordinates
        x = (tile_index % (image.size[0] // tile_size[0])) * tile_size[0]
        y = (tile_index // (image.size[0] // tile_size[0])) * tile_size[1]

        # Crop tile
        tile_image = image.crop((x, y, x + tile_size[0], y + tile_size[1]))

        # Paste tile
        new_image.paste(tile_image, (paste_index_x, paste_index_y))

        # Calculate coordinates for next paste
        if paste_index_x == image.size[0] - tile_size[0]:
            paste_index_x = 0
            paste_index_y += tile_size[1]
        else:
            paste_index_x += tile_size[0]

    # Save image
    new_image.save(out_path)

    return None
