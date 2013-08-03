import qrcode
import Image
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('$s'. $ input_url)
qr.make(fit=True)

img = qr.make_image()
img = img.resize((200,200), Image.ANTIALIAS)
img.save("temp1.png")

qrcodeimg = Image.open("temp1.png")
checkimg = Image.open("$s", $ filename) #Do assume that the source image is 400x800 pixels.Hence 
fillerimg = Image.open("fillerimg.png")
newWidth, originalHeight = checkimg.size
totalHeight = originalHeight + 200 #image total height
newHeight = 200 #height of QR code image
newImage = Image.new("RGB", (newWidth,totalHeight))
newImage.paste(checkimg, (0, 0))
newImage.paste(qrcodeimg, (0, originalHeight))
newImage.paste(fillerimg, (200, originalHeight))
newImage.save("$s.png", $ title)

