#!/usr/bin/env python

"""
Pandoc filter to insert the right image format based on output type.

Images in Markdown should be defined in the form "images/name-of-image-without-extension".
The image in .svg, .pdf and .png should be pre-generated.
"""

from pandocfilters import toJSONFilter, Image
import logging

#imagedir = "images"

def change_image_format(key, value, format, meta):
  if key == 'Image':
    [captions, target] = value
    [target_path, title_text] = target
    if format == "html5":
      filetype = "svg"
    elif format == "latex":
      filetype = "pdf"
    elif format == "pdf":
      filetype = "pdf"
    else:
      filetype = "png"
    
    target_path = target_path + '.' + filetype
    
    return Image(captions, [target_path,title_text])

if __name__ == "__main__":
  toJSONFilter(change_image_format)
