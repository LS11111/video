from vidstab import VidStab

stabilizer = VidStab()
stabilizer.stabilize(input_path='D:\\稳像\\test2.mp4', output_path='D:\\稳像\\stable_test2.avi')
#
# Using a specific keypoint detector
stabilizer = VidStab(kp_method='ORB')
stabilizer.stabilize(input_path='D:\\稳像\\test1.mp4', output_path='D:\\稳像\\stable\\stable_test1_ORB.avi')
stabilizer.stabilize(input_path='D:\\稳像\\test2.mp4', output_path='D:\\稳像\\stable\\stable_test2_ORB.avi')
#
# Using a specific keypoint detector and customizing keypoint parameters
stabilizer = VidStab(kp_method='FAST', threshold=42, nonmaxSuppression=False)
# stabilizer.stabilize(input_path='D:\\稳像\\stable\\test1\\test1.mp4', output_path='D:\\稳像\\stable\\test1\\stable_test1_FAST.avi')
stabilizer.stabilize(input_path='D:\\稳像\\stable\\test2\\test2.mp4', output_path='D:\\稳像\\stable\\test2\\stable_test2_FAST.avi')
#
from vidstab import VidStab
import matplotlib.pyplot as plt
#
# stabilizer = VidStab()
# stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')
#
# stabilizer.plot_trajectory()
# plt.show()
#
# stabilizer.plot_transforms()
# plt.show()
#
# from vidstab import VidStab
#
# stabilizer = VidStab()
#
# # black borders
# stabilizer.stabilize(input_path='D:\\稳像\\stable\\test2\\test2.mp4',
#                      output_path='D:\\稳像\\stable\\test2\\stable_test2_border_black.avi',
#                      border_type='black')
# stabilizer.stabilize(input_path='D:\\稳像\\stable\\test1\\test1.mp4',
#                      output_path='D:\\稳像\\stable\\test1\\stable_test1_border_black_100.avi',
#                      border_type='black',
#                      border_size=100)

# filled in borders
# stabilizer.stabilize(input_path='D:\\稳像\\stable\\test2\\test2.mp4',
#                      output_path='D:\\稳像\\stable\\test2\\stable_test2_reflect.avi',
#                      border_type='reflect')
# stabilizer.stabilize(input_path='D:\\稳像\\stable\\test2\\test2.mp4',
#                      output_path='D:\\稳像\\stable\\test2\\stable_test2_replicate.avi',
#                      border_type='replicate')
#
# from vidstab import VidStab, layer_overlay, layer_blend
#
# # init vid stabilizer
# stabilizer = VidStab()
#
# # use vidstab.layer_overlay for generating a trail effect
# stabilizer.stabilize(input_path=INPUT_VIDEO_PATH,
#                      output_path='trail_stable_video.avi',
#                      border_type='black',
#                      border_size=100,
#                      layer_func=layer_overlay)
#
#
# # create custom overlay function
# # here we use vidstab.layer_blend with custom alpha
# #   layer_blend will generate a fading trail effect with some motion blur
# def layer_custom(foreground, background):
#     return layer_blend(foreground, background, foreground_alpha=.8)
#
# # use custom overlay function
# stabilizer.stabilize(input_path=INPUT_VIDEO_PATH,
#                      output_path='blend_stable_video.avi',
#                      border_type='black',
#                      border_size=100,
#                      layer_func=layer_custom)
#
# from vidstab import VidStab, layer_overlay
#
# stabilizer = VidStab()
#
# stabilizer.stabilize(input_path=INPUT_VIDEO_PATH,
#                      output_path='auto_border_stable_video.avi',
#                      border_size='auto',
#                      # frame layering to show performance of auto sizing
#                      layer_func=layer_overlay)
#
# from vidstab.VidStab import VidStab
#
# stabilizer = VidStab()
# vidcap = cv2.VideoCapture('input_video.mov')
#
# while True:
#     grabbed_frame, frame = vidcap.read()
#
#     if frame is not None:
#         # Perform any pre-processing of frame before stabilization here
#         pass
#
#     # Pass frame to stabilizer even if frame is None
#     # stabilized_frame will be an all black frame until iteration 30
#     stabilized_frame = stabilizer.stabilize_frame(input_frame=frame,
#                                                   smoothing_window=30)
#     if stabilized_frame is None:
#         # There are no more frames available to stabilize
#         break
#
#     # Perform any post-processing of stabilized frame here
#     pass
#
import os
import cv2
from vidstab import VidStab, layer_overlay, download_ostrich_video

# Download test video to stabilize
if not os.path.isfile("ostrich.mp4"):
    download_ostrich_video("ostrich.mp4")

# Initialize object tracker, stabilizer, and video reader
object_tracker = cv2.TrackerCSRT_create()
stabilizer = VidStab(kp_method='ORB')
vidcap = cv2.VideoCapture("ostrich.mp4")

# Initialize bounding box for drawing rectangle around tracked object
object_bounding_box = None

while True:
    grabbed_frame, frame = vidcap.read()

    # Pass frame to stabilizer even if frame is None
    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame, border_size=50, border_type='replicate')

    # If stabilized_frame is None then there are no frames left to process
    if stabilized_frame is None:
        break

    # Draw rectangle around tracked object if tracking has started
    if object_bounding_box is not None:
        success, object_bounding_box = object_tracker.update(stabilized_frame)

        if success:
            (x, y, w, h) = [int(v) for v in object_bounding_box]
            cv2.rectangle(stabilized_frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)

    # Display stabilized output
    cv2.imshow('Frame', stabilized_frame)

    key = cv2.waitKey(5)

    # Select ROI for tracking and begin object tracking
    # Non-zero frame indicates stabilization process is warmed up
    if stabilized_frame.sum() > 0 and object_bounding_box is None:
        object_bounding_box = cv2.selectROI("Frame",
                                            stabilized_frame,
                                            fromCenter=False,
                                            showCrosshair=True)
        object_tracker.init(stabilized_frame, object_bounding_box)
    elif key == 27:
        break

vidcap.release()
cv2.destroyAllWindows()


# from vidstab import VidStab
#
# stabilizer = VidStab()
# stabilizer.stabilize(input_path=0,
#                      output_path='stable_webcam.avi',
#                      max_frames=1000,
#                      playback=True)
#
# import numpy as np
# from vidstab import VidStab, download_ostrich_video
#
# # Download video if needed
# download_ostrich_video(INPUT_VIDEO_PATH)
#
# # Generate transforms and save to TRANSFORMATIONS_PATH as csv (no headers)
# stabilizer = VidStab()
# stabilizer.gen_transforms(INPUT_VIDEO_PATH)
# np.savetxt(TRANSFORMATIONS_PATH, stabilizer.transforms, delimiter=',')
#
# import numpy as np
# from vidstab import VidStab
#
# # Read in csv transform data, of form (delta x, delta y, delta angle):
# transforms = np.loadtxt(TRANSFORMATIONS_PATH, delimiter=',')
#
# # Create stabilizer and supply numpy array of transforms
# stabilizer = VidStab()
# stabilizer.transforms = transforms
#
# # Apply stabilizing transforms to INPUT_VIDEO_PATH and save to OUTPUT_VIDEO_PATH
# stabilizer.apply_transforms(INPUT_VIDEO_PATH, OUTPUT_VIDEO_PATH)