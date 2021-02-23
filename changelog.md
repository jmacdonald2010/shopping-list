for commits to the in-progress branch

02/22/2021 22:01
Added a recently added items list to the add items screen. At this time, it does not show up when first loading the screen, but updates once an item is added (or the add item button is pressed). Need to make it show up when that screen is loaded, add text-wrapping, and adjust the grid layout so it looks better. Once that is done, I will attempt to compile to iOS. Changes will be made depending on how it runs on iPhone. Once stable, I will be taking a break from the project.

02/22/2021 20:43
Added text wrapping to the item and datetime labels in the accordion items. Accordion size is adjusted based on the the largest number of items for a single department. Perhaps a future version will have different sized accordion items depending on the department. Next goal is to add a recently added items page to the add item page.

02/20/2021 10:33
Current store spinner is now working and filtering the database appropriately. 

02/20/2021 10:20
Changed the current store variable to a global, added a dict of store names as keys and their id's in the database as values, so the next step is using that to filter what populates the accordions. Commit/push in case something breaks.

02/19/2021 22:44
Added a select store spinner, currently it only prints to the console and refreshes the main screen when a new store is selected, but from here it should be somewhat straight-ahead to add the filtering based on stores. Close to having a working base version to compile to iOS.

02/17/2021 20:55
Dataframes are now sorted and displayed by isle #.

02/17/2021 20:37
Added the add department button. At this time, in order for the changes made in settings to be reflected, the app needs to be relaunched. The same applies to the add store button.

02/17/2021 19:43
Added the add store button. Unfortunately, this still requires the app to be relaunched in order for the store change to be reflected in the AddItems page. Making this a feature will likely require redoing a lot of the AddItems class to change most of its methods to class methods.

02/16/2021 22:30
Started building the settings accordion. Only button I have so far is the delete button, which after some testing (and redownloading the db from github a few times), works quite nicely with a popup warning. Looking to add the other settings items soon (add department, add store, select store) soon, then hopefully figure out text wrapping in a grid layout.

02/16/2021 20:58 
The basic functionality works now. Remove collected items removes items marked as collected and refreshes the main screen. Adding and item from the AddItem page also refreshes the main screen. Clicking a toggle button updates the database appropriately. I know that the way I have done this is not the most appropriate way in the world of OOP, but it is functional, and it's not likely that I'll be creating multiple MainScreen or AddItems objects.

TODO: Need to add a settings accordion, which also means I need to add a variable/object property for the # of rows in the grid layout for the accordion.

02/16/2021 20:40
Got the add items button on the add items screen to refresh the main screen. Had to convert some of my instance methods in MainScreen to class methods. Now errors are occuring in other parts of the MainScreen (eg toggle button push, remove selected items, etc.), so more of this is likely to become class methods with few instance methods (if any), which, hypothetically, shouldn't be an issue, because I will only ever have one instance of the MainScreen class.

02/15/2021 21:54
Working on getting the add item button on the add item screen to refresh the accordions on the main screen without requiring the user to manually do this on their own. Sort of struggling here, I know there's a way to do it but I'm not sure the best way to do so, and I don't know how I feel about rewriting a ton of code to make it work, which I'm afraid it may use. On another note, updated the add item screen to grid layout. Doesn't look fantastic, and I still need to add a recently added items part to the bottom of that screen, but hey, it's progress.

02/15/2021 16:18
The remove collected items button works now; it refreshes the main screen (deletes all children of Accordion, then rebuilds them). Now trying to figure out how to refresh the main screen when new items are added.

02/14/2021 17:18
Got the init func to populate all of the department data in the appropriate accordions. Also got it so the buttons write properly to the database. Next step is converting this to one big function, so I can refresh the whole app with ease when new items are added. Maybe not the most efficient thing ever, but hey, it works. A lot of code cleanup is needed, and also I need to figure out text wrapping in the grid layout. Remove Items button needs functionality. Need a settings dropdown.

02/14/2021 16:46
Going to make it so that the dropdowns just populate when the main screen is initialized. I think it will be easier that way. Hopefully, I will be able to make it so the items in the accordions refresh when an item is added to the db. Going to delete a lot of the things I had been trying earlier today, b/c my code is currently a mess.

02/14/2021 12:50
Realized that the way I was building the accordion item for the produce accordion was not necessarily the best approach, as I would need to duplicate it for every single accordion item, and the number of accordion items would be fixed, which is not necessarily what I want. I have started to add the accordion items with python instead of the .kv file, but am running into some issues binding the build_accordion function to the on_touch_down part of the function. Got it so the function works when an accordion item is clicked, but now we don't have dropdowns, which is another issue to resolve. Need to do some housework, may work on it more later.

02/13/2021 22:03
Toggle buttons work! They now write to a DB whether or not that object is collected. Might not be the smoothest or cleanest method for doing so, but it is functional now. Commit/push b/c it works now, very much needs cleaned up, but also will be the last bit of work for the night.

02/12/2021 22:02
Figured out my lambda issue w/ the toggle button. Now they return their button ID when pressed, which is a big step forward in getting them to properly write to the db. Enough work for the night, going to commit and keep pushing on at another time, but the end of the problem is coming into sight now.

02/12/2021 0:00
Made the produce accordion load upon opening instead of during the screen's __init__. However, the toggle button issue is still not resolved, they still always print the last button value that was iterated over. I'm not quite sure how to address this, as I'm not sure how to add values to the buttons as they're created while avoiding this issue while iterating. I have a feeling that this issue is going to take a long time to resolve.

02/11/2021 22:36
Still have the toggle box issues. Going to try to see if building the accordion item contents outside of the __int__ helps w/ my toggle issue. At the very least, it will make it more robust for when items are added to the database. Commit/push as a backup in case it fails hard.

02/11/2021 21:48
Toggle boxes are working now w/ button presses, but they are only writing to one item in the database. Going to try removing the actual variable name and going back to a similar approach to what I had last night, only keeping the lambda for on_press.

02/10/2021 22:22
Building the formatting for the data for the departments. Running into issues figuring out how to make the toggle boxes (or checkboxes) actively update the 'collected' column in the database, and actually running into issues w/ getting the program to run w/ the initialization of the toggle buttons. once this is all figured out I will be applying it to all departments.

02/09/2021 23:30
working on importing the data from the database into pandas dataframes so as to more easily store them in the tables that will be assembled in the accordion items. Final commit/push for the night.

02/09/2021 23:11
Added a lot of ObjectProperties for the main screen class, committing/pushing b/c I know something is going to break when I try to make these tables for the accordionItems.

02/09/2021 22:50
Fixed my overlapping accordion menus issue by commenting out the builder line. Next step is figuring out how to get the data to display in the accordions w/ varying #'s of rows

02/08/2021 20:26
Working on the scrollview for the accordion menus. They scroll, but the actual accordion action is pretty messed up. Suspecting it may be a backgrounds issue, but we'll have to see when I investigate it further. 

02/08/2021 19:36
I have added the accordian menus to the main page, but they are formatting poorly. I am attempting to implement a scroll view w/o much success. This commit/push is to save myself before I break it real bad.

02/08/2021 14:13
Started working on the main screen. Using a grid layout b/c it seems to be the easiest way to organize everything. Going to likely use accordian widgets to display the different departments.

02/08/2021 13:47
Cleaned up the code and tested it to make sure it all still works.

02/08/2021 13:40
I made the code that writes to the database a bit more robust and added in some logic to help avoid errors or incomplete entries from being added to the database. Committing/pushing b/c I'm worried that when I go thru and clean up the code that I may break something.

02/07/2021 10:50
Fixed my normalization for writing to the items table. Next step, clearing the entry fields after adding an item.

02/07/2021 10:37
The app now writes to the db, now I am going to work on normalizing the foreign key fields in the items table

02/06/2021 10:41
Added the rest of the entry fields for the add item page. The formatting is not good, but I will change that once I get it writing to the database. Likely the last commit of the day.

02/06/2021 09:54
I figured out how to do the dropdown menu I want to! I have it working now. I'm not a big fan of the current layout so I'm likely to switch to either a grid layout or a float layout.

02/05/2021 22:09
No progress today. Trying to build a dropdown menu that has values from a database (list of units). Having absolutely no luck with this and unable to find anything useful online. Can't really make the input for w/ a normalized db w/o a dropdown list. 

02/04/2021 22:18
Typing in an item name now creates a new item object, and then after that, you can assign other values to that object (eg, quantity). Next step is creating the dropdown lists for units and stores. Units could be a hard-coded list, but stores can't be per my design, so this will be a challenge.

02/04/2021 21:37
Added a working text field. Well, it makes text appear in the console, so that's a start.

02/04/2021 21:12
Got the kivy button to do something w/ multiple screens! Pushing before I break it as I start to add more features.

02/03/2021 23:10
I thought things were working, but apparently I was wrong. Trying to implement buttons that do things w/ the .kv file, not quite sure how. Feel like it shouldn't be as complicated as everything I am reading is making it out to be. I want the add items button the on add items page to write some data to a DB. Nothing is really working at the moment but I'm going to bed now.

02/03/2021 21:37
Continued working w/ screen manager. Have buttons now. Next step is working on the add item page. Committing before breaking anything.

02/03/2021 20:59
Started working w/ kivy screen manager. Now it's time to figure out how to build a UI. Committing before I break anything as this works now as is.

02/02/2021 22:59
last commit of the night. Working on building a multiscreen app using kivy. About to largely demolish the current MainApp class to accomdate the new multiscreen code, wanted to commit so it's not gone forever. Going to bed soon.

02/02/2021 22:30
add some methods to the item class. next version will be attempting to ingegrate kivy

02/02/2021 21:54 
created a class file for items (not yet tested)
started the main.py file
main.py now creates/initializes a new sqlite database
