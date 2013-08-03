import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('www.facebook.com')
qr.make(fit=True)

img = qr.make_image()
img.save("file2.png")

qrcodeimg = img.open("file2.png")
checkimg = img.open("file1.png")
newWidth, originalHeight = checkimg.size
totalHeight = originalHeight + 290 #image total height
newHeight = 290 #height of QR code image
newImage = Image.new(mode, (newWidth,newHeight))
newImage.paste(checkimg, (0, 0, newWidth, originalHeight))
newImage.paste(qrcodeimg, (0, originalHeight, newWidth, originalHeight+290))

