ux.Image
========

methods
-------

Image.**named**(name)

- If name begins with 'system:', returns system sfsymbol image.
  - ux.Image.named('system:ellipsis.circle')
- If name contains ':'
  - Pythonista returns built-in image.
    - ux.Image.named('iob:ios7_folder_outline_32.png')
  - Other applications return image from 'ux/media/Images'
    - ux.Image.named('iob:document_32.png')
- Can be path to image file.
  - ux.Image.named('./path/to/file/image.png')
