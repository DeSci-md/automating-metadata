# import sys
# import requests
# from io import BytesIO
# from PIL import Image

# response1 = requests.get('https://ipfs.io/ipfs/QmVQmXgcTDZAYx3ynS6HhWXVeEHUN6CCYy3ykQuUshAK76', stream=True)
# response2 = requests.get('http://api.qrserver.com/v1/create-qr-code/?data=https://ipfs.io/ipfs/QmVQmXgcTDZAYx3ynS6HhWXVeEHUN6CCYy3ykQuUshAK76?filename=QmVQmXgcTDZAYx3ynS6HhWXVeEHUN6CCYy3ykQuUshAK76?&size=300x300&format=jpeg', stream=True)
# response3 = requests.get('https://picsum.photos/536/354')
# response3 = requests.get('http://bafybeidjb7l6zdnsvpuhlr3735znqqwl4leibbz5ocaflluznwqaqlbm2e.ipfs.localhost:8080/')
# # images = Image.open(BytesIO(response1.content))
# # images.save('test.jpg')

# # img_url = 'https://blog.finxter.com/wp-content/uploads/2022/04/greenland_01a.jpg'
# # response = requests.get(img_url)
# if response4.status_code:
#     fp = open('foto.jpg', 'wb')
#     fp.write(response4.content)
#     fp.close()
# # images = [Image.open(BytesIO(x)) for x in [response3.content, response3.content]]
# # widths, heights = zip(*(i.size for i in images))

# # total_width = sum(heights)
# # max_height = max(widths)

# # new_im = Image.new('RGB', (total_width, max_height))

# # x_offset = 0
# # for im in images:
# #   new_im.paste(im, (x_offset,0))
# #   x_offset += im.size[0]

# # new_im.save('test.jpg')