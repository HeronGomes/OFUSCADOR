# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

imagem = cv.imread('cnh.jpg')


imagem = cv.resize(imagem,(400,200))

imagem_complemento = np.zeros((30,400,3),dtype=np.uint8)

list_rect_selecionados = list()


def pixel_face(imagemParam,blocos=3):
    (h,w) = imagemParam.shape[:2]
    xSteps = np.linspace(0,w,blocos +1, dtype='int')
    ySteps = np.linspace(0,h,blocos +1, dtype='int')
    
    for i in range(1,len(ySteps)):
        for j in range(1,len(xSteps)):
            startX = xSteps[j - 1]
            startY = ySteps[i - 1]
            endX = xSteps[j]
            endY = ySteps[i]
    
            roi = imagemParam[startY:endY,startX:endX]
            (B,G,R) = [int(x) for x in cv.mean(roi)[:3]]
            cv.rectangle(
                imagemParam,
                (startX,startY),
                (endX,endY),
                (B,G,R),
                -1        
                )

    return imagemParam

cv.putText(
    imagem_complemento,
    '(q - Sair)(c - Cancelar Selecao)',
    (5,10),
    cv.FONT_HERSHEY_COMPLEX_SMALL,
    0.5,
    (255,127,255),
    1,
    cv.LINE_AA 
    
    )

cv.putText(
    imagem_complemento,
    '([Espaco] - Confirmar Selecao)',
    (5,25),
    cv.FONT_HERSHEY_COMPLEX_SMALL,
    0.5,
    (255,127,255),
    1,
    cv.LINE_AA 
    
    )


imagem_exibicao = cv.vconcat([imagem,imagem_complemento])


while True:

    
    rect = cv.selectROI('Ofuscador',imagem_exibicao,False,None)
    
    if rect and np.sum(rect) > 0:
        list_rect_selecionados.append(rect)


    key = cv.waitKey()
    if key == ord('q'):
        break

cv.destroyAllWindows()



for roi in list_rect_selecionados:
    
    x0,y0,w,h = roi
    
    imagem[y0:(y0+h),x0:(x0+w)] = pixel_face(imagem[y0:(y0+h),x0:(x0+w)],15)
    
    cv.imshow('Ofuscador',imagem)
    cv.waitKey()
    cv.destroyAllWindows()

