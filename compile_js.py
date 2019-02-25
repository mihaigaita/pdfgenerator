# -*- coding: utf-8 -*-

# Import all needed libraries
import httplib, urllib, sys
import base64
import re
from text2png import text2png

# Main functionality
def main():
    """
        Update and then compile JS code
    """

    # Convert Logo to Base64 to be able to be understood by PDFMake JS library
    with open("logo.png", "rb") as image_file:
        logo_base64 = base64.b64encode(image_file.read())

    # Read JS code
    with open('script.js', 'r') as in_file:
        js_code = in_file.read()

    # Create telephone number
    text2png(   'Telefon: 0728 811 446', 
                'telephone.png', 
                fontfullpath = "/home/mihai/.fonts/Roboto-Bold.ttf",
                fontsize = 30,
                leftpadding = 0)

    # Convert Telephone number image to Base64 to be able to be understood by PDFMake JS library
    with open("telephone.png", "rb") as image_file:
        tel_base64 = base64.b64encode(image_file.read())

    # Update logo and telephone image in Base64 format in JS code before compiling it
    sub_pattern = "{id}\:\s*'data\:image\/png\;base64\,\S*'\,"
    updated_img = "{id}: 'data:image/png;base64,{img_base64_string}',"

    sub_pattern_logo = sub_pattern.format(id = 'logo')
    updated_img_logo = updated_img.format(id = 'logo', img_base64_string = logo_base64)

    js_code_new = re.sub(sub_pattern_logo, updated_img_logo, js_code)

    sub_pattern_tel = sub_pattern.format(id = 'telephone')
    updated_img_tel = updated_img.format(id = 'telephone', img_base64_string = tel_base64)

    js_code_new = re.sub(sub_pattern_tel, updated_img_tel, js_code_new)

    # Update original JS file as well
    with open('script.js', 'w') as f:
        f.write(js_code_new)

    if len(sys.argv) == 2:
        # Define the parameters for the POST request and encode them in
        # a URL-safe format.
        params = urllib.urlencode([
            ('js_code', js_code_new),
            ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
            ('output_format', 'text'),
            ('output_info', 'compiled_code'),
          ])

        # Always use the following value for the Content-type header.
        headers = { "Content-type": "application/x-www-form-urlencoded" }
        conn = httplib.HTTPConnection('closure-compiler.appspot.com')
        conn.request('POST', '/compile', params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        # Write Compiled JS code into path passed from command line
        with open(sys.argv[1], 'w') as out_file:
            out_file.write(data)

# %
if __name__ == "__main__":
    main()