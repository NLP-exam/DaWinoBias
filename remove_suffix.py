import os

def remove_suffix(path, suffix) -> str:
    """
    Remove the suffix from the path if file name without extension ends with it

    Parameters
    ----------
    path
        name with prefix
    suffix
        suffix to remove

    Returns
    -------
    name_without_suffix
        name with removed suffix

    """
    if not suffix:
        return path
    directory, basename = os.path.split(path)
    basename, ext = os.path.splitext(basename)
    if basename.endswith(suffix):
        word_split = basename.rsplit(suffix, 1)
        basename = "".join(word_split[:-1])
        path = os.path.join(directory, basename + ext)
    return path 

text = 'håndværkerens'
print(remove_suffix(text, 's'))