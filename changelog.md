for commits to the in-progress branch

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
