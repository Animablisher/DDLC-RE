# File: glitchtext.rpy
init python:
    import random

    nonunicode = "أببَبُبْثَثُثْثِججَجُجْششَشُشْضضَضُضْططَطُطْطِظظَظُظْظِققَقُقْقِككَكُكْكِههَهُهْئئَئُئْؤؤَؤُؤْءءَءُءْءِىىَىُىْةةَةُةْةِااَاُاْاِآآِ\".,،؛:0123456789"

#    nonunicode = "أببَبُبْتتَتُتْتِثَثُثْثِججَجُجْححَحُحْخخَخُخْسسَسُسْششَشُشْصصَصُضضَضُضْططَطُطْطِظظَظُظْظِععَعُعْغغَغُغْففَفُفْفِققَقُقْقِككَكُكْكِللَلُلْلِممَمُمْننَنُنْنِههَهُهْووَوُوْييَيُيْئئَئُئْؤؤَؤُؤْءءَءُءْءِىىَىُىْةةَةُةْةِااَاُاْاِآآِ\".,،؛:0123456789"

    def glitchtext(length):
        output = ""
        for x in range(length):
            output += random.choice(nonunicode)
        return output
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
