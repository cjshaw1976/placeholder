from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from PIL import Image, ImageDraw, ImageFont

""" Home page """
class HomeView(TemplateView):
    template_name = "mysite/home.html"


""" Function to convert a hex color value to RGB tuple """
def hex_to_rgb(hex):
    # strip leading hash if it is there
    hex = hex.lstrip('#')

    # Convert a 3 character hex to a 6 character by doubling each character
    if len(hex) == 3:
        hex6 = ''
        for chr in hex:
            hex6 += chr+chr
        hex = hex6

    # Return the tuple of RGB values
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))


""" Recursive function to determine a fontsize that will fit our shape """
def fit_font(width, height, drawobject, text1, text2=None, fontsize=25):
    font = ImageFont.truetype('fonts/grundschrift/Grundschrift-Bold.otf',
                               fontsize)
    # Determine the width and height of the first text line
    text_width, text_height = drawobject.textsize(text1, font=font)

    # If there is a second text line, determine its width and height
    if text2:
        text2_width, text2_height = drawobject.textsize(text2, font=font)
        text_height *= 3 # Triple the height for two lines of text

    # Work with the widest text line
    if text2_width > text_width:
        text_width = text2_width

    # Check the text width and height is at most 66% of the image size
    if text_width > width * 0.666 or text_height > height * 0.666:
        fontsize -= 1 # If fails, reduced the fontsize by 1
        if fontsize < 8:
            return None # If font size too small, return nothing
        return fit_font(width, height, drawobject, text1, text2, fontsize)
    return font


""" Function to create placeholder rectangle """
def placeholder(width, height, backcolor, forecolor, text):
    # If only width set, make the shape a square
    if height==0:
        height=width

    # Create our 'canvas'
    img = Image.new('RGB', (width, height), color = hex_to_rgb(backcolor))
    drawobject = ImageDraw.Draw(img)

    # Create our size text line
    textd = "{}px  X  {}px".format(width, height)

    # Call function to set font
    font = fit_font(width, height, drawobject, text, textd)

    # If font set, add the text to the image
    if font:
        text_width, text_height = drawobject.textsize(text, font=font)
        textd_width, textd_height = drawobject.textsize(textd, font=font)

        if text:    # Two lines of text
            drawobject.text((((width/2)-(textd_width/2)),(height/2)-(textd_height*1.5)),
                            textd, font=font, fill=hex_to_rgb(forecolor))
            drawobject.text((((width/2)-(text_width/2)),(height/2)+(text_height*0.5)),
                            text, font=font, fill=hex_to_rgb(forecolor))
        else:       # One line of text
            drawobject.text((((width/2)-(textd_width/2)),(height/2)-(textd_height*0.5)),
                            textd, font=font, fill=hex_to_rgb(forecolor))
    return img


""" View to return the placeholder created """
def PlaceholderView(request, width, height=0, backcolor='#f1f1f1',
                    forecolor='#000', format='png'):
    if format.lower()=='jpg':
        format = 'JPEG'
    text = request.GET.get('text', 'placeholder.amid.africa')
    response = HttpResponse(content_type="image/{}".format(format))
    image = placeholder(width, height, backcolor, forecolor, text)
    image.save(response, format)
    return response

""" Custom Error pages """
def error_400_view(request, exception):
    data = {"event_id": id,
            "code": 400,
            "title": "BAD REQUEST",
            "description": "The server cannot process the request due to a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing)."}
    return render(request,'error.html', data, status=400)

def error_403_view(request, exception):
    data = {"event_id": id,
            "code": 403,
            "title": "FORBIDDEN",
            "description": "The client has insufficient authentication credentials for the server to process this request."}
    return render(request,'error.html', data, status=403)

def error_404_view(request, exception):
    data = {"event_id": id,
            "code": 404, "title":
            "NOT FOUND", "description":
            "The server is not able to find the requested resource. AKA, Page Not Found."}
    return render(request,'error.html', data, status=404)

def error_500_view(request):
    data = {"event_id": id,
            "code": 500,
            "title": "INTERNAL SERVER ERROR",
            "description": "The server encountered an unexpected condition that prevented it from fulfilling the request."}
    return render(request,'error.html', data, status=500)
