import requests

def sendImage(chat_id, caption, photo):
    url = "https://api.telegram.org/bot970406731:AAGRJVcUeDSnWZP39x70jRdcfvlmECVLHNQ/sendPhoto"
    files = {'photo': photo}
    data = {'chat_id' : chat_id,
             'caption': caption}
    r = requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendVideo(chat_id, caption, video):
    url = "https://api.telegram.org/bot970406731:AAGRJVcUeDSnWZP39x70jRdcfvlmECVLHNQ/sendVideo"
    files = {'video': video}
    data = {'chat_id' : "910667518",
             'caption':caption}
    r = requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendMessage(chat_id, text):
    url = "https://api.telegram.org/bot970406731:AAGRJVcUeDSnWZP39x70jRdcfvlmECVLHNQ/sendMessage"
    data = {'chat_id' : chat_id,
            'text': text}
    r = requests.post(url,  data=data)
    print(r.status_code, r.reason, r.content)



img = open('media/robot.jpg', 'rb')
video = open('media/animation.mp4', 'rb')

#sendImage(910667518, "The robot!", img)
#sendVideo(910667518, "", video)
#sendMessage(910667518, "test is success!")
