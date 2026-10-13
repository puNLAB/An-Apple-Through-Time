# # import mediapipe as mp
# # import cv2
# # import math
# # import numpy as np
# # from collections import deque

# # # MediaPipe setup
# # mp_hands = mp.solutions.hands
# # hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # # Circular buffer to store recent distances
# # distance_buffer = deque(maxlen=30)  # Keeps the last 30 distances (about 1 second at 30 FPS)

# # # Start video capture
# # cap = cv2.VideoCapture(0)  # 0 for the default camera

# # # Set window size to make the video larger
# # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width to 1280 pixels
# # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height to 720 pixels

# # # Function to calculate 3D Euclidean distance in real-world cm
# # def calculate_3d_distance(hand1, hand2):
# #     x1, y1, z1 = hand1
# #     x2, y2, z2 = hand2
# #     real_world_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100  # Scaling factor
# #     return real_world_distance

# # # Function to detect "Point" gesture
# # def is_point_gesture(hand_landmarks):
# #     extended_fingers = []
# #     for i in [8, 12, 16, 20]:  # Tip landmarks of index, middle, ring, and pinky fingers
# #         tip = hand_landmarks.landmark[i]
# #         pip = hand_landmarks.landmark[i - 2]
# #         extended_fingers.append(tip.y < pip.y)  # Check if the finger is extended

# #     thumb_tip = hand_landmarks.landmark[4]
# #     thumb_ip = hand_landmarks.landmark[3]
# #     thumb_extended = thumb_tip.x > thumb_ip.x  # Check thumb direction

# #     return extended_fingers == [True, False, False, False] and not thumb_extended

# # # Function to draw ripples on the frame
# # def draw_ripples(frame, center, ripples, max_radius):
# #     for radius in ripples:
# #         alpha = max(0, 255 - int((radius / max_radius) * 255))  # Fade effect
# #         overlay = frame.copy()
# #         cv2.circle(overlay, center, int(radius), (255, 255, 255, alpha), thickness=2)
# #         frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
# #     return frame

# # # Initialize ripples
# # ripple_centers = []
# # ripple_radii = []
# # max_ripple_radius = 200
# # ripple_speed = 5

# # while cap.isOpened():
# #     success, img = cap.read()
# #     img = cv2.flip(img, 1)
# #     if not success:
# #         print("Ignoring empty camera frame.")
# #         continue

# #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #     results = hands.process(img_rgb)

# #     hand_positions = []
# #     if results.multi_hand_landmarks:
# #         for hand_landmarks in results.multi_hand_landmarks:
# #             # Collect middle finger tip (ID 12) for distance calculation
# #             middle_finger_x = hand_landmarks.landmark[12].x
# #             middle_finger_y = hand_landmarks.landmark[12].y
# #             middle_finger_z = hand_landmarks.landmark[12].z
# #             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

# #             # Check for "Point" gesture
# #             if is_point_gesture(hand_landmarks):
# #                 finger_tip_x = int(hand_landmarks.landmark[8].x * img.shape[1])
# #                 finger_tip_y = int(hand_landmarks.landmark[8].y * img.shape[0])
# #                 ripple_centers.append((finger_tip_x, finger_tip_y))
# #                 ripple_radii.append(0)

# #         # Calculate distance and midpoint if two hands are detected
# #         if len(hand_positions) == 2:
# #             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
# #             distance_buffer.append(distance)  # Add the new distance to the buffer

# #             # Calculate the midpoint (average) between the two hands
# #             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
# #             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

# #             # Adjust the y-position downward by 100 pixels (~10 cm)
# #             midpoint_x_px = int(midpoint_x * img.shape[1])
# #             midpoint_y_px = int(midpoint_y * img.shape[0] + 100)  # Total 100 pixels (10 cm down)
# #             dynamic_radius = int(distance * 4)  # Quadruple the radius (original * 2 * 2)
# #             cv2.circle(img, (midpoint_x_px, midpoint_y_px), dynamic_radius, (255, 0, 0), -1)  # Blue circle

# #             # Display the current distance on screen with smaller text
# #             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
# #                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  # Reduced text size
# #             print(f"Hand Distance: {distance:.2f} cm")

# #     # Update ripples
# #     ripple_radii = [r + ripple_speed for r in ripple_radii]
# #     ripple_centers = [c for c, r in zip(ripple_centers, ripple_radii) if r < max_ripple_radius]
# #     ripple_radii = [r for r in ripple_radii if r < max_ripple_radius]

# #     # Draw ripples on the frame
# #     for center in ripple_centers:
# #         img = draw_ripples(img, center, ripple_radii, max_ripple_radius)

# #     # Draw a small graph of recent distances for debugging
# #     for i, d in enumerate(distance_buffer):
# #         cv2.line(img, (50 + i * 10, 150), (50 + i * 10, 150 - int(d / 2)), (255, 255, 255), 2)

# #     # Display the video with larger window size
# #     cv2.imshow("MediaPipe Hands with Hidden Lines, Dynamic Circle, and Ripple Effects", img)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
# #         break

# # cap.release()
# # cv2.destroyAllWindows()


# #-------------------------------------------------------------------------------------------------------------------------------#


# # #可缩放蓝色圆球，白色波纹从指尖溢出

# # import mediapipe as mp
# # import cv2
# # import math
# # import numpy as np
# # from collections import deque

# #  # MediaPipe setup
# # mp_hands = mp.solutions.hands
# # hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# #  # Circular buffer to store recent distances
# # distance_buffer = deque(maxlen=30)  # Keeps the last 30 distances (about 1 second at 30 FPS)

# #  # Start video capture
# # cap = cv2.VideoCapture(0)  # 0 for the default camera

# #  # Set window size to make the video larger
# # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width to 1280 pixels
# # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height to 720 pixels

# #  # Function to calculate 3D Euclidean distance in real-world cm
# # def calculate_3d_distance(hand1, hand2):
# #     x1, y1, z1 = hand1
# #     x2, y2, z2 = hand2
# #     real_world_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100  # Scaling factor
# #     return real_world_distance

# #  # Function to detect "Point" gesture
# # def is_point_gesture(hand_landmarks):
# #     extended_fingers = []
# #     for i in [8, 12, 16, 20]:  # Tip landmarks of index, middle, ring, and pinky fingers
# #         tip = hand_landmarks.landmark[i]
# #         pip = hand_landmarks.landmark[i - 2]
# #         extended_fingers.append(tip.y < pip.y)  # Check if the finger is extended

# #     thumb_tip = hand_landmarks.landmark[4]
# #     thumb_ip = hand_landmarks.landmark[3]
# #     thumb_extended = thumb_tip.x > thumb_ip.x  # Check thumb direction

# #     return extended_fingers == [True, False, False, False] and not thumb_extended

# #  # Function to draw ripples on the frame
# # def draw_ripples(frame, center, ripples, max_radius):
# #     for radius in ripples:
# #         alpha = max(0, 255 - int((radius / max_radius) * 255))  # Fade effect
# #         overlay = frame.copy()
# #         cv2.circle(overlay, center, int(radius), (255, 255, 255, alpha), thickness=2)
# #         frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
# #     return frame

# #  # Initialize ripples
# # ripple_centers = deque(maxlen=30)
# # ripple_radii = deque(maxlen=30)
# # max_ripple_radius = 200
# # ripple_speed = 5

# # while cap.isOpened():
# #     success, img = cap.read()
# #     img = cv2.flip(img, 1)
# #     if not success:
# #         print("Ignoring empty camera frame.")
# #         continue

# #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #     results = hands.process(img_rgb)

# #     hand_positions = []
# #     if results.multi_hand_landmarks:
# #         for hand_landmarks in results.multi_hand_landmarks:
# #             # Collect middle finger tip (ID 12) for distance calculation
# #             middle_finger_x = hand_landmarks.landmark[12].x
# #             middle_finger_y = hand_landmarks.landmark[12].y
# #             middle_finger_z = hand_landmarks.landmark[12].z
# #             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

# #             # Check for "Point" gesture
# #             if is_point_gesture(hand_landmarks):
# #                 finger_tip_x = int(hand_landmarks.landmark[8].x * img.shape[1])
# #                 finger_tip_y = int(hand_landmarks.landmark[8].y * img.shape[0])
# #                 ripple_centers.append((finger_tip_x, finger_tip_y))
# #                 ripple_radii.append(0)

# #          # Calculate distance and midpoint if two hands are detected
# #         if len(hand_positions) == 2:
# #             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
# #             distance_buffer.append(distance)  # Add the new distance to the buffer

# #             # Calculate the midpoint (average) between the two hands
# #             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
# #             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

# #             # Adjust the y-position downward by 100 pixels (~10 cm)
# #             midpoint_x_px = int(midpoint_x * img.shape[1])
# #             midpoint_y_px = int(midpoint_y * img.shape[0] + 100)  # Total 100 pixels (10 cm down)
# #             dynamic_radius = int(distance * 4)  # Quadruple the radius (original * 2 * 2)
# #             cv2.circle(img, (midpoint_x_px, midpoint_y_px), dynamic_radius, (255, 0, 0), -1)  # Blue circle

# #             # Display the current distance on screen with smaller text
# #             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
# #                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  # Reduced text size
# #             print(f"Hand Distance: {distance:.2f} cm")

# #     # Update ripples
# #     for i in range(len(ripple_radii)):
# #         ripple_radii[i] += ripple_speed
# #     while len(ripple_radii) > 0 and ripple_radii[0] >= max_ripple_radius:
# #         ripple_centers.popleft()
# #         ripple_radii.popleft()

# #      # Draw ripples on the frame
# #     for center, radius in zip(ripple_centers, ripple_radii):
# #         img = draw_ripples(img, center, [radius], max_ripple_radius)

# #      # Draw a small graph of recent distances for debugging
# #     for i, d in enumerate(distance_buffer):
# #         cv2.line(img, (50 + i * 10, 150), (50 + i * 10, 150 - int(d / 2)), (255, 255, 255), 2)

# #      # Display the video with larger window size
# #     cv2.imshow("MediaPipe Hands with Hidden Lines, Dynamic Circle, and Ripple Effects", img)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
# #         break

# # cap.release()
# # cv2.destroyAllWindows()


# #------------------------------------------------------------------------------------------------------------------

# #全屏哈哈镜

# # import mediapipe as mp
# # import cv2
# # import math
# # import numpy as np
# # from collections import deque

# # # MediaPipe setup
# # mp_hands = mp.solutions.hands
# # hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # # Circular buffer to store recent distances
# # distance_buffer = deque(maxlen=30)  # Keeps the last 30 distances (about 1 second at 30 FPS)

# # # Start video capture
# # cap = cv2.VideoCapture(0)  # 0 for the default camera

# # # Set window size to make the video larger
# # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width to 1280 pixels
# # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height to 720 pixels

# # # Function to calculate 3D Euclidean distance in real-world cm
# # def calculate_3d_distance(hand1, hand2):
# #     x1, y1, z1 = hand1
# #     x2, y2, z2 = hand2
# #     real_world_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100  # Scaling factor
# #     return real_world_distance

# # # Function to detect "Point" gesture
# # def is_point_gesture(hand_landmarks):
# #     extended_fingers = []
# #     for i in [8, 12, 16, 20]:  # Tip landmarks of index, middle, ring, and pinky fingers
# #         tip = hand_landmarks.landmark[i]
# #         pip = hand_landmarks.landmark[i - 2]
# #         extended_fingers.append(tip.y < pip.y)  # Check if the finger is extended

# #     thumb_tip = hand_landmarks.landmark[4]
# #     thumb_ip = hand_landmarks.landmark[3]
# #     thumb_extended = thumb_tip.x > thumb_ip.x  # Check thumb direction

# #     return extended_fingers == [True, False, False, False] and not thumb_extended

# # # Function to apply ripple-like distortion
# # def apply_ripple_effect(frame, center, max_radius, frequency):
# #     height, width = frame.shape[:2]
# #     y, x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    
# #     # Calculate distances from the ripple center
# #     distances = np.sqrt((x - center[0])**2 + (y - center[1])**2)

# #     # Generate sinusoidal wave for distortion
# #     ripple = np.sin((distances / max_radius) * 2 * np.pi * frequency) * 10

# #     # Map distortion to coordinates
# #     map_x = (x + ripple).astype(np.float32)
# #     map_y = (y + ripple).astype(np.float32)

# #     # Apply the distortion to the frame
# #     distorted_frame = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
# #     return distorted_frame

# # # Initialize variables for ripple effect
# # ripple_center = None
# # max_ripple_radius = 200
# # ripple_frequency = 2

# # while cap.isOpened():
# #     success, img = cap.read()
# #     img = cv2.flip(img, 1)
# #     if not success:
# #         print("Ignoring empty camera frame.")
# #         continue

# #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #     results = hands.process(img_rgb)

# #     hand_positions = []
# #     if results.multi_hand_landmarks:
# #         for hand_landmarks in results.multi_hand_landmarks:
# #             # Collect middle finger tip (ID 12) for distance calculation
# #             middle_finger_x = hand_landmarks.landmark[12].x
# #             middle_finger_y = hand_landmarks.landmark[12].y
# #             middle_finger_z = hand_landmarks.landmark[12].z
# #             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

# #             # Check for "Point" gesture
# #             if is_point_gesture(hand_landmarks):
# #                 finger_tip_x = int(hand_landmarks.landmark[8].x * img.shape[1])
# #                 finger_tip_y = int(hand_landmarks.landmark[8].y * img.shape[0])
# #                 ripple_center = (finger_tip_x, finger_tip_y)

# #         # Calculate distance and midpoint if two hands are detected
# #         if len(hand_positions) == 2:
# #             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
# #             distance_buffer.append(distance)  # Add the new distance to the buffer

# #             # Calculate the midpoint (average) between the two hands
# #             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
# #             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

# #             # Adjust the y-position downward by 100 pixels (~10 cm)
# #             midpoint_x_px = int(midpoint_x * img.shape[1])
# #             midpoint_y_px = int(midpoint_y * img.shape[0] + 100)  # Total 100 pixels (10 cm down)
# #             dynamic_radius = int(distance * 4)  # Quadruple the radius (original * 2 * 2)
# #             cv2.circle(img, (midpoint_x_px, midpoint_y_px), dynamic_radius, (255, 0, 0), -1)  # Blue circle

# #             # Display the current distance on screen with smaller text
# #             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
# #                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  # Reduced text size
# #             print(f"Hand Distance: {distance:.2f} cm")

# #     # Apply ripple effect if center is set
# #     if ripple_center:
# #         img = apply_ripple_effect(img, ripple_center, max_ripple_radius, ripple_frequency)

# #     # Draw a small graph of recent distances for debugging
# #     for i, d in enumerate(distance_buffer):
# #         cv2.line(img, (50 + i * 10, 150), (50 + i * 10, 150 - int(d / 2)), (255, 255, 255), 2)

# #     # Display the video with larger window size
# #     cv2.imshow("MediaPipe Hands with Ripple Effect", img)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
# #         break

# # cap.release()
# # cv2.destroyAllWindows()



# #-----------------------------------------------------------------------------------------------------------------------------#

# # import mediapipe as mp
# # import cv2
# # import math
# # import numpy as np
# # from collections import deque
# # import pywavefront  # Library for loading .obj files

# # # MediaPipe setup
# # mp_hands = mp.solutions.hands
# # hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # # Circular buffer to store recent distances
# # distance_buffer = deque(maxlen=30)  # Keeps the last 30 distances (about 1 second at 30 FPS)

# # # Start video capture
# # cap = cv2.VideoCapture(0)  # 0 for the default camera

# # # Set window size to make the video larger
# # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width to 1280 pixels
# # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height to 720 pixels

# # # Load the apple.obj file
# # apple_model = pywavefront.Wavefront('apple.obj', collect_faces=True)

# # def render_apple_on_frame(frame, center, scale):
# #     """
# #     Overlay a 3D model (apple.obj) on the frame at the specified center position.
# #     """
# #     h, w, _ = frame.shape
# #     x, y = center

# #     # Placeholder to render the apple model
# #     # Use OpenGL or other tools for 3D rendering here
# #     cv2.putText(frame, "Rendering apple.obj here!", (x - 50, y - 10),
# #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
# #     return frame

# # # Function to calculate 3D Euclidean distance in real-world cm
# # def calculate_3d_distance(hand1, hand2):
# #     x1, y1, z1 = hand1
# #     x2, y2, z2 = hand2
# #     real_world_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100  # Scaling factor
# #     return real_world_distance

# # while cap.isOpened():
# #     success, img = cap.read()
# #     img = cv2.flip(img, 1)
# #     if not success:
# #         print("Ignoring empty camera frame.")
# #         continue

# #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #     results = hands.process(img_rgb)

# #     hand_positions = []
# #     if results.multi_hand_landmarks:
# #         for hand_landmarks in results.multi_hand_landmarks:
# #             # Collect middle finger tip (ID 12) for distance calculation
# #             middle_finger_x = hand_landmarks.landmark[12].x
# #             middle_finger_y = hand_landmarks.landmark[12].y
# #             middle_finger_z = hand_landmarks.landmark[12].z
# #             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

# #         # Calculate distance and midpoint if two hands are detected
# #         if len(hand_positions) == 2:
# #             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
# #             distance_buffer.append(distance)  # Add the new distance to the buffer

# #             # Calculate the midpoint (average) between the two hands
# #             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
# #             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

# #             # Adjust the midpoint for placement
# #             midpoint_x_px = int(midpoint_x * img.shape[1])
# #             midpoint_y_px = int(midpoint_y * img.shape[0])

# #             # Render the apple.obj at the midpoint
# #             img = render_apple_on_frame(img, (midpoint_x_px, midpoint_y_px), scale=1.0)

# #     # Draw a small graph of recent distances for debugging
# #     for i, d in enumerate(distance_buffer):
# #         cv2.line(img, (50 + i * 10, 150), (50 + i * 10, 150 - int(d / 2)), (255, 255, 255), 2)

# #     # Display the video with larger window size
# #     cv2.imshow("MediaPipe Hands with apple.obj Overlay", img)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
# #         break

# # cap.release()
# # cv2.destroyAllWindows()


# #-------------------------------------------------------------------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple image (placeholder for apple.obj)
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     if apple_img is None:
#         return frame
#     h, w, _ = apple_img.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple_img, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = (1 - alpha) * frame[y1:y2, x1:x2, c] + alpha * apple_resized[:, :, c]
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         # Calculate distance and midpoint if two hands are detected
#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             # Overlay apple at the midpoint
#             img = overlay_apple(img, (midpoint_x_px, midpoint_y_px), scale=distance / 50)

#             # Display the current distance on screen
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Draw a small graph of recent distances
#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 150), (50 + i * 10, 150 - int(d / 2)), (255, 255, 255), 2)

#     # Display the video
#     cv2.imshow("MediaPipe Hands with Apple Overlay", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#------------------------------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple image (placeholder for apple.obj)
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     if apple_img is None:
#         return frame
#     h, w, _ = apple_img.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple_img, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = (1 - alpha) * frame[y1:y2, x1:x2, c] + alpha * apple_resized[:, :, c]
#     return frame

# # Function to draw the ruler line and arrow
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the horizontal ruler line
#     cv2.line(frame, (50, line_y), (w - 50, line_y), (0, 255, 0), 2)
#     cv2.arrowedLine(frame, (50, line_y), (apple_center[0], line_y), (0, 0, 255), 2)

#     # Add axis labels
#     cv2.putText(frame, 'Time', (50, line_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#     cv2.putText(frame, f'Growing: {apple_center[0]} ', (apple_center[0] - 50, line_y - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)  # Default center position

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         # Calculate distance and midpoint if two hands are detected
#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             img = overlay_apple(img, apple_center, scale=distance / 50)

#             # Display the current distance on screen
#             cv2.putText(img, f"Size: {distance:.2f} ", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Draw the ruler line and axis arrow
#     img = draw_ruler(img, apple_center)

#     # Draw a small graph of recent distances
#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 150), (50 + i * 10, 150 - int(d / 2)), (255, 255, 255), 2)

#     # Display the video
#     cv2.imshow("MediaPipe Hands with Apple Overlay and Ruler Line", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#------------------------------------手势控停苹果大小----------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque

# global apple_locked, locked_size

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple image
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)

# # Variables for locked apple size
# apple_locked = False
# locked_size = None

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     if apple_img is None:
#         return frame
#     h, w, _ = apple_img.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple_img, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = (1 - alpha) * frame[y1:y2, x1:x2, c] + alpha * apple_resized[:, :, c]
#     return frame

# # Function to detect if a hand is in a fist gesture
# def is_fist_gesture(hand_landmarks):
#     fingers_closed = []
#     for i in [8, 12, 16, 20]:  # Tip landmarks of index, middle, ring, and pinky fingers
#         tip = hand_landmarks.landmark[i]
#         pip = hand_landmarks.landmark[i - 2]
#         fingers_closed.append(tip.y > pip.y)  # Check if the finger is closed
#     return all(fingers_closed)

# # Function to draw the ruler line and arrow
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the horizontal ruler line
#     cv2.line(frame, (50, line_y), (w - 50, line_y), (0, 255, 0), 2)
#     cv2.arrowedLine(frame, (50, line_y), (apple_center[0], line_y), (0, 0, 255), 2)

#     # Add axis labels
#     cv2.putText(frame, 'Time', (50, line_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)  # Default center position


#     if results.multi_hand_landmarks:
#         fists_detected = 0
#         for hand_landmarks in results.multi_hand_landmarks:
#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#             if is_fist_gesture(hand_landmarks):
#                 fists_detected += 1

#         # Lock apple size when two fists are detected
#         if fists_detected == 2 and not apple_locked:
#             apple_locked = True
#             locked_size = calculate_3d_distance(hand_positions[0], hand_positions[1])

#         # Calculate distance and midpoint if two hands are detected
#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = locked_size / 50 if apple_locked else distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)

#             # Display the current distance on screen
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Draw the ruler line
#     img = draw_ruler(img, apple_center)

#     # Draw a small graph of recent distances
#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     # Display the video
#     cv2.imshow("MediaPipe Hands with Apple Overlay and Fist Lock", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#----------------------------------------手势识别是否固定、重启苹果大小变化-----------------------------------------------------------------------


# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple image
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)

# # Variables for locked apple size
# apple_locked = False
# locked_size = None
# last_fist_time = time.time()  # To track the time of the last fist detection
# cooldown_interval = 3  # 3-second cooldown interval

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     if apple_img is None:
#         return frame
#     h, w, _ = apple_img.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple_img, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect if a hand is in a fist gesture
# def is_fist_gesture(hand_landmarks):
#     fingers_closed = []
#     for i in [8, 12, 16, 20]:  # Tip landmarks of index, middle, ring, and pinky fingers
#         tip = hand_landmarks.landmark[i]
#         pip = hand_landmarks.landmark[i - 2]
#         fingers_closed.append(tip.y > pip.y)  # Check if the finger is closed
#     return all(fingers_closed)

# # Function to draw the ruler line and arrow
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the horizontal ruler line
#     cv2.line(frame, (50, line_y), (w - 50, line_y), (0, 255, 0), 2)
#     cv2.arrowedLine(frame, (50, line_y), (apple_center[0], line_y), (0, 0, 255), 2)

#     # Add axis labels
#     cv2.putText(frame, 'Time', (50, line_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)  # Default center position
#     current_time = time.time()

#     if results.multi_hand_landmarks:
#         fists_detected = 0
#         for hand_landmarks in results.multi_hand_landmarks:
#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#             if is_fist_gesture(hand_landmarks):
#                 fists_detected += 1

#         # Lock or unlock apple size based on fist gestures and 3-second timer
#         if fists_detected == 2 and (current_time - last_fist_time >= cooldown_interval):
#             if not apple_locked:  # Lock size
#                 apple_locked = True
#                 locked_size = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             else:  # Unlock size after 3 seconds
#                 apple_locked = False
#                 locked_size = None
#             last_fist_time = current_time

#         # Calculate distance and midpoint if two hands are detected
#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = locked_size / 50 if apple_locked else distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)

#             # Display the current distance on screen
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Draw the ruler line
#     img = draw_ruler(img, apple_center)

#     # Draw a small graph of recent distances
#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     # Display the video
#     cv2.imshow("MediaPipe Hands with Apple Overlay and Fist Lock", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#-----------------------------------------emoji变苹果-----------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# import time
# from collections import deque

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_fixed_img = cv2.imread('apple_1.png', cv2.IMREAD_UNCHANGED)

# # Variables for locked apple size and timing
# apple_locked = False
# locked_size = None
# lock_time = None  # Track the time when apple size is locked

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0, locked=False):
#     apple = apple_fixed_img if locked else apple_img  # Choose the correct image
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect if a hand is in a fist gesture
# def is_fist_gesture(hand_landmarks):
#     fingers_closed = []
#     for i in [8, 12, 16, 20]:  # Tip landmarks of index, middle, ring, and pinky fingers
#         tip = hand_landmarks.landmark[i]
#         pip = hand_landmarks.landmark[i - 2]
#         fingers_closed.append(tip.y > pip.y)  # Check if the finger is closed
#     return all(fingers_closed)

# # Function to draw the ruler line and arrow
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the horizontal ruler line
#     cv2.line(frame, (50, line_y), (w - 50, line_y), (0, 255, 0), 2)
#     cv2.arrowedLine(frame, (50, line_y), (apple_center[0], line_y), (0, 0, 255), 2)

#     # Add axis labels
#     cv2.putText(frame, 'Time', (50, line_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)  # Default center position
#     current_time = time.time()

#     fists_detected = 0
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#             if is_fist_gesture(hand_landmarks):
#                 fists_detected += 1

#         # Lock or unlock apple size based on fist gestures and 3-second timer
#         if fists_detected == 2 and (current_time - lock_time >= 3 if lock_time else True):
#             if not apple_locked:  # Lock size
#                 apple_locked = True
#                 locked_size = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             lock_time = current_time  # Start or reset timer

#         # Calculate distance and midpoint if two hands are detected
#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = locked_size / 50 if apple_locked else distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use, locked=apple_locked)

#             # Display the current distance on screen
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Draw the ruler line
#     img = draw_ruler(img, apple_center)

#     # Draw a small graph of recent distances
#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     # Display the video
#     cv2.imshow("MediaPipe Hands with Apple Image Lock Toggle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#----------------------------------------------emoji变苹果，苹果变emoji------------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_fixed_img = cv2.imread('apple_1.png', cv2.IMREAD_UNCHANGED)

# # Variables for locked apple size and state
# display_fixed_image = False  # Toggle between apple.png and apple_1.png
# apple_locked = False
# locked_size = None
# last_fist_time = time.time()  # Time of the last fist detection
# cooldown_interval = 3  # 3-second cooldown interval

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0, locked=False):
#     apple = apple_fixed_img if locked else apple_img  # Choose the correct image
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect if a hand is in a fist gesture
# def is_fist_gesture(hand_landmarks):
#     fingers_closed = []
#     for i in [8, 12, 16, 20]:  # Tip landmarks of index, middle, ring, and pinky fingers
#         tip = hand_landmarks.landmark[i]
#         pip = hand_landmarks.landmark[i - 2]
#         fingers_closed.append(tip.y > pip.y)  # Check if the finger is closed
#     return all(fingers_closed)

# # Function to draw the ruler line and arrow
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the horizontal ruler line
#     cv2.line(frame, (50, line_y), (w - 50, line_y), (0, 255, 0), 2)
#     cv2.arrowedLine(frame, (50, line_y), (apple_center[0], line_y), (0, 0, 255), 2)

#     # Add axis labels
#     cv2.putText(frame, 'Time', (50, line_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)  # Default center position
#     current_time = time.time()

#     fists_detected = 0
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#             if is_fist_gesture(hand_landmarks):
#                 fists_detected += 1

#         # Toggle between locked and unlocked states every 3 seconds
#         if fists_detected == 2 and (current_time - last_fist_time >= cooldown_interval):
#             display_fixed_image = not display_fixed_image  # Toggle image
#             if display_fixed_image:  # Lock size
#                 apple_locked = True
#                 locked_size = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             else:  # Unlock size
#                 apple_locked = False
#                 locked_size = None
#             last_fist_time = current_time  # Reset the timer

#         # Calculate distance and midpoint if two hands are detected
#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = locked_size / 50 if apple_locked else distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use, locked=display_fixed_image)

#             # Display the current distance on screen
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Draw the ruler line
#     img = draw_ruler(img, apple_center)

#     # Draw a small graph of recent distances
#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     # Display the video
#     cv2.imshow("MediaPipe Hands with Apple Image Toggle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#--------------------------------------------------------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_fixed_img = cv2.imread('apple_1.png', cv2.IMREAD_UNCHANGED)

# # Variables for locked apple size and state
# display_fixed_image = False
# apple_locked = False
# locked_size = None
# last_fist_time = time.time()
# cooldown_interval = 3

# # Function to calculate 3D Euclidean distance
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0, locked=False):
#     apple = apple_fixed_img if locked else apple_img
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to draw the gradient line and blue rectangle
# def draw_gradient_ruler_with_rectangle(frame, rect_x):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position of the gradient line
#     rect_y = line_y - 10  # Blue rectangle position
#     rect_width = 20
#     rect_height = 20

#     # Create gradient colors for the line
#     for i in range(w - 100):  # Exclude 50px margins on both sides
#         ratio = i / (w - 100)
#         color = (0, int(255 * (1 - ratio)), int(255 * ratio))  # Gradient from green to red
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)

#     # Draw the blue rectangle
#     rect_x1 = rect_x - rect_width // 2
#     rect_x2 = rect_x + rect_width // 2
#     cv2.rectangle(frame, (rect_x1, rect_y), (rect_x2, rect_y + rect_height), (255, 0, 0), -1)

#     # Add "growing" text above the rectangle
#     cv2.putText(frame, "growing", (rect_x - 30, rect_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     rect_x = apple_center[0]  # Default x-axis position for the rectangle

#     if results.multi_hand_landmarks:
#         hand_positions = []
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Get hand positions
#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])
#             rect_x = midpoint_x_px  # Update rectangle position

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             img = overlay_apple(img, apple_center, scale=distance / 50, locked=display_fixed_image)
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Draw the gradient line with the moving blue rectangle
#     img = draw_gradient_ruler_with_rectangle(img, rect_x)

#     # Draw the distance graph
#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     # Display the video
#     cv2.imshow("MediaPipe Hands with Gradient Ruler and Moving Rectangle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#----------------------------------------------------------------------------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_fixed_img = cv2.imread('apple_1.png', cv2.IMREAD_UNCHANGED)

# # Variables for locked apple size and state
# display_fixed_image = False
# apple_locked = False
# locked_size = None
# last_fist_time = time.time()
# cooldown_interval = 3

# # Function to calculate 3D Euclidean distance
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0, locked=False):
#     apple = apple_fixed_img if locked else apple_img
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Gesture recognition functions
# def is_fist_gesture(hand_landmarks):
#     fingers_closed = []
#     for i in [8, 12, 16, 20]:  # Tip landmarks of index, middle, ring, pinky fingers
#         tip = hand_landmarks.landmark[i]
#         pip = hand_landmarks.landmark[i - 2]
#         fingers_closed.append(tip.y > pip.y)  # Check if the finger is closed
#     return all(fingers_closed)

# def is_palm_gesture(hand_landmarks):
#     fingers_extended = []
#     for i in [8, 12, 16, 20]:
#         tip = hand_landmarks.landmark[i]
#         pip = hand_landmarks.landmark[i - 2]
#         fingers_extended.append(tip.y < pip.y)  # Check if the finger is extended

#     thumb_tip = hand_landmarks.landmark[4]
#     thumb_ip = hand_landmarks.landmark[2]
#     thumb_extended = thumb_tip.x > thumb_ip.x
#     return all(fingers_extended) and thumb_extended

# def is_time_gesture(hand_landmarks):
#     thumb_tip = hand_landmarks.landmark[4]
#     thumb_ip = hand_landmarks.landmark[2]
#     index_tip = hand_landmarks.landmark[8]
#     index_pip = hand_landmarks.landmark[6]

#     thumb_raised = thumb_tip.y < thumb_ip.y
#     index_raised = index_tip.y < index_pip.y
#     other_fingers_bent = all(
#         hand_landmarks.landmark[i].y > hand_landmarks.landmark[i - 2].y
#         for i in [12, 16, 20]
#     )
#     return thumb_raised and index_raised and other_fingers_bent

# def recognize_and_display_gestures(frame, hand_landmarks, bounding_box):
#     if is_fist_gesture(hand_landmarks):
#         gesture_name = "Generate"  # Fist
#     elif is_palm_gesture(hand_landmarks):
#         gesture_name = "Define"  # All fingers open
#     elif is_time_gesture(hand_landmarks):
#         gesture_name = "Time"  # Thumb + Index finger raised
#     else:
#         gesture_name = "Unknown"

#     x1, y1, x2, y2 = bounding_box
#     cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw a blue box
#     cv2.putText(frame, gesture_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

# # Function to draw the gradient line with a moving rectangle
# def draw_gradient_ruler_with_rectangle(frame, rect_x):
#     h, w = frame.shape[:2]
#     line_y = h - 50
#     rect_y = line_y - 10
#     rect_width = 20
#     rect_height = 20

#     for i in range(w - 100):  # Gradient
#         ratio = i / (w - 100)
#         color = (0, int(255 * (1 - ratio)), int(255 * ratio))
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)

#     rect_x1 = rect_x - rect_width // 2
#     rect_x2 = rect_x + rect_width // 2
#     cv2.rectangle(frame, (rect_x1, rect_y), (rect_x2, rect_y + rect_height), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (rect_x - 30, rect_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     rect_x = apple_center[0]

#     if results.multi_hand_landmarks:
#         hand_positions = []
#         for hand_landmarks in results.multi_hand_landmarks:
#             x_min = min([lm.x for lm in hand_landmarks.landmark])
#             y_min = min([lm.y for lm in hand_landmarks.landmark])
#             x_max = max([lm.x for lm in hand_landmarks.landmark])
#             y_max = max([lm.y for lm in hand_landmarks.landmark])
#             bounding_box = (int(x_min * img.shape[1]), int(y_min * img.shape[0]),
#                             int(x_max * img.shape[1]), int(y_max * img.shape[0]))

#             recognize_and_display_gestures(img, hand_landmarks, bounding_box)

#             hand_positions.append((hand_landmarks.landmark[12].x,
#                                    hand_landmarks.landmark[12].y,
#                                    hand_landmarks.landmark[12].z))

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             rect_x = int(midpoint_x * img.shape[1])

#             apple_center = (rect_x, apple_center[1])
#             img = overlay_apple(img, apple_center, scale=distance / 50, locked=display_fixed_image)
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     img = draw_gradient_ruler_with_rectangle(img, rect_x)

#     cv2.imshow("MediaPipe Hands with Gesture Recognition and Gradient Ruler", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



#------------------------------------------Define, Generate, Time手势识别，苹果emoji->青苹果-------------------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_1_img = cv2.imread('apple_1.png', cv2.IMREAD_UNCHANGED)
# current_apple_img = apple_img  # Current apple image to display

# # Variables for locked apple size and state
# last_generate_time = time.time()  # Time of the last 'Generate' gesture detection
# cooldown_interval = 3  # 3-second cooldown interval

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     global current_apple_img
#     apple = current_apple_img
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect gestures
# def detect_gesture(hand_landmarks):
#     fingers = [False] * 5  # Thumb, Index, Middle, Ring, Pinky
#     for i, tip_index in enumerate([4, 8, 12, 16, 20]):
#         tip = hand_landmarks.landmark[tip_index]
#         pip = hand_landmarks.landmark[tip_index - 2]
#         fingers[i] = tip.y < pip.y  # Open if tip is above pip
    
#     if all(fingers): 
#         return "Define"  # All fingers open
#     elif fingers[1] and fingers[0] and not any(fingers[2:]):
#         return "Time"  # Thumb and index finger only
#     return "Generate" # Fist

# # Function to draw the gradient ruler line
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the gradient ruler
#     for i in range(w - 100):
#         color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))  # Green to red gradient
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)

#     # Draw the moving blue rectangle arrow
#     arrow_x = apple_center[0]
#     cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# # Function to draw hand gesture recognition frames
# def draw_gesture_frame(frame, hand_landmarks, gesture_name):
#     h, w, _ = frame.shape
#     x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
#     x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

#     # Draw rectangle and label
#     cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (255, 0, 0), 2)
#     cv2.putText(frame, gesture_name, (x_min, y_min - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     current_time = time.time()

#     generate_detected = 0
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             gesture_name = detect_gesture(hand_landmarks)
#             if gesture_name == "Generate":
#                 generate_detected += 1

#             img = draw_gesture_frame(img, hand_landmarks, gesture_name)

#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         if generate_detected == 2 and (current_time - last_generate_time >= cooldown_interval):
#             current_apple_img = apple_1_img if current_apple_img is apple_img else apple_img
#             last_generate_time = current_time

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)

#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     img = draw_ruler(img, apple_center)

#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     cv2.imshow("MediaPipe Hands with Apple Image Toggle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#----------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_images = [cv2.imread(f'apple_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(1, 8)]
# apple_1_img = apple_images[0]  # Default to apple_1.png
# current_apple_img = apple_1_img  # Current apple image to display

# # Variables for locked apple size and state
# last_generate_time = time.time()  # Time of the last 'Generate' gesture detection
# cooldown_interval = 3  # 3-second cooldown interval
# switch_image = False  # Control flag to switch images dynamically

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     global current_apple_img
#     apple = current_apple_img
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect gestures
# def detect_gesture(hand_landmarks):
#     fingers = [False] * 5  # Thumb, Index, Middle, Ring, Pinky
#     for i, tip_index in enumerate([4, 8, 12, 16, 20]):
#         tip = hand_landmarks.landmark[tip_index]
#         pip = hand_landmarks.landmark[tip_index - 2]
#         fingers[i] = tip.y < pip.y  # Open if tip is above pip
    
#     if all(fingers): 
#         return "Define"  # All fingers open
#     elif fingers[1] and fingers[0] and not any(fingers[2:]):
#         return "Time"  # Thumb and index finger only
#     return "Generate" # Fist

# # Function to draw the gradient ruler line
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the gradient ruler
#     for i in range(w - 100):
#         color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))  # Green to red gradient
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)

#     # Draw the moving blue rectangle arrow
#     arrow_x = apple_center[0]
#     cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# # Function to draw hand gesture recognition frames
# def draw_gesture_frame(frame, hand_landmarks, gesture_name):
#     h, w, _ = frame.shape
#     x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
#     x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

#     # Draw rectangle and label
#     cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (255, 0, 0), 2)
#     cv2.putText(frame, gesture_name, (x_min, y_min - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     current_time = time.time()

#     generate_detected = 0
#     time_gesture_active = False  # Track if 'Time' gesture is active

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             gesture_name = detect_gesture(hand_landmarks)
#             if gesture_name == "Generate":
#                 generate_detected += 1
#             elif gesture_name == "Time":
#                 time_gesture_active = True

#             img = draw_gesture_frame(img, hand_landmarks, gesture_name)

#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         if time_gesture_active and len(hand_positions) == 2:
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             segment_width = img.shape[1] // 7
#             index = min(midpoint_x_px // segment_width, 6)  # Ensure index is between 0 and 6
#             current_apple_img = apple_images[index]
#         elif not time_gesture_active:
#             current_apple_img = apple_1_img

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)

#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     img = draw_ruler(img, apple_center)

#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     cv2.imshow("MediaPipe Hands with Apple Image Toggle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



#---------------------------------------------------------------------------------


# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_images = [cv2.imread(f'apple_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(1, 8)]
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_1_img = apple_images[0]  # Default to apple_1.png
# current_apple_img = apple_img  # Current apple image to display

# # Variables for locked apple size and state
# last_generate_time = time.time()  # Time of the last 'Generate' gesture detection
# cooldown_interval = 3  # 3-second cooldown interval
# switch_image = False  # Control flag to switch images dynamically

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     global current_apple_img
#     apple = current_apple_img
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect gestures
# def detect_gesture(hand_landmarks):
#     fingers = [False] * 5  # Thumb, Index, Middle, Ring, Pinky
#     for i, tip_index in enumerate([4, 8, 12, 16, 20]):
#         tip = hand_landmarks.landmark[tip_index]
#         pip = hand_landmarks.landmark[tip_index - 2]
#         fingers[i] = tip.y < pip.y  # Open if tip is above pip
    
#     if all(fingers): 
#         return "Define"  # All fingers open
#     elif fingers[1] and fingers[0] and not any(fingers[2:]):
#         return "Time"  # Thumb and index finger only
#     return "Generate" # Fist

# # Function to draw the gradient ruler line
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the gradient ruler
#     for i in range(w - 100):
#         color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))  # Green to red gradient
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)

#     # Draw the moving blue rectangle arrow
#     arrow_x = apple_center[0]
#     cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# # Function to draw hand gesture recognition frames
# def draw_gesture_frame(frame, hand_landmarks, gesture_name):
#     h, w, _ = frame.shape
#     x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
#     x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

#     # Draw rectangle and label
#     cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (255, 0, 0), 2)
#     cv2.putText(frame, gesture_name, (x_min, y_min - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     current_time = time.time()

#     generate_detected = 0
#     time_gesture_active = False  # Track if 'Time' gesture is active

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             gesture_name = detect_gesture(hand_landmarks)
#             if gesture_name == "Generate":
#                 generate_detected += 1
#             elif gesture_name == "Time":
#                 time_gesture_active = True

#             img = draw_gesture_frame(img, hand_landmarks, gesture_name)

#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         if generate_detected == 2 and (current_time - last_generate_time >= cooldown_interval):
#             current_apple_img = apple_1_img if current_apple_img is apple_img else apple_img
#             last_generate_time = current_time

#         if time_gesture_active and len(hand_positions) == 2:
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             segment_width = img.shape[1] // 7
#             index = min(midpoint_x_px // segment_width, 6)  # Ensure index is between 0 and 6
#             current_apple_img = apple_images[index]
#         elif not time_gesture_active:
#             current_apple_img = apple_1_img

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)

#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     img = draw_ruler(img, apple_center)

#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     cv2.imshow("MediaPipe Hands with Apple Image Toggle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#---------------------------------------------------Time手势带来苹果生长---------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_images = [cv2.imread(f'apple_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(1, 8)]
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_1_img = apple_images[0]  # Default to apple_1.png
# current_apple_img = apple_img  # Current apple image to display

# # Variables for locked apple size and state
# last_generate_time = time.time()  # Time of the last 'Generate' gesture detection
# cooldown_interval = 3  # 3-second cooldown interval
# switch_image = False  # Control flag to switch images dynamically

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     global current_apple_img
#     apple = current_apple_img
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect gestures
# def detect_gesture(hand_landmarks):
#     fingers = [False] * 5  # Thumb, Index, Middle, Ring, Pinky
#     for i, tip_index in enumerate([4, 8, 12, 16, 20]):
#         tip = hand_landmarks.landmark[tip_index]
#         pip = hand_landmarks.landmark[tip_index - 2]
#         fingers[i] = tip.y < pip.y  # Open if tip is above pip
    
#     if all(fingers): 
#         return "Define"  # All fingers open
#     elif fingers[1] and fingers[0] and not any(fingers[2:]):
#         return "Time"  # Thumb and index finger only
#     return "Generate" # Fist

# # Function to draw the gradient ruler line
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the gradient ruler
#     for i in range(w - 100):
#         color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))  # Green to red gradient
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)

#     # Draw the moving blue rectangle arrow
#     arrow_x = apple_center[0]
#     cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# # Function to draw hand gesture recognition frames
# def draw_gesture_frame(frame, hand_landmarks, gesture_name):
#     h, w, _ = frame.shape
#     x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
#     x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

#     # Draw rectangle and label
#     cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (255, 0, 0), 2)
#     cv2.putText(frame, gesture_name, (x_min, y_min - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     current_time = time.time()

#     generate_detected = 0
#     time_gesture_active = False  # Track if 'Time' gesture is active

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             gesture_name = detect_gesture(hand_landmarks)
#             if gesture_name == "Generate":
#                 generate_detected += 1
#                 img = draw_gesture_frame(img, hand_landmarks, gesture_name)
#             elif gesture_name == "Time":
#                 time_gesture_active = True

#             # img = draw_gesture_frame(img, hand_landmarks, gesture_name)

#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         if generate_detected == 2 and (current_time - last_generate_time >= cooldown_interval):
#             current_apple_img = apple_1_img if current_apple_img is apple_img else apple_img
#             last_generate_time = current_time

#         if time_gesture_active and len(hand_positions) == 2:
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             segment_width = img.shape[1] // 7
#             index = min(midpoint_x_px // segment_width, 6)  # Ensure index is between 0 and 6
#             current_apple_img = apple_images[index]
#         elif not time_gesture_active:
#             current_apple_img = apple_1_img

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)

#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     img = draw_ruler(img, apple_center)

#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     cv2.imshow("MediaPipe Hands with Apple Image Toggle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



#-------------------------------------------------------------有Time功能的苹果，但没有emoji和apple.png的转换------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_images = [cv2.imread(f'apple_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(1, 8)]
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_1_img = apple_images[0]  # Default to apple_1.png
# current_apple_img = apple_img  # Current apple image to display

# # Variables for locked apple size and state
# last_generate_time = time.time()  # Time of the last 'Generate' gesture detection
# cooldown_interval = 3  # 3-second cooldown interval
# switch_image = False  # Control flag to switch images dynamically

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     global current_apple_img
#     apple = current_apple_img
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect gestures
# def detect_gesture(hand_landmarks):
#     fingers = [False] * 5  # Thumb, Index, Middle, Ring, Pinky
#     for i, tip_index in enumerate([4, 8, 12, 16, 20]):
#         tip = hand_landmarks.landmark[tip_index]
#         pip = hand_landmarks.landmark[tip_index - 2]
#         fingers[i] = tip.y < pip.y  # Open if tip is above pip
    
#     if all(fingers): 
#         return "Define"  # All fingers open
#     elif fingers[1] and fingers[0] and not any(fingers[2:]):
#         return "Time"  # Thumb and index finger only
#     return "Generate" # Fist

# # Function to draw the gradient ruler line
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the gradient ruler
#     for i in range(w - 100):
#         color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))  # Green to red gradient
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)

#     # Draw the moving blue rectangle arrow
#     arrow_x = apple_center[0]
#     cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# # Function to draw hand gesture recognition frames
# def draw_gesture_frame(frame, hand_landmarks, gesture_name):
#     h, w, _ = frame.shape
#     x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
#     x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

#     # Draw rectangle and label
#     cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (255, 0, 0), 2)
#     cv2.putText(frame, gesture_name, (x_min, y_min - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     current_time = time.time()

#     generate_detected = 0
#     time_gesture_active = False  # Track if 'Time' gesture is active

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             gesture_name = detect_gesture(hand_landmarks)
#             if gesture_name == "Generate":
#                 generate_detected += 1
#             elif gesture_name == "Time":
#                 time_gesture_active = True

#             img = draw_gesture_frame(img, hand_landmarks, gesture_name)

#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         if generate_detected == 2 and (current_time - last_generate_time >= cooldown_interval):
#             current_apple_img = apple_1_img if current_apple_img is apple_img else apple_img
#             last_generate_time = current_time

#         if time_gesture_active and len(hand_positions) == 2:
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             segment_width = img.shape[1] // 7
#             index = min(midpoint_x_px // segment_width, 6)  # Ensure index is between 0 and 6
#             current_apple_img = apple_images[index]
#         elif not time_gesture_active:
#             current_apple_img = apple_1_img

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)

#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     img = draw_ruler(img, apple_center)

#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     cv2.imshow("MediaPipe Hands with Apple Image Toggle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#---------------------------------------------------------------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Circular buffer to store recent distances
# distance_buffer = deque(maxlen=30)

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Set window size to make the video larger
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load the apple images
# apple_images = [cv2.imread(f'apple_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(1, 8)]
# apple_img = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
# apple_1_img = apple_images[0]  # Default to apple_1.png
# current_apple_img = apple_img  # Current apple image to display

# # Variables for locked apple size and state
# last_generate_time = time.time()  # Time of the last 'Generate' gesture detection
# cooldown_interval = 3  # 3-second cooldown interval
# switch_image = False  # Control flag to switch images dynamically

# # Function to calculate 3D Euclidean distance in real-world cm
# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) * 100

# # Function to overlay the apple image on the frame
# def overlay_apple(frame, center, scale=1.0):
#     global current_apple_img
#     apple = current_apple_img
#     if apple is None:
#         return frame
#     h, w, _ = apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     apple_resized = cv2.resize(apple, (x2 - x1, y2 - y1))
#     alpha = apple_resized[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha) + apple_resized[:, :, c] * alpha
#     return frame

# # Function to detect gestures
# def detect_gesture(hand_landmarks):
#     fingers = [False] * 5  # Thumb, Index, Middle, Ring, Pinky
#     for i, tip_index in enumerate([4, 8, 12, 16, 20]):
#         tip = hand_landmarks.landmark[tip_index]
#         pip = hand_landmarks.landmark[tip_index - 2]
#         fingers[i] = tip.y < pip.y  # Open if tip is above pip
    
#     if all(fingers): 
#         return "Define"  # All fingers open
#     elif fingers[1] and fingers[0] and not any(fingers[2:]):
#         return "Time"  # Thumb and index finger only
#     return "Generate" # Fist

# # Function to draw the gradient ruler line
# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50  # Position the line near the bottom

#     # Draw the gradient ruler
#     for i in range(w - 100):
#         color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))  # Green to red gradient
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)

#     # Draw the moving blue rectangle arrow
#     arrow_x = apple_center[0]
#     cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# # Function to draw hand gesture recognition frames
# def draw_gesture_frame(frame, hand_landmarks, gesture_name):
#     h, w, _ = frame.shape
#     x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
#     x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

#     # Draw rectangle and label
#     cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (255, 0, 0), 2)
#     cv2.putText(frame, gesture_name, (x_min, y_min - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#     return frame

# # Main loop
# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     current_time = time.time()

#     generate_detected = False
#     time_gesture_active = False  # Track if 'Time' gesture is active

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             gesture_name = detect_gesture(hand_landmarks)
#             if gesture_name == "Generate":
#                 generate_detected = -generate_detected
#             if gesture_name == "Define":
#                 generate_detected = generate_detected
#             elif gesture_name == "Time":
#                 time_gesture_active = True

#             img = draw_gesture_frame(img, hand_landmarks, gesture_name)

#             middle_finger_x = hand_landmarks.landmark[12].x
#             middle_finger_y = hand_landmarks.landmark[12].y
#             middle_finger_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_finger_x, middle_finger_y, middle_finger_z))

#         if generate_detected == 2 and (current_time - last_generate_time >= cooldown_interval):
#             current_apple_img = apple_1_img if current_apple_img is apple_img else apple_img
#             last_generate_time = current_time

#         if time_gesture_active and len(hand_positions) == 2:
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             segment_width = img.shape[1] // 7
#             index = min(midpoint_x_px // segment_width, 6)  # Ensure index is between 0 and 6
#             current_apple_img = apple_images[index]
#         elif not time_gesture_active:
#             current_apple_img = apple_1_img

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)

#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2

#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])

#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)

#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     img = draw_ruler(img, apple_center)

#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     cv2.imshow("MediaPipe Hands with Apple Image Toggle", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#----------------------------------------------------------------emoji到苹果，“Time”手势，苹果形象的过渡-----------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, 
#                        min_detection_confidence=0.5, min_tracking_confidence=0.5)

# distance_buffer = deque(maxlen=30)

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load all apple images (apple_0.png to apple_7.png)
# apple_images = [cv2.imread(f'apple_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(0, 8)]

# current_image_index = None  # Current displayed apple index
# previous_image_index = None # Previous apple index (for transitions)
# fade_start_time = None
# fade_duration = 1.0  # 1 second fade

# last_generate_time = time.time()
# cooldown_interval = 3

# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# def blend_images(img1, img2, alpha):
#     # Blend RGBA images (same size) using alpha for img2
#     blended = img1.astype(float)*(1.0 - alpha) + img2.astype(float)*alpha
#     return blended.astype(np.uint8)

# def overlay_apple(frame, center, scale=1.0):
#     global current_image_index, previous_image_index, fade_start_time

#     if current_image_index is None:
#         return frame

#     now = time.time()
#     alpha = 1.0
#     if fade_start_time is not None and previous_image_index is not None:
#         elapsed = now - fade_start_time
#         if elapsed < fade_duration:
#             alpha = elapsed / fade_duration
#         else:
#             alpha = 1.0
#             previous_image_index = None
#             fade_start_time = None

#     current_apple = apple_images[current_image_index]
#     if previous_image_index is not None:
#         previous_apple = apple_images[previous_image_index]
#     else:
#         previous_apple = current_apple

#     h, w, _ = current_apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     if (x2 - x1) <= 0 or (y2 - y1) <= 0:
#         return frame

#     current_resized = cv2.resize(current_apple, (x2 - x1, y2 - y1))
#     prev_resized = cv2.resize(previous_apple, (x2 - x1, y2 - y1))

#     blended = blend_images(prev_resized, current_resized, alpha)

#     final_alpha = blended[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - final_alpha) + blended[:, :, c] * final_alpha
#     return frame

# def detect_gesture(hand_landmarks):
#     fingers = [False] * 5
#     for i, tip_index in enumerate([4, 8, 12, 16, 20]):
#         tip = hand_landmarks.landmark[tip_index]
#         pip = hand_landmarks.landmark[tip_index - 2]
#         fingers[i] = tip.y < pip.y
    
#     if all(fingers): 
#         return "Define"
#     elif fingers[1] and fingers[0] and not any(fingers[2:]):
#         return "Time"
#     return "Generate"

# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50
#     for i in range(w - 100):
#         color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)
#     arrow_x = apple_center[0]
#     cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20), 
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# def draw_gesture_frame(frame, hand_landmarks, gesture_name):
#     h, w, _ = frame.shape
#     x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
#     x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)
#     cv2.rectangle(frame, (x_min - 10, y_min - 10), 
#                   (x_max + 10, y_max + 10), (255, 0, 0), 2)
#     cv2.putText(frame, gesture_name, (x_min, y_min - 15), 
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#     return frame

# def switch_apple(new_index):
#     global current_image_index, previous_image_index, fade_start_time
#     if current_image_index == new_index:
#         return
#     previous_image_index = current_image_index
#     current_image_index = new_index
#     fade_start_time = time.time()

# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     current_time = time.time()
#     time_gesture_active = False

#     if results.multi_hand_landmarks:
#         if current_image_index is None:
#             switch_apple(0)

#         for hand_landmarks in results.multi_hand_landmarks:
#             gesture_name = detect_gesture(hand_landmarks)

#             if gesture_name == "Generate":
#                 if (current_time - last_generate_time) >= cooldown_interval:
#                     if current_image_index == 0:
#                         switch_apple(1)
#                     else:
#                         switch_apple(0)
#                     last_generate_time = current_time
#             elif gesture_name == "Time":
#                 time_gesture_active = True

#             img = draw_gesture_frame(img, hand_landmarks, gesture_name)
#             middle_x = hand_landmarks.landmark[12].x
#             middle_y = hand_landmarks.landmark[12].y
#             middle_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_x, middle_y, middle_z))

#         if time_gesture_active and len(hand_positions) == 2 and current_image_index != 0:
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             segment_width = img.shape[1] // 7
#             new_index = min(max(1, midpoint_x_px // segment_width), 7)
#             if new_index != current_image_index:
#                 switch_apple(new_index)

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])
#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#         else:
#             if current_image_index is not None:
#                 img = overlay_apple(img, apple_center, scale=1.0)
#     else:
#         current_image_index = None
#         previous_image_index = None
#         fade_start_time = None

#     img = draw_ruler(img, apple_center)

#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     cv2.imshow("MediaPipe Hands with Smooth Apple Transition", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



#-----------------------------------------------------------------------------------------------------------

# import mediapipe as mp
# import cv2
# import math
# import numpy as np
# from collections import deque
# import time

# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, 
#                        min_detection_confidence=0.5, min_tracking_confidence=0.5)

# distance_buffer = deque(maxlen=30)

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Load all apple images (apple_0.png to apple_7.png)
# apple_images = [cv2.imread(f'apple_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(0, 8)]

# current_image_index = None
# previous_image_index = None
# fade_start_time = None
# fade_duration = 1.0  # 1 second fade

# last_generate_time = time.time()
# cooldown_interval = 3

# def calculate_3d_distance(hand1, hand2):
#     x1, y1, z1 = hand1
#     x2, y2, z2 = hand2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

# def blend_images(img1, img2, alpha):
#     blended = img1.astype(float)*(1.0 - alpha) + img2.astype(float)*alpha
#     return blended.astype(np.uint8)

# def overlay_apple(frame, center, scale=1.0):
#     global current_image_index, previous_image_index, fade_start_time

#     if current_image_index is None:
#         return frame

#     now = time.time()
#     alpha = 1.0
#     if fade_start_time is not None and previous_image_index is not None:
#         elapsed = now - fade_start_time
#         if elapsed < fade_duration:
#             alpha = elapsed / fade_duration
#         else:
#             alpha = 1.0
#             previous_image_index = None
#             fade_start_time = None

#     current_apple = apple_images[current_image_index]
#     if previous_image_index is not None:
#         previous_apple = apple_images[previous_image_index]
#     else:
#         previous_apple = current_apple

#     h, w, _ = current_apple.shape
#     h, w = int(h * scale), int(w * scale)
#     x, y = center

#     x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
#     x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

#     if (x2 - x1) <= 0 or (y2 - y1) <= 0:
#         return frame

#     current_resized = cv2.resize(current_apple, (x2 - x1, y2 - y1))
#     prev_resized = cv2.resize(previous_apple, (x2 - x1, y2 - y1))
#     blended = blend_images(prev_resized, current_resized, alpha)

#     final_alpha = blended[:, :, 3] / 255.0
#     for c in range(3):
#         frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - final_alpha) + blended[:, :, c] * final_alpha
#     return frame

# def detect_gesture(hand_landmarks):
#     fingers = [False] * 5
#     for i, tip_index in enumerate([4, 8, 12, 16, 20]):
#         tip = hand_landmarks.landmark[tip_index]
#         pip = hand_landmarks.landmark[tip_index - 2]
#         fingers[i] = tip.y < pip.y
    
#     if all(fingers): 
#         return "Define"
#     elif fingers[1] and fingers[0] and not any(fingers[2:]):
#         return "Time"
#     return "Generate"

# def draw_ruler(frame, apple_center):
#     h, w = frame.shape[:2]
#     line_y = h - 50
#     for i in range(w - 100):
#         color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))
#         cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)
#     arrow_x = apple_center[0]
#     cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y), (255, 0, 0), -1)
#     cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return frame

# def draw_gesture_frame(frame, hand_landmarks, gesture_name):
#     h, w, _ = frame.shape
#     x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
#     x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
#     y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)
#     cv2.rectangle(frame, (x_min - 10, y_min - 10),
#                   (x_max + 10, y_max + 10), (255, 0, 0), 2)
#     cv2.putText(frame, gesture_name, (x_min, y_min - 15),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
#     return frame

# def switch_apple(new_index):
#     global current_image_index, previous_image_index, fade_start_time
#     if current_image_index == new_index:
#         return
#     previous_image_index = current_image_index
#     current_image_index = new_index
#     fade_start_time = time.time()

# while cap.isOpened():
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     hand_positions = []
#     apple_center = (img.shape[1] // 2, img.shape[0] // 2)
#     current_time = time.time()
#     time_gesture_active = False

#     if results.multi_hand_landmarks:
#         if current_image_index is None:
#             switch_apple(0)

#         for hand_landmarks in results.multi_hand_landmarks:
#             gesture_name = detect_gesture(hand_landmarks)

#             if gesture_name == "Generate":
#                 if (current_time - last_generate_time) >= cooldown_interval:
#                     if current_image_index == 0:
#                         switch_apple(1)
#                     else:
#                         switch_apple(0)
#                     last_generate_time = current_time
#             elif gesture_name == "Time":
#                 time_gesture_active = True

#             img = draw_gesture_frame(img, hand_landmarks, gesture_name)
#             middle_x = hand_landmarks.landmark[12].x
#             middle_y = hand_landmarks.landmark[12].y
#             middle_z = hand_landmarks.landmark[12].z
#             hand_positions.append((middle_x, middle_y, middle_z))

#         if time_gesture_active and len(hand_positions) == 2 and current_image_index != 0:
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             segment_width = img.shape[1] // 7
#             new_index = min(max(1, midpoint_x_px // segment_width), 7)
#             if new_index != current_image_index:
#                 switch_apple(new_index)

#         if len(hand_positions) == 2:
#             distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
#             distance_buffer.append(distance)
#             midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
#             midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2
#             midpoint_x_px = int(midpoint_x * img.shape[1])
#             midpoint_y_px = int(midpoint_y * img.shape[0])
#             apple_center = (midpoint_x_px, midpoint_y_px)
#             size_to_use = distance / 50
#             img = overlay_apple(img, apple_center, scale=size_to_use)
#             cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#         else:
#             if current_image_index is not None:
#                 img = overlay_apple(img, apple_center, scale=1.0)
#     else:
#         current_image_index = None
#         previous_image_index = None
#         fade_start_time = None

#     img = draw_ruler(img, apple_center)
#     for i, d in enumerate(distance_buffer):
#         cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

#     # Move the dialog box to the right and align its first line of text with the distance text at y=50
#     # Since first line is drawn at y_start+30, set y_start = 20 to get y=50
#     x_start = 860
#     y_start = 20
#     box_width = 370
#     box_height = 100

#     if current_image_index == 0:
#         cv2.rectangle(img, (x_start, y_start), (x_start + box_width, y_start + box_height), (255, 255, 255), -1)
#         cv2.putText(img, "Now you are defining an apple.", (x_start + 10, y_start + 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
#         cv2.putText(img, "Try making a fist to generate", (x_start + 10, y_start + 60),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
#         cv2.putText(img, "a real apple.", (x_start + 10, y_start + 90),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

#     cv2.imshow("MediaPipe Hands with Smooth Apple Transition and Dialog", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



#-----------------------------------------------小心生长的苹果-----------------------------------------------

import mediapipe as mp
import cv2
import math
import numpy as np
from collections import deque
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

distance_buffer = deque(maxlen=30)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Load all apple images (apple_0.png to apple_7.png)
apple_images = [cv2.imread(f'apple_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(0, 8)]

current_image_index = None
previous_image_index = None
fade_start_time = None
fade_duration = 1.0  # 1 second fade

last_generate_time = time.time()
cooldown_interval = 3

def calculate_3d_distance(hand1, hand2):
    x1, y1, z1 = hand1
    x2, y2, z2 = hand2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) * 100

def blend_images(img1, img2, alpha):
    blended = img1.astype(float)*(1.0 - alpha) + img2.astype(float)*alpha
    return blended.astype(np.uint8)

def overlay_apple(frame, center, scale=1.0):
    global current_image_index, previous_image_index, fade_start_time

    if current_image_index is None:
        return frame

    now = time.time()
    alpha = 1.0
    if fade_start_time is not None and previous_image_index is not None:
        elapsed = now - fade_start_time
        if elapsed < fade_duration:
            alpha = elapsed / fade_duration
        else:
            alpha = 1.0
            previous_image_index = None
            fade_start_time = None

    current_apple = apple_images[current_image_index]
    if previous_image_index is not None:
        previous_apple = apple_images[previous_image_index]
    else:
        previous_apple = current_apple

    h, w, _ = current_apple.shape
    h, w = int(h * scale), int(w * scale)
    x, y = center

    x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
    x2, y2 = min(frame.shape[1], x + w // 2), min(frame.shape[0], y + h // 2)

    if (x2 - x1) <= 0 or (y2 - y1) <= 0:
        return frame

    current_resized = cv2.resize(current_apple, (x2 - x1, y2 - y1))
    prev_resized = cv2.resize(previous_apple, (x2 - x1, y2 - y1))
    blended = blend_images(prev_resized, current_resized, alpha)

    final_alpha = blended[:, :, 3] / 255.0
    for c in range(3):
        frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - final_alpha) + blended[:, :, c] * final_alpha
    return frame

def detect_gesture(hand_landmarks):
    fingers = [False] * 5
    for i, tip_index in enumerate([4, 8, 12, 16, 20]):
        tip = hand_landmarks.landmark[tip_index]
        pip = hand_landmarks.landmark[tip_index - 2]
        fingers[i] = tip.y < pip.y
    
    if all(fingers):
        return "Define"
    elif fingers[1] and fingers[0] and not any(fingers[2:]):
        return "Live"
    return "Generate"

def draw_ruler(frame, apple_center):
    h, w = frame.shape[:2]
    line_y = h - 50
    for i in range(w - 100):
        color = (0, 255 * (1 - i / (w - 100)), 255 * (i / (w - 100)))
        cv2.line(frame, (50 + i, line_y), (50 + i + 1, line_y), color, 2)
    arrow_x = apple_center[0]
    cv2.rectangle(frame, (arrow_x - 5, line_y - 10), (arrow_x + 5, line_y+5), (0, 255, 0), -1)
    cv2.putText(frame, "growing", (arrow_x - 30, line_y - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def draw_gesture_frame(frame, hand_landmarks, gesture_name):
    h, w, _ = frame.shape
    x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
    y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
    x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
    y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)
    cv2.rectangle(frame, (x_min - 10, y_min - 10),
                  (x_max + 10, y_max + 10), (255, 0, 0), 2)
    cv2.putText(frame, gesture_name, (x_min, y_min - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    return frame

def switch_apple(new_index):
    global current_image_index, previous_image_index, fade_start_time
    if current_image_index == new_index:
        return
    previous_image_index = current_image_index
    current_image_index = new_index
    fade_start_time = time.time()

while cap.isOpened():
    success, img = cap.read()
    img = cv2.flip(img, 1)
    if not success:
        print("Ignoring empty camera frame.")
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    hand_positions = []
    apple_center = (img.shape[1] // 2, img.shape[0] // 2)
    current_time = time.time()
    time_gesture_active = False

    if results.multi_hand_landmarks:
        if current_image_index is None:
            switch_apple(0)

        for hand_landmarks in results.multi_hand_landmarks:
            gesture_name = detect_gesture(hand_landmarks)

            if gesture_name == "Generate":
                if (current_time - last_generate_time) >= cooldown_interval:
                    if current_image_index == 0:
                        # from apple_0 to apple_1
                        switch_apple(1)
                    else:
                        # from something else back to apple_0
                        switch_apple(0)
                    last_generate_time = current_time
            elif gesture_name == "Live":
                time_gesture_active = True

            img = draw_gesture_frame(img, hand_landmarks, gesture_name)
            middle_x = hand_landmarks.landmark[12].x
            middle_y = hand_landmarks.landmark[12].y
            middle_z = hand_landmarks.landmark[12].z
            hand_positions.append((middle_x, middle_y, middle_z))

        if time_gesture_active and len(hand_positions) == 2 and current_image_index != 0:
            midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
            midpoint_x_px = int(midpoint_x * img.shape[1])
            segment_width = img.shape[1] // 7
            new_index = min(max(1, midpoint_x_px // segment_width), 7)
            if new_index != current_image_index:
                switch_apple(new_index)

        if len(hand_positions) == 2:
            distance = calculate_3d_distance(hand_positions[0], hand_positions[1])
            distance_buffer.append(distance)
            midpoint_x = (hand_positions[0][0] + hand_positions[1][0]) / 2
            midpoint_y = (hand_positions[0][1] + hand_positions[1][1]) / 2
            midpoint_x_px = int(midpoint_x * img.shape[1])
            midpoint_y_px = int(midpoint_y * img.shape[0])
            apple_center = (midpoint_x_px, midpoint_y_px)
            size_to_use = distance / 50
            img = overlay_apple(img, apple_center, scale=size_to_use)
            cv2.putText(img, f"Distance: {distance:.2f} cm", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            if current_image_index is not None:
                img = overlay_apple(img, apple_center, scale=1.0)
    else:
        current_image_index = None
        previous_image_index = None
        fade_start_time = None

    # Draw the ruler line and distance graph as before
    img = draw_ruler(img, apple_center)
    for i, d in enumerate(distance_buffer):
        cv2.line(img, (50 + i * 10, 100), (50 + i * 10, 100 - int(d / 2)), (255, 255, 255), 2)

    # Dialogue box location
    x_start = 860
    y_start = 20
    box_width = 370
    box_height = 100


    if current_image_index == 0:
        #white dialogue rectangle
        cv2.rectangle(img, (x_start, y_start), (x_start + box_width, y_start + box_height), (181, 181, 181), -1)
        # apple_0.png
        cv2.putText(img, "Now you are defining an apple.", (x_start + 10, y_start + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(img, "Try making a fist to generate", (x_start + 10, y_start + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(img, "a real apple.", (x_start + 10, y_start + 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    if current_image_index == 1 or current_image_index == 2 or current_image_index == 3 or current_image_index == 4 or current_image_index == 5 or current_image_index == 6 or current_image_index == 7:
        #white dialogue rectangle
        cv2.rectangle(img, (x_start, y_start), (x_start + box_width, y_start + box_height), (255, 255, 255), -1)
        # apple_1.png to apple_7.png
        cv2.putText(img, "Spread your index fingers and", (x_start + 10, y_start + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(img, "thumbs and move them", (x_start + 10, y_start + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.imshow("MediaPipe Hands with Smooth Apple Transition and Dialog", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
