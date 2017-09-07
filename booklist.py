import random
amber = ['BORDERLINE by Mishelle Baker',
         'MAGIC FOR BEGINNERS by Kelly Link']
anie = ['ASH by Malinda Lo',
        'FILTER HOUSE by Nisi Shawl',
        'GHOST TALKERS by Mary Robinette Kowal',
        'INK by Sabrina Vourvoulias',
        'MY SOUL TO KEEP by Tananarive Due',
        'REDEMPTION IN INDIGO by Karen Lord',
        'SISTER MINE by Nalo Hopkinson',
        'THE DEVOURERERS by Indra Das',
        'THE LOST GIRL by Sangu Mandanna',
        'THE SPARROW by Mary Russell',
        'THE SUDDEN APPEARANCE OF HOPE by Claire North',
        'UP THE WALLS OF THE WORLD by James Tiptree, Jr.',
        'LAVINIA by Ursula K. LeGuin']
clara = ['AND AGAIN by Jessica Chiarella',
         'JONATHAN STRANGE AND MR. NORRELL by Susanna Clarke',
         'MINDSCAPE by Andrea Hairston',
         'ROOMS by Lauren Oliver',
         'THE FEMALE MAN by Joanna Russ',
         'THE MEMORY GARDEN by Mary Rickert',
         'ZERO BOXES by Fonda Lee',
         'THE ILLUMINAE by Amie Kaufman and Jay Kristoff',
         'THE HANDMAID\'S TALE by Margaret Atwood',
         'BOOK OF THE UNNAMED MIDWIFE by Meg Elison',
         'EVERFAIR by Nisi Shawl',
         'HARMLESS LIKE YOU by Rowan Hisayo Buchanan'
         'WHAT IT MEANS WHEN A MAN FALLS FROM THE SKY by Lesley Nneka Arimah',
         'HER BODY AND OTHER PARTIES by Carmen Maria Machado']
emma = ['SILENTLY AND VERY FAST by Pat Cadigan',
        'THE LEFT HAND OF DARKNESS by Ursula K LeGuin']
juniper = ['ALIF THE UNSEEN by G. Willow Wilson',
           'ASSASSIN\'S APPRENTICE by Robin Hobb',
           'BLACK SUN RISING by C.S. Friedman',
           'DREAMSNAKE by Vonda N. McIntire',
           'HER SMOKE ROSE UP FOREVER by James Tiptree, Jr.',
           'HUNTRESS by Malinda Lo',
           'TEHANU by Ursula K LeGuin',
           'THE BLUE SWORD by Robin McKinley',
           'THE DARKEST PART OF THE FOREST by Holly Black',
           'THE GOBLIN EMPEROR by Katherine Addison',
           'THE TOMBS OF ATUAN by Ursula K LeGuin',
           'THE WARRIOR\'S APPRENTICE by Lois McMaster Bujold',
           'THIS IS NOT A TEST by Courtney Summers',
           'THRONE OF GLASS by Sarah J. Maas',
           'WHEN WOMEN WERE WARRIORS by Catherine M. Wilson']
karena = ['ANCILLARY JUSTICE by Ann Leckie',
          'WOMAN NO. 17 by Edan Lepucki',
          'GHOST SUMMER: STORIES by Tananarive Due',
          'MEMOIRS OF A SPACE WOMAN by Naomi Mitchinson',
          'MIDNIGHT ROBBER by Nalo Hopkinson',
          'PLANETFALL by Emma Newton',
          'THE KILLING MOON by N.K. Jemisin',
          'THE OFFICE OF MERCY by Ariel Djanikian',
          'THE SNOW QUEEN by Joan D. Vinge',
          'THE WINGED HISTORIES by Sofia Samatar',
          'THE WORD EXCHANGE by Alena Graedon',
          'WOMAN ON THE EDGE OF TIME by Marge Piercy',
          'ASCENSION by Jacqueline Koyanagi',
          'BEHIND THE THRONE by K.B. Wagers',
          'INFOMANCY by Malka Older',
          'NINEFOX GAMBIT by Yoon Ha Lee',
          'CERTAIN DARK THINGS by Silvia Moreno Garcia',
          'BOOK OF JOAN by Lidia Yuknavitch',
          'THE GUNS ABOVE by Robyn Bennis',
          'AMBERLOUGH by Lara Elena Donnelly',
          'SISTERS OF THE REVOLUTION by Ann Vandermeer',
          'THE QUICK by Laren Owen',
          'VICIOUS by V.E. Schwab']

bookSet = [random.sample(clara, 1), random.sample(karena,1),
         random.sample(anie, 1), random.sample(amber, 1),
         random.sample(juniper,1)]

bookSample = random.sample(bookSet,4)

print(bookSample[0])
print(bookSample[1])
print(bookSample[2])
print(bookSample[3])
