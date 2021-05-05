from tkinter import *
import pygame
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('My MP3 Player')
root.geometry("550x350")

# Initialize Pygame Mixer
pygame.mixer.init()

# Play selected song
def play_the_song():
	song = List_of_songs.get(ACTIVE)
	song = f'D:/MP3_PLAYER/GUI/Music/{song}.mp3'


	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

# Stop playing current song
def stop_the_song():
	pygame.mixer.music.stop()
	List_of_songs.selection_clear(ACTIVE)


# Play the next song in the playlist
def next_song():
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
	# Delete currently selected song
	List_of_songs.delete(ANCHOR)
	#Stop music if it's playing
	pygame.mixer.music.stop()


# Remove all songs from the playlist
def remove_all_songs():
	# Delete all songs
	List_of_songs.delete(0, END)
	#Stop music if it's playing
	pygame.mixer.music.stop()


specify_font= font.Font(size=15)

#Create Playlist box
List_of_songs = Listbox(root, bg="black", fg="blue" , width=200 , height=35)
List_of_songs.pack(pady= 50)

# Define Player Control Buttons Images
back_btn_img = PhotoImage(file = 'Images_buttons/back55.png')
forward_btn_img = PhotoImage(file = 'Images_buttons/forward55.png')
play_btn_img = PhotoImage(file = 'Images_buttons/play55.png')
pause_btn_img = PhotoImage(file = 'Images_buttons/pause55.png')
stop_btn_img = PhotoImage(file = 'Images_buttons/stop55.png')


# Create Player Control Frames 
controls_frame = Frame(root)
controls_frame.pack(side=BOTTOM, padx=20, pady=30)

# Create Player Control Buttons
back_button = Button(controls_frame, image= back_btn_img, borderwidth=0, command= previous_song)
forward_button = Button(controls_frame, image= forward_btn_img, borderwidth=0, command= next_song)
play_button = Button(controls_frame, image= play_btn_img, borderwidth=0, command= play_the_song)
pause_button = Button(controls_frame, image= pause_btn_img, borderwidth=0, command= lambda: pause_or_unpause(is_paused))
stop_button = Button(controls_frame, image= stop_btn_img, borderwidth=0, command= stop_the_song)

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


root.mainloop()