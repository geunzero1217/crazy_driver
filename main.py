import sys
import pygame
import os, random

# 현재 위치 정의
GAME_ROOT_FOLDER = os.path.dirname(__file__)
# 이미지 폴더 위치 정의
IMAGE_FOLDER = os.path.join(GAME_ROOT_FOLDER, "Images")

from pygame.locals import*

#게임 색상 정의하기
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

#게임 변수 초기화 하기
moveSpeed = 5 #적의 움직이는 속도

#게임 끝내기 함수(사용자 정의 함수)
def GameOver():
    pygame.quit()
    sys.exit()

#게임 시작
#파이게임 초기화
pygame.init()

#프레임 매니저 초기화
clock = pygame.time.Clock() #파이게임의 time 라이브러리에서 시계 클래스를 이용해 시간 인스턴스(객체)를 만드는 과정
#프레임 레이트 설정, 1초에 60프레임 또는 그 이하로 화면을 업데이트 하라는 뜻
clock.tick(60)

#제목 표시줄 설정
pygame.display.set_caption("Crazy Driver")

#이미지 불러오기
IMG_ROAD = pygame.image.load(os.path.join(IMAGE_FOLDER, "Road.png"))
IMG_PLAYER = pygame.image.load(os.path.join(IMAGE_FOLDER, "Player.png")) #플레이어 자동차
IMG_ENEMY = pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy.png")) #적 자동차

#게임화면 초기화
screen = pygame.display.set_mode(IMG_ROAD.get_size())

#게임 객체 만들기
#플레이어 초기 위치 계산하기
h= IMG_ROAD.get_width()//2
v= IMG_ROAD.get_height() - (IMG_PLAYER.get_height()//2)
#player 스프라이트 만들기
player = pygame.sprite.Sprite() #Sprite가 클래스를 만드는 것
player.image = IMG_PLAYER
player.surf = pygame.Surface(IMG_PLAYER.get_size())
player.rect = player.surf.get_rect(center=(h,v))

#적
#적 초기 위치 계산하기
hl= IMG_ENEMY.get_width()//2 #가장 왼쪽에 위치 하는 값
hr= IMG_ROAD.get_width() - (IMG_ENEMY.get_width()//2) #가장 오른쪽에 위치 하는 값
h = random.randrange(hl,hr)
v = 0
#enemy 스프라이트 만들기
enemy = pygame.sprite.Sprite() #Sprite가 클래스를 만드는 것
enemy.image = IMG_ENEMY
enemy.surf = pygame.Surface(IMG_ENEMY.get_size())
enemy.rect = enemy.surf.get_rect(center=(h,v))

"""
스프라이트: 컴퓨터 그래픽에서 큰 이미지 위에 놓인 2차원 이미지, 스프라이트는 표시하거나 숨길 수도 있고
움직이거나 회전하거나 다양한 방식으로 변형할 수 도 있음. 게임에서 애니메이션과 움직임 등을 만드는 데 필요한 핵심 요소

자동차는 움직여야하므로 스프라이트로 만든다
"""

#메인 게임 루프
while True:
    #이벤트 확인하기
    #pygame.event.get()은 응답해야할 이벤트들을 리스트 형태로 반환하는데 이를 for 루프에 넣어 모든 이벤트를 대상으로 반복한다.
    for event in pygame.event.get():
        #플레이어가 게임을 그만두는지?
        if event.type==pygame.QUIT: #닫기 아이콘을 눌렀다면 #3번째 줄을 불러왔으니 QUIT만 써도 됨
            #게임 끝내기
            pygame.quit()
            sys.exit()
    
    #배경 이미지 그리기
    screen.blit(IMG_ROAD,(0,0))

    #플레이어 화면에 두기
    screen.blit(player.image, player.rect)

    #키보드를 눌렀을 때
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player.rect.left > 0: #왼쪽 방향키
        player.rect.move_ip(-moveSpeed,0) 
    if keys[K_RIGHT] and player.rect.right < IMG_ROAD.get_width():
        player.rect.move_ip(moveSpeed,0) 


    #적 화면에 두기
    screen.blit(enemy.image, enemy.rect)
    #적을 아래쪽으로 움직이기
    enemy.rect.move_ip(0,moveSpeed) 
    #move_ip : 스프라이트를 움직이는 함수 move_ip(수평으로 움지기이는 픽셀 숫자, 수직으로 움직이는 이는 픽셀 숫자)

    #화면 밖으로 나갔는지 확인하기
    if(enemy.rect.bottom>IMG_ROAD.get_height()):
        hl= IMG_ENEMY.get_width()//2 #가장 왼쪽에 위치 하는 값
        hr= IMG_ROAD.get_width() - (IMG_ENEMY.get_width()//2) #가장 오른쪽에 위치 하는 값
        h = random.randrange(hl,hr)
        v = 0
        #화면에 두기
        enemy.rect.center = (h,v)
        
        #중복코드의 문제점이 존재!

    #충돌 확인하기
    #player와 enemy의 스프라이트가 겹치는지를 확인
    #collide_rect() : 충돌감지 함수
    if pygame.sprite.collide_rect(player, enemy): 
        #충돌, 게임 오버 함수 호출
        GameOver()
    
    #화면 업데이트
    pygame.display.update()
