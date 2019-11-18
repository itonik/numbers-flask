import os
from collections import namedtuple
import recognition

class ProcessingResult():
    def __init__(self, filename):
        self.source = os.path.join('uploads', filename)
        self.filter = os.path.join('intermediate', filename + '.filter.png')
        self.contour = os.path.join('intermediate', filename + '.contour.png')
        self.segment_template = os.path.join('intermediate', filename + '.segment-{0}.png')
    def create_segments_list(self, n):
        self.segments = [self.segment_template.format(i) for i in range(n)]
        return self.segments

def process_image(filename):
    res = ProcessingResult(filename)
    recognition.filter(res.source, res.filter)
    recognition.segment(res.filter, res.contour, res.create_segments_list)
    res.recognition = recognition.numbers_recognition(res.segments)

    return res