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
    pygame.mixer.pre_init(44100, -16, 2, 512) #To reduce lag of the sound
    pygame.mixer.init()
    
    snare_img = cv2.imread("pictures/snare.png")
    hihat_img = cv2.imread("pictures/hiHat.png")
    cymbal_img = cv2.imread("pictures/cymbal.png")
    bass_img = cv2.imread("pictures/bass.png")  

    print(snare_img.shape)
    
    #1) Initialization, capture webcam and hand tracking model
    cap = cv2.VideoCapture(0)
        #creates a Hand Tracking Object.
    hands = mp_hands.Hands(max_num_hands=4,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7)

    prev_y = None
    last_hit_time = 0
    cooldown = 0.2
    hit_state = {"Cymbal": 0, "Hi-Hat": 0, "Snare": 0, "Bass": 0}
    
    #2) Main loop, read frames from webcam, process them with the hand tracking model and display the results
    while True:
    
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        current_time = time.time()
        #convert image to RGB and process it with the hand tracking model
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        h,w,c = frame.shape
        instruments = {
        "Cymbal": {"color": (0, 255, 255), "sound_file": "soundEffect/cymbal.wav", "box": (3*w//4, 0, w, h//3), "sound": pygame.mixer.Sound('soundEffect/cymbal.wav')},
        "Hi-Hat": {"color": (0, 165, 255), "sound_file": "soundEffect/hiHat.wav", "box": (0, 0, w//4, h//3), "sound": pygame.mixer.Sound('soundEffect/hihat.wav')},
        "Snare":  {"color": (0, 0, 255), "sound_file": "soundEffect/snare.wav", "box": (0, 2*h//3, w//4, h), "sound": pygame.mixer.Sound('soundEffect/snare.wav')},
        "Bass":   {"color": (255, 0, 0), "sound_file": "soundEffect/bass.wav", "box": (3*w//4, 2*h//3, w, h), "sound": pygame.mixer.Sound('soundEffect/bass.wav')}
        } 
    # snare_sound = pygame.mixer.Sound('soundEffect/snare.wav')
    # hi_hat_sound = pygame.mixer.Sound('soundEffect/hihat.wav')
    # cymbal_sound = pygame.mixer.Sound('soundEffect/cymbal.wav')
    #bass_drum_sound = pygame.mixer.Sound('soundEffect/bass.wav')  
        current_hits = {name: 0 for name in instruments}
        #resize
        snare_img = cv2.resize(snare_img, ((w//4, h//3)))
        hihat_img = cv2.resize(hihat_img, (w//4, h//3))
        cymbal_img = cv2.resize(cymbal_img, ((w//4, h//3)))
        bass_img = cv2.resize(bass_img, ((w//4, h//3)))
        frame[0:h//3, 0:w//4] = hihat_img
        frame[2*h//3:h, 0:w//4] = snare_img
        frame[0:h//3, 3*w//4:w] = cymbal_img
        frame[2*h//3:h, 3*w//4:w] = bass_img



        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:   
                #Draws hands
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
                
                
                index_finger = hand_landmarks.landmark[6]
                xI = int(index_finger.x * w)
                yI = int(index_finger.y * h)

                cv2.circle(frame, (xI,yI), 10, (0,255,0), cv2.FILLED)
                
                hi_hat = (0, 0, w//4, h//3)
                snare = (0, 2*h//3, w//4, h)
                #snare = (0, h, w//4, 2*h//3)
                cymbal = (3*w//4, 0, w, h//3)
                bass_drum = (3*w//4, 2*h//3, w, h)

                cv2.rectangle(frame, (instruments["Snare"]["box"][0], instruments["Snare"]["box"][1]), (instruments["Snare"]["box"][2], instruments["Snare"]["box"][3]), (255,255,255), 2) 
                cv2.rectangle(frame, (instruments["Hi-Hat"]["box"][0], instruments["Hi-Hat"]["box"][1]), (instruments["Hi-Hat"]["box"][2], instruments["Hi-Hat"]["box"][3]), (255,0,0), 2)
                cv2.rectangle(frame, (instruments["Cymbal"]["box"][0], instruments["Cymbal"]["box"][1]), (instruments["Cymbal"]["box"][2], instruments["Cymbal"]["box"][3]), (0,255,255), 2)
                cv2.rectangle(frame, (instruments["Bass"]["box"][0], instruments["Bass"]["box"][1]), (instruments["Bass"]["box"][2], instruments["Bass"]["box"][3]), (0,0,255), 2)
                

                cv2.putText(frame, "SNARE", (snare[2]-70, snare[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.putText(frame, "HI-HAT", (hi_hat[2]-70, hi_hat[3]+40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


                cv2.putText(frame, "CYMBAL", (cymbal[0]+10, cymbal[3]+30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.putText(frame, "BASS DRUM", (bass_drum[0]+10, bass_drum[1]-30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
                for name, data in instruments.items():
                    if inside_zone(xI,yI, data["box"]):
                        current_hits[name] +=1
                
            if current_time - last_hit_time > cooldown:
                for name, data in instruments.items():
                    if current_hits[name] > hit_state[name]:
                        data["sound"].play()
                        last_hit_time = current_time
                        cv2.putText(frame, f"HIT {name}!", (w//2, h//2), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                    hit_state[name] = current_hits[name]

        cv2.imshow("Drum Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

main()
