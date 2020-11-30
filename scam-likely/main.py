import sys

import pandas as pd
import numpy as np
import re
from string import punctuation
from datetime import datetime, timedelta

import markovify
import pyttsx3
from pydub import AudioSegment as player

import random
import os

BAD_WORDS = ['sex', 'http:', 'www.']
INBOX = './audiobook/messages'
SPAM = 0
HAM = 1
MIN_SPAM_WORDS = 15
MAX_SPAM_WORDS = 25
MAX_WORD_COUNT = 60000
MAX_HAM_LEN = 60

year = random.randint(2008, 2015)
month = random.randint(1, 12)
day = random.randint(1, 28)
hour = random.randint(1, 12)
minute = random.randint(0, 59)
call_date = datetime(year, month, day, hour, minute)
MICROSECOND = timedelta(seconds=0.001)
SILENCE = player.silent(duration=800)

transcripts = {}
ham = []
robots = []

novel = ''
total_calls = 0
words = 0


def parse(line):
    t = None
    try:
        times = line.split()
        end = timedelta(seconds=float(times[1]))
        start = timedelta(seconds=float(times[0]))
        t = start, end
    except IndexError:
        pass  # oddball empty lines exist in some transcripts

    try:
        line = line[line.find(next(filter(str.isalpha, line))):]  # remove timestamp
    except StopIteration:
        pass  # alpha character not found in line

    line = re.sub('[A-Z]{2,}', '', line)  # remove sounds (in all caps)
    line = re.sub('\(H[x]?\)', '', line)
    line = re.sub('[A-Z]:', '', line)  # remove speaker labels
    line = re.sub('\d', '', line)  # remove numbers
    line = re.sub('[A-Z][>)]', '', line)  # <P in middle of line
    line = re.sub('[<(][A-Z]', '', line)  # P> in middle of line
    line = re.sub('[<\[(][A-Z][>)\]]', '', line)
    line = re.sub(' ?X ?', '', line)

    line = re.sub('[^A-Za-z0-9 .,\'?!]', '', line)  # remove special characters
    line = re.sub('\.{2,}', '', line)  # remove extra periods.
    line = ' '.join(line.split())  # remove extra whitespace
    line = line if line not in punctuation else None  # remove line if only contains punctuation
    return t, line if line else None


class ButtDial:
    def __init__(self, chat_id):
        self.recording = player.from_file('./sounds/recordings/' + chat_id + '.wav', format='wav')
        self.transcript = transcripts[chat_id]

        self.start_times = pd.Series([time[0] for time in self.transcript.index])
        self.end_times = pd.Series([time[1] for time in self.transcript.index])

        self.index = 0
        self.end = len(self.end_times) - 1

    def ended(self):
        return self.index >= self.end

    def play(self, interval, filename):
        call_len = timedelta(seconds=interval)
        end_time_estimate = self.end_times[self.index] + call_len
        end_index = np.argmin(np.abs(self.end_times - end_time_estimate))

        call = self.transcript.iloc[self.index: end_index]
        transcript = ' '.join(call.transcription)

        start_time = self.start_times[self.index]
        end_time = self.end_times[end_index]

        # split and save recording of conversation
        conversation = self.recording[start_time.total_seconds() * 1000: end_time.total_seconds() * 1000]
        conversation.export(os.path.join(INBOX, filename), format='wav')

        self.index = end_index + 1
        return len(transcript.split()), transcript


def get_spam():
    call = random.choice([
        'Hello.',
        'Alert:',
        'Attention:',
        'This is an important call.',
        ''
    ])

    words = random.randint(MIN_SPAM_WORDS, MAX_SPAM_WORDS)
    word_count = 0

    while word_count < words:
        sentence = spam.make_sentence()

        while sentence and any(bad_word in sentence.lower() for bad_word in BAD_WORDS):
            sentence = spam.make_sentence()

        if sentence:
            call += ' ' + sentence

        word_count = len(call.split())

    return word_count, call


def get_ham():
    call = random.choice(ham)

    while call.ended():
        ham.remove(call)
        call = random.choice(ham)

    return call


class Robot:
    def __init__(self, robot):
        self.robot = robot

    def say(self, text, path):
        """
        Performs text-to-speech on the given test with the given
        robot voice, and saves the resulting speech to a file.

        :param text:        the text to say.
        :param path:        where to save the spoken text.
        """
        engine.setProperty('voice', self.robot.id)
        engine.setProperty('rate', 120)  # slow down the reading speed.
        engine.save_to_file(text, os.path.join(INBOX, path))
        engine.runAndWait()


# # load text message spam
# messages = pd.read_csv('./data/text_messages.csv', encoding='ISO-8859-1')
# spam = messages[messages.v1 == 'spam'].v2
#
# # text message preprocessing
# spam = spam.str.replace('å', '')
# spam = spam.str.replace('"', '')
# spam = spam.str.replace('&amp', '')
#
# # save processed spam to file
# spam.to_csv('./data/spam_texts.txt', sep=' ', index=False)

# process transcripts for ham recordings
for file in os.listdir('./data/TRN'):
    filename = os.fsdecode(file)
    chat_id = filename[:-4]  # remove file extension
    transcripts[chat_id] = pd.DataFrame(columns=['time', 'transcription'])

    with open('./data/TRN/' + filename, encoding='cp1252') as f:
        file = f.readlines()
        f.close()

    transcript = transcripts[chat_id]

    for index, line in enumerate(file):
        time, transcription = parse(line)
        transcript = transcript.append(
            {'time': time, 'transcription': transcription},
            ignore_index=True
        )
        transcript.dropna(inplace=True)

    transcript.set_index('time', inplace=True)
    transcripts[chat_id] = transcript
    ham.append(ButtDial(chat_id))
    print('Processed', chat_id)

# initialize spam model and robot voices
with open('./data/spam_texts.txt', encoding='utf8') as f:
    spam = f.readlines()
    f.close()

spam = markovify.Text(spam)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
robots = [Robot(voice) for voice in voices]

call_machine = robots[0]
robots.remove(call_machine)
audio_id = 1

# make answering machine transcript
while words < MAX_WORD_COUNT:
    total = 0
    call = ''
    date = call_date.strftime("%A, %I:%M %p.")
    novel += '\n' + date + '\n---------------------------------------\n'

    call_machine.say(date, f'{audio_id:04}' + '.wav')
    audio_id += 1

    message_type = random.randint(0, 1)
    filename = f'{audio_id:04}' + '.wav'  # name of file for saved message
    audio_id += 1

    if message_type == SPAM:
        total, call = get_spam()
        random.choice(robots).say(call, filename)
    elif message_type == HAM:
        message = get_ham()
        total, call = message.play(random.randint(20, MAX_HAM_LEN), filename)

    novel += call + '\n\n'

    words += total + len(date.split())
    total_calls += 1
    call_date = call_date + timedelta(minutes=random.randint(10, 1450))

call_machine.say('End of messages.', f'{audio_id:04}' + '.wav')
novel += '\nEnd of messages.'

preamble = 'You have {0} new messages.\n\n'.format(total_calls)
call_machine.say(preamble, '0000.wav')
novel = preamble + novel

print('total words {0}'.format(words))

# save transcript to file
with open(os.path.join('./audiobook/transcript.txt'), 'w') as out:
    sys.stdout = out
    print(novel)
    out.close()

# read all saved audio messages
messages = [player.from_file(os.path.join(INBOX, message), format='wav') for message in sorted(os.listdir(INBOX))]
messages.remove('.gitignore')  # ignore the gitignore
combined = player.empty()  # for combined audiobook

message_count = messages[0]
combined += message_count  # start audiobook with message count preamble

for index, message in enumerate(messages[1:]):
    combined += message

    # every even numbered index is voice machine. Beep only after message.
    if index % 2 == 1:
        combined += player.from_file('./sounds/beep_koenig.wav', format='wav')
        combined += SILENCE

# save audiobook
combined.export('./audiobook/messages.wav', format='wav')
