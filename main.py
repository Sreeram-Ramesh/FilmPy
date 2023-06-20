from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.config import Config
from urllib.request import urlopen
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList
from kivymd.theming import ThemableBehavior
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivymd.uix.button import MDRectangleFlatButton , MDFlatButton , MDRaisedButton
from filmpy_sql import *
import mysql
import imdb

#Window.fullscreen = True
#Window.maximize()

Config.set('input', 'mouse', 'mouse,disable_multitouch')

class Startup(Screen):
	pass

class Login(Screen):
	pass

class Signup(Screen):
	pass	

class Genre(Screen):
	pass

class Home(Screen):
	class ContentNavigationDrawer(BoxLayout):
		def changetologin(self):
			MDApp.get_running_app().root.current = 'login'

	class DrawerList(ThemableBehavior, MDList):
		pass

	def on_pre_enter(self):
		addwindow_instance = MDApp.get_running_app().root.get_screen('home')
		
		review_list = getrandom_sql(8)


		for review in review_list:
			addwindow_instance.ids["image{}".format(review_list.index(review))].source = review["image url"]
			addwindow_instance.ids["username{}".format(review_list.index(review))].text = str(review["username"])
			addwindow_instance.ids["rate{}".format(review_list.index(review))].text = "           {} / 10".format(review["rating"])
			addwindow_instance.ids["time{}".format(review_list.index(review))].text = "           {}".format(review["datetime"])
			addwindow_instance.ids["review{}".format(review_list.index(review))].text = "[b]{}[/b]".format(str(review["review"]))
			addwindow_instance.ids["title{}".format(review_list.index(review))].text = str(review["title"])

class Account(Screen):
	pass

class ReadWrite(Screen):
	movieid = ""
	source = StringProperty 
	
	def on_pre_enter(self):

		dic = moviedesc_sql(self.movieid)

		self.ids.widget.height = 30
		self.ids.title.text = "[b]{}[/b]".format(dic["title"])
		self.ids.image.source = "{}".format(dic["full-size cover url"])
		self.ids.plotoutline.text = dic["plot outline"]
		if len(dic["plot outline"]) > 600:
			self.ids.widget.height = 90
		self.ids.genres.text = "Genres : {}".format(", ".join(dic["genres"]))
		self.ids.director.text = "Directed by: {}".format(dic["director"])
		self.ids.year.text = "Year: {}".format(dic["year"])
		self.ids.cast.text = "\nCast : {}".format(", ".join(dic["cast"]))
		self.ids.submit.disabled = False
		
	def spinner_clicked(self, value):
		pass	


class Reviews(Screen):

	def on_pre_enter(self):
		review_list = getbymovie_sql(ReadWrite.movieid)

		if len(review_list) == 0:
			self.ids.reviewboxin.add_widget(Factory.MDLabel(
				text= "No reviews to display.",
				halign= "center",
				font_style= "H4"
				))
			
			self.ids.reviewboxin.add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			self.ids.reviewboxin.add_widget(Factory.MDCard(
				orientation= "vertical",
				size_hint_x= 0.7,
				size_hint_y= None,
				height= 5,
				elevation= 0
				))


		for review in review_list: 

			self.ids.reviewboxin.add_widget(Factory.MDRectangleFlatIconButton(
					icon= "account-circle",
					text= "[b]{}[/b]".format(review["username"]),
					font_size= 22,
					theme_text_color= "Custom",
					text_color= (1, 1, 1, 1),
					line_color= (0, 0, 0, 0),
					theme_icon_color= "Custom",
					icon_color= (14/255, 122/255, 254/255, 1),
				))

			self.ids.reviewboxin.add_widget(Factory.MDLabel(
				markup= True,
				text= "         {}".format(review["datetime"]),
				theme_text_color= "Custom",
				text_color= (0/255, 255/255, 255/255, 1),
				halign= "left",
				font_style= "Caption"
				))

			self.ids.reviewboxin.add_widget(Factory.MDLabel(
				markup= True,
				text= "         [b]Rating[/b]: {} / 10".format(review["rating"]),
				theme_text_color= "Custom",
				text_color= (255/255, 215/255, 0/255, 1),
				halign= "left",
				font_style= "Subtitle2"
				))

			if review["review"].count("\n") > 4 or len(review["review"]) > 400:
				self.ids.reviewboxin.add_widget(Factory.Widget(
					size_hint_y= None,
					height= 110
					))
			else:
				self.ids.reviewboxin.add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			self.ids.reviewboxin.add_widget(Factory.MDLabel(
				markup= True,
				text= "{}".format(review["review"]),
				halign= "left",
				font_style= "H6"
				))

			if review["review"].count("\n") > 4 or len(review["review"]) > 400:
				self.ids.reviewboxin.add_widget(Factory.Widget(
					size_hint_y= None,
					height= 70
					))

			self.ids.reviewboxin.add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			self.ids.reviewboxin.add_widget(Factory.MDCard(
				orientation= "vertical",
				size_hint_x= 1,
				size_hint_y= None,
				height= 5,
				elevation= 0
				))

	def on_leave(self):
		self.ids.reviewboxin.clear_widgets()
		
class Search(Screen):
	pass

class YourReviews(Screen):

	current_username = ""

	def on_pre_enter(self):
		review_list = getbyuser_sql(self.current_username)

		if len(review_list) == 0:
			self.ids.yourreviewboxin.add_widget(Factory.MDLabel(
				text= "No reviews to display.",
				halign= "center",
				font_style= "H4"
				))
			
			self.ids.yourreviewboxin.add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			self.ids.yourreviewboxin.add_widget(Factory.MDCard(
				orientation= "vertical",
				size_hint_x= 0.7,
				size_hint_y= None,
				height= 5,
				elevation= 0
				))


		for review in review_list: 

			self.ids.yourreviewboxin.add_widget(Factory.MDRectangleFlatIconButton(
					icon= "movie-open",
					text= "[b]{}[/b]".format(review["title"]),
					font_size= 22,
					theme_text_color= "Custom",
					text_color= (1, 1, 1, 1),
					line_color= (0, 0, 0, 0),
					theme_icon_color= "Custom",
					icon_color= (14/255, 122/255, 254/255, 1),
				))

			self.ids.yourreviewboxin.add_widget(Factory.MDLabel(
				markup= True,
				text= "         {}".format(review["datetime"]),
				theme_text_color= "Custom",
				text_color= (0/255, 255/255, 255/255, 1),
				halign= "left",
				font_style= "Caption"
				))

			self.ids.yourreviewboxin.add_widget(Factory.MDLabel(
				markup= True,
				text= "         [b]Rating[/b]: {} / 10".format(review["rating"]),
				theme_text_color= "Custom",
				text_color= (255/255, 215/255, 0/255, 1),
				halign= "left",
				font_style= "Subtitle2"
				))

			if review["review"].count("\n") > 4 or len(review["review"]) > 400:
				self.ids.yourreviewboxin.add_widget(Factory.Widget(
					size_hint_y= None,
					height= 110
					))
			else:
				self.ids.yourreviewboxin.add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			self.ids.yourreviewboxin.add_widget(Factory.MDLabel(
				markup= True,
				text= "{}".format(review["review"]),
				halign= "left",
				font_style= "H6"
				))

			if review["review"].count("\n") > 4 or len(review["review"]) > 400:
				self.ids.yourreviewboxin.add_widget(Factory.Widget(
					size_hint_y= None,
					height= 70
					))

			self.ids.yourreviewboxin.add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			self.ids.yourreviewboxin.add_widget(Factory.MDCard(
				orientation= "vertical",
				size_hint_x= 1,
				size_hint_y= None,
				height= 5,
				elevation= 0
				))

	def on_leave(self):
		self.ids.yourreviewboxin.clear_widgets()


class MovieSuggestion(Screen):
	current_username = ""
	def on_pre_enter(self):
		movieids = suggest_sql(self.current_username, r"dataset.dat")
		addwindow_instance = MDApp.get_running_app().root.get_screen('moviesuggestion')
		
		count = 0

		for i in movieids:
			dic = moviedesc_sql(i)
			addwindow_instance.ids["widget{}".format(count)].height = 30
			addwindow_instance.ids["title{}".format(count)].text = "[b]{}[/b]".format(dic["title"])
			addwindow_instance.ids["image{}".format(count)].source = "{}".format(dic["full-size cover url"])
			addwindow_instance.ids["plotoutline{}".format(count)].text = dic["plot outline"]
			if len(dic["plot outline"]) > 600:
				addwindow_instance.ids["widget{}".format(count)].height = 90
			addwindow_instance.ids["genres{}".format(count)].text = "Genres : {}".format(", ".join(dic["genres"]))
			addwindow_instance.ids["director{}".format(count)].text = "Directed by: {}".format(dic["director"])
			addwindow_instance.ids["year{}".format(count)].text = "Year: {}".format(dic["year"])
			addwindow_instance.ids["cast{}".format(count)].text = "\nCast : {}".format(", ".join(dic["cast"]))

			count += 1



class WindowManager(ScreenManager):
	pass	

class FilmPyApp(MDApp):

	genrelist = []
	dialog = None
	current_username = ""

	def build(self):
		self.passwd_user = ""
		self.img = r"Images\flm.png"
		self.no_net = MDDialog(
			title =	"No Internet",
			text = "Check your network connection.",
			buttons = [
				MDFlatButton(
					text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
			
			] 
			)

		self.theme_cls.theme_style = 'Dark'
		return Builder.load_file('init_pg.kv')

	def is_internet_available(self):
		try:
			urlopen('https://www.google.com/', timeout=1)
			return True
		except:
			return False

	def forgot_passwd(self,username,passwd):
		self.passwd_user = username
		
		if login_sql(username , passwd) == "invalid":
			self.show_alert_dialog(MDDialog(
				title = "Username error",
				text = "Username does not exist!",
				buttons = [
					MDFlatButton(
						text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
			
				],
				))
		else:
			self.show_alert_dialog(MDDialog(
				title = "Confirm",
				text = "Press 'OK' if you want your password be sent to your registered email id. [Please check your spam folder]",
				buttons = [
					MDFlatButton(
						text = "CANCEL", text_color=self.theme_cls.primary_color, on_release = self.close_dialog),
					MDFlatButton(
						text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog_pass)
			
				],
				))			

	def show_alert_dialog(self,box_content):
		self.dialog = box_content

		self.dialog.open()

	def close_dialog(self,obj):
		self.dialog.dismiss()

	def close_dialog_pass(self,obj):
		pwdrecovery_sql(self.passwd_user)
		self.dialog.dismiss()

	def home_logout(self):
		MDApp.get_running_app().root.current = 'login'

	def home_account(self):
		MDApp.get_running_app().root.current = 'account'	
	
	def home_search(self):
		MDApp.get_running_app().root.current = 'search'		

	def signer(self):
		addwindow_instance = self.root.get_screen('signup')

		username = addwindow_instance.ids["signupuser"].text
		email = addwindow_instance.ids["signemail"].text
		passwd = addwindow_instance.ids["signpassword"].text


		if len(passwd) < 8:
			self.show_alert_dialog(MDDialog(
				title = "Password error",
				text = "Minimum 8 characters required.",
				buttons = [
					MDFlatButton(
						text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
			
				],
				))
		elif email == "":
			self.show_alert_dialog(MDDialog(
				text = "Email id is required for password retention.",
				buttons = [
					MDFlatButton(
						text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
			
				],
				))
		else:
			passed_func = signup_sql(username,email,passwd)
			if passed_func == False:
				self.show_alert_dialog(MDDialog(
					title = "Username error", 
					text = "Username already exists!",
					buttons = [
						MDFlatButton(
							text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
				
					],
					))	
			elif passed_func == 'invalid email':
				self.show_alert_dialog(MDDialog(
					title = "Email error", 
					text = "Invalid email address!",
					buttons = [
						MDFlatButton(
							text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
				
					],
					))	
			else:
				self.genrelist = []
				self.current_username = username
				MovieSuggestion.current_username = username
				YourReviews.current_username = username
				MDApp.get_running_app().root.current = 'genre'


	def logger(self):
		addwindow_instance = self.root.get_screen("login")

		username = addwindow_instance.ids["loguser"].text
		passwd = addwindow_instance.ids["logpassword"].text

		addwindow_instance.ids["loguser"].text = ""
		addwindow_instance.ids["logpassword"].text = ""

		cond = login_sql(username , passwd)

		if cond == "invalid":
			self.show_alert_dialog(MDDialog(
				title = "Username error",
				text = "Username does not exist!",
				buttons = [
					MDFlatButton(
						text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
			
				],
				))
		elif cond == False:
			self.show_alert_dialog(MDDialog(
				title = "Password error",
				text = "Password incorrect! Please check your password.",
				buttons = [
					MDFlatButton(
						text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
			
				],
				))
		else:
			self.current_username = username
			MovieSuggestion.current_username = username
			YourReviews.current_username = username
			MDApp.get_running_app().root.current = 'home'

	def revwriter(self):
		addwindow_instance = self.root.get_screen('readwrite')

		username = self.current_username
		movieid = ReadWrite.movieid
		review = addwindow_instance.ids["review"].text
		rate = int(addwindow_instance.ids["spin_rev"].text)

		if len(review) > 600:
			by = len(review) - 600
			self.show_alert_dialog(MDDialog(
				title = "Review out of range",
				text = "Review has exceeded the characters limit, 600, by " + str(by) + ".",
				buttons = [
					MDFlatButton(
						text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
			
				],
				))
		else:		
			reviewwrite_sql(username,movieid,review,rate)
			reviewgenres_sql(username,movieid,rate)
			addwindow_instance.ids["review"].text = ""
			addwindow_instance.ids["spin_rev"].text = "0"

	def searchquery(self):
		addwindow_instance = self.root.get_screen('search')
		addwindow_instance.ids["searchbox"].clear_widgets()

		query = addwindow_instance.ids["searchquery"].text

		results = search_sql(query)

		if len(results) == 0:
			addwindow_instance.ids["searchbox"].add_widget(Factory.MDLabel(
				text= "No results found.",
				halign= "center",
				font_style= "H4"
				))
			
			addwindow_instance.ids["searchbox"].add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.MDCard(
				orientation= "vertical",
				size_hint_x= 0.7,
				size_hint_y= None,
				height= 2,
				elevation= 0
				))

		for i in range(5):
			self.result_block(results,i)


	def clearwidget_search(self):
		addwindow_instance = self.root.get_screen('search')
		addwindow_instance.ids["searchbox"].clear_widgets()

	def goto_movie(self,_id):
		ReadWrite.movieid = _id
		MDApp.get_running_app().root.current = 'readwrite'

	def genre_button(self,genre):
		if genre not in self.genrelist:
			self.genrelist.append(genre)

	def result_block(self , results, n):
		if results[n:n+1] != []:

			result = results[n]

			addwindow_instance = self.root.get_screen('search')
			addwindow_instance.ids["searchbox"].add_widget(Factory.Widget(
					size_hint_y= None,
					height= 30
					))

			addwindow_instance.ids["searchbox"].add_widget(Factory.MDLabel(
				markup= True,
				text= "{}".format(result.get("title","-")),
				halign= "center",
				font_style= "H5"				
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.MDLabel(
				markup= True,
				text= "{}".format(result.get("year","-")),
				halign= "center",
				font_style= "H6"				
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.Widget(
				size_hint_y= None,
				height= 30
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.AsyncImage(
				source= "{}".format(result.get("full-size cover url")),
				mipmap= True,
				size_hint_y= None,
				height= 250,
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.Widget(
				size_hint_y= None,
				height= 20
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.MDRaisedButton(
				markup= True,
				text= "[b]Read & Review[/b]",
				font_size= 19,
				md_bg_color= (14/255, 122/255, 254/255, 1),
				pos_hint= {"center_x":.5},
				on_press = lambda x : print(0),
				on_release= lambda x : self.goto_movie(str(result.get("movieid","")))
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.Widget(
				size_hint_y= None,
				height= 20
				))

			addwindow_instance.ids["searchbox"].add_widget(Factory.MDCard(
				orientation= "vertical",
				size_hint_x= 1,
				size_hint_y= None,
				height= 2,
				elevation= 0
				))

	def clear_genre(self):
		addwindow_instance = self.root.get_screen('genre')
		for i in range(0,22):
			addwindow_instance.ids["button{}".format(i)].icon = "checkbox-blank"

		self.genrelist = []	

	def submit_genre(self):
		if len(self.genrelist) < 4:
			self.show_alert_dialog(MDDialog(
				title = "Less than minimum selection",
				text = "Please select atleast 4 genres",
				buttons = [
					MDFlatButton(
						text = "OK", text_color=self.theme_cls.primary_color, on_release = self.close_dialog)
			
				],
				))

		else:
			maingenres_sql(self.current_username,self.genrelist)
			MDApp.get_running_app().root.current = 'home'			


if __name__ == '__main__':
	FilmPyApp().run()
