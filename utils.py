import os.path

import cv2
import numpy as np
from pydub import AudioSegment

FACE_CLASSIFIER = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def has_face(img: np.ndarray) -> bool:
    """
    Checks faces on the photo
    """
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return bool(
        len(
            FACE_CLASSIFIER.detectMultiScale(
                gray_image,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(40, 40)
            )
        )
    )


def ogg_to_wav_with_sample_rate(source_path: str, destination_path: str, sample_rate_hz: int = 16000):
    """
    Converts ogg audio file to wav audio file.
    :param source_path: ogg file path
    :param destination_path: wav file path
    :param sample_rate_hz: sample rate (Hz)
    """
    (
        AudioSegment
            .from_ogg(source_path)
            .set_frame_rate(16000)
            .export(destination_path, format='wav')
    )


def ensure_path(*paths) -> str:
    path = os.path.join(*paths)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path
