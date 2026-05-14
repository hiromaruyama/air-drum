import cv2
import mediapipe as mp
#import mediapipe.python.solutions.hands as mp_hands
#import mediapipe.python.solutions.drawing_utils as mp_draw
import time
import pygame



mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
#Detects if inside the zone.
def inside_zone(x, y, zone):
    x1, y1, x2, y2 = zone
    if x1 <= x <= x2 and y1 <= y <= y2:
      return True
    return False

def main():
    pygame.mixer.init()
    snare_sound = pygame.mixer.Sound('air-Drum/soundEffect/snare.wav')
    hi_hat_sound = pygame.mixer.Sound('air-Drum/soundEffect/hi-hat.wav')
    cymbal_sound = pygame.mixer.Sound('air-Drum/soundEffect/crash-cymbal.wav')
    bass_drum_sound = pygame.mixer.Sound('air-Drum/soundEffect/kick-drum.wav')  
    snare_img = cv2.imread("air-Drum/pictures/snare.jpg")
    hihat_img = cv2.imread("air-Drum/pictures/hi-hat.jpg")
    cymbal_img = cv2.imread("air-Drum/pictures/crash-cymbal.jpg")
    kick_img = cv2.imread("air-Drum/pictures/kick-drum.jpeg")  
    snare_img = cv2.resize(snare_img, (300, 300))
    hihat_img = cv2.resize(hihat_img, (300, 300))
    cymbal_img = cv2.resize(cymbal_img, (300, 300))
    kick_img = cv2.resize(kick_img, (300, 300))

    
    #1) Initialization, capture webcam and hand tracking model
    cap = cv2.VideoCapture(0)
        #creates a Hand Tracking Object.
    hands = mp_hands.Hands(max_num_hands=4,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7)

    prev_y = None
    #2) Main loop, read frames from webcam, process them with the hand tracking model and display the results
    last_hit_time = 0
    cooldown = 0.2
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        current_time = time.time()
        #convert image to RGB and process it with the hand tracking model
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:   
                #Draws hands
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
                
                h,w,c = frame.shape
                frame[0:300, 0:300] = hihat_img
                frame[h-300:h, 0:300] = snare_img
                frame[0:300, w-300:w] = cymbal_img
                frame[h-300:h, w-300:w] = kick_img

                index_finger = hand_landmarks.landmark[6]
                xI = int(index_finger.x * w)
                yI = int(index_finger.y * h)

                cv2.circle(frame, (xI,yI), 10, (0,255,0), cv2.FILLED)
                
                hi_hat = (0, 0, w//4, h//3)
                snare = (0, 2*h//3, w//4, h)
                #snare = (0, h, w//4, 2*h//3)
                cymbal = (3*w//4, 0, w, h//3)
                bass_drum = (3*w//4, 2*h//3, w, h)

                cv2.rectangle(frame, (snare[0], snare[1]), (snare[2], snare[3]), (255,255,255), 2) 
                cv2.rectangle(frame, (hi_hat[0], hi_hat[1]), (hi_hat[2], hi_hat[3]), (255,0,0), 2)
                cv2.rectangle(frame, (cymbal[0], cymbal[1]), (cymbal[2], cymbal[3]), (0,255,255), 2)
                cv2.rectangle(frame, (bass_drum[0], bass_drum[1]), (bass_drum[2], bass_drum[3]), (0,0,255), 2)
                

                cv2.putText(frame, "SNARE", (snare[2]-70, snare[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.putText(frame, "HI-HAT", (hi_hat[2]-70, hi_hat[3]+40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


                cv2.putText(frame, "CYMBAL", (cymbal[0]+10, cymbal[3]+30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.putText(frame, "BASS DRUM", (bass_drum[0]+10, bass_drum[1]-30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                

                if prev_y is not None:
                    if current_time - last_hit_time > cooldown:
                        velocity_y = yI - prev_y
                        if abs(velocity_y) > 80 and inside_zone(xI, yI, snare):
                            snare_sound.play()
                            last_hit_time = current_time
                            cv2.putText(frame, "HIT SNARE!", (w//2, h//2),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                        if abs(velocity_y) > 80 and inside_zone(xI, yI, hi_hat):
                            hi_hat_sound.play()
                            last_hit_time = current_time
                            cv2.putText(frame, "HIT HI-HAT!", (w//2, h//2),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                        if abs(velocity_y) > 80 and inside_zone(xI, yI, cymbal):
                            cymbal_sound.play()
                            last_hit_time = current_time
                            cv2.putText(frame, "HIT CYMBAL!", (w//2, h//2),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                        if abs(velocity_y) > 80 and inside_zone(xI, yI, bass_drum):
                            bass_drum_sound.play()
                            last_hit_time = current_time
                            cv2.putText(frame, "HIT BASS DRUM!", (w//2, h//2),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        
                prev_y = yI

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

main()
