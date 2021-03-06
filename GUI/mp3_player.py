from tkinter import *
import pygame
from tkinter import filedialog
from tkinter import font
import time
from mutagen.mp3 import MP3
from ShazamAPI import Shazam
import tkinter.ttk as ttk

root = Tk()
root.title('My MP3 Player')
root.geometry("550x400")

# Initialize Pygame Mixer
pygame.mixer.init()


#Get Song Length Time Information
def play_time():

	# Check for double timing
	if stopped:
		return
	# Grab current song elapsed time
	current_time = pygame.mixer.music.get_pos() /1000
	
	#throw up temporary label to get data
	#slider_label.config(text=f'Slider:{int(my_slider.get())} and Song Pos: {int(current_time)}')

	# Convert to time format
	Converted_format = time.strftime('%M:%S', time.gmtime(current_time))

	# Get song title from the playlist
	current_song = List_of_songs.get(ACTIVE)
	# Add directory structure and mp3 to song title  
	current_song = f'D:/MP3_PLAYER/GUI/Music/{current_song}.mp3'

	# Load song with Mutagen
	song_mut = MP3(current_song)
	# Get Song Length
	global song_length
	song_length = song_mut.info.length
	# Convert to time format
	Converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	# Increase current time by 1 second
	current_time += 1

	if int(my_slider.get()) == int(song_length):
		status_bar.config(text=f'Time Elapsed: {Converted_song_length} of {Converted_song_length}  ')

	elif is_paused:
		pass

	elif int(my_slider.get()) == int(current_time):
		#Update slider to position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(current_time))
	else:
		#Update slider to position
		slider_position = int(song_length)	
		my_slider.config(to=slider_position, value=int(my_slider.get()))

		# Convert to time format
		Converted_format = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

		# Output time to status bar
		status_bar.config(text=f'Time Elapsed: {Converted_format} of {Converted_song_length}  ')

		# Move this thing along by one second
		next_time = int(my_slider.get()) + 1
		my_slider.config(value=next_time)


	# Update slider position value to current song position
	#my_slider.config(value=int(current_time))

	# Update time
	status_bar.after(1000, play_time)

 
global playing 
playing = False 

# Play selected song
def play_the_song():
	# Set stopped variable to false so song can play
	global stopped
	global playing 
	stopped = False
	playing = True
	song = List_of_songs.get(ACTIVE)
	song = f'D:/MP3_PLAYER/GUI/Music/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	#Call the play_time function to get song length
	play_time()

	#Update slider to position
	#slider_position = int(song_length)
	#my_slider.config(to=slider_position, value=0)

	#Get current volume
	#current_volume = pygame.mixer.music.get_volume()
	#slider_label.config(text=current_volume*100)
	

# Stop playing current song
global stopped
stopped  = False


# Stop playing current song
def stop_the_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# Stop song from playing
	pygame.mixer.music.stop()
	List_of_songs.selection_clear(ACTIVE)

	# Clear the Status Bar
	status_bar.config(text='')

	# Set stop variable to true
	global stopped
	stopped  = True
	

# Play the next song in the playlist
def next_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# Get the current song tuple number
	next_one = List_of_songs.curselection()
	# Add one to the current song number
	next_one = next_one[0]+1
	# Get song title from the playlist
	curr_song = List_of_songs.get(next_one)
	# Add directory structure and mp3 to song title  
	curr_song = f'D:/MP3_PLAYER/GUI/Music/{curr_song}.mp3'
	# Load and play song
	pygame.mixer.music.load(curr_song)
	pygame.mixer.music.play(loops=0)

	#Clear active bar in the playlist
	List_of_songs.selection_clear(0, END)
	
	#Activate next song bar
	List_of_songs.activate(next_one)
	# Set Activate Bar to next song
	List_of_songs.selection_set(next_one, last=None)



# Play Previous Song In Playlist
def previous_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# Get the current song tuple number
	next_one = List_of_songs.curselection()
	# Add one to the current song number
	next_one = next_one[0]-1
	# Get song title from the playlist
	curr_song = List_of_songs.get(next_one)
	# Add directory structure and mp3 to song title  
	curr_song = f'D:/MP3_PLAYER/GUI/Music/{curr_song}.mp3'
	# Load and play song
	pygame.mixer.music.load(curr_song)
	pygame.mixer.music.play(loops=0)

	#Clear active bar in the playlist
	List_of_songs.selection_clear(0, END)
	
	#Activate next song bar
	List_of_songs.activate(next_one)
	# Set Activate Bar to next song
	List_of_songs.selection_set(next_one, last=None)



# Pause and Unpause The Current Song
global is_paused
is_paused = False

def pause_or_unpause(paused):
	global is_paused
	is_paused = paused
    
	if paused:
		pygame.mixer.music.unpause()
		is_paused = False

	else:
		pygame.mixer.music.pause()
		is_paused = True



# Add Song Function
def add_song():
	song = filedialog.askopenfilename(initialdir= 'Music/', title="Pick a Song", filetypes= (("mp3 files", "*.mp3"), ))

	# Strip out the directory info and .mp3 extension from the song name 
	song_name=song.split('/')[-1].split('.')[0]

    # Add song to listbox
	List_of_songs.insert(END, song_name)

# Add many songs to playlist
def add_many_songs():
	Songs = filedialog.askopenfilenames(initialdir= 'Music/', title="Pick one or many songs", filetypes= (("mp3 files", "*.mp3"), ))


	# Loop through song list 
	for song in Songs :
		song=song.split('/')[-1].split('.')[0]

		List_of_songs.insert(END, song)
 	


# Remove one song from the playlist
def remove_a_song():
	stop_the_song()
	# Delete currently selected song
	List_of_songs.delete(ANCHOR)
	#Stop music if it's playing
	pygame.mixer.music.stop()


# Remove all songs from the playlist
def remove_all_songs():
	stop_the_song()
	# Delete all songs
	List_of_songs.delete(0, END)
	#Stop music if it's playing
	pygame.mixer.music.stop()


# Create Slider function
def Slider(x):
	#slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
	song = List_of_songs.get(ACTIVE)
	song = f'D:/MP3_PLAYER/GUI/Music/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start= int(my_slider.get()))


specify_font= font.Font(size=15)

# Create Volume Function
def Volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

	# Get current volume
	#current_volume = pygame.mixer.music.get_volume()
	#slider_label.config(text=current_volume*100)


def getDetails(fileloc, all=False):
	content = open(fileloc,'rb').read()
	shazam = Shazam(content)
	gen = shazam.recognizeSong()
	res = next(gen)
	returnees=[]
	if all:
		return res
	
	

	try:
		Details_of_song.insert(1, res[1]["track"]["share"]["subject"])
	except:
		Details_of_song.insert(1, "Title not found!")
	try:
		Details_of_song.insert(2, res[1]["track"]["sections"][1]['footer'].split(maxsplit = 6))
	except:
		Details_of_song.insert(2, "Details not found!")
	try:
		Details_of_song.insert(3, "Lyrics: ")
		i = 4
		for lines in res[1]["track"]["sections"][1]["text"]:
			Details_of_song.insert(i, lines)
			i += 1
	except:
		Details_of_song.insert(3, "Lyrics not found!")


# To get the details of the song
global list_details 
list_details =[]

def getDetailsButton(is_playing):
	global playing
	playing = is_playing
	if playing == True :
		Details_of_song.delete(0, 'end')
		song = List_of_songs.get(ACTIVE)
		song = f'D:/MP3_PLAYER/GUI/Music/{song}.mp3'		
		list_details = getDetails(song)


# Add background image
bg = PhotoImage(file="Images_buttons/newbg.png") 


# Add Label
bg_label = Label(root, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Create Canvas
#canvas1 = Canvas( root, width = 400, height = 400)
#canvas1.pack(fill = "both", expand = True)
  
# Display image
#canvas1.create_image( 0, 0, image = bg, anchor = "nw")

# Add Text
#canvas1.create_text( 200, 250, text = "Welcome")


# Create Master Frame
master_frame = Frame(root, bg="black", height=250, width=100)
master_frame.pack(pady=10, padx=10)

# Create Song Frames 
song_frame = Frame(master_frame, bg="black")
song_frame.grid(row=0, column=0)


# Create Scrollbar for details
details_scroll = Scrollbar(song_frame, orient=VERTICAL)

#Create Playlist box
List_of_songs = Listbox(song_frame, bg="black", fg="#37a6bf" , width=75 , height=25)
List_of_songs.grid(row=0, column=0)

#Create Detail box
Details_of_song = Listbox(song_frame, bg="black", fg="#37a6bf", width=75, height=25, yscrollcommand=details_scroll.set)
Details_of_song.grid(row=0, column=1)

#Details_of_song = list_details.copy()

#Config Scrollbar
details_scroll.config(command= Details_of_song.yview)
#details_scroll.pack(side=RIGHT, fill=Y)
details_scroll.grid(row=0, column=2)


# Define Player Control Buttons Images
back_btn_img = PhotoImage(file = 'Images_buttons/skip-back-button.png')
forward_btn_img = PhotoImage(file = 'Images_buttons/fast-forward-button.png')
play_btn_img = PhotoImage(file = 'Images_buttons/playbutton.png')
pause_btn_img = PhotoImage(file = 'Images_buttons/video-pause-button.png')
stop_btn_img = PhotoImage(file = 'Images_buttons/stop-button.png')


# Create Player Control Frames 
controls_frame = Frame(master_frame, bg="black")
controls_frame.grid(row=1, column=0, pady=30)

# Create Volume Label Frame
volume_frame = LabelFrame(master_frame, bg="black", text="Volume", foreground="white")
volume_frame.grid(row=0, column=1, padx = 10)

# Create Player Control Buttons
back_button = Button(controls_frame, background= "black" , image= back_btn_img, borderwidth=0, command= previous_song)
forward_button = Button(controls_frame, background= "black" , image= forward_btn_img, borderwidth=0, command= next_song)
play_button = Button(controls_frame, background= "black" , image= play_btn_img, borderwidth=0, command= play_the_song)
pause_button = Button(controls_frame, background= "black" , image= pause_btn_img, borderwidth=0, command= lambda: pause_or_unpause(is_paused))
stop_button = Button(controls_frame, background= "black" , image= stop_btn_img, borderwidth=0, command= stop_the_song)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Menu
my_menu = Menu(root)
root.config(menu = my_menu)

# Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label= "Add Songs", menu=add_song_menu)
# Add One Song to Playlist
add_song_menu.add_command(label= "Add one song to playlist", command= add_song)
# Add Many Songs to Playlist
add_song_menu.add_command(label= "Add many songs to playlist", command= add_many_songs)

#Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Remove Songs", menu= remove_song_menu)
# Remove One Song from the Playlist
remove_song_menu.add_command(label= "Delete a song from playlist", command= remove_a_song)
# Remove Many Songs from the Playlist
remove_song_menu.add_command(label= "Delete all songs from playlist", command= remove_all_songs)



# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=3)


# Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=Slider, length=450)
my_slider.grid(row=2, column=0, pady=10)

# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=Volume, length=125)
volume_slider.pack(pady=40)


# Create temporary slider label
#slider_label = Label(root, text="0")
#slider_label.pack(pady=10)

#Add Button for details
detailbutton = Button(root, text="Details", font="operetta", background="white", pady=10, padx=10, foreground= "black",  command= lambda: getDetailsButton(playing))
detailbutton.pack()

root.mainloop()