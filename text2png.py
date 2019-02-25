# coding=utf8

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def text2png(text, fullpath, color = "#000", bgcolor = "#FFF", fontfullpath = None, fontsize = 13, leftpadding = 3, rightpadding = 3, width = -1):
	"""
		If width < 0, then the size of the image is adjusted autoamtically around the text.
		Example: text2png(u"This is\na\ntest şğıöç zaa xd ve lorem hipster", 'test.png', fontfullpath = "font.ttf")
	"""
	REPLACEMENT_CHARACTER = u'\uFFFD'
	NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '

	font = ImageFont.load_default() if fontfullpath == None else ImageFont.truetype(fontfullpath, fontsize)
	text = text.replace('\n', NEWLINE_REPLACEMENT_STRING)

	lines = []
	line = u""

	for word in text.split():
		# print word
		if word == REPLACEMENT_CHARACTER: #give a blank line
			lines.append( line[1:] ) #slice the white space in the begining of the line
			line = u""
			lines.append( u"" ) #the blank line
		elif width < 0 or font.getsize( line + ' ' + word )[0] <= (width - rightpadding - leftpadding):
			line += ' ' + word
		else: #start a new line
			lines.append( line[1:] ) #slice the white space in the begining of the line
			line = u""

			# TODO: handle too long words at this point. I was able to solve by using textwrap. 
			# Just import it and set the maximum width. Something like: list=textwrap.wrap(text, width=30)
			line += ' ' + word #for now, assume no word alone can exceed the line width

	if len(line) != 0:
		lines.append( line[1:] ) #add the last line

	max_line_length = 0;
	for l in lines:
		if font.getsize(l)[0] > max_line_length:
			max_line_length = font.getsize(l)[0]

	line_height = int(font.getsize(text)[1] * 0.7)
	img_height = line_height * (len(lines) + 1)

	if width < 0:
		width = max_line_length + rightpadding

	img = Image.new("RGBA", (width, img_height), bgcolor)
	draw = ImageDraw.Draw(img)

	y = 0
	for line in lines:
		draw.text( (leftpadding, y), line, color, font=font)
		y += line_height

	img.save(fullpath)

if __name__ == "__main__":
    text2png(	'Telefon: 0728 811 446', 
    			'test.png', 
    			fontfullpath = "Roboto-Bold.ttf",
    			fontsize = 15,
    			leftpadding = 0)
