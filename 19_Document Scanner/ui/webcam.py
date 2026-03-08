"""
웹캠 실시간 문서 검출 모듈 (보너스)

웹캠 프레임에서 실시간으로 문서 윤곽선을 검출하여 표시하고,
's' 키로 현재 프레임을 캡처하여 스캔 결과를 저장한다.
"""

import cv2
import os

from core.preprocessing import preprocess
from core.contour_detector import detect_document, draw_contour
from core.perspective_transform import warp_perspective
from core.postprocessing import postprocess


def run_webcam(camera_index=0, output_dir='webcam_captures'):
    """
    웹캠 기반 실시간 문서 스캐너를 실행한다.

    조작법:
    - 's' 키: 현재 프레임 캡처 및 스캔 결과 저장
    - 'q' 키: 프로그램 종료

    Parameters:
        camera_index: 카메라 장치 번호 (기본값 0)
        output_dir: 캡처 결과 저장 디렉토리
    """
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print('[ERROR] Cannot open webcam.')
        return

    os.makedirs(output_dir, exist_ok=True)
    capture_count = 0

    print('[INFO] Webcam started.')
    print('  s: Capture and scan')
    print('  q: Quit')

    while True:
        ret, frame = cap.read()
        if not ret:
            print('[ERROR] Failed to read frame.')
            break

        # 실시간 윤곽선 검출
        _, _, edges = preprocess(frame)
        quad = detect_document(edges, frame.shape)
        display = draw_contour(frame, quad)

        # 검출 상태 텍스트 표시
        status = 'Document DETECTED' if quad is not None else 'Searching...'
        color = (0, 255, 0) if quad is not None else (0, 0, 255)
        cv2.putText(display, status, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow('Webcam Scanner', display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('s') and quad is not None:
            # 캡처 및 스캔
            warped = warp_perspective(frame, quad)
            if warped is not None:
                scanned = postprocess(warped)
                capture_count += 1
                filename = f'capture_{capture_count:03d}.png'
                filepath = os.path.join(output_dir, filename)
                cv2.imwrite(filepath, scanned)
                print(f'[INFO] Saved: {filepath}')

                cv2.imshow('Captured Scan', scanned)

    cap.release()
    cv2.destroyAllWindows()
    print('[INFO] Webcam closed.')
