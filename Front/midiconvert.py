from mido import MidiFile
import operator


def MIDIconvert(file):
	mid = MidiFile(file)
	sequence=[]
	previous=0
	for i, track in enumerate(mid.tracks):
	    #print('Track {}: {}'.format(i, track.name))
	    for msg in track:
	        if msg.type == 'note_on'or msg.type == 'note_off':
	    		#(msg.note)
	    		if msg.type == 'note_on':
	    			note=1
	    		else:
	    			note=0
	    		sequence.append([msg.time/6+previous+1,msg.note-24,note,0])
	    		previous+=msg.time/6
	#print(sequence)

	i=0
	while i<=len(sequence)-1:
		if sequence[i][2]==1:
			j=i
			while j<=len(sequence)-1:
				if sequence[j][2]==0 and sequence[j][1]==sequence[i][1]:
					duration=sequence[j][0]-sequence[i][0]
					sequence[i][3]=duration
					sequence[j][3]=duration
					#print(i, j ,"here")
					break
				j+=1
		i+=1
	#print(sequence)
	sequence=sorted(sequence, key=operator.itemgetter(0,1,2))
	#print(sequence)
	return sequence


#MIDIconvert('test4.mid')
