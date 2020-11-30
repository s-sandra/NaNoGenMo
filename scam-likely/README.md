# Scam Likely
Created as my 2020 entry for National Novel Generation Month, this Python program writes an audiobook and transcript that 
emulates a recording of a (very long) list of messages on an answering machine. The calls largely consist of 
excerpts of recorded conversations (butt dials, perhaps?), as well as occasional spam thrown in for comedic effect. 
The spam text was generated using a Markov chain "trained" on the [University of California, Urvine SMS Spam Collection Dataset](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection),
with audio created using the SAPI5 text-to-speech engine. The human conversations and transcripts were taken directly 
from the [University of California, Santa Barbara Corpus of Spoken American English](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus).
To listen to the full +7 hour long audiobook, go [here](https://drive.google.com/file/d/10ZACURKBeYQudqj8Nk8Ae7cZM1Q-rAcK/view?usp=sharing/view?t=1m20s).

## Excerpts
Read along to a [short preview of the audiobook](https://drive.google.com/file/d/1eueWZ_x4RIVldpA04uIFa1e6T3o8YZHu/view?usp=sharing)!
The first call is a portion of [*Wonderful Abstract Notions*](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus#SBC017),
where two old friends have a philosophical discussion about the future of science and technology. The second
call, titled [*Stay Out of It*](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus#SBC042), is an argument
that takes place in a car between Kitty and her teenage daughter, Kendra. Kitty believes that 
Kendra slept over at her friend Melanie's house without her permission.
```
Thursday, 02:15 AM.
---------------------------------------
Hm. yeah. And even if I go out and ask for it. you know, I say, Q can I 
copy that . I won't feel guilty. I really won't . It's just a set of 
instructions, I used to program. a little bit, and, and um, those guys 
have so much fun writing those programs. you know, that's the I think 
that's that's pretty Yeah well, That's pretty much the end of it. 
creative people generally do what they love to do. Yeah, right. And 
that's pretty much the end of the truthful part of the process. The 
rest of it is all marketing. Hm. and the marketplace is uh, you know, 
maybe I think I live in Tangiers. you know? Maybe I think the 
marketplace is uh, you get what you can get. yeah. Uh, seems to be 
that way. you know, I as long as I'm not hurting another person 
directly, Right. You know? or even indirectly. but just throwing my 
money out there, he may never see a penny of it. he may have sold the 
rights.


Thursday, 03:37 PM.
---------------------------------------
You're so stupid thinking I spent the night. I came home last night 
and told you. Kendra, just let it go. You No, because she doesn't 
All you said last night was, She thinks I spent the night in my jeans
 Kim wasn't staying the night . If I did spend the night, and I was 
trying to lie, I would give up. Cause then I wouldn't care. Cause 
I knew I deserved it. But I didn't spend the night, and I don't 
deserve this. Kim couldn't spend the night, I told you. She could, 
but then af I wanted to stay at the game longer? And her mom wanted 
to take her home early, and I'm like, no let's stay longer. But her 
mom wouldn't let her? And so she went home and, I was like, I'll call 
you when I get home, and then you come over. And she goes, no just 
spend the night. We'll do this some other weekend. Okay cool, cause 
she had to go bowling in the morning. Talk to Melanie's mom . Her 
mom would know. I'll have Melanie call you. Oh, Her mom call you, 
right, right, her mom wouldn't lie, right, Melanie will call me 
to confirm your lie, Melanie lies but,


Friday, 06:25 AM.
---------------------------------------
This is an important call. Txt NOKIA to 83383 now. Auction is FREE 2 
join & take a friend 4 FREE.

```

## Dependencies
To create an audiobook, you must have installed the `pyttsx3` library for text-to-speech 
conversion,`markovify` to generate the spam text, `pydub` for audio processing, slicing and merging,
and `pandas` for data processing. These can be installed through the following commands.

```
pip install pandas
pip install pydub
pip install pyttsx3
pip install markovify
```

## How It Works
### Robot.Say(Spam)
To generate calls, the program randomly selects to create spam or ham messages. 
Spam is written using a Markovify model, between 15 and 25 words long. The local TTS engine
then converts the spam to sound and saves it in a separate `wav` file. There are
three available robot voices on my machine. Microsoft David serves as the voice for
the answering machine, while MS Hazel and MS Zira are randomly selected to narrate
the spam.<br>

### Can You Pass the Ham?
To create ham, the program randomly selects from a list of sixty conversations 
within the Santa Barbara Corpus. The transcript of each conversation is previously 
cleaned and parsed for timestamps. The program "plays" up to sixty seconds of the 
selected conversation, returns the corresponding portions of the transcript, 
saves the excerpt to a separate `wav` file, and stores the paused location in 
the recording. As such, the next time the conversation is randomly selected, the 
call will continue where it left off, until the entire recording is exhausted and 
removed from the list of possible selections.

### Putting it All Together
The separate audio files are then merged together using `pydub`, with an answering
machine beep inserted in between calls. The beep was recorded by [Mike Koenig](http://soundbible.com/5-Answering-Machine-Beep.html)
and shared via SoundBible under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/).
