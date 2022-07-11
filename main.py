import cv2
import PLR

plr = PLR.PLR()



for i in range(1,19):   
    txt =''
    image = cv2.imread(f'Placas/{i}.jpg')
    

    txt = plr.readPlate(image)

    plate = plr.plate
    print(txt)
    cv2.imshow("plate", plate)
    cv2.waitKey(0)


   
