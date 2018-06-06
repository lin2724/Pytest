import os
import sys
import re


def test_utf_8(file_path):
    with open(file_path, 'r') as fd:
        buf = fd.read()
    buf = buf.decode('utf-8')
    for c in buf:
        print c
    pass


class CharPointer:
    def __init__(self, buf, char, pos):
        self.m_decode_m = 'utf-8'
        self.m_char = char
        self.m_pos = pos
        self.m_orig_buf = buf
        pass

    def __str__(self):
        ret_str = '[%s] at [%d]' % (self.m_char.decode(self.m_decode_m), self.m_pos)
        return ret_str

    def get_words(self, word_len):
        words = ''
        words = self.m_orig_buf[self.m_pos:self.m_pos + word_len]
        words = words.split(' ')[0]
        if len(words) != word_len:
            return None
        return words
    pass


class CoupleRember:
    def __init__(self, str_word):
        self.m_decode_m = 'utf-8'
        self.m_str_word = str_word
        self.m_ref = 0
        pass

    def __add__(self, other):
        if int != other:
            raise TypeError
        self.m_ref += 1
        pass

    def add_ref(self, ref):
        self.m_ref += ref
        pass

    def __str__(self):
        return '[%s] count [%d]' % (self.m_str_word, self.m_ref)

    def get_info(self):
        print '[%s] count [%d]' % (self.m_str_word, self.m_ref)
        pass

    def get_ref(self):
        return self.m_ref

    def __cmp__(self, other):
        if str == type(other) or unicode == type(other):
            return cmp(self.m_str_word, other)
        return cmp(self.m_str_word, other.m_str_word)
        pass


def process(file_path):
    max_word_len = 4
    pointer_list = list()
    couple_list = list()
    with open(file_path, 'r') as fd:
        buf = fd.read()
    buf = buf.decode('utf-8')
    for idx, c in enumerate(buf):
        pointer_item = CharPointer(buf, c, idx)
        pointer_list.append(pointer_item)
    for pointer_item in pointer_list:
        for len_word in range(2, max_word_len+1):
            words = pointer_item.get_words(len_word)
            if not words:
                continue
            try:
                idx = couple_list.index(words)
                couple_list[idx].add_ref(1)
            except ValueError:
                coup_words = CoupleRember(words)
                couple_list.append(coup_words)
    for item in couple_list:
        if item.get_ref() > 3:
            item.get_info()
        pass
    pass


if __name__ == '__main__':
    process(sys.argv[1])
    # test_utf_8(sys.argv[1])
    pass
